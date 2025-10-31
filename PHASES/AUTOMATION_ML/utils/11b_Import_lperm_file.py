# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 09:42:22 2024

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
#	Date				:  	Thu Feb 22 09:38:45 2024
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
ret=VE.ChangeContext( r"Visual-Distortion" )
VE.SetActiveWindow( r"p1w1" )
ret=VE.ChangeContext( r"Visual-RTM" )
VE.SetCurrentPage( 1 )
VExpMngr.SetFilesOfType( r"All" )

import os
Scriptsfolder = os.getcwd()
VariablesList = os.path.join(Scriptsfolder, 'VariablesList.txt')
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
            VdbRTMFilePath = linesplit[2]
        if 'lpermfile' in line:
            linesplit = line.partition('= ')
            #Extract Variable name, value and IDnumber identificator                           
            lpermfile = linesplit[2]
            
ret=VExpMngr.LoadFile(VdbRTMFilePath,0)
ret=VE.ModelChange( "M  @0" )

#__________________ ImportExportLocalProperties BEGIN __________________
var4=VCmd.Activate( 1, r"VRTMUtilities.VRTMInterface", r"ImportExportLocalProperties" )
VCmd.SetGuStringValue( var4, r"ImportFileName", lpermfile )
ret=VCmd.ExecuteCommand( var4, r"ImportLocalResults" )

VExpMngr.ExportFile( VdbRTMFilePath, 0 )