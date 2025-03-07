from functools import wraps
from flask import redirect, url_for, flash, g
from flask_login import current_user
from models import User

def check_rights(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated or not current_user.has_role(role):
                flash("У вас недостаточно прав для доступа к данной странице.")
                return redirect(url_for('index'))  # Или другая страница
            return f(*args, **kwargs)
        return decorated_function
    return decorator