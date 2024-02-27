from flask import Flask, render_template, request, url_for, redirect, session
from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField, RadioField, SubmitField, FileField, validators
from user_agents import parse
from forms import *
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
websitename = ''

def checkextension(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/testpage1', methods = ['GET', 'POST'])
def testpage1():
    
    global imagecount
    global websitename
    global assetlist

    if 'i' not in session:
        session['i'] = 0

    if websitename == '':
        chatbox = WebsiteName()
        if chatbox.validate_on_submit():
            websitename = chatbox.userinput.data
            chatbox = formfields[session['i']]()
            chatbox.userinput.data = ''

    else:
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

    return render_template('testpage1.html', chatbox = chatbox)

@app.route('/testpage2')
def testpage2():

    stopnum = session.get('stopnum')

    #filenames = []
    
    #for i in range(2, stopnum):
        #filenames.append(assetlist[i][1])
    
    print(allassets)
    return render_template('testpage2.html', assetlist = assetlist, stopnum = stopnum, websitename = websitename)

@app.route('/testpage2/<currenturl>')
def currentpage(currenturl):


    currentassets = allassets[currenturl]
    stopnum = currentassets[-1]

    print('navbarlinks:')
    print(navbarlinks)
    print('sitenames:')
    print(sitenames)
    print('websitename:')
    print(websitename)
    print('allassets:')
    print(allassets)
    print('currentassets:')
    print(currentassets)
    print('stopnum:')
    print(stopnum)
    
    return render_template('testpage2.html', currentassets = currentassets, stopnum = stopnum, websitename = websitename)

@app.route('/testpage3')
def testpage3():

    findbrowser = request.user_agent.string
    browser = parse(findbrowser)
    browsername = browser.browser.family

    return render_template('testpage3.html', browsername=browsername)

if __name__ == '__main__':
    app.run(debug = True)


