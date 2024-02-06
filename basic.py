from flask import Flask, render_template, request, url_for, redirect, session
from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField, RadioField, SubmitField, validators
from user_agents import parse

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret'

class NameForm(FlaskForm):
    sitename = StringField('Enter the name of your website *', [validators.DataRequired()])
    textcontent = TextAreaField('Enter the text for the first section of your website *', [validators.DataRequired()])
    textcontent2 = TextAreaField('If you would like a second section, enter the text here')
    submit = SubmitField('Generate Website!')
    
@app.route('/', methods = ['GET', 'POST'])
def index():
    sitename = False
    textcontent = False
    textcontent2 = False
    nameform = NameForm()

    if nameform.validate_on_submit():
        session['sitename'] = nameform.sitename.data
        nameform.sitename.data = ''
        #print(f"Step 1: {sitename}")
        session['textcontent'] = nameform.textcontent.data
        nameform.textcontent.data = ''
        #print(f"Step 2: {textcontent}")
        session['textcontent2'] = nameform.textcontent2.data
        nameform.textcontent2.data = ''
        return redirect(url_for('yourwebsite'))

    return render_template('index.html', nameform=nameform)

@app.route('/yourwebsite')
def yourwebsite():

    return render_template('yourwebsite.html')

@app.route('/showcode')
def showcode():

    findbrowser = request.user_agent.string
    browser = parse(findbrowser)
    browsername = browser.browser.family
    #print(f"Browser: {browsername}")

    return render_template('showcode.html', browsername=browsername)

if __name__ == '__main__':
    app.run(debug = True)
