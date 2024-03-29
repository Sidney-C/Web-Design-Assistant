from flask import Flask
from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField, RadioField, SubmitField, FileField, validators

submittext = 'Submit'
websitenametext = '''Hi there! To get started, enter the name of your website. Keep in mind that this will appear at the top of every page.'''
websitethemetext = '''Choose a theme for your website. This will be applied to every page.'''
pagenametext = '''Now, enter the name of this page. The name you enter will appear at the top of the page.'''
urlnametext = '''Enter the URL for this page. This will appear at the end of its address, so I recommend you make it short and simple. For technical reasons, it can only contain letters, numbers, "_", and "-".'''
pagetexttext = '''Enter the text for the current section of this page. Don't worry about fitting everything in, as you will have the option to add another section soon'''
addimagetext = '''Would you like to add an image?'''
pageimagetext = '''Select and upload an image from your computer using the "Browse" button. It must be in .jpg, .jpeg, or .png format.'''
alttexttext = '''Enter a text description of the image, so that the page is accessible to people using screen readers.'''
imagepositiontext = '''Choose where you would like the image to be placed in relation to the current paragraph of text.'''
imagesizetext = '''Choose a size for the image, or select auto if you would like it to remain the size it currently is on your computer.'''
addlinktext = '''Would you like to include a link to another page or an external website in this section?'''
linkdestinationtext = '''Enter the address of the page you would like to link to.'''
linktexttext = '''Enter the text of the link for the user to see.'''
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

class AddImage(FlaskForm):
    userinput = RadioField(addimagetext, choices = [('Yes', 'Yes'), ('No', 'No')])
    submit = SubmitField(submittext)

class PageImage(FlaskForm):
    userinput = FileField(pageimagetext)
    submit = SubmitField(submittext)

class AltText(FlaskForm):
    userinput = TextAreaField(alttexttext, [validators.DataRequired()])
    submit = SubmitField(submittext)

class ImagePosition(FlaskForm):
    userinput = RadioField(imagepositiontext, choices = [('Above', 'Above'), ('Below', 'Below'), ('Left', 'Left'), ('Right', 'Right')])
    submit = SubmitField(submittext)

class ImageSize(FlaskForm):
    userinput = RadioField(imagesizetext, choices = [('Extra Small', 'Extra Small'), ('Small', 'Small'), ('Medium', 'Medium'), ('Large', 'Large'), ('Extra Large', 'Extra Large'), ('Auto', 'Auto')])
    submit = SubmitField(submittext)

class AddLink(FlaskForm):
    userinput = RadioField(addlinktext, choices = [('Yes', 'Yes'), ('No', 'No')])
    submit = SubmitField(submittext)

class LinkDestination(FlaskForm):
    userinput = StringField(linkdestinationtext, [validators.DataRequired()])
    submit = SubmitField(submittext)

class LinkText(FlaskForm):
    userinput = StringField(linktexttext, [validators.DataRequired()])
    submit = SubmitField(submittext)
    
class NewSection(FlaskForm):
    userinput = RadioField(newsectiontext, choices=[('Yes', 'Yes'), ('No', 'No')])
    submit = SubmitField(submittext)

class AddToNavbar(FlaskForm):
    userinput = RadioField(addtonavbartext, choices=[('Yes', 'Yes'), ('No', 'No')])
    submit = SubmitField(submittext)

class LaunchApp(FlaskForm):
    submit = SubmitField('Begin')

class UndoButton(FlaskForm):
    submit = SubmitField('Undo Last Step')

