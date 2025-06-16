# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 14:55:18 2023

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
#	Date				:  	Thu Mar 30 14:52:08 2023
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

print('100*_')
print('DISTORTION, Characterize Laminate. p35')
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
        if 'DistortionSolverFilePath' in line:
            linesplit = line.partition('= ')
            #Extract Variable name, value and IDnumber identificator                           
            DistortionSolverFilePath = linesplit[2]
        if 'DistortionSolverFolderPath' in line:
            linesplit = line.partition('= ')
            #Extract Variable name, value and IDnumber identificator                           
            DistortionSolverFolderPath = linesplit[2]    

print('solver path is : ', DistortionSolverFolderPath)

ret=VExpMngr.LoadFile( VdbDistortionFilePath, 0 )
ret=VE.ModelChange( "M  @0" )

#__________________ SolverManager BEGIN __________________
var13=VCmd.Activate( 1, r"VRTMUtilities.VRTMInterface", r"SolverManager" )
VCmd.SetGuStringValue( var13, r"SolverPath", DistortionSolverFolderPath )
VCmd.Quit( var13 )
#__________________ CompositeLayerDesignManager BEGIN __________________
var10=VCmd.Activate( 1, r"VCompUtils.VCompUtilsCmdInterface", r"CompositeLayerDesignManager" )
VCmd.SetGuStringValue( var10, r"LayerLaminateListFlag", r"LayerList" )
VCmd.SetGuStringValue( var10, r"PlyReinforcementLaminate", r"Ply" )
VCmd.SetStringValue( var10, r"MatDBFilter", r"User" )
VCmd.SetStringValue( var10, r"MatTypeFilter", r"Ply" )
VCmd.SetStringValue( var10, r"MatDBFilter", r"User" )
VCmd.SetStringValue( var10, r"MatTypeFilter", r"Ply" )
VCmd.SetStringValue( var10, r"MatNameFilter", r"L_PLY" )
VCmd.SetIntValue( var10, r"SameMatAssignmentOtherLayerFlag", 7 )
VCmd.SetGuStringValue( var10, r"SameMatAssignmentOtherLayer", r"True" )
ret=VCmd.ExecuteCommand( var10, r"TransferMaterialToInterfaceList" )
VCmd.Accept( var10 )
VCmd.Quit( var10 )
var5=VCmd.Activate( 1, r"VMaterial.VMaterialInterface", r"GenericMaterialEditor" )
VCmd.SetStringValue( var5, r"SelectDb", r"User" )
ret=VCmd.ExecuteCommand( var5, r"ClearSearchPtr" )
VCmd.SetStringValue( var5, r"ActiveCategoryTab", r"General" )
VCmd.SetStringValue( var5, r"ActiveCategoryTab", r"General" )
VCmd.SetStringValue( var5, r"SelectDb", r"Model" )
ret=VCmd.ExecuteCommand( var5, r"ClearSearchPtr" )
VCmd.SetStringValue( var5, r"ActiveCategoryTab", r"General" )
VCmd.SetStringValue( var5, r"ActiveFolderClassID", r"Resin" )
VCmd.SetStringValue( var5, r"FolderPath", r"Resin" )
VCmd.SetStringValue( var5, r"ActiveClass", r"Resin" )
VCmd.SetStringValue( var5, r"ActiveCategoryTab", r"General" )
VCmd.SetStringValue( var5, r"ActiveFolderClassID", r"Reinforcement" )
VCmd.SetStringValue( var5, r"FolderPath", r"Reinforcement" )
VCmd.SetStringValue( var5, r"ActiveClass", r"Reinforcement" )
VCmd.SetStringValue( var5, r"ActiveCategoryTab", r"General" )
VCmd.SetStringValue( var5, r"ActiveFolderClassID", r"Resin" )
VCmd.SetStringValue( var5, r"FolderPath", r"Resin" )
VCmd.SetStringValue( var5, r"ActiveClass", r"Resin" )
VCmd.SetStringValue( var5, r"ActiveCategoryTab", r"General" )
VCmd.SetStringValue( var5, r"ActiveFolderClassID", r"Reinforcement" )
VCmd.SetStringValue( var5, r"FolderPath", r"Reinforcement" )
VCmd.SetStringValue( var5, r"ActiveClass", r"Reinforcement" )
VCmd.SetStringValue( var5, r"ActiveCategoryTab", r"General" )
VCmd.SetStringValue( var5, r"SelectDb", r"User" )
ret=VCmd.ExecuteCommand( var5, r"ClearSearchPtr" )
VCmd.SetStringValue( var5, r"ActiveCategoryTab", r"General" )
VCmd.SetStringValue( var5, r"Filter", r"All" )
VCmd.SetStringValue( var5, r"FolderPath", r"All" )
VCmd.SetStringValue( var5, r"ActiveMaterial", '' )
VCmd.SetStringValue( var5, r"ActiveCategoryTab", r"General" )
VCmd.SetStringValue( var5, r"ActiveFolderClassID", r"Ply" )
VCmd.SetStringValue( var5, r"FolderPath", r"Ply" )
VCmd.SetStringValue( var5, r"ActiveClass", r"Ply" )
VCmd.SetStringValue( var5, r"ActiveMaterial", r"Ply_New_1" )
VCmd.SetStringValue( var5, r"ActiveCategoryTab", r"General" )
VCmd.SetStringValue( var5, r"RecentMaterialList", r"User/Ply_New_1" )
VCmd.SetStringValue( var5, r"ActiveProperty", r"Compute properties..." )
VCmd.SetStringValue( var5, r"ActiveModelID", r"LaminaCharacterizationMacro" )
ret=VCmd.ExecuteCommand( var5, r"UpdateComputeCb" )
ret=VCmd.ExecuteCommand( var5, r"ExecuteCompute" )
VCmd.Quit( var5 )

