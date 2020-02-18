#!/usr/bin/env python

#*************************************************************************
# Copyright (c) 2009-2010 The University of Chicago, as Operator of Argonne
#     National Laboratory.
# Copyright (c) 2009-2010 The Regents of the University of California, as
#     Operator of Los Alamos National Laboratory.
# This file is distributed subject to a Software License Agreement found
# in the file LICENSE that is included with this distribution. 
#*************************************************************************

'''@note: support the XML settings file for the wxmtxy application

This Python file provides routines to read and write XML settings
files for the wxmtxy application.  An example of the XML file is 
shown below.  The routines manage the settings internally with a 
Python dictionary.  Interface routines are used to read and write 
the various components of the file.  *HOWEVER*, the EPICS configuration 
is communicated in a Python dictionary.  An example of the Python 
dictionary with the EPICS configuration is shown below.

@version: 
########### SVN repository information ###################
# $Date: 2010-12-06 15:13:14 -0600 (Mon, 06 Dec 2010) $
# $Author: jemian $
# $Revision: 216 $
# $URL: https://subversion.xor.aps.anl.gov/bcdaext/wxmtxy/trunk/wxmtxy_xml.py $
# $Id: wxmtxy_xml.py 216 2010-12-06 21:13:14Z jemian $
########### SVN repository information ###################

@note: for help with xml.dom, see http://docs.python.org/library/xml.dom.html

@note: Here is an example XML file:
<?xml version="1.0" ?>
<wxmtxy date="2009-04-09" time="10:27:00" version="1.0">
  <XYpair name="example" selected="True">
    <EPICS_configuration>
      <axis name="x">
        <flag isMotorRec="False" />
        <field name="VAL" pv="32idbLAX:float1" />
        <field name="RBV" pv="32idbLAX:float2" />
        <field name="DESC" pv="32idbLAX:string1" />
        <field name="EGU" pv="32idbLAX:string2" />
        <field name="DMOV" pv="32idbLAX:bit1" />
        <field name="STOP" pv="32idbLAX:bit2" />
      </axis>
      <axis name="y">
        <flag isMotorRec="True" />
        <field name="VAL" pv="32idbLAX:m58:c1:m1" /><!-- USAXS a1y -->
      </axis>
    </EPICS_configuration>
    <tab name="page 1">
      <row name="page 1, row 0" x="1.0" y="-1.0" selected="True"/>
      <row name="page 1, row 1" x="1.1" y="-1.1"/>
      <row/>
    </tab>
    <tab name="page 2" selected="True">
      <row name="page 2, row 0" x="2.0" y="-2.0"/>
      <row name="page 2, row 1" x="2.1" y="-2.1"/>
      <row name="page 2, row 2" x="2.2" y="-2.2" selected="True"/>
      <row name="page 2, row 3" x="2.3" y="-2.3"/>
      <row name="page 2, row 4" x="2.4" y="-2.4"/>
      <row name="page 2, row 5" x="2.5" y="-2.5"/>
      <row name="page 2, row 6" x="2.6" y="-2.6"/>
    </tab>
    <tab name="empty page"/>
    <tab name="page 3">
  </XYpair>
</wxmtxy>

@note: Here is an example Python dictionary of the EPICS configuration above:
    example_dictionary = {
        'x': {
            'isMotorRec': False,
            'VAL': '32idbLAX:float1',
            'RBV': '32idbLAX:float2',
            'DESC': '32idbLAX:string1',
            'EGU': '32idbLAX:string2',
            'DMOV': '32idbLAX:bit1',
            'STOP': '32idbLAX:bit2'
        },
        'y': {
            'isMotorRec': True,
            'VAL': '32idbLAX:m58:c1:m1.VAL'
        }
    }
'''


from xml.dom import minidom
import datetime
import copy
import wxmtxy_axis


