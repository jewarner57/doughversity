from flask import render_template, Blueprint, session
from bson.objectid import ObjectId
from __init__ import mongo

############################################################
# MAIN ROUTES
############################################################

main = Blueprint('main', __name__, template_folder="templates")


@main.route('/')
def home():
    """Display the home page."""
    # find all unanswered posts
    post_data = mongo.db.posts.find()

    context = {
        'posts': post_data
    }
    return render_template('home.html', **context)


@main.route('/plans')
def plans():
    """Display a list of subscription plans to the users"""

    plans = mongo.db.shop_items.find({"repeating": True})

    context = {
        'plans': plans
    }

    return render_template('plans.html', **context)


@main.route('/addToCart/<itemid>')
def addToCart(itemid):
    """Add a store item to the shopping cart"""
    item = mongo.db.shop_items.find_one_or_404({"_id": ObjectId(itemid)})
    amount = 1

    if "cart_items" not in session:
        session["cart_items"] = []

    cartArray = session["cart_items"]

    cartArray.append({
        "id": itemid,
        "price": item["price"],
        "quantity": amount
    })

    session["cart_items"] = cartArray

    context = {
        "items": session["cart_items"]
    }

    return render_template('cart.html', **context)
