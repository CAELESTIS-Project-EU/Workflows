# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 11:04:14 2024

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
#	Date				:  	Fri Feb 23 10:57:09 2024
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

import os
import json

#SMO: read macro directory from temporary file
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
        if 'VdbRTMFilePath' in line:
            linesplit = line.partition('= ')
            #Extract Variable name, value and IDnumber identificator                           
            VdbFilePath = linesplit[2]
            
ret=VExpMngr.LoadFile(VdbFilePath,0)
ret=VE.ModelChange( "M  @0" )
lst1_count,lst1 =  VScn.List( "  P 10001:10044 "  )
VCmd.SetObjectArrayValue( var1, r"ExplorerSelection", lst1_count, lst1 )
ret=VCmd.ExecuteCommand( var1, r"HideSelected" )
lst1_count,lst1 =  VScn.List( "  P 10001:10044 "  )
VCmd.SetObjectArrayValue( var1, r"ExplorerSelection", lst1_count, lst1 )
ret=VCmd.ExecuteCommand( var1, r"ShowSelected" )

for element in gaps:
    
    ###WRITE HERE
    #__________________ CompositeLayerDesignManager BEGIN __________________
    var17=VCmd.Activate( 1, r"VCompUtils.VCompUtilsCmdInterface", r"CompositeLayerDesignManager" )
    VCmd.SetGuStringValue( var17, r"LayerLaminateListFlag", r"LayerList" )
    VCmd.SetGuStringValue( var17, r"LayerLaminateListFlag", r"LayerList" )
    VCmd.SetIntValue( var17, r"SelectedRowForAssignment", 4 )
    lst1_count,lst1 =  VScn.StringList( r" 10005/PART_10005  "  )
    VCmd.SetStringArrayValue( var1, r"ListSelection", lst1_count, lst1 )
    VCmd.SetStringValue( var17, r"SelectedPartIds", r"10005" )
    ret=VCmd.ExecuteCommand( var17, r"TransferPartsToInterfaceList" )
    VCmd.SetGuStringValue( var17, r"LayerLaminateListFlag", r"LayerList" )
    VCmd.SetGuStringValue( var17, r"PlyReinforcementLaminate", r"Ply" )
    VCmd.SetGuStringValue( var17, r"PlyReinforcementLaminate", r"Ply" )
    VCmd.SetStringValue( var17, r"MatDBFilter", r"User" )
    VCmd.SetStringValue( var17, r"MatTypeFilter", r"Ply" )
    VCmd.SetStringValue( var17, r"MatNameFilter", r"Ply_New_2" )
    VCmd.SetIntValue( var17, r"SameMatAssignmentOtherLayerFlag", 7 )
    VCmd.SetGuStringValue( var17, r"SameMatAssignmentOtherLayer", r"False" )
    ret=VCmd.ExecuteCommand( var17, r"TransferMaterialToInterfaceList" )
    VCmd.SetGuStringValue( var17, r"LayerLaminateListFlag", r"LayerList" )
    VCmd.SetIntValue( var17, r"SelectedRowForAssignment", 3 )
    VCmd.SetGuStringValue( var17, r"LayerName", r"Layer_4" )
    VCmd.SetDoubleValue( var17, r"LayerThickness", 0.111122  )
    VCmd.SetGuStringValue( var17, r"LayerLaminateListFlag", r"LayerList" )
    VCmd.SetIntValue( var17, r"SelectedRowForAssignment", 4 )
    VCmd.SetGuStringValue( var17, r"LayerName", r"Layer_5" )
    VCmd.SetDoubleValue( var17, r"LayerThickness", 0.111122  )
    VCmd.SetGuStringValue( var17, r"LayerLaminateListFlag", r"LayerList" )
    VCmd.SetGuStringValue( var17, r"LayerName", r"Layer_5" )
    VCmd.SetDoubleValue( var17, r"LayerAngle", 0.  )
    VCmd.SetStringValue( var17, r"SelectedPartIds", r"10005" )
    ret=VCmd.ExecuteCommand( var17, r"TransferPartsToInterfaceList" )
    

VCmd.Accept( var17 )
VCmd.Quit( var17 )
