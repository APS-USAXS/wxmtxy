#!/usr/bin/env python
#Boa:FramePanel:XYpair

#*************************************************************************
# Copyright (c) 2009-2010 The University of Chicago, as Operator of Argonne
#     National Laboratory.
# Copyright (c) 2009-2010 The Regents of the University of California, as
#     Operator of Los Alamos National Laboratory.
# This file is distributed subject to a Software License Agreement found
# in the file LICENSE that is included with this distribution. 
#*************************************************************************

'''
Define the GUI elements and interface for one X,Y pair

@version: 
########### SVN repository information ###################
# $Date: 2010-06-03 16:04:15 -0500 (Thu, 03 Jun 2010) $
# $Author: jemian $
# $Revision: 184 $
# $URL: https://subversion.xor.aps.anl.gov/bcdaext/wxmtxy/trunk/wxmtxy_pair.py $
# $Id: wxmtxy_pair.py 184 2010-06-03 21:04:15Z jemian $
########### SVN repository information ###################
'''

import wx
import wx.lib.stattext
import wxmtxy_tab
import wxmtxy_row
import wxmtxy_axis
import wx.lib.scrolledpanel
#import pvConnect
import copy
import pprint


[wxID_XYPAIR, wxID_XYPAIRLBLMOTOR, wxID_XYPAIRLBLREADBACK, 
 wxID_XYPAIRLBLTARGET, wxID_XYPAIRLBL_X_TITLE, wxID_XYPAIRLBL_Y_TITLE, 
 wxID_XYPAIRSTOP, wxID_XYPAIRTABLE, wxID_XYPAIRTITLE, wxID_XYPAIRX_RBV, 
 wxID_XYPAIRX_VAL, wxID_XYPAIRY_RBV, wxID_XYPAIRY_VAL, 
] = [wx.NewId() for _init_ctrls in range(13)]


