from functools import wraps

from flask import redirect, url_for, flash
from flask_login import current_user

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # replicate login_required check
        if not current_user.is_authenticated:
            flash("Log in to access this page.", "warning")
            return redirect(url_for("auth.login"))
        
        # check for admin role
        if current_user.role != "admin":
            flash("You are not allowed there.", "danger")
            return redirect("/")
        
        return f(*args, **kwargs)
    
    return decorated_function