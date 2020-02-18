#!/usr/bin/env python

# full contents of __file_license__ appear at the top of each file
__file_license__ = '''
#*************************************************************************
# Copyright (c) 2009-2010 The University of Chicago, as Operator of Argonne
#     National Laboratory.
# Copyright (c) 2009-2010 The Regents of the University of California, as
#     Operator of Los Alamos National Laboratory.
# This file is distributed subject to a Software License Agreement found
# in the file LICENSE that is included with this distribution. 
#*************************************************************************
'''

'''
version information for wxmtxy

########### SVN repository information ###################
# $Date: 2010-12-06 15:28:19 -0600 (Mon, 06 Dec 2010) $
# $Author: jemian $
# $Revision: 217 $
# $URL: https://subversion.xor.aps.anl.gov/bcdaext/wxmtxy/trunk/wxmtxy_version.py $
# $Id: wxmtxy_version.py 217 2010-12-06 21:28:19Z jemian $
########### SVN repository information ###################
'''


__author__ = "Pete R. Jemian"
__author_email__ = "jemian@anl.gov"
__contributor_credits__ = [
       "",
       "other contributors:",
       "Geoff Savage/FNAL and John Hammonds/APS for CaChannel", 
       "Tim Mooney/APS for ca_util"]
__company_name__ = "Advanced Photon Source"
__version__ = "0.5"
__copyright__ = "(c) 2009, 2010"
#fp = open('LICENSE', 'r')
#__license__ = fp.read()
#fp.close()
__license__ = "APS extensions license.  See LICENSE file for details"
__long_description__ = '''wxmtxy is an EPICS GUI tool to assist users in routine operation of positioning devices''' 
__main_script__ = "wxmtxy.py"
__summary__ = "wxmtxy: a GUI tool for EPICS"
__target_name__ = "wxmtxy"
__url__ = "https://subversion.xor.aps.anl.gov/trac/bcdaext/wiki/wxmtxy"
__urlsvn__ = "https://subversion.xor.aps.anl.gov/bcdaext/wxmtxy"
__svndesc__ = 'wxmtxy SVN repo page'
__documentation__ = '''
    *wxmtxy* (an EPICS GUI tool) provides support for an X,Y positioner 
    (motor) pair by allowing users to define a table of known positions 
    and providing a one-button click to drive a chosen X,Y pair to a specific
    table setting.  Also can record current position into a setting.

    Several sets of X,Y positioners can be configured.  (Each set is 
    separate.)  In fact, the positioners do not have to be motors,
    but can be any type of EPICS PV that will accept a numeric value.
'''

