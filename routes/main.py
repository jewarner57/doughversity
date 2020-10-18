from flask import render_template, Blueprint
from __init__ import mongo

############################################################
# MAIN ROUTES
############################################################

main = Blueprint('main', __name__, template_folder="templates")


@main.route('/')
def home():
    """Display the home page."""
    shop_items = mongo.db.shop_items.find({"repeating": False})

    context = {
        "shop_items": shop_items
    }

    return render_template('home.html', **context)


@main.route('/about')
def about():
    """Display the about page"""
    return render_template("about.html")


@main.route('/plans')
def plans():
    """Display a list of subscription plans to the users"""

    plans = mongo.db.shop_items.find({"repeating": True})

    context = {
        'plans': plans
    }

    return render_template('plans.html', **context)


@main.route('/shop')
def shop():
    """Display The Shop Page"""
    items = mongo.db.shop_items.find({"repeating": False})

    context = {
        'items': items
    }

    return render_template('shop.html', **context)
