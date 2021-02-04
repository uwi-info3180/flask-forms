"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""
import os
from app import app
from flask import render_template, request, redirect, url_for, flash, session, abort, send_from_directory
from werkzeug.utils import secure_filename

# Note: that when using Flask-WTF we need to import the Form Class that we created
# in forms.py
from .forms import MyForm, PhotoForm


###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/basic-form', methods=['GET', 'POST'])
def basic_form():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']

        return render_template('result.html',
                               firstname=firstname,
                               lastname=lastname,
                               email=email)

    return render_template('form.html')


@app.route('/wtform', methods=['GET', 'POST'])
def wtform():
    myform = MyForm()

    if request.method == 'POST':
        if myform.validate_on_submit():
            # Note the difference when retrieving form data using Flask-WTF
            # Here we use myform.firstname.data instead of request.form['firstname']
            firstname = myform.firstname.data
            lastname = myform.lastname.data
            email = myform.email.data

            flash('You have successfully filled out the form', 'success')
            return render_template('result.html', firstname=firstname, lastname=lastname, email=email)

        flash_errors(myform)
    return render_template('wtform.html', form=myform)


@app.route('/photo-upload', methods=['GET', 'POST'])
def photo_upload():
    photoform = PhotoForm()

    if request.method == 'POST' and photoform.validate_on_submit():

        photo = photoform.photo.data # we could also use request.files['photo']
        description = photoform.description.data

        filename = secure_filename(photo.filename)
        photo.save(os.path.join(
            app.config['UPLOAD_FOLDER'], filename
        ))

        return render_template('display_photo.html', filename=filename, description=description)

    flash_errors(photoform)
    return render_template('photo_upload.html', form=photoform)

# Example route using send_from_directory
# for files that are not in the "static" folder
@app.route("/uploads/<filename>")
def get_uploaded_file(filename):
    root_dir = os.getcwd()

    return send_from_directory(os.path.join(root_dir, app.config['UPLOAD_FOLDER']), filename)

###
# The functions below should be applicable to all Flask apps.
###

# Flash errors from the form if validation fails
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8080")