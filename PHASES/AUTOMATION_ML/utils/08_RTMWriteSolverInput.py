# -*- coding: utf-8 -*-
"""
Created on Fri Jan 20 12:30:07 2023

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
#	Date				:  	Fri Jan 20 12:10:21 2023
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
            VdbFilePath = linesplit[2]
        if 'outputs_files_folder' in line:
            linesplit = line.partition('= ')
            new_working_directory = linesplit[2]
            
ret=VExpMngr.LoadFile(VdbFilePath,0)
ret=VE.ModelChange( "M  @0" )
#__________________ SolverManager BEGIN __________________
var4=VCmd.Activate( 1, r"VRTMUtilities.VRTMInterface", r"SolverManager" )
VCmd.SetGuStringValue( var4, r"WorkingDir", new_working_directory )
ret=VCmd.ExecuteCommand( var4, r"RunDataCAST" )
VCmd.Quit( var4 )
#__________________ SolverManager END __________________
# ret=VE.ModelDestroy( "M  @0" )
# VE.SetCurrentPage( 1 )
# VE.SetCurrentPage( 1 )
# VE.SetActiveWindow( r"p1w1" )
# VE.NewSession(  )
