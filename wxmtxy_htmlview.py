#!/usr/bin/env python
#Boa:Frame:HtmlView

#*************************************************************************
# Copyright (c) 2009-2010 The University of Chicago, as Operator of Argonne
#     National Laboratory.
# Copyright (c) 2009-2010 The Regents of the University of California, as
#     Operator of Los Alamos National Laboratory.
# This file is distributed subject to a Software License Agreement found
# in the file LICENSE that is included with this distribution. 
#*************************************************************************

'''
HtmlView to view HTML-formatted help files

@version: 
########### SVN repository information ###################
# $Date: 2010-06-03 16:04:15 -0500 (Thu, 03 Jun 2010) $
# $Author: jemian $
# $Revision: 184 $
# $URL: https://subversion.xor.aps.anl.gov/bcdaext/wxmtxy/trunk/wxmtxy_htmlview.py $
# $Id: wxmtxy_htmlview.py 184 2010-06-03 21:04:15Z jemian $
########### SVN repository information ###################
'''


import wx
import wx.html
import wx.lib.stattext
import wx.lib.buttons
import os
import inspect


def create(parent):
    return HtmlView(parent)


[wxID_HTMLVIEW, wxID_HTMLVIEWBACK, wxID_HTMLVIEWFORWARD, 
 wxID_HTMLVIEWGENSTATICTEXT1, wxID_HTMLVIEWHOME, wxID_HTMLVIEWHTML, 
 wxID_HTMLVIEWLBLPAGENAME, wxID_HTMLVIEWREFRESH, 
] = [wx.NewId() for _init_ctrls in range(8)]


