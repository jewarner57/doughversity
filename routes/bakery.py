from flask import Blueprint, abort, render_template, request, flash
from flask_login import current_user, login_required
from __init__ import mongo

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
                    flash("Your account does not have permission to view this page.")
                    abort(401)

            return function()
        return inner
    return wrapper

############################################################
# BAKERY ROUTES
############################################################


@bakery.route('/register-bakery', methods=["GET", "POST"])
@role_required("user")
@login_required
def register_bakery():
    if request.method == 'POST':

        ownerId = current_user.get_id()
        name = request.form.get('name')
        email = request.form.get('email')
        phonenumber = request.form.get('phonenumber')
        address = request.form.get('address')

        newBakery = {
            "ownerId": ownerId,
            "name": name,
            "email": email,
            "phonenumber": phonenumber,
            "address": address
        }

        isUniqueEmail = mongo.db.bakeries.find({"email": email}).count() == 0
        isUniquePhone = mongo.db.bakeries.find(
            {"phonenumber": phonenumber}).count() == 0
        isUniqueOwner = mongo.db.bakeries.find(
            {"ownerId": ownerId}).count() == 0

        if(isUniqueEmail and isUniquePhone and isUniqueOwner):
            mongo.db.bakeries.insert_one(newBakery)
        else:
            if not isUniqueOwner:
                flash("You have already submitted this form.")
            if not isUniqueEmail:
                flash("Your bakery email has already been registered.")
            if not isUniquePhone:
                flash("Your bakery phone number has already been registered")

        flash("Bakery Regsistrationn Application Sent Successfully.")
        return render_template("register-bakery.html")

    else:
        return render_template("register-bakery.html")


@bakery.route('/bakery/<ownerId>')
def view_bakery(ownerId):
    mongo.db.bakeries.find_one_or_404({"ownderId": ownerId})

    context = {
        ""
    }

    return render_template("bakery-profile.html", **context)
    pass
