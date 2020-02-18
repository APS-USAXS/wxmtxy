#!/usr/bin/env python
#Boa:App:BoaApp

#*************************************************************************
# Copyright (c) 2009-2010 The University of Chicago, as Operator of Argonne
#     National Laboratory.
# Copyright (c) 2009-2010 The Regents of the University of California, as
#     Operator of Los Alamos National Laboratory.
# This file is distributed subject to a Software License Agreement found
# in the file LICENSE that is included with this distribution. 
#*************************************************************************

'''
start the wxmtxy GUI

@version: 
########### SVN repository information ###################
# $Date: 2010-06-03 16:04:15 -0500 (Thu, 03 Jun 2010) $
# $Author: jemian $
# $Revision: 184 $
# $URL: https://subversion.xor.aps.anl.gov/bcdaext/wxmtxy/trunk/wxmtxy.py $
# $Id: wxmtxy.py 184 2010-06-03 21:04:15Z jemian $
########### SVN repository information ###################

README

    *wxmtxy* (an EPICS GUI tool) provides support for an X,Y positioner 
    (motor) pair by allowing users to define a table of known positions 
    and providing a one-button click to drive a chosen X,Y pair to a specific
    table setting.  Also can record current position into a setting.

    Several sets of X,Y positioners can be configured.  (Each set is 
    separate.)  In fact, the positioners do not have to be motors,
    but can be any type of EPICS PV that will accept a numeric value.


    wxmtxy is based on wxPython and relies on CaChannel to communicate 
    with EPICS. 
    
    In the Graphical User Interface (GUI), tooltips are provided for 
    most items.  Moving and pausing the mouse over a widget (GUI 
    component such as a button or a label) will cause a terse description 
    of that widget to be displayed. Moving the mouse away will cause that 
    tooltip to disappear. 
    
    For more help, explanations are provided in the HTML pages.
    
    TRAC wiki
    @see: https://subversion.xor.aps.anl.gov/trac/bcdaext/wiki/wxmtxy
    
    @note: subversion checkout:  svn co https://subversion.xor.aps.anl.gov/bcdaext/wxmtxy/

----
 @note: wxPython does not provide standard tear-off windows
 @see: http://wiki.python.org/moin/Distutils/Tutorial
 @see: http://www.py2exe.org/index.cgi/Tutorial
 @note: for an undo example, see: http://wiki.wxpython.org/AnotherTutorial
'''


import wx
import wxmtxy_root
import pvConnect
import sys


modules ={u'wxmtxy_htmlview': [0,
                      'HtmlView to view HTML-formatted help files',
                      u'wxmtxy_htmlview.py'],
 u'wxmtxy_pair': [0,
                  'configuration for X,Y pair of EPICS positioners',
                  u'wxmtxy_pair.py'],
 u'wxmtxy_pvsetup': [0, 'configure EPICS for X,Y pair', u'wxmtxy_pvsetup.py'],
 u'wxmtxy_root': [1, 'Main frame of Application', u'wxmtxy_root.py'],
 u'wxmtxy_row': [0, 'one row of settings', u'wxmtxy_row.py'],
 u'wxmtxy_tab': [0, 'set of rows with positioner settings', u'wxmtxy_tab.py']}


class BoaApp(wx.App):
    '''Built using Boa-constructor (as a subclass of wx.App)'''

    def OnInit(self):
        '''demonstrate the use of this tool'''
        self.main = wxmtxy_root.create(None)
        self.main.Show()
        self.SetTopWindow(self.main)
        return True


def on_exit(timer, epics_db):
    '''Exit handler to stop the ca.poll()
        @param timer: CaPollWx object
        @param epics_db: Python list of pvConnect.EpicsPv objects to be released'''
    #print __name__, "exit handler"
    #for item in epics_db:
    #    item.release()
    if pvConnect.IMPORTED_CACHANNEL:
        pvConnect.on_exit(timer)


def main():
    '''operate the tool'''
    application = wx.App()
    settingsFile = None
    if len(sys.argv) == 2:
        settingsFile = sys.argv[1]
    wxmtxy_root.root(None, settingsFile).Show()
    capoll_timer = None
    if pvConnect.IMPORTED_CACHANNEL:
        capoll_timer = pvConnect.CaPollWx(0.1)
        capoll_timer.start()
    application.MainLoop()
    on_exit(capoll_timer, None)


if __name__ == '__main__':
    main()
