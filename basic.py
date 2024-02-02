from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, SubmitField

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret'

class NameForm(FlaskForm):
    sitename = StringField('Enter the name of your website')
    submit = SubmitField('Submit')
    textcontent = StringField('Enter the text for your website')

@app.route('/', methods = ['GET', 'POST'])
def index():
    step = request.args.get('step', default = 1, type = int)
    sitename = False
    textcontent = False
    nameform = NameForm()

    if nameform.validate_on_submit():
        if step == 1:
            sitename = nameform.sitename.data
            nameform.sitename.data = ''
        elif which == 2:
            textcontent = nameform.textcontent.data
            nameform.textcontent.data = ''

        step += 1

    return render_template('index.html', nameform=nameform, sitename=sitename, step=step)

if __name__ == '__main__':
    app.run(debug = True)
