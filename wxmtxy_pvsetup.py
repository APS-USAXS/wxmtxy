#!/usr/bin/env python
#Boa:Dialog:PvDialog

#*************************************************************************
# Copyright (c) 2009-2010 The University of Chicago, as Operator of Argonne
#     National Laboratory.
# Copyright (c) 2009-2010 The Regents of the University of California, as
#     Operator of Los Alamos National Laboratory.
# This file is distributed subject to a Software License Agreement found
# in the file LICENSE that is included with this distribution. 
#*************************************************************************

'''
Provides Python Class: PvDialog
   Dialog to configure the EPICS PVs for an X,Y pair

@version: 
########### SVN repository information ###################
# $Date: 2010-06-03 16:04:15 -0500 (Thu, 03 Jun 2010) $
# $Author: jemian $
# $Revision: 184 $
# $URL: https://subversion.xor.aps.anl.gov/bcdaext/wxmtxy/trunk/wxmtxy_pvsetup.py $
# $Id: wxmtxy_pvsetup.py 184 2010-06-03 21:04:15Z jemian $
########### SVN repository information ###################
'''


import wx
import pvConnect
import pprint
import wxmtxy_axis
import inspect
import os


COLOR_PV_OK = wx.Colour(235, 254, 231)          # pale green
COLOR_PV_NOT_OK = wx.Colour(254, 232, 255)      # pale pink
COLOR_PV_AUTOFILL = wx.Colour(200, 200, 200)    # pale grey

[wxID_PVDIALOG, wxID_PVDIALOGBUTTON_CANCEL, wxID_PVDIALOGBUTTON_CLEAR_X, 
 wxID_PVDIALOGBUTTON_CLEAR_Y, wxID_PVDIALOGBUTTON_OK, 
 wxID_PVDIALOGBUTTON_REVERT, wxID_PVDIALOGCB_IS_MOTOR_X, 
 wxID_PVDIALOGCB_IS_MOTOR_Y, wxID_PVDIALOGEPICS_LOGO, wxID_PVDIALOGLBL_DESC, 
 wxID_PVDIALOGLBL_DONE, wxID_PVDIALOGLBL_EGU, wxID_PVDIALOGLBL_RBV, 
 wxID_PVDIALOGLBL_STOP, wxID_PVDIALOGLBL_VAL, wxID_PVDIALOGPV_X_DESC, 
 wxID_PVDIALOGPV_X_DMOV, wxID_PVDIALOGPV_X_EGU, wxID_PVDIALOGPV_X_RBV, 
 wxID_PVDIALOGPV_X_STOP, wxID_PVDIALOGPV_X_VAL, wxID_PVDIALOGPV_Y_DESC, 
 wxID_PVDIALOGPV_Y_DMOV, wxID_PVDIALOGPV_Y_EGU, wxID_PVDIALOGPV_Y_RBV, 
 wxID_PVDIALOGPV_Y_STOP, wxID_PVDIALOGPV_Y_VAL, wxID_PVDIALOGTITLE, 
] = [wx.NewId() for _init_ctrls in range(28)]


