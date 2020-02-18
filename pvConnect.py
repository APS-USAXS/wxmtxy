#!/usr/bin/env python

#*************************************************************************
# Copyright (c) 2009-2010 The University of Chicago, as Operator of Argonne
#     National Laboratory.
# Copyright (c) 2009-2010 The Regents of the University of California, as
#     Operator of Los Alamos National Laboratory.
# This file is distributed subject to a Software License Agreement found
# in the file LICENSE that is included with this distribution. 
#*************************************************************************

'''
simplified connections to an EPICS PV using CaChannel

Provides these classes:

    CaPollWx
        Use in WX-based GUIs to call ca.poll() in the background
        @param interval_s: [float] interval between calls to ca.poll()

    EpicsPv
        manage a CaChannel connection with an EPICS PV
        @param name: [string] EPICS PV to connect

Provides these utility routines:

    on_exit(timer)
        Exit handler to stop the ca.poll()
        @param timer: CaPollWx object

    CaPoll()
        Use in non-GUI scripts to call ca.poll() in the background

    GetRTYP(pv)
        Returns the record type of "pv"
        @param pv:[string]
        @return: [string] EPICS record type or None if cannot connect

    testConnect(pv)
        Tests if a CaChannel connection can be established to "pv"
        @param pv:[string]
        @return: True if can connect, otherwise False

    receiver(value)
        Example response to an EPICS monitor on the channel
        @param value: str(epics_args['pv_value'])

@version: 
########### SVN repository information ###################
# $Date: 2010-06-03 16:04:15 -0500 (Thu, 03 Jun 2010) $
# $Author: jemian $
# $Revision: 184 $
# $URL: https://subversion.xor.aps.anl.gov/bcdaext/wxmtxy/trunk/pvConnect.py $
# $Id: pvConnect.py 184 2010-06-03 21:04:15Z jemian $
########### SVN repository information ###################
'''


import sys
import time


try:
    # CaChannel provides access to the EPICS PVs
    import CaChannel
    IMPORTED_CACHANNEL = True
except:
    IMPORTED_CACHANNEL = False


try:
    # wx is needed for the timer to call CaChannel.ca.poll()
    # only use this with a wx-based GUI
    import wx
    IMPORTED_WX = True
except:
    IMPORTED_WX = False


class CaPollWx:
    '''Use in WX-based GUIs to call ca.poll() in the background
        
        Set up a separate thread to trigger periodic calls to the 
        EPICS CaChannel.ca.poll() connection.  Awaiting (a.k.a., 
        outstanding or pending) channel access background 
        activity executes during the poll.  Calls pend_event() 
        with a timeout short enough to poll.  

        The default polling interval is 0.1 second.
    
        @note: The code will silently do nothing if wx was not imported.
        This routine use the wx.PyTimer() to call ca.poll() frequently 
        during the main WX event loop.

        @warning: Only use this in a routine that has already called 
        wx.App() or an exception will occur.  
        Command line code will need to call ca.poll() using a different 
        method (such as CaPoll() below).
    '''

    def __init__(self, interval_s = 0.1):
        '''@param interval_s: [float] interval between calls to ca.poll()'''
        if IMPORTED_WX:     # only if wx was imported
            self.running = False
            self.interval_s = interval_s
            self.timer = wx.PyTimer(self.poll)
            self.timer.Start(int(self.interval_s*1000))

    def start(self):
        '''start polling'''
        if IMPORTED_WX:     # only if wx was imported
            self.running = True
            self.timer.Start(int(self.interval_s*1000))

    def stop(self):
        '''stop polling'''
        if IMPORTED_WX:     # only if wx was imported
            self.running = False
            self.timer.Stop()

    def poll(self):
        '''Poll for changes in Channel'''
        if IMPORTED_WX:     # only if wx was imported
            CaChannel.ca.poll()

    def GetInterval(self):
        '''return the current interval between calls to CaChannel.ca.poll()'''
        if IMPORTED_WX:     # only if wx was imported
            return self.interval_s

    def SetInterval(self, interval_s):
        '''set the next interval between calls to CaChannel.ca.poll()'''
        if IMPORTED_WX:     # only if wx was imported
            self.interval_s = interval_s


