from flask import Flask, render_template, request, url_for, redirect, session
from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField, RadioField, SubmitField, FileField, validators
from user_agents import parse
from forms import *
from helpdocumentation import helpdocs
import os

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret'
app.config['ALLOWED_EXTENSIONS'] = {'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = 'static'

allassets = {}
assetlist = []
imagecount = 1
navbarlinks = {}
sitenames = []
formfields = [PageName, URLName, PageText, PageImage, NewSection, AddToNavbar]
starterfields = [WebsiteName, WebsiteTheme]
starterassets = []
websitename = ''
websitetheme = ''
stopnum = 0
chatbox = ''

def checkextension(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def landingpage():

    return redirect(url_for('welcome'))

@app.route('/welcome', methods = ['GET', 'POST'])
def welcome():

    launchapp = LaunchApp()

    if launchapp.validate_on_submit():
        return redirect(url_for('choosename'))

    return render_template('welcome.html', launchapp = launchapp)

@app.route('/choosename', methods = ['GET', 'POST'])
def choosename():
    
    global websitename
    global chatbox

    chatbox = WebsiteName()

    if chatbox.validate_on_submit():
        websitename = chatbox.userinput.data
        chatbox.userinput.data = ''
        return redirect(url_for('choosetheme'))

    return render_template('chat.html', chatbox = chatbox)

@app.route('/choosetheme', methods = ['GET', 'POST'])
def choosetheme():
    
    global websitetheme
    global chatbox

    chatbox = WebsiteTheme()

    if chatbox.validate_on_submit():
        websitetheme = chatbox.userinput.data
        chatbox.userinput.data = ''
        return redirect(url_for('chat'))

    return render_template('chat.html', chatbox = chatbox)

@app.route('/chat', methods = ['GET', 'POST'])
def chat():
    
    global imagecount
    global websitename
    global assetlist
    global websitetheme
    global stopnum
    global chatbox

    if 'i' not in session:
        session['i'] = 0

    chatbox = formfields[session['i']]()

    if chatbox.validate_on_submit():

        if session['i'] == 2:
            assetlist.append([chatbox.userinput.data])

        elif session['i'] == 3:
            session['image'] = chatbox.userinput.data
            if session['image'] and checkextension(session['image'].filename):
                filename = 'user_image' + str(imagecount)
                imagecount += 1
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                session['image'].save(filepath)
                assetlist[-1].append(filename)
                chatbox.userinput.data = ''
                session.pop('image', None)
            else:
                assetlist[-1].append("no file uploaded")
                chatbox.userinput.data = ''
                session.pop('image', None)
        
        else:
            assetlist.append(chatbox.userinput.data)

        if session['i'] == 4:
            if chatbox.userinput.data == 'Yes':
                session['i'] = 1
            else:
                stopnum = assetlist.index('No', -1)
                session['stopnum'] = stopnum
            assetlist.pop(-1)

        if session['i'] == 5:
            if chatbox.userinput.data == 'Yes':
                navbarlinks[assetlist[0]] = (url_for('currentpage', currenturl=assetlist[1]))
                sitenames.append(assetlist[0])
            assetlist.pop(-1)
                
        session['i'] += 1
        if session['i'] == len(formfields):
            assetlist.append(session['stopnum'])
            allassets[assetlist[1]] = assetlist
            currenturl = assetlist[1]
            assetlist = []
            session['i'] = 0
            return redirect(url_for('currentpage', currenturl = currenturl))
        
        chatbox = formfields[session['i']]()
        chatbox.userinput.data = ''

    return render_template('chat.html', chatbox = chatbox)

@app.route('/yourwebsite')
def yourwebsite():

    stopnum = session.get('stopnum')
    
    print(allassets)
    return render_template('yourwebsite.html', assetlist = assetlist, stopnum = stopnum, websitename = websitename)

@app.route('/yourwebsite/<currenturl>')
def currentpage(currenturl):

    print(websitetheme)
    print(websitename)
    currentassets = allassets[currenturl]
    stopnum = currentassets[-1]
    
    return render_template('yourwebsite.html', websitename = websitename, websitetheme = websitetheme, currentassets = currentassets, stopnum = stopnum, navbarlinks = navbarlinks, sitenames = sitenames)

@app.route('/showsource')
def showsource():

    findbrowser = request.user_agent.string
    browser = parse(findbrowser)
    browsername = browser.browser.family

    return render_template('showsource.html', browsername=browsername)

@app.route('/help')
def help():

    helpdoc = helpdocs(str(chatbox.__class__))

    return render_template('help.html', helpdoc = helpdoc)

if __name__ == '__main__':
    app.run(debug = True)


