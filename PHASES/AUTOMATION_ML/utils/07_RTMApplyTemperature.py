# -*- coding: utf-8 -*-
"""
Created on Fri Jan 20 11:48:17 2023

@author: SMO
"""

#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#-------------------------------------------------------------------------------
#                          Session File
#                           ESI Group
#                      https://www.esi-group.com
#        Copyright (C) ESI Group 2022.  All rights reserved.
#-------------------------------------------------------------------------------
#	Product				:  	Visual-Environment 18.0
#	Date				:  	Fri Jan 20 11:41:54 2023
#-------------------------------------------------------------------------------
null='' 
from VgPoint3 import *
from VgPoint2 import *
from VgMatrix import *
import VScn
import VGuiUtl
import VCmdGui
import VCmd
import VCmdFramework
import VistaDb
NULL=VistaDb.PythonCNULL() 
import VistaDb
#__________________ VhmCommand BEGIN __________________
var1=VCmd.Activate( 1, r"VHostManagerPlugin.VhmInterface", r"VhmCommand" )
import VHostManager
import VE
import VExpMngr
#__________________ SessionCommand BEGIN __________________
var2=VCmd.Activate( 1, r"VSessionManager.Command", r"SessionCommand" )
import VToolKit
#__________________ VEAction BEGIN __________________
var3=VCmd.Activate( 1, r"VToolKit.VSectionCutInterface", r"VEAction" )
import VBrowserManager
import VMaterial
import VMeshMdlr
ret=VE.ChangeContext( r"Visual-RTM" )
VE.SetActiveWindow( r"p1w1" )
VE.SetCurrentPage( 1 )
VExpMngr.SetFilesOfType( r"All" )
import os
#SMO: read macro directory from temporary file
Scriptsfolder = os.getcwd()
VariablesList = os.path.join(Scriptsfolder,'VariablesList.txt')

line_no = 0
incfile= open(VariablesList,"r")
if incfile.mode == 'r':
    inclines = incfile.read().splitlines()
    incfile.close()
    for line in inclines:
        line_no += 1
        if 'VdbRTMFilePath' in line:
            linesplit = line.partition('= ')
            #Extract Variable name, value and IDnumber identificator                           
            VdbFilePath = linesplit[2]
        if 'Injection_temperature' in line:
            linesplit = line.partition('= ')
            #Extract Variable name, value and IDnumber identificator                           
            Temperature = linesplit[2]
            
ret=VExpMngr.LoadFile(VdbFilePath,0)
ret=VE.ModelChange( "M  @0" )

VCmd.SetStringValue( var1, r"DisplayMode", r"Flat and Wireframe" )
#__________________ BoundaryConditions BEGIN __________________
var4=VCmd.Activate( 1, r"VRTMUtilities.VRTMInterface", r"BoundaryConditions" )
VCmd.SetStringValue( var4, r"ActiveBcType", r"Pressure" )
VCmd.SetStringValue( var4, r"ActiveBcName", r"Pressure_1" )
VCmd.SetGuStringValue( var4, r"OpeningMode", r"Edit" )
VCmd.SetStringValue( var4, r"ActiveBcParam", r"temperatureValue" )
VCmd.SetDoubleValue( var4, r"ParamDoubleValue", float(Temperature)  )
VCmd.Accept( var4 )
VCmd.Quit( var4 )
#__________________ UserDefineRegionChild END __________________
VExpMngr.ExportFile( VdbFilePath, 0 )
# ret=VE.ModelDestroy( "M  @0" )
# VE.SetCurrentPage( 1 )
# VE.SetActiveWindow( r"p1w1" )
# VE.NewSession(  )