#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#-------------------------------------------------------------------------------
#                          Session File
#                           ESI Group
#                      https://www.esi-group.com
#        Copyright (C) ESI Group 2022.  All rights reserved.
#-------------------------------------------------------------------------------
#	Product				:  	Visual-Environment 18.5
#	Date				:  	Fri Apr  7 10:28:05 2023
#-------------------------------------------------------------------------------
import os

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

print('100*_')
print('DISTORTION, Run data cast. p38')
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
            VdbDistortionFilePath = linesplit[2]
        if 'DistortionSolverFolderPath' in line:
            linesplit = line.partition('= ')
            DistortionSolverFolderPath = linesplit[2]            
        if 'outputs_files_folder' in line:
            linesplit = line.partition('= ')
            new_working_directory = linesplit[2]           

ret=VExpMngr.LoadFile( VdbDistortionFilePath, 0 )
ret=VE.ModelChange( "M  @0" )

#__________________ SolverManager BEGIN __________________
var4=VCmd.Activate( 1, r"VRTMUtilities.VRTMInterface", r"SolverManager" )
VCmd.SetGuStringValue( var4, r"WorkingDir", new_working_directory )
ret=VCmd.ExecuteCommand( var4, r"RunDataCAST" )
VCmd.Quit( var4 )
#__________________ SolverManager BEGIN __________________
# var4=VCmd.Activate( 1, r"VRTMUtilities.VRTMInterface", r"SolverManager" )
# VCmd.SetGuStringValue( var4, r"SolverPath", DistortionSolverFolderPath )
# VCmd.SetIntValue( var4, r"NumProcesrs", 1 )
# ret=VCmd.ExecuteCommand( var4, r"RUN" )
# ret=VE.ModelDestroy( "M  @0" )
# VE.SetCurrentPage( 1 )
# VE.SetCurrentPage( 1 )
# VE.SetActiveWindow( r"p1w1" )
# VE.NewSession(  )