class PvDialog(wx.Dialog):
    '''Dialog to configure the EPICS PVs for an X,Y pair
    
       This code also checks to see if the PV names entered are valid.
       User is expected to press the [enter] key to submit a PV name 
       for validation.  Background of text entry box will turn green 
       to signify that the chosen PV name is valid (has been found).
       The background will be pink for invalid PV strings.
       The background will be grey for PV standard fields in motor records.
    '''

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Dialog.__init__(self, id=wxID_PVDIALOG, name='EPICS configuration', parent=prnt,
              pos=wx.Point(191, 166), size=wx.Size(638, 434),
              style=wx.DIALOG_MODAL | wx.DEFAULT_DIALOG_STYLE,
              title='PvDialog')
        self.SetClientSize(wx.Size(630, 400))
        self.SetToolTipString('Configure EPICS PVs')

        self.cb_is_motor_x = wx.CheckBox(id=wxID_PVDIALOGCB_IS_MOTOR_X,
              label='X axis is motor', name='cb_is_motor_x', parent=self,
              pos=wx.Point(72, 80), size=wx.Size(256, 16), style=0)
        self.cb_is_motor_x.SetValue(True)
        self.cb_is_motor_x.SetToolTipString('Autofill the fields for a motor record for the X axis')

        self.pv_x_desc = wx.TextCtrl(id=wxID_PVDIALOGPV_X_DESC,
              name='pv_x_desc', parent=self, pos=wx.Point(72, 108),
              size=wx.Size(256, 21), style=wx.TE_PROCESS_ENTER, value='')
        self.pv_x_desc.SetToolTipString('PV for X axis description')
        self.pv_x_desc.Bind(wx.EVT_TEXT_ENTER, self.OnPv_x_descTextEnter,
              id=wxID_PVDIALOGPV_X_DESC)

        self.pv_x_rbv = wx.TextCtrl(id=wxID_PVDIALOGPV_X_RBV, name='pv_x_rbv',
              parent=self, pos=wx.Point(72, 148), size=wx.Size(256, 21),
              style=wx.TE_PROCESS_ENTER, value='')
        self.pv_x_rbv.SetToolTipString('PV for X axis readback value')
        self.pv_x_rbv.Bind(wx.EVT_TEXT_ENTER, self.OnPv_x_rbvTextEnter,
              id=wxID_PVDIALOGPV_X_RBV)

        self.pv_x_val = wx.TextCtrl(id=wxID_PVDIALOGPV_X_VAL, name='pv_x_val',
              parent=self, pos=wx.Point(72, 188), size=wx.Size(256, 21),
              style=wx.TE_PROCESS_ENTER, value='')
        self.pv_x_val.SetToolTipString('PV for X axis target (commanded) value')
        self.pv_x_val.Bind(wx.EVT_TEXT_ENTER, self.OnPv_x_valTextEnter,
              id=wxID_PVDIALOGPV_X_VAL)

        self.pv_x_dmov = wx.TextCtrl(id=wxID_PVDIALOGPV_X_DMOV,
              name='pv_x_dmov', parent=self, pos=wx.Point(72, 228),
              size=wx.Size(256, 21), style=wx.TE_PROCESS_ENTER, value='')
        self.pv_x_dmov.SetToolTipString('PV for X axis NOT MOVING bit (1=not moving)')
        self.pv_x_dmov.Bind(wx.EVT_TEXT_ENTER, self.OnPv_x_dmovTextEnter,
              id=wxID_PVDIALOGPV_X_DMOV)

        self.pv_x_egu = wx.TextCtrl(id=wxID_PVDIALOGPV_X_EGU, name='pv_x_egu',
              parent=self, pos=wx.Point(72, 268), size=wx.Size(256, 21),
              style=wx.TE_PROCESS_ENTER, value='')
        self.pv_x_egu.SetToolTipString('PV for X axis engineering units)')
        self.pv_x_egu.Bind(wx.EVT_TEXT_ENTER, self.OnPv_x_eguTextEnter,
              id=wxID_PVDIALOGPV_X_EGU)

        self.pv_x_stop = wx.TextCtrl(id=wxID_PVDIALOGPV_X_STOP,
              name='pv_x_stop', parent=self, pos=wx.Point(72, 308),
              size=wx.Size(256, 21), style=wx.TE_PROCESS_ENTER, value='')
        self.pv_x_stop.SetToolTipString('PV to STOP X axis')
        self.pv_x_stop.Bind(wx.EVT_TEXT_ENTER, self.OnPv_x_stopTextEnter,
              id=wxID_PVDIALOGPV_X_STOP)

        self.cb_is_motor_y = wx.CheckBox(id=wxID_PVDIALOGCB_IS_MOTOR_Y,
              label='Y axis is motor', name='cb_is_motor_y', parent=self,
              pos=wx.Point(352, 88), size=wx.Size(256, 16), style=0)
        self.cb_is_motor_y.SetValue(True)
        self.cb_is_motor_y.SetToolTipString('Autofill the fields for a motor record for the Y axis')

        self.pv_y_desc = wx.TextCtrl(id=wxID_PVDIALOGPV_Y_DESC,
              name='pv_y_desc', parent=self, pos=wx.Point(352, 108),
              size=wx.Size(256, 21), style=wx.TE_PROCESS_ENTER, value='')
        self.pv_y_desc.SetToolTipString('PV for Y axis description')
        self.pv_y_desc.SetBackgroundColour(wx.Colour(254, 232, 255))
        self.pv_y_desc.Bind(wx.EVT_TEXT_ENTER, self.OnPv_y_descTextEnter,
              id=wxID_PVDIALOGPV_Y_DESC)

        self.pv_y_rbv = wx.TextCtrl(id=wxID_PVDIALOGPV_Y_RBV, name='pv_y_rbv',
              parent=self, pos=wx.Point(352, 148), size=wx.Size(256, 21),
              style=wx.TE_PROCESS_ENTER, value='')
        self.pv_y_rbv.SetToolTipString('PV for Y axis readback value')
        self.pv_y_rbv.Bind(wx.EVT_TEXT_ENTER, self.OnPv_y_rbvTextEnter,
              id=wxID_PVDIALOGPV_Y_RBV)

        self.pv_y_val = wx.TextCtrl(id=wxID_PVDIALOGPV_Y_VAL, name='pv_y_val',
              parent=self, pos=wx.Point(352, 188), size=wx.Size(256, 21),
              style=wx.TE_PROCESS_ENTER, value='')
        self.pv_y_val.SetToolTipString('PV for Y axis target (commanded) value')
        self.pv_y_val.Bind(wx.EVT_TEXT_ENTER, self.OnPv_y_valTextEnter,
              id=wxID_PVDIALOGPV_Y_VAL)

        self.pv_y_dmov = wx.TextCtrl(id=wxID_PVDIALOGPV_Y_DMOV,
              name='pv_y_dmov', parent=self, pos=wx.Point(352, 228),
              size=wx.Size(256, 21), style=wx.TE_PROCESS_ENTER, value='')
        self.pv_y_dmov.SetToolTipString('PV for Y axis NOT MOVING bit (1=not moving)')
        self.pv_y_dmov.Bind(wx.EVT_TEXT_ENTER, self.OnPv_y_dmovTextEnter,
              id=wxID_PVDIALOGPV_Y_DMOV)

        self.pv_y_egu = wx.TextCtrl(id=wxID_PVDIALOGPV_Y_EGU, name='pv_y_egu',
              parent=self, pos=wx.Point(352, 268), size=wx.Size(256, 21),
              style=wx.TE_PROCESS_ENTER, value='')
        self.pv_y_egu.SetToolTipString('PV for Y axis engineering units')
        self.pv_y_egu.Bind(wx.EVT_TEXT_ENTER, self.OnPv_y_eguTextEnter,
              id=wxID_PVDIALOGPV_Y_EGU)

        self.pv_y_stop = wx.TextCtrl(id=wxID_PVDIALOGPV_Y_STOP,
              name='pv_y_stop', parent=self, pos=wx.Point(352, 308),
              size=wx.Size(256, 21), style=wx.TE_PROCESS_ENTER, value='')
        self.pv_y_stop.SetToolTipString('PV to STOP Y axis')
        self.pv_y_stop.Bind(wx.EVT_TEXT_ENTER, self.OnPv_y_stopTextEnter,
              id=wxID_PVDIALOGPV_Y_STOP)

        self.title = wx.StaticText(id=wxID_PVDIALOGTITLE,
              label='Configure EPICS PVs', name='title', parent=self,
              pos=wx.Point(136, 16), size=wx.Size(233, 27),
              style=wx.ALIGN_CENTRE)
        self.title.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.NORMAL, False,
              'Arial'))

        self.lbl_done = wx.StaticText(id=wxID_PVDIALOGLBL_DONE, label='DMOV',
              name='lbl_done', parent=self, pos=wx.Point(24, 232),
              size=wx.Size(40, 13), style=0)

        self.lbl_val = wx.StaticText(id=wxID_PVDIALOGLBL_VAL, label='VAL',
              name='lbl_val', parent=self, pos=wx.Point(24, 192),
              size=wx.Size(40, 13), style=0)

        self.lbl_rbv = wx.StaticText(id=wxID_PVDIALOGLBL_RBV, label='RBV',
              name='lbl_rbv', parent=self, pos=wx.Point(24, 152),
              size=wx.Size(40, 13), style=0)

        self.lbl_desc = wx.StaticText(id=wxID_PVDIALOGLBL_DESC, label='DESC',
              name='lbl_desc', parent=self, pos=wx.Point(24, 112),
              size=wx.Size(40, 13), style=0)

        self.lbl_egu = wx.StaticText(id=wxID_PVDIALOGLBL_EGU, label='EGU',
              name='lbl_egu', parent=self, pos=wx.Point(24, 272),
              size=wx.Size(40, 13), style=0)

        self.lbl_stop = wx.StaticText(id=wxID_PVDIALOGLBL_STOP, label='STOP',
              name='lbl_stop', parent=self, pos=wx.Point(24, 312),
              size=wx.Size(40, 13), style=0)

        self.button_ok = wx.Button(id=wx.ID_OK, label='Ok', name='button_ok',
              parent=self, pos=wx.Point(40, 352), size=wx.Size(100, 30),
              style=0)
        self.button_ok.SetToolTipString('accept all changes')
        self.button_ok.Bind(wx.EVT_BUTTON, self.OnButton_okButton,
              id=wxID_PVDIALOGBUTTON_OK)

        self.button_cancel = wx.Button(id=wx.ID_CANCEL, label='Cancel',
              name='button_cancel', parent=self, pos=wx.Point(150, 352),
              size=wx.Size(100, 30), style=0)
        self.button_cancel.SetToolTipString('cancel all changes')
        self.button_cancel.Bind(wx.EVT_BUTTON, self.OnButton_cancelButton,
              id=wxID_PVDIALOGBUTTON_CANCEL)

        self.button_clear_x = wx.Button(id=wxID_PVDIALOGBUTTON_CLEAR_X,
              label='Clear X', name='button_clear_x', parent=self,
              pos=wx.Point(260, 352), size=wx.Size(100, 30), style=0)
        self.button_clear_x.SetToolTipString('clear all fields for X axis')
        self.button_clear_x.Bind(wx.EVT_BUTTON, self.OnButton_clear_x_Button,
              id=wxID_PVDIALOGBUTTON_CLEAR_X)

        self.button_clear_y = wx.Button(id=wxID_PVDIALOGBUTTON_CLEAR_Y,
              label='Clear Y', name='button_clear_y', parent=self,
              pos=wx.Point(370, 352), size=wx.Size(100, 30), style=0)
        self.button_clear_y.SetToolTipString('clear all fields for X axis')
        self.button_clear_y.Bind(wx.EVT_BUTTON, self.OnButton_clear_y_Button,
              id=wxID_PVDIALOGBUTTON_CLEAR_Y)

        self.button_revert = wx.Button(id=wxID_PVDIALOGBUTTON_REVERT,
              label='Revert', name='button_revert', parent=self,
              pos=wx.Point(480, 352), size=wx.Size(100, 30), style=0)
        self.button_revert.SetToolTipString('Change all fields back to original values as dialog was started')
        self.button_revert.Bind(wx.EVT_BUTTON, self.OnButton_revertButton,
              id=wxID_PVDIALOGBUTTON_REVERT)

        self.epics_logo = wx.StaticBitmap(
              id=wxID_PVDIALOGEPICS_LOGO,
              name='epics_logo', parent=self, pos=wx.Point(16, 8),
              size=wx.Size(50, 51), style=0)
        self.epics_logo.SetToolTipString('EPICS logo')
        self.epics_logo.SetLabel('EPICS logo')
        self.epics_logo.SetHelpText('EPICS logo')

    def __init_names__(self):
        '''conversion table of widget names

           Create a dictionary of names for the widgets by axis.
           This should simplify addressing these widgets internally.'''
        self.widget = {'x': {}, 'y': {}}
        self.widget['x']['isMotorRec'] = self.cb_is_motor_x
        self.widget['x']['DESC'] = self.pv_x_desc
        self.widget['x']['RBV'] = self.pv_x_rbv
        self.widget['x']['VAL'] = self.pv_x_val
        self.widget['x']['DMOV'] = self.pv_x_dmov
        self.widget['x']['STOP'] = self.pv_x_stop
        self.widget['x']['EGU'] = self.pv_x_egu
        self.widget['y']['isMotorRec'] = self.cb_is_motor_y
        self.widget['y']['DESC'] = self.pv_y_desc
        self.widget['y']['RBV'] = self.pv_y_rbv
        self.widget['y']['VAL'] = self.pv_y_val
        self.widget['y']['DMOV'] = self.pv_y_dmov
        self.widget['y']['STOP'] = self.pv_y_stop
        self.widget['y']['EGU'] = self.pv_y_egu

    def __init__(self, parent, original_config):
        '''establish the dialog box
            @param parent: widget that owns this class
            @param original_config: Python dictionary with axes configurations'''
        # first, find the directory where this code is installed
        # so the bitmaps can be found
        # Note that this breaks edit ability of BoaConstructor
        root_dir = os.path.split(inspect.getsourcefile(PvDialog))[0]
        self.bmp = {}
        for item in ['epicslogo101']:
            file = os.path.join(root_dir,  'graphics',  item + '.bmp')
            self.bmp[item] = wx.Bitmap(file, wx.BITMAP_TYPE_BMP)
        self._init_ctrls(parent)     # create the controls
        self.epics_logo.SetBitmap(self.bmp['epicslogo101'])
        self.__init_names__()        # widget conversion table
        self.SetConfiguration(original_config)          # initial values
        self.original_config = self.GetConfiguration()  # for "Revert"

