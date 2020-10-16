from flask import Blueprint
from flask_login import current_user, login_required
from routes.bakery import role_required

shopItem = Blueprint('shopItem', __name__, template_folder="templates")


############################################################
# SHOP ITEM
############################################################

@shopItem.route('/create-item', methods=["GET", "POST"])
@role_required("baker")
@login_required
def create_item():
    pass