class XYpair(wx.Panel):
    '''Table of settings for a specified X,Y pair of EPICS motors'''

    # see:  http://wiki.wxpython.org/BoaFAQ    
    _custom_classes = {
        'wx.lib.scrolledpanel.ScrolledPanel': ['Tab'],
        'wx.Dialog': ['PvDialog']
    }
    
    COLOR_MOVING = wx.Colour(179, 250, 142)     # pale green
    COLOR_NOT_MOVING = wx.Colour(200, 191, 140) # default below
    COLOR_NOT_MOVING = wx.Colour(237, 233, 227) # Boa shows this one, which?

    def _init_coll_fgsEpics_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.lblMotor, 0, border=2,
              flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.GROW)
        parent.AddWindow(self.lbl_x_title, 1, border=2,
              flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.GROW)
        parent.AddWindow(self.lbl_y_title, 1, border=2,
              flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.GROW)
        parent.AddWindow(self.lblReadback, 0, border=2,
              flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.GROW)
        parent.AddWindow(self.x_rbv, 1, border=2, flag=wx.ALL | wx.GROW)
        parent.AddWindow(self.y_rbv, 1, border=2, flag=wx.ALL | wx.GROW)
        parent.AddWindow(self.lblTarget, 0, border=2,
              flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.GROW)
        parent.AddWindow(self.x_val, 1, border=2, flag=wx.ALL | wx.GROW)
        parent.AddWindow(self.y_val, 1, border=2, flag=wx.ALL | wx.GROW)

    def _init_coll_sizer_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.title, 0, border=0, flag=wx.GROW)
        parent.AddSizer(self.fgsEpics, 0, border=4, flag=wx.ALL | wx.GROW)
        parent.AddWindow(self.stop, 0, border=0, flag=wx.ALIGN_CENTER)
        parent.AddWindow(self.table, 1, border=0, flag=wx.GROW)

    def _init_coll_fgsEpics_Growables(self, parent):
        # generated method, don't edit

        parent.AddGrowableCol(1)
        parent.AddGrowableCol(2)

    def _init_sizers(self):
        # generated method, don't edit
        self.sizer = wx.BoxSizer(orient=wx.VERTICAL)

        self.fgsEpics = wx.FlexGridSizer(cols=3, hgap=4, rows=3, vgap=4)

        self._init_coll_sizer_Items(self.sizer)
        self._init_coll_fgsEpics_Items(self.fgsEpics)
        self._init_coll_fgsEpics_Growables(self.fgsEpics)

        self.SetSizer(self.sizer)

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Panel.__init__(self, id=wxID_XYPAIR, name='XYpair', parent=prnt,
              pos=wx.Point(532, 345), size=wx.Size(408, 274),
              style=wx.TRANSPARENT_WINDOW | wx.TAB_TRAVERSAL)
        self.SetClientSize(wx.Size(400, 240))
        self.SetMinSize(wx.Size(240, 240))

        self.title = wx.lib.stattext.GenStaticText(ID=wxID_XYPAIRTITLE,
              label='Window Title', name='title', parent=self, pos=wx.Point(0,
              0), size=wx.Size(400, 23), style=wx.ALIGN_CENTRE)
        self.title.SetFont(wx.Font(15, wx.SWISS, wx.NORMAL, wx.NORMAL, False,
              u'Arial'))
        self.title.Center(wx.BOTH)
        self.title.SetToolTipString('description of this X,Y set')

        self.lblMotor = wx.lib.stattext.GenStaticText(ID=wxID_XYPAIRLBLMOTOR,
              label='motor', name='lblMotor', parent=self, pos=wx.Point(6, 29),
              size=wx.Size(80, 20), style=wx.ALIGN_CENTRE)
        self.lblMotor.SetToolTipString(u'values obtained from EPICS')
        self.lblMotor.Center(wx.BOTH)
        self.lblMotor.SetBackgroundColour(wx.Colour(200, 191, 140))
        self.lblMotor.SetMinSize(wx.Size(80, 20))

        self.lbl_x_title = wx.lib.stattext.GenStaticText(ID=wxID_XYPAIRLBL_X_TITLE,
              label='title_x', name='lbl_x_title', parent=self, pos=wx.Point(94,
              29), size=wx.Size(146, 20), style=wx.ALIGN_CENTRE)
        self.lbl_x_title.SetToolTipString('name and units of X axis')
        self.lbl_x_title.Center(wx.BOTH)
        self.lbl_x_title.SetBackgroundColour(wx.Colour(200, 191, 140))
        self.lbl_x_title.SetMinSize(wx.Size(80, 20))

        self.lbl_y_title = wx.lib.stattext.GenStaticText(ID=wxID_XYPAIRLBL_Y_TITLE,
              label='title_y', name='lbl_y_title', parent=self,
              pos=wx.Point(248, 29), size=wx.Size(146, 20),
              style=wx.ALIGN_CENTRE)
        self.lbl_y_title.SetToolTipString(u'name and units of Y axis')
        self.lbl_y_title.Center(wx.BOTH)
        self.lbl_y_title.SetBackgroundColour(wx.Colour(200, 191, 140))
        self.lbl_y_title.SetMinSize(wx.Size(80, 20))

        self.lblReadback = wx.lib.stattext.GenStaticText(ID=wxID_XYPAIRLBLREADBACK,
              label='readback', name='lblReadback', parent=self, pos=wx.Point(6,
              57), size=wx.Size(80, 20), style=wx.ALIGN_CENTRE)
        self.lblReadback.SetToolTipString(u'indicates current position')
        self.lblReadback.Center(wx.BOTH)
        self.lblReadback.SetBackgroundColour(wx.Colour(200, 191, 140))
        self.lblReadback.SetMinSize(wx.Size(80, 20))

        self.x_rbv = wx.lib.stattext.GenStaticText(ID=wxID_XYPAIRX_RBV,
              label='x_rbv', name='x_rbv', parent=self, pos=wx.Point(94, 57),
              size=wx.Size(146, 20), style=wx.ALIGN_CENTRE)
        self.x_rbv.SetToolTipString(u'X axis readback value')
        self.x_rbv.Center(wx.BOTH)
        self.x_rbv.SetMinSize(wx.Size(80, 20))

        self.y_rbv = wx.lib.stattext.GenStaticText(ID=wxID_XYPAIRY_RBV,
              label='y_rbv', name='y_rbv', parent=self, pos=wx.Point(248, 57),
              size=wx.Size(146, 20), style=wx.ALIGN_CENTRE)
        self.y_rbv.SetToolTipString(u'Y axis readback value')
        self.y_rbv.Center(wx.BOTH)
        self.y_rbv.SetMinSize(wx.Size(80, 20))

        self.lblTarget = wx.lib.stattext.GenStaticText(ID=wxID_XYPAIRLBLTARGET,
              label='target', name='lblTarget', parent=self, pos=wx.Point(6,
              85), size=wx.Size(80, 20), style=wx.ALIGN_CENTRE)
        self.lblTarget.SetToolTipString(u'also known as "commanded value"')
        self.lblTarget.Center(wx.BOTH)
        self.lblTarget.SetBackgroundColour(wx.Colour(200, 191, 140))
        self.lblTarget.SetMinSize(wx.Size(80, 20))

        self.x_val = wx.lib.stattext.GenStaticText(ID=wxID_XYPAIRX_VAL,
              label='x_val', name='x_val', parent=self, pos=wx.Point(94, 85),
              size=wx.Size(146, 20), style=wx.ALIGN_CENTRE)
        self.x_val.SetToolTipString(u'X axis target value')
        self.x_val.Center(wx.BOTH)
        self.x_val.SetMinSize(wx.Size(80, 20))

        self.y_val = wx.lib.stattext.GenStaticText(ID=wxID_XYPAIRY_VAL,
              label='y_val', name='y_val', parent=self, pos=wx.Point(248, 85),
              size=wx.Size(146, 20), style=wx.ALIGN_CENTRE)
        self.y_val.SetToolTipString(u'Y axis target value')
        self.y_val.Center(wx.BOTH)
        self.y_val.SetMinSize(wx.Size(80, 20))

        self.stop = wx.Button(id=wxID_XYPAIRSTOP, label='Stop', name='stop',
              parent=self, pos=wx.Point(140, 111), size=wx.Size(120, 32),
              style=0)
        self.stop.SetBackgroundColour(wx.Colour(223, 0, 0))
        self.stop.SetForegroundColour(wx.Colour(255, 255, 255))
        self.stop.SetToolTipString(u'command EPICS to stop these two motors')
        self.stop.SetHelpText(u'command EPICS to stop these two motors')
        self.stop.SetFont(wx.Font(11, wx.SWISS, wx.NORMAL, wx.BOLD, False,
              'Arial'))
        self.stop.Bind(wx.EVT_BUTTON, self.OnStopButton, id=wxID_XYPAIRSTOP)

        self.table = wx.Notebook(id=wxID_XYPAIRTABLE, name='table', parent=self,
              pos=wx.Point(0, 143), size=wx.Size(400, 97), style=0)
        self.table.SetMinSize(wx.Size(240, 50))
        self.table.SetToolTipString(u'table of various settings for X,Y motors"')

        self._init_sizers()

    def __init_names__(self):
        '''cross-reference the widgets to a dictionary'''
        self.widget = {"x": {}, "y": {}}
        self.widget["x"]["VAL"] = self.x_val
        self.widget["y"]["VAL"] = self.y_val
        self.widget["x"]["RBV"] = self.x_rbv
        self.widget["y"]["RBV"] = self.y_rbv
        self.widget["x"]["title"] = self.lbl_x_title
        self.widget["y"]["title"] = self.lbl_y_title

    def __init__(self, parent, name, root, rootCallback, newtab=False):
        '''initialize an instance of this class
            @param parent: object that owns this class
            @param name: display test that describes this XYpair
            @param root: root object
            @param rootCallback: routine in the parent to handle Button events from the Tab
            @param newtab: [Boolean] create a default Tab group?'''
        self.tab_count = 0
        self.epics = {}
        self.titles = {}
        for axis in ['x', 'y']:
            self.epics[axis] = wxmtxy_axis.Axis()
            self.titles[axis] = {}
            for field in ['DESC', 'EGU']:
                self.titles[axis][field] = ""
        self._init_ctrls(parent)
        self.__init_names__()   # build a cross-reference
        self.parent = parent
        self.SetName(name)
        self.root = root
        self.rootCallback = rootCallback
        self.SetAxisTitles('X axis, egu', 'Y axis, egu')
        if newtab == True:
            self.NewTab()
        self.Layout()
        #self.SetMotorColor("x", True)
        #self.SetMotorColor("y", False)
        self.SetEpicsConfig({'x': {}, 'y': {}})