class EpicsPv:
    '''manage a connection with an EPICS PV'''

    def __init__(self, name):
        '''initialize the class and set default values
           @param name: [string] EPICS PV to connect'''
        self.pv = name
        self.chan = None
        self.value = None
        self.user_callback = None
        self.epics_args = None
        self.user_args = None
        self.mask = None
        if IMPORTED_CACHANNEL:
            self.mask = CaChannel.ca.DBE_VALUE

    def callback(self, epics_args, user_args):
        '''receive an EPICS callback, copy epics_args and user_args, then call user'''
        self.epics_args = epics_args
        self.user_args = user_args
        self.value = epics_args['pv_value']
        if self.user_callback != None:
            self.user_callback(epics_args, user_args)

    def connect(self):
        '''initiate the connection with EPICS'''
        if IMPORTED_CACHANNEL:
            if len(self.pv) > 0:
                self.chan = CaChannel.CaChannel()
                self.chan.search(str(self.pv))

    def connectw(self):
        '''initiate the connection with EPICS, standard wait for the connection'''
        if IMPORTED_CACHANNEL:
            if len(self.pv) > 0:
                self.chan = CaChannel.CaChannel()
                self.chan.searchw(str(self.pv))

    def release(self):
        '''release the connection with EPICS
            @note: Release ALL channels before calling on_exit()'''
        if self.chan != None:
            del self.chan
            self.chan = None

    def monitor(self):
        '''Initiate a monitor on the EPICS channel, delivering the 
            CaChannel callback to the supplied function.
            
            @note: Example:
                ch = EpicsPv(test_pv)
                ch.connectw()
                uargs = test_pv, widget.SetLabel
                ch.SetUserArgs(uargs)
                ch.SetUserCallback(myCallback)
                ch.monitor()
            
            @warning: At this time, there is not an easy way to turn off monitors.
                Instead, ch.release() the channel (which will set self.chan = None),
                To re-start a monitor after a ch.release(), connect as usual and start
                the monitor again, as the first time.
        '''
        if IMPORTED_CACHANNEL and self.chan != None:
            type = CaChannel.ca.dbf_type_to_DBR_GR(self.chan.field_type())
            # call supplied callback routine with default argument list
            #       self.user_callback(epics_args, user_args)
            self.chan.add_masked_array_event(type, 
                None, self.mask, self.callback, self.user_args)

    def GetPv(self):
        '''@return: PV name'''
        return self.pv

    def GetValue(self):
        '''@return: value from EPICS from the most recent monitor event'''
        return self.value

    def SetPv(self, name):
        '''redefine the PV name only if there is no connection
            @param name: valid EPICS PV name'''
        if self.chan == None:
            self.pv = name

    def GetChan(self):
        '''@return: CaChannel channel'''
        return self.chan

    def GetEpicsArgs(self):
        '''@return: epics_args from the most recent monitor event'''
        return self.epics_args

    def GetUserArgs(self):
        '''@return: user_args from the most recent monitor event'''
        return self.user_args

    def SetUserArgs(self, user_args):
        '''define the user_args tuple to use when monitoring
            @param user_args: tuple of user data (for use in user_callback function)'''
        self.user_args = user_args

    def SetMask(self, mask):
        '''Define the mask used when applying a channel monitor.
            The default is: self.mask = CaChannel.ca.DBE_VALUE
            @param mask: as defined in the CaChannel manual'''
        self.pv = mask

    def GetUserCallback(self):
        '''return the callback function supplied by the caller
            values will be set by self.user_callback(value)
            @return: function object'''
        return self.user_callback

    def SetUserCallback(self, user_callback):
        '''Set the callback function supplied by the caller
            values will be set by self.user_callback(value)
            @param user_callback: function object'''
        self.user_callback = user_callback


def on_exit(timer = None):
    '''Exit handler to stop the ca.poll()
       @param timer: CaPollWx object

       Call this to cleanup when program is exiting.
       ONLY call this function during a program's exit handling.
       If ca.task_exit() is not called, then expect to see the errors:
            FATAL: exception not rethrown
            Abort
    '''
    if IMPORTED_CACHANNEL:     # only if ca binding was loaded
        CaChannel.ca.task_exit()
    try:        # fail no matter what
        if timer != None:
            timer.stop()
    except:
        pass


def CaPoll():
    '''Use in non-GUI scripts to call ca.poll() in the background'''
    if IMPORTED_CACHANNEL:
        CaChannel.ca.poll()


def GetRTYP(pv):
    '''Returns the record type of "pv"
       @param pv:[string]
       @return: [string] EPICS record type or None if cannot connect'''
    if not IMPORTED_CACHANNEL:
        return None
    if len(pv) == 0:
        return None
    base = pv.split('.')[0]
    if testConnect(base):
        rtyp_pv = base + '.RTYP'
        ch = EpicsPv(rtyp_pv)
        ch.connectw()
        rtyp = ch.chan.getw()
        del ch
        return rtyp
    else:
        return None


def testConnect(pv):
    '''Tests if a CaChannel connection can be established to "pv"
       @param pv:[string]
       @return: True if can connect, otherwise False'''
    result = False
    if not IMPORTED_CACHANNEL:
        return result
    try:
        #print 'testConnect:', type(pv), pv
        chan = CaChannel.CaChannel()
        chan.searchw(str(pv))
        val = chan.getw()
        del chan
        result = True
    except (TypeError, CaChannel.CaChannelException), status:
        # python3: (TypeError, CaChannel.CaChannelException) as status
        #print 'testConnect:', status
        pass
    return result


def receiver(epics_args, user_args):
    '''Example response to an EPICS monitor on the channel
       @param value: str(epics_args['pv_value'])'''
    value = epics_args['pv_value']
    print 'receiver', 'updated value:', str(value)


if __name__ == '__main__':
    if IMPORTED_CACHANNEL:
        test_pv = 'S:SRcurrentAI'
        if testConnect(test_pv):
            print "recordType(%s) = %s" % (test_pv, GetRTYP(test_pv))
            ch = EpicsPv(test_pv)
            ch.connectw()
            ch.SetUserCallback(receiver)
            ch.monitor()
            ch.chan.pend_event()
            import time
            count = 5
            for seconds in range(count):
                time.sleep(1)
                ch.chan.pend_event()
                print count - seconds - 1, ch.GetPv(), '=', ch.GetValue()
            ch.release()
            on_exit()
    else:
        print "CaChannel is missing, cannot run"