# ################################
# ##       added methods       ###
# ################################

    def _applyConfiguration_(self, xref, config):
        '''load/configure the widgets with the configuration of one axis
            
            @param xref:  self.widget[axis] where axis is either "x" or "y"
            @param config:  dictionary of values for this axis
        '''
        field = 'isMotorRec'
        isMotorRec = False
        if config.has_key(field):
            xref[field].SetValue(config[field])
            isMotorRec = config[field]
        for field in wxmtxy_axis.field_list:
            if config.has_key(field):
                #pprint.pprint(config)
                #print field,  repr(config[field]),  str(config[field])
                xref[field].SetValue(config[field])
            state = False
            pv = xref[field].GetValue()
            if len(pv) > 0:
                state = pvConnect.testConnect(pv)
                #print pv, state
            self._SetPvColor(xref[field], state, isMotorRec)

    def _SetPvColor(self, widget, state, ismotor):
        '''Change the background color on the PV string widgets.
           Also base color choice on whether the PV is part
           of a motor record or not.
           @param widget: used as widget.SetBackgroundColour(map[state])
           @param state: [Boolean] Moving = True
           @param ismotor: [Boolean] Is it an EPICS "motor" record?  
        '''
        map = {
            True: COLOR_PV_OK,
            False: COLOR_PV_NOT_OK
        }
        if ismotor:     # remap if maybe part of motor record
            map["False"] = COLOR_PV_AUTOFILL
        widget.SetBackgroundColour(map[state])

    def SetColor(self, axis, field):
        '''change the background color on the given widgets
            @param axis: [string] "x" or "y"
            @param field: [string] member of wxmtxy_axis.field_list'''
        pv = self.widget[axis][field].GetValue()
        isMotorRec = self.widget[axis]['isMotorRec'].GetValue()
        state = False
        if len(pv) > 0:
            state = pvConnect.testConnect(pv)
        self._SetPvColor(self.widget[axis][field], state, isMotorRec)

    def _pv_base_name(self, pv):
        '''given an EPICS PV name, return the base name
            @param pv: [string] EPICS Process Variable name
            @return: base part of PV name
            
            @note: _pv_base_name("the:pv:name.VAL") = "the:pv:name"
            @note: _pv_base_name("another:name") = "another:name"
            '''
        return pv.split('.')[0]

    def GetConfiguration(self):
        '''@return Python dictionary containing the PV info for X & Y axes'''
        config = {'x': {}, 'y': {}}
        for axis in ['x', 'y']:
            field = 'isMotorRec'
            config[axis][field]=self.widget[axis][field].GetValue()
            for field in wxmtxy_axis.field_list:
                config[axis][field]=self.widget[axis][field].GetValue()
        return config

    def SetConfiguration(self, config):
        '''Set the configuration of the widgets.
            @param config: Python dictionary containing the PV info for X & Y axes'''
        for axis in ['x', 'y']:
            if config.has_key(axis):
                self._applyConfiguration_(self.widget[axis], config[axis])

    def _SetIsMotorCheckbox_(self, axis):
        '''Set/clear the "isMotorRec" checkbox if the VAL PV is/not from a motor record.
           @param axis: [string] "x" or "y"
        '''
        base = self._pv_base_name(self.widget[axis]['VAL'].GetValue())
        isMotorRec = self._isMotorRec_(base)
        self.widget[axis]['isMotorRec'].SetValue(isMotorRec)

    def _isMotorRec_(self, pv):
        '''test if the given PV is a motor record
            @param pv: [string] EPICS Process Variable name'''
        return pvConnect.GetRTYP(pv) == 'motor'

    def _clear_axis(self, axis):
        '''clear all the fields on the named axis
           @param axis: [string] "x" or "y"'''
        config = {'isMotorRec': False}
        for field in wxmtxy_axis.field_list:
            config[field] = ''
        self._applyConfiguration_(self.widget[axis], config)

