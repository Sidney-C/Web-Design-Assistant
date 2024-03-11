from flask import Flask, render_template, request, url_for, redirect, session
from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField, RadioField, SubmitField, FileField, validators
from user_agents import parse
from forms import *
from helpdocumentation import helpdocs
import os

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret'
app.config['ALLOWED_EXTENSIONS'] = {'jpg', 'jpeg', 'png'}
app.config['UPLOAD_FOLDER'] = 'static'

allassets = {}
assetlist = []
imagecount = 1
navbarlinks = {}
sitenames = []
formfields = [PageName, URLName, PageText, AddImage, PageImage, AltText, ImagePosition, ImageSize, AddLink, LinkDestination, LinkText, NewSection, AddToNavbar]
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


    global allassets
    global assetlist
    global imagecount
    global navbarlinks
    global sitenames
    global formfields
    global starterfields
    global starterassets
    global websitename
    global websitetheme
    global stopnum
    global chatbox
    global errormessage
    
    allassets = {}
    assetlist = []
    imagecount = 1
    navbarlinks = {}
    sitenames = []
    formfields = [PageName, URLName, PageText, AddImage, PageImage, AltText, ImagePosition, ImageSize, AddLink, LinkDestination, LinkText, NewSection, AddToNavbar]
    starterfields = [WebsiteName, WebsiteTheme]
    starterassets = []
    websitename = ''
    websitetheme = ''
    stopnum = 0
    chatbox = ''
    errormessage = ''

    launchapp = LaunchApp()

    if launchapp.validate_on_submit():
        return redirect(url_for('choosename'))

    return render_template('welcome.html', launchapp = launchapp)

@app.route('/choosename', methods = ['GET', 'POST'])
def choosename():
    
    global websitename
    global chatbox

    session['isname'] = True

    chatbox = WebsiteName()

    if chatbox.validate_on_submit():
        session['websitename'] = chatbox.userinput.data
        chatbox.userinput.data = ''
        return redirect(url_for('choosetheme'))

    return render_template('chat.html', chatbox = chatbox, mainchat = False)

