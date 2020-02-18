#!/usr/bin/env python
from compiler.ast import TryExcept

#*************************************************************************
# Copyright (c) 2009-2010 The University of Chicago, as Operator of Argonne
#     National Laboratory.
# Copyright (c) 2009-2010 The Regents of the University of California, as
#     Operator of Los Alamos National Laboratory.
# This file is distributed subject to a Software License Agreement found
# in the file LICENSE that is included with this distribution. 
#*************************************************************************

'''EPICS PVs and connections for one axis

@version: 
########### SVN repository information ###################
# $Date: 2010-06-03 16:04:15 -0500 (Thu, 03 Jun 2010) $
# $Author: jemian $
# $Revision: 184 $
# $URL: https://subversion.xor.aps.anl.gov/bcdaext/wxmtxy/trunk/wxmtxy_axis.py $
# $Id: wxmtxy_axis.py 184 2010-06-03 21:04:15Z jemian $
########### SVN repository information ###################
'''


import pvConnect
import pprint
import copy
import time


field_list = ['VAL', 'RBV', 'EGU', 'DESC', 'DMOV', 'STOP']


class Axis:
    '''EPICS PVs and connections for one axis'''

    def __init__(self):
        '''declare initial storage'''
        self.db = {}
        self.config = None
        self.isMotorRec = False
        for field in field_list:
            self.db[field] = _data()

    def Connect(self):
        '''Try to initiate EPICS connection with named PVs
            @return: [Boolean] if all axes connected'''
        failures = 0
        for field in field_list:
            # TODO: Can these connections be done together?
            ch = self.db[field].GetConnection()
            if ch != None:
                try:
                    ch.connectw()
                    ch.monitor()
                except:
                    failures += 1
                    print "Could not connect with PV: " + self.db[field].pv
        return failures > 0

    def Disconnect(self):
        '''Terminate EPICS connection with named PVs'''
        for field in field_list:
            ch = self.db[field].GetConnection()
            if ch != None:
                ch.release()

    def Stop(self):
        '''Send a STOP to EPICS'''
        field = 'STOP'
        ch = self.db[field].GetConnection()
        ch.chan.putw(1)

    def Move(self, position):
        '''Send new position to VAL field of EPICS'''
        field = 'VAL'
        ch = self.db[field].GetConnection()
        #print __name__, 'Move:', position
        ch.chan.putw(position)

    def GetConfigure(self):
        '''Get the EPICS PVs for this X,Y pair
            @return: Python dictionary of EPICS PV configuration'''
        return copy.deepcopy(self.config)

    def SetConfigure(self, config):
        '''Define the EPICS PVs for this X,Y pair
            @param config: Python dictionary of EPICS PV configuration'''
        # pprint.pprint(config)
        self.config = copy.deepcopy(config)
        if not self.config.has_key('isMotorRec'):
            return
        self.isMotorRec = self.config['isMotorRec']
        base = self.config['VAL'].split('.')[0]
        for field in self.config:
            if field in field_list:
                self.db[field].SetPv(self.config[field])
        if self.isMotorRec:
            # fill in default fields of motor records
            for field in field_list:
                pv = self.db[field].GetPv()
                if pv == None or len(pv) == 0:
                    self.db[field].SetPv(base + '.' + field)
        # What about checking to see how many fields have connected?
        # And then dumping if not all fields connect?


class _data:
    '''the internal data associated with a single PV'''

    def __init__(self):
        '''only create the space'''
        self.pv = None
        self.connection = None
        self.widget = None

    def GetPv(self):
        '''@return: [string] EPICS PV name'''
        return self.pv

    def SetPv(self, pv):
        '''set the PV name
            @param pv: [string] EPICS PV name'''
        self.pv = pv
        self.connection = pvConnect.EpicsPv(pv)

    def GetConnection(self):
        '''@return: pvConnect.EpicsPv object'''
        return self.connection

    def GetWidget(self):
        '''@return: widget object'''
        return self.widget

    def SetWidget(self, widget):
        '''set widget object to be used in a callback
            @param widget: used as self.widget(value)'''
        self.widget = widget

    def _callback(self, value):
        '''receive EPICS CA monitor value
            @param value: from epics_get['pv_value']'''
        # print __name__, self.pv, value, self.connection.epics_args, self.connection.user_args
        if self.widget != None:
            self.widget(value)


# example code follows


def _main_callback(epics_args, user_args):
    '''EPICS monitor event received for test code'''
    value = epics_args['pv_value']
    pv = user_args[0]
    # pprint.pprint(epics_args)
    print '_main_callback:', pv, value


if __name__ == '__main__':
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
        },
        'sr': {
            # USAXS a1y: 32idbLAX:m58:c1:m1
            'isMotorRec': False,
            'VAL': 'S:SRcurrentAI'
        }
    }
    axes = {}
    for axis in config:
        item = Axis()
        axes[axis] = item
        item.SetConfigure(config[axis])
        ch = item.db['VAL'].GetConnection()
        ch.SetUserArgs(axis)
        ch.SetUserCallback(_main_callback)
        cfg = item.GetConfigure()
        cfg['AXIS'] = axis
        # pprint.pprint(cfg)
        item.Connect()
        print 'axis', axis
        interval = 5
        for seconds in range(interval):
            time.sleep(1)
            ch.chan.pend_event()
            print interval - seconds - 1, ch.GetPv(), '=', ch.GetValue()
            # pprint.pprint(ch.epics_args)
        # pprint.pprint(cfg)
    for axis in config:
        axes[axis].Disconnect()
    pvConnect.on_exit()
