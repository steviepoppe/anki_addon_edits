#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    Kokugo Jiten Online Definitions addon for Anki,
    pulls definitions from kokugo.jitenon.jp

    This addon is adapted from kqueryful's Sanseido-Definitions addon
    All credit goes to them, I've just changed some webscraping specifics

    @author     = steviep
    @date         = 4/17/2021
    @version     = 1.0
"""
from bs4 import BeautifulSoup
import urllib.request, urllib.parse, urllib.error
import re

# Edit these field names if necessary ==========================================
expressionField = 'Expression'
definitionField = 'Sanseido'
# ==============================================================================

# Fetch definition from Sanseido ===============================================
def fetchDef(term):
    defText = ""

    searched = re.search(r'^[^\[]+',expression)
    if searched:
        expression = searched.group(0)

    pageUrl = "https://kokugo.jitenon.jp/word/p18894?getdata=" + urllib.parse.quote(term.encode('utf-8')) + "&amp;search=match"
    response = urllib.request.urlopen(pageUrl)
    soup = BeautifulSoup(response, "html.parser")
    NetDicBody = soup.find('div', class_ = "NetDicBody")

    if NetDicBody != None:
        defFinished = False
        
        for line in NetDicBody.children:
            if line.name == "b":
                if len(line) != 1:
                    for child in line.children:
                        if child.name == "span":
                            defFinished = True
            if defFinished:
                break
            
            if line.string != None and line.string != "\n":
                defText += line.string

    defText = re.sub(r"［(?P<no>[２-９]+)］", r"<br/><br/>［\1］", defText)
    return re.sub(r"（(?P<num>[２-９]+)）", r"<br/>（\1）", defText)

# Update note ==================================================================
#from PyQt4.QtCore import *
#from PyQt4.QtGui import *
from anki.hooks import addHook
from anki.notes import Note
from aqt import mw
from aqt.qt import *
import aqt


def glossNote( f ):
    if f[ definitionField ]: return
    f[ definitionField ] = fetchDef( f[ expressionField ] )
    f.flush()

def setupMenu( ed ):
    a = QAction( 'Regenerate Sanseido definitions', ed )
    #ed.connect( a, SIGNAL('triggered()'), lambda e=ed: onRegenGlosses( e ) )
    a.triggered.connect(lambda : onRegenGlosses(ed))
    ed.form.menuEdit.addAction( a )

def onRegenGlosses( ed ):
    n = "Regenerate Sanseido definitions"
    def callback():
        regenGlosses(ed, ed.selectedNotes() )   
        mw.requireReset()
    ed.editor.saveNow(callback)
    
def regenGlosses( ed, fids ):
    mw.progress.start( max=len( fids ) , immediate=True)
    for (i,fid) in enumerate( fids ):
        mw.progress.update( label='Generating Sanseido definitions...', value=i )
        f = mw.col.getNote(id=fid)
        try: glossNote( f )
        except:
            import traceback
            print('definitions failed:')
            traceback.print_exc()
        try: f.flush()
        except:
            raise Exception()
        ed.onRowChanged(f,f)
    mw.progress.finish()
    
addHook( 'browser.setupMenus', setupMenu )




