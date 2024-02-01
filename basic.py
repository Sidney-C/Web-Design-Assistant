from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, SubmitField

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret'

class NameForm(FlaskForm):
    sitename = StringField('Enter the name of your website')
    submit = SubmitField('Submit')

@app.route('/', methods = ['GET', 'POST'])
def index():
    sitename = False
    nameform = NameForm()

    if nameform.validate_on_submit():
        sitename = nameform.sitename.data
        nameform.sitename.data = ''

    return render_template('index.html', nameform=nameform, sitename=sitename)

if __name__ == '__main__':
    app.run(debug = True)
