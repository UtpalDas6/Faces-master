from flask import Flask, render_template, request
from flask_uploads import UploadSet, configure_uploads, IMAGES
import faces
from PIL import Image
import os
import io
import datetime,random
app = Flask(__name__,static_url_path = "/templates", static_folder = "templates")
photos = UploadSet('photos', IMAGES)
app.config['UPLOADED_PHOTOS_DEST'] = "templates/"
configure_uploads(app, photos)
@app.route('/')
def my_form():
    return render_template('index.html')
@app.route('/submit', methods=['POST'])
def my_form_post():
    if request.method == 'POST' and 'photo' in request.files:
        filename = photos.save(request.files['photo'])
    full_filename = os.path.join(app.config['UPLOADED_PHOTOS_DEST'], filename)
    pic = open(full_filename, 'rb')
    try:
        image = faces.FaceAppImage(file=pic)
    except faces.ImageHasNoFaces:
        return('Your face is not recognized. Are you an alien?')
    except faces.BadImageType:
        return('This image is not valid. Get some good bytes.')
    except faces.BaseFacesException:
        return('Some unknown wrong things happened.')
    try:
        happy = image.apply_filter('female')
    except faces.BadFilterID:
        return('Too cool filter to exist.')
    image = Image.open(io.BytesIO(happy))
    o="op"+filename
    op=os.path.join(app.config['UPLOADED_PHOTOS_DEST'], o)
    image.save(op)
    return render_template('output.html',input="/templates/"+filename,output="/templates/"+o)

if __name__ == "__main__":
    app.run(debug=True)