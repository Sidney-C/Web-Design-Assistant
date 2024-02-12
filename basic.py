from flask import Flask, render_template, request, url_for, redirect, session
from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField, RadioField, SubmitField, FileField, validators
from user_agents import parse
import os

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret'
app.config['ALLOWED_EXTENSIONS'] = {'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = 'static'

pageassets = {}
navbarlinks = {}
sitenames = []

def checkextension(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

class NameForm(FlaskForm):
    urlname = StringField('Enter URL *', [validators.DataRequired()])
    sitename = StringField('Enter the name of this page *', [validators.DataRequired()])
    textcontent = TextAreaField('Enter the text for the first section of your website *', [validators.DataRequired()])
    textcontent2 = TextAreaField('If you would like a second section, enter the text here')
    image = FileField('Upload an image (must be in .jpg format)')
    submit = SubmitField('Generate Website!')
    addtonavbar = RadioField('Add page to navbar? *', choices=[('Yes', 'Yes'), ('No', 'No')])
    
@app.route('/', methods = ['GET', 'POST'])
def index():
    sitename = False
    textcontent = False
    textcontent2 = False
    urlname = False
    image = False
    filename = ''
    addtonavbar = ''
    nameform = NameForm()

    if nameform.validate_on_submit():
        session['url'] = nameform.urlname.data
        nameform.urlname.data =''
        session['sitename'] = nameform.sitename.data
        nameform.sitename.data = ''
        session['textcontent'] = nameform.textcontent.data
        nameform.textcontent.data = ''
        session['textcontent2'] = nameform.textcontent2.data
        nameform.textcontent2.data = ''
        session['addtonavbar'] = nameform.addtonavbar.data
        
        if session['addtonavbar'] == 'Yes':
            navbarlinks[session['sitename']] = (url_for('newurl', yoururl=session['url']))
            sitenames.append(session['sitename'])
            
        nameform.addtonavbar.data = ''
        session['image'] = nameform.image.data
        if session['image'] and checkextension(session['image'].filename):
            filename = 'user_image'
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            session['image'].save(filepath)
            assetlist = [session['sitename'], session['textcontent'], session['textcontent2'], filename]
        else:
            assetlist = [session['sitename'], session['textcontent'], session['textcontent2'], "no file uploaded"]
        nameform.image.data = ''
        session.pop('image', None)
        pageassets[session['url']] = assetlist
        print(filename + " is correct in the index function")
        return redirect(url_for('newurl', yoururl=session['url']))

    return render_template('index.html', nameform=nameform)

@app.route('/yourwebsite')
def yourwebsite():

    return render_template('yourwebsite.html')

@app.route('/yourwebsite/<yoururl>')
def newurl(yoururl):

    currentassets = pageassets[yoururl]
    filename = currentassets[3]
    for i, j in enumerate(sitenames):
        print(j)
        print(navbarlinks.get(j))
    return render_template('yourwebsite.html', currentassets = currentassets, filename = filename, sitenames = sitenames, navbarlinks = navbarlinks)

@app.route('/showcode')
def showcode():

    findbrowser = request.user_agent.string
    browser = parse(findbrowser)
    browsername = browser.browser.family

    return render_template('showcode.html', browsername=browsername)

if __name__ == '__main__':
    app.run(debug = True)