@app.route('/choosetheme', methods = ['GET', 'POST'])
def choosetheme():
    
    global websitetheme
    global chatbox

    session['isname'] = False
    session['istheme'] = True

    chatbox = WebsiteTheme()

    if chatbox.validate_on_submit():
        session['websitetheme'] = chatbox.userinput.data
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

    mainchat = False
    session['istheme'] = False

    if 'i' not in session:
        session['i'] = 0
        
    if session['i'] > 0:
        mainchat = True

    if 'assetlist' not in session:
        session['assetlist'] = []

    if 'allassets' not in session:
        session['allassets'] = {}

    if 'navbarlinks' not in session:
        session['navbarlinks'] = {}

    if 'sitenames' not in session:
        session['sitenames'] = []

    if 'imagecount' not in session:
        session['imagecount'] = 0

    increasei = True

    chatbox = formfields[session['i']]()
    undobutton = UndoButton()

    if chatbox.validate_on_submit():

        if session['i'] == 0:

            session['assetlist'].append(chatbox.userinput.data)

            #errormessage = ''
            
            #if session['allassets']:
                #for j in session['allassets']:

                    #if session['allassets'][j][0] == chatbox.userinput.data:
                        #errormessage = 'ERROR: Name already in use. Choose another name.'
                        #chatbox.userinput.data = ''
                        #session['i'] = -1
                        
                #session['assetlist'].append(chatbox.userinput.data)
                #print("adding once")

            #else:
                #session['assetlist'].append(chatbox.userinput.data)
                #print("adding twice")
            
            
        if session['i'] == 1:
            
            print(assetlist)
            errormessage = ''
            doappend = True

            for j in session['allassets']:
                
                if session['allassets'][j][1] == chatbox.userinput.data:
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
                session['assetlist'].append(chatbox.userinput.data)

        if session['i'] == 2:
            print(assetlist)
            session['assetlist'].append([chatbox.userinput.data])

        if session['i'] == 3:
            print(assetlist)
            if chatbox.userinput.data == 'No':
                session['assetlist'][-1].append("no file uploaded")
                increasei = False

        if session['i'] == 4:
            print(assetlist)
            if chatbox.userinput.data and checkextension(chatbox.userinput.data.filename):
                session['image'] = chatbox.userinput.data.filename
            else:
                session['image'] = None
            if session['image']:
                filename = 'user_image' + str(session['imagecount'])
                session['imagecount'] += 1
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                chatbox.userinput.data.save(filepath)
                session['assetlist'][-1].append(filename)
                chatbox.userinput.data = ''
                session.pop('image', None)
            else:
                session['assetlist'][-1].append("repeat")
                chatbox.userinput.data = ''
                session.pop('image', None)
                increasei = False
                
        if session['i'] == 5:
            print(assetlist)
            if chatbox.validate_on_submit():
                session['assetlist'][-1].append(chatbox.userinput.data)

        if session['i'] == 6:
            print(assetlist)
            if chatbox.validate_on_submit():
                session['assetlist'][-1].append(chatbox.userinput.data)

        if session['i'] == 7:
            print(assetlist)
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
                session['assetlist'][-1].append(size)

        if session['i'] == 8:
            print(assetlist)
            if chatbox.userinput.data == 'No':
                session['assetlist'][-1].append("No Link")
                increasei = False

        if session['i'] == 9:
            print(assetlist)
            session['assetlist'][-1].append(chatbox.userinput.data)

        if session['i'] == 10:
            print(assetlist)
            session['assetlist'][-1].append(chatbox.userinput.data)

        if session['i'] == 11:
            print(assetlist)
            session['assetlist'].append(chatbox.userinput.data)
            
            if chatbox.userinput.data == 'Yes':
                session['i'] = 1
            else:
                stopnum = session['assetlist'].index('No', -1)
                session['stopnum'] = stopnum
            session['assetlist'].pop(-1)

        if session['i'] == 12:
            print(assetlist)
            if chatbox.userinput.data == 'Yes':
                session['navbarlinks'][session['assetlist'][0]] = (url_for('currentpage', currenturl=session['assetlist'][1]))
                session['sitenames'].append(session['assetlist'][0])

        if increasei:
            session['i'] += 1
        else:
            if session['i'] == 8:
                session['i'] = 11
            elif session['assetlist'][-1][-1] == "no file uploaded":
                session['i'] = 8
            else:
                session['i'] = 3
                session['assetlist'][-1].pop(-1)
        
        if session['i'] == len(formfields):
            session['assetlist'].append(session['stopnum'])
            session['allassets'][session['assetlist'][1]] = session['assetlist']
            currenturl = session['assetlist'][1]
            session['assetlist'] = []
            session.pop('i', None)
            return redirect(url_for('currentpage', currenturl = currenturl))
        
        chatbox = formfields[session['i']]()
        chatbox.userinput.data = ''
        if session['i'] > 0:
            mainchat = True

    elif undobutton.validate_on_submit():

        if session['i'] == 1:
            session['assetlist'].pop(-1)
            session['i'] += -1
            chatbox.userinput.data = ''
            chatbox = formfields[session['i']]()
            mainchat = False

        elif session['i'] == 2:
            if len(session['assetlist']) == 2:
                session['assetlist'].pop(-1)
                session['i'] += -1
                chatbox.userinput.data = ''
                chatbox = formfields[session['i']]()
                mainchat = True
            else:
                session['i'] = 11
                chatbox.userinput.data = ''
                chatbox = formfields[session['i']]()
                mainchat = True
                
        elif session['i'] == 3:
            session['assetlist'].pop(-1)
            session['i'] += -1
            chatbox.userinput.data = ''
            chatbox = formfields[session['i']]()
            mainchat = True

        elif session['i'] == 5:
            session['assetlist'][-1].pop(-1)
            imagecount += -1
            session['i'] += -1
            chatbox.userinput.data = ''
            chatbox = formfields[session['i']]()
            mainchat = True

        elif session['i'] == 6:
            session['assetlist'][-1].pop(-1)
            session['i'] += -1
            chatbox.userinput.data = ''
            chatbox = formfields[session['i']]()
            mainchat = True

        elif session['i'] == 7:
            session['assetlist'][-1].pop(-1)
            session['i'] += -1
            chatbox.userinput.data = ''
            chatbox = formfields[session['i']]()
            mainchat = True

        elif session['i'] == 8:
            if session['assetlist'][-1][-1] == "no file uploaded":
                session['assetlist'][-1].pop(-1)
                session['i'] = 3
                chatbox.userinput.data = ''
                chatbox = formfields[session['i']]()
                mainchat = True
            else:
                session['assetlist'][-1].pop(-1)
                session['i'] += -1
                chatbox.userinput.data = ''
                chatbox = formfields[session['i']]()
                mainchat = True

        elif session['i'] == 9:
            session['i'] += -1
            chatbox.userinput.data = ''
            chatbox = formfields[session['i']]()
            mainchat = True

        elif session['i'] == 10:
            session['assetlist'][-1].pop(-1)
            session['i'] += -1
            chatbox.userinput.data = ''
            chatbox = formfields[session['i']]()
            mainchat = True

        elif session['i'] == 11:
            if session['assetlist'][-1][-1] == "no file uploaded":
                session['assetlist'][-1].pop(-1)
                session['i'] = 3
                chatbox.userinput.data = ''
                chatbox = formfields[session['i']]()
                mainchat = True
            elif session['assetlist'][-1][-1] == "No Link":
                session['assetlist'][-1].pop(-1)
                session['i'] = 8
                chatbox.userinput.data = ''
                chatbox = formfields[session['i']]()
                mainchat = True
            else:
                session['assetlist'][-1].pop(-1)
                session['i'] += -1
                chatbox.userinput.data = ''
                chatbox = formfields[session['i']]()
                mainchat = True

        elif session['i'] == 12:
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

    print(allassets)
    session['currentassets'] = session['allassets'][currenturl]
    session['stophere'] = session['currentassets'][-1]
    print(session['currentassets'])
    
    return render_template('yourwebsite.html', websitename = session['websitename'], websitetheme = session['websitetheme'], currentassets = session['currentassets'], stopnum = session['stophere'], navbarlinks = session['navbarlinks'], sitenames = session['sitenames'])

@app.route('/showsource')
def showsource():

    findbrowser = request.user_agent.string
    browser = parse(findbrowser)
    browsername = browser.browser.family

    return render_template('showsource.html', browsername=browsername)

@app.route('/help')
def help():

    whichclass = 0

    if session['isname'] == True:
        whichclass = 111
    elif session['istheme'] == True:
        whichclass = 999
    else:
        whichclass = session['i']

    helpdoc = helpdocs(whichclass)

    return render_template('help.html', helpdoc = helpdoc)

if __name__ == '__main__':
    app.run(debug = True)


