from flask import Flask
from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField, RadioField, SubmitField, FileField, validators

submittext = 'Submit'
websitenametext = '''Hi there! To get started, enter the name of your website. Keep in mind that this will appear at the top of every page.'''
websitethemetext = '''Choose a theme for your website. This will be applied to every page.'''
pagenametext = '''Now, enter the name of this page. The name you enter will appear at the top of the page.'''
urlnametext = '''Enter the URL for this page. This will appear at the end of its address, so I recommend you make it short and simple. For technical reasons, it can only contain letters, numbers, "_", and "-".'''
pagetexttext = '''Enter the text for the current section of this page. Don't worry about fitting everything in, as you will have the option to add another section soon'''
pageimagetext = '''If you'd like to add an image, upload it here using the "Browse" button. If you don't want an image, just click "Submit" without uploading anything.'''
alttexttext = '''Enter a text description of the image, so that the page is accessible to people using screen readers.'''
newsectiontext = '''Would you like to add another section to your page?'''
addtonavbartext = '''Would you like to add a link to this page to the navigation bar at the top of the site?'''

class WebsiteName(FlaskForm):
    userinput = StringField(websitenametext, [validators.DataRequired()])
    submit = SubmitField(submittext)

class WebsiteTheme(FlaskForm):
    userinput = RadioField(websitethemetext, choices = [('Dark', 'Dark'), ('Light', 'Light')])
    submit = SubmitField(submittext)

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

class AltText(FlaskForm):
    userinput = TextAreaField(alttexttext, [validators.DataRequired()])
    submit = SubmitField(submittext)

class NewSection(FlaskForm):
    userinput = RadioField(newsectiontext, choices=[('Yes', 'Yes'), ('No', 'No')])
    submit = SubmitField(submittext)

class AddToNavbar(FlaskForm):
    userinput = RadioField(addtonavbartext, choices=[('Yes', 'Yes'), ('No', 'No')])
    submit = SubmitField(submittext)

class LaunchApp(FlaskForm):
    submit = SubmitField('Begin')
