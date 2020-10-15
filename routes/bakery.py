from flask import Blueprint, abort, render_template
from flask_login import current_user, login_required


bakery = Blueprint('bakery', __name__, template_folder="templates")


# role required decorator
# storing this in bakery for now because it will only be used for bakery routes atm


def role_required(role):
    """Checks if the current user has the required role"""
    def wrapper(function):

        def inner(*args, **kwargs):

            if current_user.is_anonymous:
                abort(401)
            else:
                print(current_user.role)
                if not current_user.role == role:
                    abort(401)

            return function()
        return inner
    return wrapper

############################################################
# BAKERY ROUTES
############################################################


@login_required
@bakery.route('/register-bakery', methods=["GET", "POST"])
def register_bakery():
    return render_template("register-bakery.html")
