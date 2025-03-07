from flask import Blueprint, render_template, send_file, request
from flask_login import login_required, current_user
from models import VisitLog, User, db
from app.auth import check_rights
from app import app
import pandas as pd
import io

reports_bp = Blueprint('reports', __name__, url_prefix='/reports')

@reports_bp.route('/')
@login_required
def index():
    return render_template('reports/index.html')  # Create a report index page

@reports_bp.route('/pages')
@login_required
@check_rights('Admin')
def page_report():
    page_stats = db.session.query(VisitLog.path, db.func.count(VisitLog.path)).group_by(VisitLog.path).order_by(db.func.count(VisitLog.path).desc()).all()
    return render_template('reports/page_report.html', page_stats=page_stats)

@reports_bp.route('/users')
@login_required
@check_rights('Admin')
def user_report():
    user_stats = db.session.query(VisitLog.user_id, db.func.count(VisitLog.user_id)).group_by(VisitLog.user_id).order_by(db.func.count(VisitLog.user_id).desc()).all()
    users = {user.id: f"{user.first_name} {user.last_name}" for user in User.query.all()}

    return render_template('reports/user_report.html', user_stats=user_stats, users=users)

@reports_bp.route('/pages/csv')
@login_required
@check_rights('Admin')
def page_report_csv():
    page_stats = db.session.query(VisitLog.path, db.func.count(VisitLog.path)).group_by(VisitLog.path).order_by(db.func.count(VisitLog.path).desc()).all()
    df = pd.DataFrame(page_stats, columns=['Page', 'Visit Count'])
    csv = df.to_csv(index=False)
    return send_file(io.StringIO(csv), mimetype='text/csv', as_attachment=True, download_name='page_report.csv')

@reports_bp.route('/users/csv')
@login_required
@check_rights('Admin')
def user_report_csv():
    user_stats = db.session.query(VisitLog.user_id, db.func.count(VisitLog.user_id)).group_by(VisitLog.user_id).order_by(db.func.count(VisitLog.user_id).desc()).all()
    users = {user.id: f"{user.first_name} {user.last_name}" for user in User.query.all()}
    data = []
    for user_id, count in user_stats:
        if user_id:
            user_name = users.get(user_id, "Unknown User")
        else:
            user_name = "Неаутентифицированный пользователь"

        data.append({'User': user_name, 'Visit Count': count})

    df = pd.DataFrame(data)
    csv = df.to_csv(index=False)
    return send_file(io.StringIO(csv), mimetype='text/csv', as_attachment=True, download_name='user_report.csv')