# ################################
# ##  event handling routines  ###
# ################################

    def OnPv_x_dmovTextEnter(self, event):
        '''set background color
           @param event: wxPython event object'''
        self.SetColor('x', 'DMOV')

    def OnPv_y_dmovTextEnter(self, event):
        '''set background color
           @param event: wxPython event object'''
        self.SetColor('y', 'DMOV')

    def OnPv_x_valTextEnter(self, event):
        '''set background color and 'isMotorRec' checkbox for X axis
           @param event: wxPython event object'''
        self.SetColor('x', 'VAL')
        self._SetIsMotorCheckbox_('x')

    def OnPv_y_valTextEnter(self, event):
        '''set background color and 'isMotorRec' checkbox for Y axis
           @param event: wxPython event object'''
        self.SetColor('y', 'VAL')
        self._SetIsMotorCheckbox_('y')

    def OnPv_x_rbvTextEnter(self, event):
        '''set background color
           @param event: wxPython event object'''
        self.SetColor('x', 'RBV')

    def OnPv_y_rbvTextEnter(self, event):
        '''set background color
           @param event: wxPython event object'''
        self.SetColor('y', 'RBV')

    def OnPv_x_descTextEnter(self, event):
        '''set background color
           @param event: wxPython event object'''
        self.SetColor('x', 'DESC')

    def OnPv_y_descTextEnter(self, event):
        '''set background color
           @param event: wxPython event object'''
        self.SetColor('y', 'DESC')

    def OnPv_x_eguTextEnter(self, event):
        '''set background color
           @param event: wxPython event object'''
        self.SetColor('x', 'EGU')

    def OnPv_y_eguTextEnter(self, event):
        '''set background color
           @param event: wxPython event object'''
        self.SetColor('y', 'EGU')

    def OnPv_x_stopTextEnter(self, event):
        '''set background color
           @param event: wxPython event object'''
        self.SetColor('x', 'STOP')

    def OnPv_y_stopTextEnter(self, event):
        '''set background color
           @param event: wxPython event object'''
        self.SetColor('y', 'STOP')

    def OnButton_okButton(self, event):
        '''Handler for the cancel button.
           The default behavior will handle all that is needed here.

           @param event: wxPython event object
        '''
        event.Skip()

    def OnButton_cancelButton(self, event):
        '''Handler for the cancel button.
           The default behavior will handle all that is needed here.
        
           There is no chance to restore the original 
           configuration before the dialog returns.  The calling 
           routine must determine if the result was wx.ID_OK
           before calling dlg.GetConfiguration().

           @param event: wxPython event object
        '''
        event.Skip()

    def OnButton_clear_x_Button(self, event):
        '''clear all the fields on the X axis
           @param event: wxPython event object'''
        self._clear_axis('x')

    def OnButton_clear_y_Button(self, event):
        '''clear all the fields on the Y axis
           @param event: wxPython event object'''
        self._clear_axis('y')

    def OnButton_revertButton(self, event):
        '''reset all the fields on both axes to original values
           @param event: wxPython event object'''
        self.SetConfiguration(self.original_config)


if __name__ == '__main__':
    '''example of how to set up the caller for this dialog'''
    config = {
        'x': {
            # USAXS a1y: 32idbLAX:m58:c1:m1
            'isMotorRec': True,
            'VAL': '32idbLAX:m58:c1:m1.VAL'
        },
        'y': {
            # USAXS a2y: 32idbLAX:m58:c1:m2
            'isMotorRec': False,
            'VAL': '32idbLAX:m58:c1:m2.VAL',
            'RBV': '32idbLAX:m58:c1:m2.RBV',
            'EGU': '32idbLAX:m58:c1:m2.EGU',
            'DESC': '32idbLAX:m58:c1:m2.DESC',
            'DMOV': '32idbLAX:m58:c1:m2.DMOV',
            'STOP': '32idbLAX:m58:c1:m2.STOP'
        }
    }
    app = wx.PySimpleApp()
    dlg = PvDialog(None, config)
    try:
        result = dlg.ShowModal()
    finally:
        print "OK button pressed:", result == wx.ID_OK
        if result == wx.ID_OK:
            # get the new configuration
            config = dlg.GetConfiguration()
        pprint.pprint(config)
        dlg.Destroy()
    app.MainLoop()
    pvConnect.on_exit()
