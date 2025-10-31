# -*- coding: utf-8 -*-
"""
Created on Thu Feb  2 14:06:07 2023

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
#	Date				:  	Thu Feb  2 13:52:43 2023
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
import os

print(100*'-')
print('Curing mapping temp from filling 22')

ret=VE.ChangeContext( r"Visual-RTM" )
VE.SetActiveWindow( r"p1w1" )
VE.SetCurrentPage( 1 )
VExpMngr.SetFilesOfType( r"All" )

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
        if 'VdbCuringFilePath' in line:
            linesplit = line.partition('= ')
            #Extract Variable name, value and IDnumber identificator                           
            VdbFilePath = linesplit[2]
        if 'RTMunfFilePath' in line:
            linesplit = line.partition('= ')
            #Extract Variable name, value and IDnumber identificator                           
            L_RTMgUnfFile = linesplit[2]


ret=VExpMngr.LoadFile(VdbFilePath,0)
ret=VE.ModelChange( "M  @0" )
#__________________ Extract BEGIN __________________
var4=VCmd.Activate( 1, r"VCastUtilities.VCastInterface", r"Extract" )
VCmd.SetStringValue( var4, r"ExtractMethod", r"Extract" )
VCmd.SetStringValue( var4, r"StepType", r"Step" )
lst1_count,lst1 =  VScn.List( "  P 10001:10004 "  )
VCmd.SetObjectArrayValue( var4, r"Parts", lst1_count, lst1 )
VCmd.SetStringValue( var4, r"ResultFile", L_RTMgUnfFile )
VCmd.SetStringValue( var4, r"ExtractMethod", r"Mapping" )
VCmd.SetStringValue( var4, r"StepType", r"Step" )
VCmd.SetStringValue( var4, r"StepType", r"Step" )
VCmd.SetIntValue( var4, r"Step", 451 )
ret=VCmd.ExecuteCommand( var4, r"Mapping" )
VCmd.Accept( var4 )
VCmd.Quit( var4 )
#__________________ Extract END __________________
VExpMngr.ExportFile( VdbFilePath, 0 )
ret=VE.ModelDestroy( "M  @0" )
VE.SetCurrentPage( 1 )
VE.SetActiveWindow( r"p1w1" )
VE.NewSession(  )

