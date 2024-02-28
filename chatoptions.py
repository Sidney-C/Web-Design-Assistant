from flask import Flask, render_template, request, url_for, redirect, session
from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField, RadioField, SubmitField, FileField, validators
from user_agents import parse
from forms import *
import os

def options(stage, assetlist, formfields, imagecount, navbarlinks, sitenames, allassets):

    chatbox = formfields[session['i']]()
        
    if chatbox.validate_on_submit():

        if stage < 3:
            return chatbox.userinput.data

        elif stage == 3:
            session['image'] = chatbox.userinput.data
            if session['image'] and checkextension(session['image'].filename):
                filename = 'user_image' + str(imagecount)
                imagecount += 1
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                session['image'].save(filepath)
                chatbox.userinput.data = ''
                session.pop('image', None)
                return filename
            else:
                chatbox.userinput.data = ''
                session.pop('image', None)
                return("no file uploaded")

        elif stage == 4:
            if chatbox.userinput.data == 'Yes':
                stage = 1
            else:
                assetlist.append(chatbox.userinput.data)
                stopnum = assetlist.index('No', -1)
                assetlist.pop(-1)
                return stopnum

        elif stage == 5:
            if chatbox.userinput.data == 'Yes':
                navbarlinks[assetlist[0]] = (url_for('currentpage', currenturl=assetlist[1]))
                sitenames.append(assetlist[0])
                assetlist.pop(-1)
                return navbarlinks, sitenames
                
        #session['i'] += 1
        elif stage == len(formfields):
            assetlist.append(session['stopnum'])
            allassets[assetlist[1]] = assetlist
            currenturl = assetlist[1]
            #assetlist = []
            #session['i'] = 0
            return assetlist, assetlist[1]
            #return redirect(url_for('currentpage', currenturl = currenturl))
        
        #chatbox = formfields[session['i']]()
        #chatbox.userinput.data = ''
