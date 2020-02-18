#Boa:FramePanel:Tab

#*************************************************************************
# Copyright (c) 2009-2010 The University of Chicago, as Operator of Argonne
#     National Laboratory.
# Copyright (c) 2009-2010 The Regents of the University of California, as
#     Operator of Los Alamos National Laboratory.
# This file is distributed subject to a Software License Agreement found
# in the file LICENSE that is included with this distribution. 
#*************************************************************************

'''
Define the GUI elements and interface for one tab (table) of the X,Y pair

@version: 
########### SVN repository information ###################
# $Date: 2010-06-03 16:04:15 -0500 (Thu, 03 Jun 2010) $
# $Author: jemian $
# $Revision: 184 $
# $URL: https://subversion.xor.aps.anl.gov/bcdaext/wxmtxy/trunk/wxmtxy_tab.py $
# $Id: wxmtxy_tab.py 184 2010-06-03 21:04:15Z jemian $
########### SVN repository information ###################
'''

import wx
import wxmtxy_row
import wx.lib.scrolledpanel

    #    Alternative is to use a wx.lib.scrolledpanel.ScrolledPanel
    #    and call this method after subpanels have been created:
    #        wx.lib.scrolledpanel.SetupScrolling(self, 
    #            scroll_x=False, scroll_y=True, 
    #            rate_x=20, rate_y=[get this from the subpanel height])
    #    Turns out the ScrolledPanel was developed for situations just like this!

[wxID_TAB] = [wx.NewId() for _init_ctrls in range(1)]

class Tab(wx.lib.scrolledpanel.ScrolledPanel):
    '''Create a panel to display rows of settings'''

    # see:  http://wiki.wxpython.org/BoaFAQ    
    _custom_classes = {'wx.Panel': ['Row']} 

    def _init_sizers(self):
        # generated method, don't edit
        self.sizer = wx.BoxSizer(orient=wx.VERTICAL)

        self.SetSizer(self.sizer)

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.lib.scrolledpanel.ScrolledPanel.__init__(self, 
                id=wxID_TAB, name='Tab', parent=prnt,
                pos=wx.Point(50, 39), size=wx.Size(408, 100),
                style=wx.TAB_TRAVERSAL)
        self.SetClientSize(wx.Size(400, 100))
        self.SetMinSize(wx.Size(240, 75))

        self._init_sizers()

    def __init__(self, parent, pair, pairCallback, newrow=False):
        '''create the panel'''
        self._init_ctrls(parent)
        self.pair = pair
        self.pairCallback = pairCallback
        if newrow == True:
            self.NewRow()       # make the first row if requested

# ################################
# ##       added methods       ###
# ################################

    def NewRow(self, remap = False):
        '''Make a new row and append it to the current tab
            @param remap: [Boolean] option to call self.Remap()'''
        panel = wxmtxy_row.Row(self, self.RowHandler)
        self.sizer.AddWindow(panel, 0, border=2, flag=wx.GROW)
        if remap:
            self.Remap()
        return panel

    def DeleteRow(self, theRow):
        '''Delete a row object
            @param theRow: '''
        self.sizer.Detach(theRow)
        theRow.Destroy()
        self.Remap()

    def Remap(self):
        '''adjust the layout for any changes'''
        self.SetupScrolling(scroll_x=False, scroll_y=True, rate_x=1, rate_y=25)
        self.sizer.Layout()
        self.Layout()

    def RowHandler(self, theRow, command):
        '''Handle a command from a row'''
        #print 'RowHandler', command, theRow.GetLabel(), theRow.GetXY()
        (self.pairCallback)(self, theRow, command)
    
    def GetRowLabel(self, rownum):
        '''return the text in the label slot for the given row'''
        return self.sizer.GetItem(rownum).GetWindow().GetLabel()
    
    def SetRowLabel(self, rownum, label):
        '''set the text in the label slot for the given row'''
        self.sizer.GetItem(rownum).GetWindow().SetLabel(label)
    
    def GetRowXY(self, rownum):
        '''return the X,Y values in the label slot for the given row'''
        return self.sizer.GetItem(rownum).GetWindow().GetXY()
    
    def SetRowXY(self, rownum, x, y):
        '''set the text in the label slot for the given row'''
        self.sizer.GetItem(rownum).GetWindow().SetXY(x, y)

# ################################
# ##  event handling routines  ###
# ################################

    # none
