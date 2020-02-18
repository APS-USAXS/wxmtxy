<?xml version="1.0" ?>

<!--
########### SVN repository information ###################
# $Date: 2009-05-05 14:05:50 -0500 (Tue, 05 May 2009) $
# $Author: jemian $
# $Revision: 50 $
# $URL: https://subversion.xor.aps.anl.gov/bcdaext/wxmtxy/trunk/examples/wxmtxy_settings.xsl $
# $Id: wxmtxy_settings.xsl 50 2009-05-05 19:05:50Z jemian $
########### SVN repository information ###################
-->

<xsl:stylesheet
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  version="1.0">

  <xsl:template match="/">
      <xsl:apply-templates select="wxmtxy"/>
  </xsl:template>

<xsl:template match="wxmtxy">
    <xsl:element name="html">
        <xsl:element name="head">
            <xsl:element name="title">wxmtxy (wxMotorToolXY): settings file</xsl:element>
        </xsl:element>
        <xsl:element name="body">
            <xsl:attribute name="bgcolor">#f0f0f8</xsl:attribute>
            <xsl:element name="h1">wxmtxy (wxMotorToolXY): a GUI tool for EPICS</xsl:element>
            <xsl:element name="h2">positioner settings file</xsl:element>
            <xsl:apply-templates select="XYpair"/>
            <!-- put summary info and copyright and home page links here -->
            <!-- also index to the "*" marks that indicate the selected item -->
        </xsl:element>
    </xsl:element>
</xsl:template>
    
    <xsl:template match="XYpair">
        <xsl:element name="h2">XYpair: 
            <xsl:value-of select="@name"/><xsl:if test="count(@selected)=1">*</xsl:if>
        </xsl:element>
        <xsl:apply-templates select="EPICS_configuration"/>
        <xsl:apply-templates select="tab"/>
        <xsl:element name="hr"/>
    </xsl:template>
    
    <xsl:template match="EPICS_configuration">
        <!-- 
            <axis name="y">
            <flag isMotorRec="False"/>
            <field name="VAL" pv="32idbLAX:float11"/>
            <field name="RBV" pv="32idbLAX:float12"/>
            <field name="EGU" pv="32idbLAX:string12"/>
            <field name="DESC" pv="32idbLAX:string11"/>
            <field name="DMOV" pv="32idbLAX:bit11"/>
            <field name="STOP" pv="32idbLAX:bit12"/>
            </axis>
        -->
        <xsl:element name="h3">EPICS_configuration: 
            <xsl:value-of select="@name"/><xsl:if test="count(@selected)=1">*</xsl:if>
        </xsl:element>
        <xsl:element name="ul">
            <xsl:for-each select="axis">
                <xsl:element name="dt">
                    <xsl:element name="b">
                        <xsl:value-of select="@name"/> axis</xsl:element>
                </xsl:element>
                <xsl:element name="dd">
                <xsl:for-each select="*">
                    <xsl:if test="position()!=1">, </xsl:if>
                    <xsl:choose>
                        <xsl:when test="name()='flag'">
                            isMotorRec=<xsl:value-of select="@isMotorRec"/>
                        </xsl:when>
                        <xsl:otherwise>
                            <!-- ************ trouble here ************ -->
                            <!-- <xsl:value-of select="name()"/>= -->
                            <xsl:value-of select="@pv"/>
                        </xsl:otherwise>
                    </xsl:choose>
                </xsl:for-each>
                </xsl:element>
            </xsl:for-each>
        </xsl:element>
        <!--
        <xsl:element name="table">
            <xsl:attribute name="border">2</xsl:attribute>
            <xsl:element name="tr">
                <xsl:element name="th">item</xsl:element>
                <xsl:element name="th">X axis</xsl:element>
                <xsl:element name="th">Y axis</xsl:element>
            </xsl:element>
            <xsl:element name="tr">
                <xsl:element name="td">motor record?</xsl:element>
                this XPATH/XSLT does not work in Firefox or IExplore
                <xsl:element name="td"><xsl:value-of select="axis[@name='x']/flag[@isMotorRec]"/></xsl:element>
                <xsl:element name="td"><xsl:value-of select="axis[@name='y']/flag[@isMotorRec]"/></xsl:element>
            </xsl:element>
            <xsl:element name="tr">
                <xsl:element name="td">motor record?</xsl:element>
                <xsl:element name="td"><xsl:value-of select="axis[@name='x']/field[@name]"/></xsl:element>
                <xsl:element name="td"><xsl:value-of select="axis[@name='y']/flag[@isMotorRec]"/></xsl:element>
            </xsl:element>
        </xsl:element>
        -->
    </xsl:template>
    
    <xsl:template match="tab">
        <!-- what about blank tabs? -->
        <xsl:element name="h2">Tab: 
            <xsl:value-of select="@name"/><xsl:if test="count(@selected)=1">*</xsl:if>
        </xsl:element>
        <xsl:if test="count(@selected)!=0">
            <xsl:element name="table">
                <xsl:attribute name="border">2</xsl:attribute>
                <xsl:element name="tr">
                    <xsl:element name="th">label</xsl:element>
                    <xsl:element name="th">X</xsl:element>
                    <xsl:element name="th">Y</xsl:element>
                </xsl:element>
                <xsl:apply-templates select="row"/>
            </xsl:element>
        </xsl:if>
    </xsl:template>
    
    <xsl:template match="row">
        <xsl:element name="tr">
            <!-- what about blank rows? -->
            <xsl:element name="td"><xsl:value-of select="@name"/></xsl:element>
            <xsl:element name="td"><xsl:value-of select="@x"/></xsl:element>
            <xsl:element name="td"><xsl:value-of select="@y"/></xsl:element>
        </xsl:element>
    </xsl:template>

</xsl:stylesheet>