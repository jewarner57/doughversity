from flask import session, render_template, redirect, url_for, Blueprint
from bson.objectid import ObjectId
from __init__ import mongo

main = Blueprint('cart', __name__, template_folder="templates")


@cart.route('/addToCart/<itemid>/<amount>')
def addToCart(itemid, amount):
    """Add a store item to the shopping cart"""
    item = mongo.db.shop_items.find_one_or_404({"_id": ObjectId(itemid)})
    quantity = amount

    if "cart_items" not in session:
        session["cart_items"] = []

    cartArray = session["cart_items"]

    cartArray.append({
        "id": itemid,
        "price": item["price"],
        "quantity": quantity
    })

    session["cart_items"] = cartArray

    context = {
        "items": session["cart_items"]
    }

    return redirect(url_for("cart", **context))
