from flask import send_from_directory, Blueprint
from __init__ import ALLOWED_EXTENSIONS, UPLOAD_FOLDER
import os
from werkzeug.utils import secure_filename
from random import randint


image = Blueprint('image', __name__, template_folder="templates")

############################################################
# IMAGE ROUTES
############################################################


@image.route('/viewimage/')
@image.route("/viewimage/<imagename>")
def vew_image(imagename=None):
    image = imagename
    if image is None:
        image = "default.jpg"

    print(image)
    return send_from_directory(UPLOAD_FOLDER,
                               image, as_attachment=True)

############################################################
# Helper Methods
############################################################


def uploadImage(request, prevImage):
    """Saves the uploaded image"""
    if request.method == 'POST':

        # check if the post request has the file part
        if 'image' not in request.files:
            return prevImage

        file = request.files['image']

        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':

            return prevImage

        # if the file is present and has an allowed extension
        if file and allowed_file(file.filename):

            # make sure the new filename is unique
            filename = get_unique_filename(secure_filename(file.filename))

            # save the image
            file.save(os.path.join(UPLOAD_FOLDER, filename))

            # delete the previous, but now unused image
            delete_file(prevImage)

            return filename


def delete_file(filename):
    if filename != "default.jpg":
        os.remove(os.path.join(UPLOAD_FOLDER, filename))


def get_unique_filename(filename):
    # set the file name
    new_filename = filename

    # make a list of all filenames in the upload folder
    used_file_names = []
    for filename in os.listdir(UPLOAD_FOLDER):
        used_file_names.append(filename)

    # if the new filename is already used then randomize it
    randomized_filename = new_filename
    while randomized_filename in used_file_names:
        randomized_filename = f"{randint(100000, 999999)}_{new_filename}"

    new_filename = randomized_filename

    return new_filename


def allowed_file(filename):
    """Check if the file has an allowed extension"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
