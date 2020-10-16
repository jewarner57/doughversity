from flask import redirect, render_template, url_for, flash, request
from flask_login import login_url
from __init__ import app

# import route blueprints
from routes.auth import auth
from routes.main import main
from routes.profile import profile
from routes.cart import cart
from routes.bakery import bakery
from routes.image import image
from routes.shopItem import shopItem

# register app routes
app.register_blueprint(auth)
app.register_blueprint(main)
app.register_blueprint(profile)
app.register_blueprint(cart)
app.register_blueprint(bakery)
app.register_blueprint(image)
app.register_blueprint(shopItem)

############################################################
# ERROR ROUTES
############################################################


@app.errorhandler(404)
def page_not_found(e):
    """display a 404 response page"""
    return render_template('404.html'), 404


@app.errorhandler(401)
def not_authorized(e):
    """send the user to the login screen when they try to access a locked page"""
    flash("Confirm Your Identity to Proceed")
    return redirect(login_url("/login", next_url=url_for(request.endpoint)))


if __name__ == '__main__':
    app.run(debug=True)