# ################################
# ##       added methods       ###
# ################################

    def NewTab(self, newrow=True):
        '''make a new tab
           @param newrow: [Boolean] option to create a first row'''
        panel = wxmtxy_tab.Tab(parent=self.table, pair=self,
                       pairCallback=self.TabHandler, newrow=newrow)
        self.tab_count += 1
        self.table.AddPage(imageId=-1, page=panel, select=True,
               text='tab ' + repr(self.tab_count))
        return panel

    def DeleteTab(self):
        '''Delete the given tab'''
        tabnum = self.GetSelection()
        if tabnum < 0:
            return 'No tab to delete.'
        else:
            text = self.GetTabText(tabnum)
            self.table.DeletePage(tabnum)
            return 'Deleted tab named: ' + text

    def TabHandler(self, theTab, theRow, command):
        '''Callback function to handle a command from a tab
           @param theTab: wxmtxy_tab.Tab object
           @param theRow: wxmtxy_row.Row object
           @param command: [string] Row button action to pass upward for handling'''
        self.rootCallback(self, theTab, theRow, command)

    def GetSelection(self):
        '''@return index number of the selected tab object'''
        return self.table.GetSelection()

    def GetTabSelection(self):
        '''@return selected tab object'''
        tabnum = self.GetSelection()
        if tabnum < 0:
            return None
        return self.table.GetPage(tabnum)

    def GetPageTitle(self):
        '''@return page title'''
        return self.title.GetLabel()

    def SetPageTitle(self, title):
        '''define the page title
           @param title: [string] new page title'''
        self.title.SetLabel(title)
        self.Layout()

    def GetTabText(self, tabnum):
        '''return the text of the tab numbered tabnum
           @param tabnum: [int] index of selected tab'''
        return self.table.GetPageText(tabnum)

    def SetTabText(self, tabnum, text):
        '''set the text of the tab numbered tabnum
           @param tabnum: [int] index of selected tab
           @param text: [string] new text'''
        self.table.SetPageText(tabnum, text)

    def GetAxisTitleX(self):
        '''@return X axis title'''
        return self.lbl_x_title.GetLabel()

    def GetAxisTitleY(self):
        '''@return Y axis title'''
        return self.lbl_y_title.GetLabel()

    def SetMotorColor(self, axis, state):
        '''change the background color of the RBV and VAL widgets
        
           @param axis: [string] either "x" or "y"
           @param state: [Boolean], color is green if state == False, neutral if True
        '''
        colormap = {False: self.COLOR_MOVING, True: self.COLOR_NOT_MOVING}
        rbv = {"x": self.x_rbv, "y": self.y_rbv}
        val = {"x": self.x_val, "y": self.y_val}
        rbv[axis].SetBackgroundColour(colormap[state])
        val[axis].SetBackgroundColour(colormap[state])
        self.Refresh()
        self.Layout()

    def GetRbvXY(self):
        '''@return readback values for X and Y as a tuple'''
        x = self.x_rbv.GetLabel()
        y = self.y_rbv.GetLabel()
        return x, y

    def SetAxisTitles(self, x_title, y_title):
        '''define the axis titles
            @param x_title: [string] X axis title
            @param y_title: [string] Y axis title'''
        self.lbl_x_title.SetLabel(x_title)
        self.lbl_y_title.SetLabel(y_title)
        self.Layout()

    def GetEpicsConfig(self):
        '''@return deep copy of EPICS PV configuration'''
        config = {}
        for axis in ['x', 'y']:
            config[axis] = copy.deepcopy(self.epics[axis].GetConfigure())
        return config

    def SetEpicsConfig(self, config):
        '''define the EPICS PVs from a configuration
           @param config: Python dictionary with axes configurations'''
        for axis in ['x', 'y']:
            self.epics[axis].SetConfigure(copy.deepcopy(config[axis]))

    def CallbackPositions(self, epics_args, user_args):
        '''receive a callback on the VAL and RBV fields'''
        axis = user_args[0][0]
        field = user_args[0][1]
        value = epics_args['pv_value']
        if epics_args.has_key('pv_precision'):
            # what about display precision?
            fmt = '%.' + str(epics_args['pv_precision'])
            abs_value = abs(value)
            if abs_value >= 1e5 or (abs_value < 1e-5 and abs_value > 0):
                fmt += 'E'
            else:
                fmt += 'f'
            str_value = fmt % value
        else:
            str_value = str(value)
        self.widget[axis][field] .SetLabel(str_value)
        self.Layout()

    def CallbackTitle(self, epics_args, user_args):
        '''receive a callback on the DESC and EGU fields'''
        axis = user_args[0][0]
        field = user_args[0][1]
        value = epics_args['pv_value']
        self.titles[axis][field] = value
        title = "%s, %s" % (self.titles[axis]['DESC'], self.titles[axis]['EGU'])
        self.widget[axis]['title'] .SetLabel(title)

    def CallbackDMOV(self, epics_args, user_args):
        '''receive a callback on the DMOV field'''
        axis = user_args[0][0]
        value = epics_args['pv_value']
        self.SetMotorColor(axis, value == 1)

    def ConnectEpics(self):
        '''try to connect the XY_pair PV names with EPICS'''
        #+++++++++++++++++++++++++++++++
        # need to replace this starting from the example in wxmtxy_axis.main()
        #+++++++++++++++++++++++++++++++
        for axis in ['x', 'y']:
            cfg = self.epics[axis].GetConfigure()
            for field in ['VAL', 'RBV']:
                item = self.epics[axis].db[field]
                item.connection.SetUserCallback(self.CallbackPositions)
                item.connection.SetUserArgs((axis, field))
                item.SetWidget(self.widget[axis][field] .SetLabel)

            # advanced handling
            desc = self.epics[axis].db['DESC']
            desc.connection.SetUserCallback(self.CallbackTitle)
            desc.connection.SetUserArgs((axis, 'DESC'))

            egu = self.epics[axis].db['EGU']
            egu.connection.SetUserCallback(self.CallbackTitle)
            egu.connection.SetUserArgs((axis, 'EGU'))

            dmov = self.epics[axis].db['DMOV']
            dmov.connection.SetUserCallback(self.CallbackDMOV)
            dmov.connection.SetUserArgs((axis, 'DMOV'))

            # do not need to setup the STOP button

            cfg['AXIS'] = axis
            #pprint.pprint(cfg)
            self.epics[axis].Connect()

    def ReleaseEpics(self):
        '''release connections with the XY_pair EPICS PVs
            @note: When will this be called?'''
        for axis in ['x', 'y']:
            self.epics[axis].Disconnect()

    def StopAxes(self):
        '''Send a stop to both axes'''
        for axis in ['x', 'y']:
            #print __name__, 'Stop axis', axis
            self.epics[axis].Stop()

    def MoveAxes(self, x, y):
        '''Command both axes to move to new position
            @param x: [float] new X position
            @param y: [float] new Y position'''
        #print __name__, 'MoveAxes:', x, y
        self.epics['x'].Move(x)
        self.epics['y'].Move(y)
                
# ################################
# ##  event handling routines  ###
# ################################

    def OnStopButton(self, event):
        '''user requested to stop the X and Y motors
           @param event: wxPython event object'''
        self.TabHandler(self, None, 'stop')