#__________________ GenericMaterialEditor BEGIN __________________
var4=VCmd.Activate( 1, r"VMaterial.VMaterialInterface", r"GenericMaterialEditor" )
VCmd.SetStringValue( var4, r"SelectDb", r"Model" )
VCmd.SetStringValue( var4, r"ActiveCategoryTab", r"General" )
#__________________ CompositeLayerDesignManager BEGIN __________________
var5=VCmd.Activate( 1, r"VCompUtils.VCompUtilsCmdInterface", r"CompositeLayerDesignManager" )
VCmd.SetStringValue( var5, r"MatDBFilter", r"User" )
VCmd.SetStringValue( var5, r"MatTypeFilter", r"Ply" )
VCmd.SetStringValue( var5, r"MatDBFilter", r"User" )
VCmd.SetStringValue( var5, r"MatTypeFilter", r"Ply" )
VCmd.SetStringValue( var5, r"MatNameFilter", r"Ply_New_1" )
VCmd.SetGuStringValue( var5, r"LayerLaminateListFlag", r"LayerList" )
VCmd.SetGuStringValue( var5, r"PlyReinforcementLaminate", r"Ply" )
VCmd.SetStringValue( var5, r"MatDBFilter", r"User" )
VCmd.SetStringValue( var5, r"MatTypeFilter", r"Ply" )
VCmd.SetStringValue( var5, r"MatDBFilter", r"User" )
VCmd.SetStringValue( var5, r"MatTypeFilter", r"Ply" )
VCmd.SetStringValue( var5, r"MatNameFilter", r"Ply_New_1" )
VCmd.SetIntValue( var5, r"SameMatAssignmentOtherLayerFlag", 7 )
VCmd.SetGuStringValue( var5, r"SameMatAssignmentOtherLayer", r"True" )
ret=VCmd.ExecuteCommand( var5, r"TransferMaterialToInterfaceList" )
VCmd.Accept( var5 )
VCmd.Quit( var5 )

#__________________ CompositeLayerDesignManager END __________________
VExpMngr.ExportFile( VdbDistortionFilePath, 0 )
VExpMngr.ExportFile( r'/nishome/smo/CAELESTIS/2024_RTMDIST_test/Results/line_1/zzLaminate.vdb', 0 )
# ret=VE.ModelDestroy( "M  @0" )
# VE.SetCurrentPage( 1 )
# VE.SetCurrentPage( 1 )
# VE.SetActiveWindow( r"p1w1" )
# VE.NewSession(  )