class HtmlView(wx.Frame):
    '''HtmlView to view HTML-formatted help files'''

    def _init_coll_boxSizer1_Items(self, parent):
        # generated method, don't edit

        parent.AddSizer(self.boxSizer2, 0, border=0, flag=wx.GROW)
        parent.AddWindow(self.html, 1, border=0, flag=wx.GROW)

    def _init_coll_boxSizer2_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.back, 0, border=0, flag=0)
        parent.AddWindow(self.home, 0, border=0, flag=0)
        parent.AddWindow(self.refresh, 0, border=0, flag=0)
        parent.AddWindow(self.forward, 0, border=0, flag=0)
        parent.AddWindow(self.genStaticText1, 1, border=0,
              flag=wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL)

    def _init_sizers(self):
        # generated method, don't edit
        self.boxSizer1 = wx.BoxSizer(orient=wx.VERTICAL)

        self.boxSizer2 = wx.BoxSizer(orient=wx.HORIZONTAL)

        self._init_coll_boxSizer1_Items(self.boxSizer1)
        self._init_coll_boxSizer2_Items(self.boxSizer2)

        self.lblPageName.SetSizer(self.boxSizer1)

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_HTMLVIEW, name='HtmlView', parent=prnt,
              pos=wx.Point(820, 328), size=wx.Size(800, 600),
              style=wx.DEFAULT_FRAME_STYLE, title='HtmlView: home')
        self.SetClientSize(wx.Size(792, 566))
        self.Center(wx.BOTH)

        self.lblPageName = wx.Panel(id=wxID_HTMLVIEWLBLPAGENAME,
              name='lblPageName', parent=self, pos=wx.Point(0, 0),
              size=wx.Size(792, 566), style=wx.TAB_TRAVERSAL)
        self.lblPageName.SetToolTipString('name of current page')
        self.lblPageName.SetLabel('pagename')

        self.genStaticText1 = wx.lib.stattext.GenStaticText(ID=wxID_HTMLVIEWGENSTATICTEXT1,
              label='   HtmlView is a limited-capability WWW browser to view HTML-formatted help',
              name='genStaticText1', parent=self.lblPageName, pos=wx.Point(124,
              8), size=wx.Size(370, 13), style=0)
        self.genStaticText1.SetToolTipString('name of current page')

        self.back = wx.BitmapButton(
              id=wxID_HTMLVIEWBACK, name='back',
              parent=self.lblPageName, pos=wx.Point(0, 0), size=wx.Size(31, 30),
              style=0)
        self.back.SetToolTipString('back to previous page')
        self.back.Bind(wx.EVT_BUTTON, self.OnBackButton, id=wxID_HTMLVIEWBACK)

        self.home = wx.BitmapButton(
              id=wxID_HTMLVIEWHOME, name='home',
              parent=self.lblPageName, pos=wx.Point(31, 0), size=wx.Size(31,
              30), style=0)
        self.home.SetToolTipString('home to starting page')
        self.home.Bind(wx.EVT_BUTTON, self.OnHomeButton, id=wxID_HTMLVIEWHOME)

        self.refresh = wx.BitmapButton(
              id=wxID_HTMLVIEWREFRESH, name='refresh',
              parent=self.lblPageName, pos=wx.Point(62, 0), size=wx.Size(31,
              30), style=0)
        self.refresh.SetToolTipString('refresh current page')
        self.refresh.Bind(wx.EVT_BUTTON, self.OnRefreshButton,
              id=wxID_HTMLVIEWREFRESH)

        self.forward = wx.BitmapButton(
              id=wxID_HTMLVIEWFORWARD, name='forward',
              parent=self.lblPageName, pos=wx.Point(93, 0), size=wx.Size(31,
              30), style=0)
        self.forward.SetToolTipString('forward to next page')
        self.forward.Bind(wx.EVT_BUTTON, self.OnForwardButton,
              id=wxID_HTMLVIEWFORWARD)

        self.html = wx.html.HtmlWindow(id=wxID_HTMLVIEWHTML, name='html',
              parent=self.lblPageName, pos=wx.Point(0, 30), size=wx.Size(792,
              536), style=wx.html.HW_SCROLLBAR_AUTO)
        self.html.SetToolTipString('HTML Help')

        self._init_sizers()

    def __init__(self, parent=None, homepage='index.html', id=-1, title=''):
        '''set up the mini WWW browser to view HTML-formatted help files
            @param parent: widget that owns this window
            @param homepage: local file name of HTML Help (exception if blank)
            @param id: widget identifier
            @param title: text for window bar'''
        self._init_ctrls(parent)
        self.homepage = homepage
        #
        # locate the graphics files for the bitmap buttons
        self.bmp = {}
        root_dir = os.path.split(inspect.getsourcefile(HtmlView))[0]
        for item in ['back', 'home', 'refresh', 'forward']:
            file = os.path.join(root_dir,  'graphics',  item + '.bmp')
            self.bmp[item] = wx.Bitmap(file, wx.BITMAP_TYPE_BMP)
        self.back.SetBitmapLabel(self.bmp['back'])
        self.home.SetBitmapLabel(self.bmp['home'])
        self.refresh.SetBitmapLabel(self.bmp['refresh'])
        self.forward.SetBitmapLabel(self.bmp['forward'])
        #
        self.refresh.SetToolTipString('not implemented yet')
        #
        if "gtk2" in wx.PlatformInfo:
            self.html.SetStandardFonts()
        self.html.LoadFile(str(self.homepage))

    def OnBackButton(self, event):
        '''user pressed the Back button
           @param event: wxPython event object'''
        if self.html.HistoryCanBack():
            self.html.HistoryBack()

    def OnHomeButton(self, event):
        '''user pressed the Home button
           @param event: wxPython event object'''
        self.html.LoadFile(self.homepage)

    def OnForwardButton(self, event):
        '''user pressed the Forward button
           @param event: wxPython event object'''
        if self.html.HistoryCanForward():
            self.html.HistoryForward()

    def OnOpeningURL(self, type, url):
        '''page was opened
           @param type: "WxPython in Action": page 491
           @param url: [str] Uniform Resource Locator

           @note: this code is not called yet'''
        print __name__, 'url:', url

    def OnRefreshButton(self, event):
        '''page was opened
           @param type: "WxPython in Action": page 491
           @param url: [str] Uniform Resource Locator

           @note: this code is not implemented yet'''


if __name__ == '__main__':
    app = wx.PySimpleApp()
    root_dir = os.path.split(inspect.getsourcefile(HtmlView))[0]
    page = 'index.html'
    fullname = os.path.join(root_dir, page)
    HtmlView(homepage=fullname, parent=None, id=-1, 
        title='HtmlView: '+fullname).Show()
    app.MainLoop()
