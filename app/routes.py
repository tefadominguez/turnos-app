from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import Turno
from app import db
from flask_login import login_required, current_user
from datetime import datetime

main = Blueprint('main', __name__)


@main.route('/')
@login_required
def dashboard():
    if current_user.rol == "admin":
        turnos = Turno.query.filter_by(estado="activo") \
            .order_by(Turno.fecha, Turno.hora).all()
    else:
        turnos = Turno.query.filter_by(
            user_id=current_user.id,
            estado="activo"
        ).order_by(Turno.fecha, Turno.hora).all()

    return render_template('dashboard.html', turnos=turnos)


@main.route('/crear', methods=['GET', 'POST'])
@login_required
def crear_turno():
    if request.method == 'POST':
        fecha = request.form.get('fecha')
        hora = request.form.get('hora')
        cliente = request.form.get('cliente')

        if not fecha or not hora or not cliente:
            flash("Todos los campos son obligatorios")
            return redirect(url_for('main.crear_turno'))

        try:
            fecha_turno = datetime.strptime(fecha, "%Y-%m-%d")
        except ValueError:
            flash("Fecha inválida")
            return redirect(url_for('main.crear_turno'))

        if fecha_turno.date() < datetime.now().date():
            flash("No se pueden crear turnos en el pasado")
            return redirect(url_for('main.crear_turno'))

        existente = Turno.query.filter_by(
            fecha=fecha,
            hora=hora,
            estado="activo"
        ).first()

        if existente:
            flash("Ese horario ya está ocupado")
            return redirect(url_for('main.crear_turno'))

        turno = Turno(
            fecha=fecha,
            hora=hora,
            cliente=cliente,
            user_id=current_user.id
        )

        db.session.add(turno)
        db.session.commit()

        flash("Turno creado correctamente")
        return redirect(url_for('main.dashboard'))

    return render_template('create_turno.html')


@main.route('/cancelar/<int:id>')
@login_required
def cancelar_turno(id):
    turno = Turno.query.get(id)

    if turno:
        if turno.user_id == current_user.id or current_user.rol == "admin":
            turno.estado = "cancelado"
            db.session.commit()
            flash("Turno cancelado")

    return redirect(url_for('main.dashboard'))