# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 15:07:57 2023

@author: SMO
"""
import os

#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#-------------------------------------------------------------------------------
#                          Session File
#                           ESI Group
#                      https://www.esi-group.com
#        Copyright (C) ESI Group 2022.  All rights reserved.
#-------------------------------------------------------------------------------
#	Product				:  	Visual-Environment 18.0
#	Date				:  	Thu Mar 30 15:05:43 2023
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
ret=VE.ChangeContext( r"Visual-Distortion" )
VE.SetCurrentPage( 1 )

print(100*'_')
print('DISTORTION, Simulation parameters. p37')
print('Reading list of variables')

#External Variables file:
Scriptsfolder = os.getcwd()
VariablesList = os.path.join(Scriptsfolder, 'VariablesList.txt')

#SMO: read macro directory from temporary file
line_no = 0

incfile= open(VariablesList,"r")
if incfile.mode == 'r':
    inclines = incfile.read().splitlines()
    incfile.close()
    for line in inclines:
        line_no += 1
        if 'VdbDistortionFilePath' in line:
            linesplit = line.partition('= ')
            #Extract Variable name, value and IDnumber identificator                           
            VdbDistortionFilePath = linesplit[2]
        if 'CuringCATGENerfPath' in line:
            linesplit = line.partition('= ')
            #Extract Variable name, value and IDnumber identificator                           
            CuringCATGENerfPath = linesplit[2]            

ret=VExpMngr.LoadFile( VdbDistortionFilePath, 0 )
ret=VE.ModelChange( "M  @0" )

#__________________ SimulationControl BEGIN __________________
var4=VCmd.Activate( 1, r"VCompUtils.VCompUtilsCmdInterface", r"SimulationControl" )
VCmd.SetObjectValue( var4, r"CurrentModel", "M  @0" )
VCmd.SetStringValue( var4, r"ErfModel", CuringCATGENerfPath )
VCmd.SetStringValue( var4, r"FrequencyType", r"Every Step" )
VCmd.Accept( var4 )
VCmd.Accept( var4 )
VCmd.Quit( var4 )

#__________________ SimulationControl END __________________
VExpMngr.ExportFile( VdbDistortionFilePath, 0 )
# ret=VE.ModelDestroy( "M  @0" )
# VE.SetCurrentPage( 1 )
# VE.SetCurrentPage( 1 )
# VE.SetActiveWindow( r"p1w1" )
# VE.NewSession(  )
