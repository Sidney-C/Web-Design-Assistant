from flask import Flask, render_template, request, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, SubmitField, validators

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret'

class NameForm(FlaskForm):
    sitename = StringField('Enter the name of your website', [validators.DataRequired()])
    textcontent = StringField('Enter the text for your website', [validators.DataRequired()])
    submit = SubmitField('Submit')
    
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
            print(f"Step 1: {sitename}")
        elif step == 2:
            textcontent = nameform.textcontent.data
            nameform.textcontent.data = ''
            print(f"Step 2: {textcontent}")
        step += 1
            #return redirect(url_for('yourwebsite'))

    return render_template('index.html', nameform=nameform, sitename=sitename, textcontent=textcontent, step=step)

@app.route('/yourwebsite')
def yourwebsite():
    #sitename = sitename
    #textcontent = textcontent

    return render_template('yourwebsite.html')

if __name__ == '__main__':
    app.run(debug = True)
