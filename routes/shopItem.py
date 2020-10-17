from flask import Blueprint, render_template, request, redirect, url_for, abort
from flask_login import current_user, login_required
from routes.bakery import role_required
from routes.image import uploadImage
from __init__ import mongo
from bson.objectid import ObjectId

shopItem = Blueprint('shopItem', __name__, template_folder="templates")


############################################################
# SHOP ITEM
############################################################

@shopItem.route('/create-item', methods=["GET", "POST"])
@role_required("bakery")
@login_required
def create_item():
    if request.method == 'POST':

        name = request.form.get("name")
        price = request.form.get("price")
        desc = request.form.get("desc")

        image = uploadImage(request, "default.jpg")

        bakery = mongo.db.bakeries.find_one_or_404(
            {"ownerId": current_user.get_id()})

        newItem = {
            "bakeryId": bakery["_id"],
            "name": name,
            "repeating": False,
            "price": price,
            "description": desc,
            "image": image
        }

        mongo.db.shop_items.insert_one(newItem)

        return redirect(url_for("bakery.my_bakery"))

    else:
        return render_template("create-item.html")


@shopItem.route('/delete-item/<id>')
@login_required
def deleteItem(id):

    # get the item
    item = mongo.db.shop_items.find_one_or_404({"_id": ObjectId(id)})

    # get it's bakery's ID
    bakeryId = item["bakeryId"]

    # get it's bakery
    bakery = mongo.db.bakeries.find_one_or_404(
        {"_id": ObjectId(bakeryId)})

    # get that backery's owner
    bakeryOwnerId = bakery["ownerId"]

    # if the user is not the owner then 401
    if not current_user.get_id() == bakeryOwnerId:
        return redirect(url_for("auth.login"))

    mongo.db.shop_items.delete_one({"_id": ObjectId(id)})

    return redirect(url_for("bakery.my_bakery"))


@shopItem.route('/item/<itemid>')
def view_item(itemid):

    item = mongo.db.shop_items.find_one_or_404({"_id": ObjectId(itemid)})

    bakery = mongo.db.bakeries.find_one_or_404(
        {"_id": ObjectId(item["bakeryId"])})

    context = {
        "id": item["_id"],
        "ownerId": bakery["ownerId"],
        "name": item["name"],
        "image": item["image"],
        "price": item["price"],
        "description": item["description"]
    }

    return render_template("item-detail.html", **context)


@shopItem.route('/edit-item/<id>', methods=["GET", "POST"])
@login_required
def edit_item(id):

    # get the item
    item = mongo.db.shop_items.find_one_or_404({"_id": ObjectId(id)})

    # get it's bakery's ID
    bakeryId = item["bakeryId"]

    # get it's bakery
    bakery = mongo.db.bakeries.find_one_or_404(
        {"_id": ObjectId(bakeryId)})

    # get that backery's owner
    bakeryOwnerId = bakery["ownerId"]

    # if the user is not the owner then 401
    if not current_user.get_id() == bakeryOwnerId:
        return redirect(url_for("auth.login"))

    context = {
        "name": item["name"],
        "price": item["price"],
        "description": item["description"]
    }

    if request.method == 'POST':

        name = request.form.get("name")
        price = request.form.get("price")
        desc = request.form.get("desc")

        image = uploadImage(request, "default.jpg")

        mongo.db.shop_items.update_one({
            "_id": item["_id"]
        },
            {
            '$set': {
                'name': name,
                'price': price,
                'desc': desc,
                'image': image
            }
        })

        return redirect(url_for("bakery.my_bakery"))

    else:
        return render_template("edit-item.html", **context)
