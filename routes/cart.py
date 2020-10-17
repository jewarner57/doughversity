from flask import session, render_template, redirect, url_for, Blueprint
from bson.objectid import ObjectId
from __init__ import mongo

cart = Blueprint('cart', __name__, template_folder="templates")


@cart.route('/addToCart/<itemid>/', defaults={'amount': 1})
@cart.route('/addToCart/<itemid>/<amount>')
def addToCart(itemid, amount):
    """Add a store item to the shopping cart"""
    item = mongo.db.shop_items.find_one_or_404({"_id": ObjectId(itemid)})
    print(item)
    quantity = amount or 1

    if "cart_items" not in session:
        session["cart_items"] = []

    cartArray = session["cart_items"]

    # if the item is already in the cart increase the quantity
    for current_item in cartArray:
        if current_item["id"] == itemid:
            current_item["quantity"] += quantity
            session["cart_items"] = cartArray
            return redirect(url_for("cart.show_cart"))

    # if the item is not in the cart then add it
    cartArray.append({
        "id": itemid,
        "name": item["name"],
        "price": item["price"],
        "quantity": quantity
    })
    session["cart_items"] = cartArray
    return redirect(url_for("cart.show_cart"))


@cart.route('/cart')
def show_cart():
    """Shows the cart page"""

    if session.get("cart_items") is None:
        session["cart_items"] = []

    subtotal = 0
    for item in session["cart_items"]:
        subtotal += float(item["price"]) * float(item["quantity"])
    context = {
        "items": session["cart_items"],
        "subtotal": subtotal
    }

    return render_template("cart.html", **context)


@cart.route('/removecartitem/<itemid>')
def remove_cart_item(itemid):
    """Removes a selected item from the cart"""

    cart = session["cart_items"]

    for item in cart:
        if item["id"] == itemid:
            cart.remove(item)

    session["cart_items"] = cart

    return redirect(url_for("cart.show_cart"))


@cart.route('/checkout')
def checkout():
    """Clear the cart and checkout the user"""

    session["cart_items"] = []
    return redirect(url_for("cart.show_cart"))
