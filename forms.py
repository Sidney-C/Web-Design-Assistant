from flask import Flask, render_template, request, url_for, redirect, session
from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField, RadioField, SubmitField, FileField, validators
from user_agents import parse
import os

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret'
app.config['ALLOWED_EXTENSIONS'] = {'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = 'static'

assetlist = []

submittext = 'Submit'
pagenametext = '''To get started, enter the name of this page. The name
you enter will appear at the top of the page.'''
urlnametext = '''Enter the URL for this page. This will appear at the end of it's address, so I recommend you make it short and simple.'''
pagetexttext = '''Enter the text for the first section of this page. Don't worry about fitting everything in, as you will have the option to add another section soon'''

class PageName(FlaskForm):
    userinput = StringField(pagenametext, [validators.DataRequired()])
    submit = SubmitField(submittext)

class URLName(FlaskForm):
    userinput = StringField(urlnametext, [validators.DataRequired()])
    submit = SubmitField(submittext)

class PageText(FlaskForm):
    userinput = TextAreaField(pagetexttext, [validators.DataRequired()])
    submit= SubmitField(submittext)

formfields = [PageName, URLName, PageText]

@app.route('/testpage1', methods = ['GET', 'POST'])
def testpage1():
    
    if 'i' not in session:
        session['i'] = 0

    chatbox = formfields[session['i']]()
    
    if chatbox.validate_on_submit():
        assetlist.append(chatbox.userinput.data)
        print(assetlist)
        session['i'] += 1
        print(session['i'])
        
        if session['i'] > 2:
            return redirect(url_for('testpage2'))
        
        chatbox = formfields[session['i']]()
        chatbox.userinput.data = ''

    return render_template('testpage1.html', chatbox = chatbox)

@app.route('/testpage2')
def testpage2():

    return render_template('testpage2.html')

if __name__ == '__main__':
    app.run(debug = True)

