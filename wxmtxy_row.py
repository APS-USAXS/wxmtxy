#Boa:FramePanel:Row

#*************************************************************************
# Copyright (c) 2009-2010 The University of Chicago, as Operator of Argonne
#     National Laboratory.
# Copyright (c) 2009-2010 The Regents of the University of California, as
#     Operator of Los Alamos National Laboratory.
# This file is distributed subject to a Software License Agreement found
# in the file LICENSE that is included with this distribution. 
#*************************************************************************

'''
Define the GUI elements and interface for one row of the table

@version: 
########### SVN repository information ###################
# $Date: 2010-06-03 16:04:15 -0500 (Thu, 03 Jun 2010) $
# $Author: jemian $
# $Revision: 184 $
# $URL: https://subversion.xor.aps.anl.gov/bcdaext/wxmtxy/trunk/wxmtxy_row.py $
# $Id: wxmtxy_row.py 184 2010-06-03 21:04:15Z jemian $
########### SVN repository information ###################
'''

import wx
import inspect
import os

[wxID_ROW, wxID_ROWDELETE, wxID_ROWGO, wxID_ROWLABEL, wxID_ROWSET, wxID_ROWX, 
 wxID_ROWY, 
] = [wx.NewId() for _init_ctrls in range(7)]

class Row(wx.Panel):
    '''One row of settings in a wxmtxy table'''

    def _init_coll_sizer_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.delete, 0, border=0, flag=0)
        parent.AddWindow(self.label, 0, border=0, flag=0)
        parent.AddWindow(self.set, 0, border=0, flag=0)
        parent.AddWindow(self.x, 0, border=0, flag=0)
        parent.AddWindow(self.y, 0, border=0, flag=0)
        parent.AddWindow(self.go, 0, border=0, flag=0)

    def _init_sizers(self):
        # generated method, don't edit
        self.sizer = wx.BoxSizer(orient=wx.HORIZONTAL)

        self._init_coll_sizer_Items(self.sizer)

        self.SetSizer(self.sizer)

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Panel.__init__(self, id=wxID_ROW, name='Row', parent=prnt,
              pos=wx.Point(51, 84), size=wx.Size(312, 25),
              style=wx.TAB_TRAVERSAL)
        self.SetClientSize(wx.Size(312, 25))
        self.SetMinSize(wx.Size(312, 25))

        self.delete = wx.BitmapButton(
              id=wxID_ROWDELETE, name='delete',
              parent=self, pos=wx.Point(0, 0), size=wx.Size(24, 24),
              style=wx.BU_AUTODRAW)
        self.delete.Bind(wx.EVT_BUTTON, self.OnDeleteButton, id=wxID_ROWDELETE)
        self.delete.SetToolTipString(u'Delete this row')

        self.label = wx.TextCtrl(id=wxID_ROWLABEL, name='label', parent=self,
              pos=wx.Point(24, 0), size=wx.Size(80, 25), style=0, value='')
        self.label.SetMinSize(wx.Size(80, 25))
        self.label.SetToolTipString(u'Description of this row')

        self.set = wx.BitmapButton(
              id=wxID_ROWSET, name='set', parent=self,
              pos=wx.Point(104, 0), size=wx.Size(24, 24), style=wx.BU_AUTODRAW)
        self.set.Bind(wx.EVT_BUTTON, self.OnSetButton, id=wxID_ROWSET)
        self.set.SetToolTipString(u'Copy current X,Y readback values to this row')

        self.x = wx.TextCtrl(id=wxID_ROWX, name='x', parent=self,
              pos=wx.Point(128, 0), size=wx.Size(80, 25), style=0, value='')
        self.x.SetMinSize(wx.Size(80, 25))
        self.x.SetToolTipString(u'X axis target position')

        self.y = wx.TextCtrl(id=wxID_ROWY, name='y', parent=self,
              pos=wx.Point(208, 0), size=wx.Size(80, 25), style=0, value='')
        self.y.SetMinSize(wx.Size(80, 25))
        self.y.SetToolTipString(u'Y axis target position')

        self.go = wx.BitmapButton(
              id=wxID_ROWGO, name='go', parent=self,
              pos=wx.Point(288, 0), size=wx.Size(24, 24), style=wx.BU_AUTODRAW)
        self.go.Bind(wx.EVT_BUTTON, self.OnGoButton, id=wxID_ROWGO)
        self.go.SetToolTipString(u'Command EPICS to move motors to this X,Y position')

        self._init_sizers()

    def __init__(self, tab, tabCallback):
        '''initialize the row
            @param tab: parent object (Tab object that owns this Row object)
            @param tabCallback: callback function that takes two arguments
        '''
        # first, find the directory where this code is installed
        # so the bitmaps can be found
        # Note that this breaks edit ability of BoaConstructor
        root_dir = os.path.split(inspect.getsourcefile(Row))[0]
        self.bmp = {}
        for item in ['delete', 'set',  'go']:
            file = os.path.join(root_dir,  'graphics',  item + '.bmp')
            self.bmp[item] = wx.Bitmap(file, wx.BITMAP_TYPE_BMP)
        self._init_ctrls(tab)
        self.delete.SetBitmapLabel(self.bmp['delete'])
        self.set.SetBitmapLabel(self.bmp['set'])
        self.go.SetBitmapLabel(self.bmp['go'])
        self.tab = tab
        self.tabCallback = tabCallback
        # sizes keep getting botched in Boa, fix them here
        self._fix_sizer(self.label, wx.GROW, 2)
        self._fix_sizer(self.x, wx.GROW, 1)
        self._fix_sizer(self.y, wx.GROW, 1)

# ################################
# ##       added methods       ###
# ################################

    def _fix_sizer(self, widget, flag, proportion):
        '''sizes keep getting botched in Boa, fix them here
            @param widget: GUI object to be adjusted
            @param flag: usually wx.GROW
            @param proportion: [int]'''
        item = self.sizer.GetItem(widget)
        item.SetFlag(flag)
        item.SetProportion(proportion)

    def GetLabel(self):
        '''@return row label'''
        return self.label.GetValue()

    def SetLabel(self, text):
        '''Define the label
            @param text: [string] user description of this row'''
        self.label.SetValue(text)

    def GetXY(self):
        '''@return X, Y values as a tuple'''
        x = self.x.GetValue()
        y = self.y.GetValue()
        return x, y

    def SetXY(self, x, y):
        '''Define the values
            @param x: [float] X axis position to remember
            @param y: [float] Y axis position to remember'''
        self.x.SetValue(x)
        self.y.SetValue(y)

    def DeleteRow(self, parent):
        '''Tell parent to delete this row (may be tricky)
           @param parent: object of Tab that owns this Row'''
        self.tabCallback(self, 'delete')

    def SetPositions(self, parent):
        '''Tell parent to set positions on this row
           @param parent: object of Tab that owns this Row'''
        self.tabCallback(self, 'set')

    def Go(self, parent):
        '''Tell parent to move motors to this X,Y
           @param parent: object of Tab that owns this Row'''
        self.tabCallback(self, 'go')

# ################################
# ##  event handling routines  ###
# ################################

    def OnDeleteButton(self, event):
        '''Delete button pressed
           @param event: wxPython event object'''
        self.DeleteRow(self.tab)

    def OnSetButton(self, event):
        '''Set button pressed
           @param event: wxPython event object'''
        self.SetPositions(self.tab)

    def OnGoButton(self, event):
        '''Go button pressed
           @param event: wxPython event object'''
        self.Go(self.tab)
