from flask import Flask
from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField, RadioField, SubmitField, FileField, validators

submittext = 'Submit'
pagenametext = '''To get started, enter the name of this page. The name you enter will appear at the top of the page.'''
urlnametext = '''Enter the URL for this page. This will appear at the end of it's address, so I recommend you make it short and simple.'''
pagetexttext = '''Enter the text for the current section of this page. Don't worry about fitting everything in, as you will have the option to add another section soon'''
pageimagetext = '''If you'd like to add an image, upload it here using the "Browse" button. If you don't want an image, just click "Submit" without uploading anything.'''
newsectiontext = '''Would you like to add another section to your page?'''
addtonavbartext = '''Would you like to add a link to this page to the navigation bar at the top of the site?'''

class PageName(FlaskForm):
    userinput = StringField(pagenametext, [validators.DataRequired()])
    submit = SubmitField(submittext)

class URLName(FlaskForm):
    userinput = StringField(urlnametext, [validators.DataRequired()])
    submit = SubmitField(submittext)

class PageText(FlaskForm):
    userinput = TextAreaField(pagetexttext, [validators.DataRequired()])
    submit = SubmitField(submittext)

class PageImage(FlaskForm):
    userinput = FileField(pageimagetext)
    submit = SubmitField(submittext)

class NewSection(FlaskForm):
    userinput = RadioField(newsectiontext, choices=[('Yes', 'Yes'), ('No', 'No')])
    submit = SubmitField(submittext)

class AddToNavbar(FlaskForm):
    userinput = RadioField(addtonavbartext, choices=[('Yes', 'Yes'), ('No', 'No')])
    submit = SubmitField(submittext)
