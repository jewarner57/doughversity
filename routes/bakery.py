from flask import Blueprint, abort, render_template, request, flash, redirect, url_for
from bson.objectid import ObjectId
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
                if not current_user.role == role:
                    flash("Your account does not have permission to view this page.")
                    abort(401)

            return function()
        inner.__name__ = function.__name__
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
            "address": address,
            "image": "",
            "description": ""
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


@bakery.route('/bakery/<bakeryId>')
def view_bakery(bakeryId):
    bakery = mongo.db.bakeries.find_one_or_404({"_id": ObjectId(bakeryId)})

    context = {
        "name": bakery["name"],
        "address": bakery["address"],
        "is_owner": current_user.get_id() == bakery["ownerId"]
    }

    return render_template("bakery-store.html", **context)


@bakery.route('/mybakery')
@role_required("bakery")
@login_required
def my_bakery():
    bakery = mongo.db.bakeries.find_one_or_404(
        {"ownerId": current_user.get_id()})
    bakery_id = bakery["_id"]
    return redirect(url_for("bakery.view_bakery", bakeryId=bakery_id))


@bakery.route('/edit-bakery-profile', methods=["GET", "POST"])
@role_required("bakery")
@login_required
def edit_bakery():
    """Allow the user to edit their bakery's store page"""

    bakery = mongo.db.bakeries.find_one_or_404(
        {"ownerId": current_user.get_id()})

    # if the user does not own this bakery then redirect user to login.
    if not bakery["ownerId"] == current_user.get_id():
        abort(401)

    if request.method == 'POST':

        name = request.form.get("name")
        email = request.form.get("email")
        phonenumber = request.form.get("phonenumber")
        address = request.form.get("address")
        image = request.form.get("image")
        description = request.form.get("description")

        mongo.db.bakeries.update_one({
            "_id": bakery["_id"]
        },
            {
            '$set': {
                'name': name,
                'email': email,
                'phonenumber': phonenumber,
                'address': address,
                'image': image,
                'description': description
            }
        })

        return redirect(url_for("bakery.my_bakery"))
    else:

        context = {
            "name": bakery["name"],
            "email": bakery["email"],
            "phonenumber": bakery["phonenumber"],
            "address": bakery["address"],
            "image": bakery["image"],
            "description": bakery["description"]
        }

        return render_template("edit-bakery-store.html", **context)
