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
formfields = [PageName, URLName, PageText, AddImage, PageImage, AltText, ImagePosition, ImageSize, NewSection, AddToNavbar]
starterfields = [WebsiteName, WebsiteTheme]
starterassets = []
websitename = ''
websitetheme = ''
stopnum = 0
chatbox = ''
errormessage = ''

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

    return render_template('chat.html', chatbox = chatbox, mainchat = False)

@app.route('/choosetheme', methods = ['GET', 'POST'])
def choosetheme():
    
    global websitetheme
    global chatbox

    chatbox = WebsiteTheme()

    if chatbox.validate_on_submit():
        websitetheme = chatbox.userinput.data
        chatbox.userinput.data = ''
        return redirect(url_for('chat'))

    return render_template('chat.html', chatbox = chatbox, mainchat = False)

@app.route('/chat', methods = ['GET', 'POST'])
def chat():
    
    global imagecount
    global websitename
    global assetlist
    global websitetheme
    global stopnum
    global chatbox
    global errormessage

    if 'i' not in session:
        session['i'] = 0
        
    if session['i'] < 1:
        mainchat = False

    increasei = True

    chatbox = formfields[session['i']]()
    undobutton = UndoButton()

    if chatbox.validate_on_submit():

        if session['i'] == 0:

            errormessage = ''
            
            if allassets:
                for j in allassets:

                    if allassets[j][0] == chatbox.userinput.data:
                        errormessage = 'ERROR: Name already in use. Choose another name.'
                        chatbox.userinput.data = ''
                        session['i'] = -1
                    else:
                        assetlist.append(chatbox.userinput.data)
            else:
                assetlist.append(chatbox.userinput.data)
            
            
        if session['i'] == 1:

            errormessage = ''
            doappend = True

            for j in allassets:
                
                if allassets[j][1] == chatbox.userinput.data:
                    errormessage = 'ERROR: URL already in use. Choose another URL.'
                    chatbox.userinput.data = ''
                    session['i'] = 0
                    doappend = False

            for j in chatbox.userinput.data:

                if not j.isalpha():
                    if not j.isnumeric():
                        if j != '_':
                            if j != '-':
                                errormessage = 'ERROR. URL contains an invalid character. Choose another URL, using only letters, numbers, "_", and "-".'
                                chatbox.userinput.data = ''
                                session['i'] = 0
                                doappend = False

            if doappend == True:
                assetlist.append(chatbox.userinput.data)

        if session['i'] == 2:
            assetlist.append([chatbox.userinput.data])

        if session['i'] == 3:
            if chatbox.userinput.data == 'No':
                assetlist[-1].append("no file uploaded")
                increasei = False

        if session['i'] == 4:
            if chatbox.userinput.data and checkextension(chatbox.userinput.data.filename):
                session['image'] = chatbox.userinput.data.filename
            else:
                session['image'] = None
            if session['image']:
                filename = 'user_image' + str(imagecount)
                imagecount += 1
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                chatbox.userinput.data.save(filepath)
                assetlist[-1].append(filename)
                chatbox.userinput.data = ''
                session.pop('image', None)
            else:
                assetlist[-1].append("repeat")
                chatbox.userinput.data = ''
                session.pop('image', None)
                increasei = False
                
        if session['i'] == 5:
            if chatbox.validate_on_submit():
                assetlist[-1].append(chatbox.userinput.data)

        if session['i'] == 6:
            if chatbox.validate_on_submit():
                assetlist[-1].append(chatbox.userinput.data)

        if session['i'] == 7:
            if chatbox.validate_on_submit():
                size = chatbox.userinput.data
                if size == 'Extra Small':
                    size = 'height: auto; width: 100px'
                elif size == 'Small':
                    size = 'height: auto; width: 300px'
                elif size == 'Medium':
                    size = 'height: auto; width: 500px'
                elif size == 'Large':
                    size = 'height: auto; width: 700px'
                elif size == 'Extra Large':
                    size = 'height: auto; width: 900px'
                elif size == 'Auto':
                    size = ''
                assetlist[-1].append(size)

        if session['i'] == 8:
            assetlist.append(chatbox.userinput.data)
            
            if chatbox.userinput.data == 'Yes':
                session['i'] = 1
            else:
                stopnum = assetlist.index('No', -1)
                session['stopnum'] = stopnum
            assetlist.pop(-1)

        if session['i'] == 9:
            if chatbox.userinput.data == 'Yes':
                navbarlinks[assetlist[0]] = (url_for('currentpage', currenturl=assetlist[1]))
                sitenames.append(assetlist[0])

        if increasei:
            session['i'] += 1
        else:
            if assetlist[-1][-1] == "no file uploaded":
                session['i'] = 8
            else:
                session['i'] = 3
                assetlist[-1].pop(-1)
        
        if session['i'] == len(formfields):
            assetlist.append(session['stopnum'])
            allassets[assetlist[1]] = assetlist
            currenturl = assetlist[1]
            assetlist = []
            session.pop('i', None)
            return redirect(url_for('currentpage', currenturl = currenturl))
        
        chatbox = formfields[session['i']]()
        chatbox.userinput.data = ''
        if session['i'] > 0:
            mainchat = True

    elif undobutton.validate_on_submit():

        if session['i'] == 1:
            assetlist.pop(-1)
            session['i'] += -1
            chatbox.userinput.data = ''
            chatbox = formfields[session['i']]()
            mainchat = False

        elif session['i'] == 2:
            assetlist.pop(-1)
            session['i'] += -1
            chatbox.userinput.data = ''
            chatbox = formfields[session['i']]()
            mainchat = True

        elif session['i'] == 3:
            assetlist.pop(-1)
            session['i'] += -1
            chatbox.userinput.data = ''
            chatbox = formfields[session['i']]()
            mainchat = True

        elif session['i'] == 5:
            assetlist[-1].pop(-1)
            imagecount += -1
            session['i'] += -1
            chatbox.userinput.data = ''
            chatbox = formfields[session['i']]()
            mainchat = True

        elif session['i'] == 6:
            assetlist[-1].pop(-1)
            session['i'] += -1
            chatbox.userinput.data = ''
            chatbox = formfields[session['i']]()
            mainchat = True

        elif session['i'] == 7:
            assetlist[-1].pop(-1)
            session['i'] += -1
            chatbox.userinput.data = ''
            chatbox = formfields[session['i']]()
            mainchat = True

        elif session['i'] == 8:
            if assetlist[-1][1] == "no file uploaded":
                assetlist[-1].pop(-1)
                session['i'] = 3
                chatbox.userinput.data = ''
                chatbox = formfields[session['i']]()
                mainchat = True
            else:
                assetlist[-1].pop(-1)
                session['i'] += -1
                chatbox.userinput.data = ''
                chatbox = formfields[session['i']]()
                mainchat = True

        elif session['i'] == 9:
            session['i'] += -1
            chatbox.userinput.data = ''
            chatbox = formfields[session['i']]()
            mainchat = True

    return render_template('chat.html', chatbox = chatbox, errormessage = errormessage, undobutton = undobutton, mainchat = mainchat)

@app.route('/yourwebsite')
def yourwebsite():

    stopnum = session.get('stopnum')
    
    return render_template('yourwebsite.html', assetlist = assetlist, stopnum = stopnum, websitename = websitename)

@app.route('/yourwebsite/<currenturl>')
def currentpage(currenturl):

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