class Settings:
    '''handle the XML settings file'''

    def __init__(self, settingsFile=None):
        '''prepare the settings file
            @param settingsFile: [string] name of XML file with settings'''
        self.rootElement = 'wxmtxy'
        self.Clear()
        self.SetSettingsFile(settingsFile)

    def GetDb(self):
        '''@return: database'''
        return self.db

    def GetSettingsFile(self):
        '''@return: name of XML settings file'''
        return self.settingsFile

    def SetSettingsFile(self, thefile):
        '''set the name of XML settings file
            @param thefile: [string] name of XML file with settings'''
        self.settingsFile = thefile

    def Clear(self):
        '''reset the internal data representation (db) to empty'''
        self.db = {}

    def NewPair(self, title=''):
        ''' create space in the database (db) for a new pair
            and sets defaults for fields

            @param title: [string] the title of the XY_pair set (default="")
            @return: the index number'''
        if self.CountPairs() == -1:
            self.db[u"pairs"] = []
        pairdb = {}
        pairdb[u"@name"] = title
        pairdb[u"@selected"] = False
        self.db[u'pairs'].append(pairdb)
        return len(self.db[u'pairs'])-1

    def GetPairTitle(self, pairnum):
        '''return the name of the XY_pair
            @param pairnum: [int] index number of the XY_pair'''
        return self.db[u"pairs"][pairnum][u"@name"]

    def SetPairTitle(self, pairnum, title):
        '''set the name of the XY_pair
            @param pairnum: [int] index number of the XY_pair'
            @param title: [string] name of the XY_pair'''
        self.db[u"pairs"][pairnum][u"@name"] = title

    def SelectPair(self, pairnum):
        '''set the "selected" attribute of the pair
            @param pairnum: [int] index number of the XY_pair'''
        for pair in self.db[u"pairs"]:   # first, deselect all pairs
            pair[u"@selected"] = False
        self.db[u"pairs"][pairnum][u"@selected"] = True

    def GetSelectedPair(self):
        '''@return: index number of the "selected" pair (-1 if none selected)'''
        selected = -1
        try:
            pairs = self.db[u"pairs"]
            for pairnum in range(len(pairs)):
                if pairs[pairnum][u"@selected"]:
                    selected = pairnum
                    break
        except:
            pass
        return selected

    def CountPairs(self):
        '''@return: number of pairs'''
        try:
            return len(self.db[u"pairs"])
        except:
            return -1

    def NewEpicsConfig(self, pairnum):
        '''Create internal space for a new EPICS configuration
            @param pairnum: [int] index number of the XY_pair'''
        pairdb = self.db[u"pairs"][pairnum]
        pairdb[u"epics"] = {}
        epicsdb = pairdb[u"epics"]
        for axis in ['x', 'y']:
            epicsdb[axis] = {}
            axisdb = epicsdb[axis]
            for field in wxmtxy_axis.field_list:
                axisdb[field] = ""
            axisdb[u"isMotorRec"] = False

    def GetEpicsConfig(self, pairnum):
        '''Get a deep copy Python dictionary of the current EPICS PV config.
            @param pairnum: [int] index number of the XY_pair
            @return: the current EPICS configuration'''
        return copy.deepcopy(self.db[u"pairs"][pairnum][u"epics"])

    def SetEpicsConfig(self, pairnum, config):
        '''set the current EPICS configuration
            @param pairnum: [int] index number of the XY_pair
            @param config: Python dictionary of EPICS PV configuration'''
        pairdb = self.db[u"pairs"][pairnum]
        deep = copy.deepcopy(config)
        pairdb[u"epics"] = deep

    def SetEpicsField(self, pairnum, axis, field, value):
        '''Define the EPICS config for a specific field
            @param pairnum: [int] index number of the XY_pair'
            @param axis: [string] "x" or "y"'
            @param field: [string] member of wxmtxy_axis.field_list'
            @param value: [string] value of this field'''
        try:
            axisdb = self.db[u"pairs"][pairnum][u"epics"][axis]
            axisdb[field] = value
        except:
            print "Could not assign EPICS field", pairnum, axis, field, value


    def NewTab(self, pairnum, title=''):
        ''' create space in the database (db) pair for a new tab
            and sets defaults for fields

            @param pairnum: [int] index number of the XY_pair
            @param title: the title of the pair set (default="")
            @return the index number'''
        pairdb = self.db[u"pairs"][pairnum]
        if not pairdb.has_key(u"tabs"):
            pairdb[u"tabs"] = []
        tabdb = {}
        tabdb[u"@name"] = title
        tabdb[u"@selected"] = False
        pairdb[u"tabs"].append(tabdb)
        return len(pairdb[u"tabs"])-1

    def GetTabTitle(self, pairnum, tabnum):
        '''return the name of the tab
            @param pairnum: [int] index number of the XY_pair
            @param tabnum: [int] index number of the Tab object'''
        return self.db[u"pairs"][pairnum][u"tabs"][tabnum][u"@name"]

    def SetTabTitle(self, pairnum, tabnum, title):
        '''set the name attribute of the tab
            @param pairnum: [int] index number of the XY_pair
            @param tabnum: [int] index number of the Tab object
            @param title: [string] title the Tab object'''
        self.db[u"pairs"][pairnum][u"tabs"][tabnum]["@name"] = title

    def SelectTab(self, pairnum, tabnum):
        '''set the selected attribute of the pair
            @param pairnum: [int] index number of the XY_pair
            @param tabnum: [int] index number of the Tab object'''
        pairdb = self.db[u"pairs"][pairnum]
        for tab in pairdb[u"tabs"]:   # first, deselect all tabs
            tab[u"@selected"] = False
        pairdb[u"tabs"][tabnum][u"@selected"] = True

    def GetSelectedTab(self, pairnum):
        '''return the index number of the selected tab
            @param pairnum: [int] index number of the XY_pair'''
        selected = -1
        try:
            tabs = self.db[u"pairs"][pairnum][u"tabs"]
            for tabnum in range(len(tabs)):
                if tabs[tabnum][u"@selected"]:
                    selected = tabnum
                    break
        except:
            pass
        return selected

    def CountTabs(self, pairnum):
        '''return the number of tabs
            @param pairnum: [int] index number of the XY_pair'''
        try:
            return len(self.db[u"pairs"][pairnum][u"tabs"])
        except:
            return -1

    def NewRow(self, pairnum, tabnum, title=''):
        ''' create space in the database (db) pair for a new tab
            and sets defaults for fields

            @param pairnum: [int] index number of the XY_pair
            @param tabnum: [int] index number of the Tab object
            @param title: the title of the Tab object (default="")
            @return the index number'''
        tabdb = self.db[u"pairs"][pairnum][u"tabs"][tabnum]
        if not tabdb.has_key(u"rows"):
            tabdb[u"rows"] = []
        rowdb = {}
        rowdb[u"@name"] = title
        rowdb[u"@selected"] = False
        rowdb[u"@x"] = ""
        rowdb[u"@y"] = ""
        tabdb[u"rows"].append(rowdb)
        return len(tabdb[u"rows"])-1

    def GetRowTitle(self, pairnum, tabnum, rownum):
        '''return the name of the row
            @param pairnum: [int] index number of the XY_pair
            @param tabnum: [int] index number of the Tab object
            @param rownum: [int] index number of the Row object'''
        tabdb = self.db[u"pairs"][pairnum][u"tabs"][tabnum]
        return tabdb[u"rows"][rownum][u"@name"]

    def SetRowTitle(self, pairnum, tabnum, rownum, title):
        '''set the name attribute of the row
            @param pairnum: [int] index number of the XY_pair
            @param tabnum: [int] index number of the Tab object
            @param rownum: [int] index number of the Row object
            @param title: [string] title the Tab object'''
        tabdb = self.db[u"pairs"][pairnum][u"tabs"][tabnum]
        tabdb[u"rows"][rownum][u"@name"] = title

    def GetRowXY(self, pairnum, tabnum, rownum):
        '''return the name of the row
            @param pairnum: [int] index number of the XY_pair
            @param tabnum: [int] index number of the Tab object
            @param rownum: [int] index number of the Row object'''
        tabdb = self.db[u"pairs"][pairnum][u"tabs"][tabnum]
        x = tabdb[u"rows"][rownum][u"@x"]
        y = tabdb[u"rows"][rownum][u"@y"]
        return x, y

    def SetRowXY(self, pairnum, tabnum, rownum, x, y):
        '''set the name attribute of the row
            @param pairnum: [int] index number of the XY_pair
            @param tabnum: [int] index number of the Tab object
            @param x: [float] X axis position
            @param y: [float] Y axis position'''
        tabdb = self.db[u"pairs"][pairnum][u"tabs"][tabnum]
        tabdb[u"rows"][rownum][u"@x"] = x
        tabdb[u"rows"][rownum][u"@y"] = y

    def CountRows(self, pairnum, tabnum):
        '''return the number of rows
            @param pairnum: [int] index number of the XY_pair
            @param tabnum: [int] index number of the Tab object'''
        try:
            return len(self.db[u"pairs"][pairnum][u"tabs"][tabnum][u"rows"])
        except:
            return -1

    def GetSelectedRow(self, pairnum, tabnum):
        '''return the index number of the selected row
            @param pairnum: [int] index number of the XY_pair
            @param tabnum: [int] index number of the Tab object'''
        selected = -1
        try:
            rows = self.db[u"pairs"][pairnum][u"tabs"][tabnum][u"rows"]
            for rownum in range(len(rows)):
                if rows[rownum][u"@selected"]:
                    selected = rownum
                    break
        except:
            pass
        return selected

    def SelectRow(self, pairnum, tabnum, rownum):
        '''set the selected attribute of the pair
            @param pairnum: [int] index number of the XY_pair
            @param tabnum: [int] index number of the Tab object
            @param rownum: [int] index number of the Row object'''
        tabdb = self.db[u"pairs"][pairnum][u"tabs"][tabnum]
        for row in tabdb[u"rows"]:   # first, deselect all rows
            row[u"@selected"] = False
        tabdb[u"rows"][rownum][u"@selected"] = True

    def ReadXmlFile(self):
        '''read the settings from a file into an internal dictionary (self.db)

            @note: this method uses xml.dom.minidom (built into all Pythons)
            @see: http://docs.python.org/library/xml.dom.minidom.html
        '''
        try:
            doc = minidom.parse(self.settingsFile) # parse an XML file by name
            assert doc.documentElement.tagName == self.rootElement
        except IOError:
            return 'Could not read the XML file: ' + self.settingsFile
        except AssertionError:
            return 'XML root element is not ' + self.rootElement
        #... read all attributes from the root element
        docElem = doc.documentElement
        self.Clear()
        version = self._get_attribute(docElem, "version", "not-specified")
        try:
            # only handle v1.0 resource configuration files
            assert version == u'1.0'
        except AssertionError:
            doc.unlink()
            return 'Cannot handle file version:', version
        # file verified now
        for pairNode in docElem.getElementsByTagName("XYpair"):
            title = self._get_attribute(pairNode, "name", "")
            selected = self._get_attribute(pairNode, "selected", "")
            pairnum = self.NewPair(title)
            if selected.lower() == "true":
                self.SelectPair(pairnum)
            self.NewEpicsConfig(pairnum)
            for EpicsNode in pairNode.getElementsByTagName("EPICS_configuration"):
                for axisNode in EpicsNode.getElementsByTagName("axis"):
                    axis = self._get_attribute(axisNode, "name", "")
                    #isMotorRec
                    for flagNode in axisNode.getElementsByTagName("flag"):
                        text = self._get_attribute(flagNode, "isMotorRec", "False")
                        self.SetEpicsField(pairnum, axis, "isMotorRec", (text == "True"))
                    for fieldNode in axisNode.getElementsByTagName("field"):
                        name = self._get_attribute(fieldNode, "name", "")
                        pv = self._get_attribute(fieldNode, "pv", "")
                        if (len(name)>0) and (len(pv)>0):
                            #print pairnum, axis, name, pv
                            self.SetEpicsField(pairnum, axis, name, pv)
            for tabNode in pairNode.getElementsByTagName("tab"):
                title = self._get_attribute(tabNode, "name", "")
                selected = self._get_attribute(tabNode, "selected", "")
                tabnum = self.NewTab(pairnum, title)
                if selected.lower() == "true":
                    self.SelectTab(pairnum, tabnum)
                # EPICS settings here
                for rowNode in tabNode.getElementsByTagName("row"):
                    title = self._get_attribute(rowNode, "name", "")
                    selected = self._get_attribute(rowNode, "selected", "")
                    x = self._get_attribute(rowNode, "x", "")
                    y = self._get_attribute(rowNode, "y", "")
                    rownum = self.NewRow(pairnum, tabnum, title)
                    self.SetRowXY(pairnum, tabnum, rownum, x, y)
        doc.unlink()  # ensures XML document is disposed cleanly
        return None

    def _get_attribute(self, node, key, default):
        '''get a specific attribute or return the default
            @param node: XML Node object
            @param key: [string] name of attribute to find
            @param default: [string] default value to return'''
        value = default
        if node.attributes.has_key(key):
            value = node.attributes[key].value
        return value

    def SaveXmlFile(self):
        '''save the internal dictionary (self.db) to an XML file
           @note: What about using/saving a default stylesheet?
           @see: http://www.boddie.org.uk/python/XML_intro.html
        '''
        out = open(self.settingsFile, 'w')
        out.write(repr(self))
        out.close()
        #
        # What about a default stylesheet?
        #
        
        return 'Saved settings to ' + self.settingsFile

    def _SetAttr(self, node, attribute, value):
        '''add attributes that are not empty (but do not strip the whitespace)
            @param node: XML Node object
            @param attribute: [string] name of attribute
            @param value: [string] value of attribute'''
        if len(value) > 0:
            node.setAttribute(attribute, value)

    def _makeTextNode(self, doc, tag, value):
        '''create a text node for the XML file
            @param doc: [xml.dom.minidom documentElement object]
            @param tag: [string] element name
            @param value: [string] element text'''
        node = doc.createElement(tag)
        text = doc.createTextNode(value)
        node.appendChild(text)
        return node

    def __repr__(self):
        '''default representation of this structure is XML
            @return: XML representation of internal database (db)
            @note: What about a default stylesheet?
        '''
        t = datetime.datetime.now()
        yyyymmdd = t.strftime("%Y-%m-%d")
        hhmmss = t.strftime("%H:%M:%S")

        # Create the minidom document
        doc = minidom.Document()

        # Create the root element
        root = doc.createElement(self.rootElement)
        self._SetAttr(root, "version", "1.0")
        self._SetAttr(root, "date", yyyymmdd)
        self._SetAttr(root, "time", hhmmss)
        doc.appendChild(root)
        selectedpairnum = self.GetSelectedPair()
        for pairnum in range(self.CountPairs()):
            pairnode = doc.createElement("XYpair")
            self._SetAttr(pairnode, "name", 
                   self.GetPairTitle(pairnum))
            if selectedpairnum == pairnum:
                self._SetAttr(pairnode, "selected", "True")
            if self.db[u"pairs"][pairnum].has_key(u"epics"):
                epicsnode = doc.createElement("EPICS_configuration")
                epicsdb = self.db[u"pairs"][pairnum][u"epics"]
                for axis in epicsdb:
                    axisnode = doc.createElement("axis")
                    self._SetAttr(axisnode, "name", axis)
                    field = "isMotorRec"
                    if field in epicsdb[axis]:
                        node = doc.createElement("flag")
                        self._SetAttr(node, field, str(epicsdb[axis][field]))
                        axisnode.appendChild(node)
                    for field in wxmtxy_axis.field_list:
                        if field in epicsdb[axis]:
                            if len(epicsdb[axis][field])>0:
                                node = doc.createElement("field")
                                self._SetAttr(node, "name", field)
                                self._SetAttr(node, "pv", str(epicsdb[axis][field]))
                                axisnode.appendChild(node)
                    epicsnode.appendChild(axisnode)
                pairnode.appendChild(epicsnode)
            selectedtabnum = self.GetSelectedTab(pairnum)
            for tabnum in range(self.CountTabs(pairnum)):
                tabnode = doc.createElement("tab")
                self._SetAttr(tabnode, "name", self.GetTabTitle(pairnum, tabnum))
                if selectedtabnum == tabnum:
                    self._SetAttr(tabnode, "selected", "True")
                selectedrownum = self.GetSelectedRow(pairnum, tabnum)
                for rownum in range(self.CountRows(pairnum, tabnum)):
                    rownode = doc.createElement("row")
                    label = self.GetRowTitle(pairnum, tabnum, rownum)
                    x, y = self.GetRowXY(pairnum, tabnum, rownum)
                    self._SetAttr(rownode, "name", label)
                    self._SetAttr(rownode, "x", x)
                    self._SetAttr(rownode, "y", y)
                    if selectedrownum == rownum:
                        self._SetAttr(rownode, "selected", "True")
                    tabnode.appendChild(rownode)
                pairnode.appendChild(tabnode)
            root.appendChild(pairnode)
        return doc.toprettyxml(indent="  ")


if __name__ == '__main__':
    rc = Settings("examples/test-settings.xml")
    rc.ReadXmlFile()
    rc.SetSettingsFile('output-test.xml')
    rc.SaveXmlFile()

    pj = Settings()
    pairnum = pj.NewPair("my test pair")
    tabnum = pj.NewTab(pairnum, title='my test tab')
    tabnum = pj.NewTab(pairnum, title='another')
    pj.SelectTab(pairnum, tabnum)
    tabnum = pj.NewTab(pairnum, title='another')
    tabnum = pj.NewTab(pairnum, title='another')
    pairnum = pj.NewPair("another")
    pj.SelectPair(pairnum)
    tabnum = pj.NewTab(pairnum, title='another')
    rownum = pj.NewRow(pairnum, tabnum, "beam center")
    pj.SelectRow(pairnum, tabnum, rownum)
    tabnum = pj.NewTab(pairnum, title='another')
    pairnum = pj.NewPair("another")
    print str(pj)
