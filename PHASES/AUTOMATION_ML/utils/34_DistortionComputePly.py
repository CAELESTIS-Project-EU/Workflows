# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 14:39:50 2023

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
#	Date				:  	Thu Mar 30 14:34:45 2023
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

print(100*'_')
print('DISTORTION, Ply. p34')
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
            
ret=VExpMngr.LoadFile( VdbDistortionFilePath, 0 )
ret=VE.ModelChange( "M  @0" )

#__________________ SolverManager BEGIN __________________
var8=VCmd.Activate( 1, r"VRTMUtilities.VRTMInterface", r"SolverManager" )
VCmd.SetGuStringValue( var8, r"SolverPath", DistortionSolverFolderPath )
VCmd.Quit( var8 )

# #__________________ GenericMaterialEditor BEGIN __________________
# var4=VCmd.Activate( 1, r"VMaterial.VMaterialInterface", r"GenericMaterialEditor" )
# ret=VCmd.ExecuteCommand( var4, r"MaterialNamingSystem" )
# VCmd.SetStringValue( var4, r"ActiveDomain", r"Visual Distortion" )
# VCmd.SetStringValue( var4, r"SelectDb", r"Public" )
# ret=VCmd.ExecuteCommand( var4, r"ClearSearchPtr" )
# VCmd.SetStringValue( var4, r"ActiveCategoryTab", r"General" )
# VCmd.SetStringValue( var4, r"ActiveCategoryTab", r"General" )
# VCmd.SetObjectValue( var4, r"CurrentModularMaterial", "PLY  2" )
# VCmd.SetStringValue( var4, r"SelectDb", r"User" )
# VCmd.SetStringValue( var4, r"ActiveCategoryTab", r"General" )
# VCmd.SetStringValue( var4, r"Filter", r"Ply" )
# VCmd.SetStringValue( var4, r"ActiveMaterial", r"L_PLY" )
# VCmd.SetStringValue( var4, r"ActiveFolderClassID", r"Ply" )
# VCmd.SetStringValue( var4, r"FolderPath", r"Ply" )
# VCmd.SetStringValue( var4, r"ActiveClass", r"Ply" )
# VCmd.SetStringValue( var4, r"ActiveMaterial", r"L_PLY" )
# VCmd.SetStringValue( var4, r"ActiveCategoryTab", r"General" )
# VCmd.SetStringValue( var4, r"ActiveFolderClassID", r"Ply" )
# VCmd.SetStringValue( var4, r"FolderPath", r"Ply" )
# VCmd.SetStringValue( var4, r"ActiveClass", r"Ply" )
# VCmd.SetStringValue( var4, r"ActiveMaterial", r"L_PLY" )
# VCmd.SetStringValue( var4, r"ActiveCategoryTab", r"General" )
# VCmd.SetStringValue( var4, r"RecentMaterialList", r"User/L_PLY" )
# VCmd.SetStringValue( var4, r"ActiveProperty", r"Density" )
# VCmd.SetStringValue( var4, r"ActiveModelID", r"Distortion_General" )
# VCmd.SetStringValue( var4, r"PropertyValueUnit", r"kg/m^3" )
# ret=VCmd.ExecuteCommand( var4, r"UpdateParamForUnit" )
# VCmd.SetStringValue( var4, r"PropertySValue", r"            1100" )
# VCmd.SetStringValue( var4, r"ActiveProperty", r"DatabaseName" )
# VCmd.SetStringValue( var4, r"ActiveModelID", r"Distortion_rein_fiber_reference" )
# VCmd.SetStringValue( var4, r"ActiveProperty", r"rein_resin_selection" )
# VCmd.SetStringValue( var4, r"PropertySValue", r"L_RTM" )
# VCmd.SetStringValue( var4, r"ActiveProperty", r"rein_fiber_selection" )
# VCmd.SetStringValue( var4, r"PropertySValue", r"L_FIBER" )
# VCmd.SetStringValue( var4, r"ActiveProperty", r"Distorotion_Fiber_Content" )
# VCmd.SetStringValue( var4, r"ActiveModelID", r"Distortion_rein_fiber_reference" )
# VCmd.SetStringValue( var4, r"PropertySValue", r"           0.664" )
# VCmd.SetStringValue( var4, r"ActiveProperty", r"Compute properties..." )
# VCmd.SetStringValue( var4, r"ActiveModelID", r"LaminaCharacterizationMacro" )
# VCmd.Quit( var4 )
# #__________________ GenericMaterialEditor END __________________
#__________________ SolverManager BEGIN __________________
# var4=VCmd.Activate( 1, r"VRTMUtilities.VRTMInterface", r"SolverManager" )
# VCmd.SetGuStringValue( var4, r"SolverPath", DistortionSolverFolderPath )
# VCmd.Quit( var4 )
#__________________ SolverManager END __________________
#__________________ GenericMaterialEditor BEGIN __________________
# var5=VCmd.Activate( 1, r"VMaterial.VMaterialInterface", r"GenericMaterialEditor" )
# VCmd.SetStringValue( var5, r"SelectDb", r"Model" )
# VCmd.SetStringValue( var5, r"ActiveCategoryTab", r"General" )
# VCmd.SetObjectValue( var5, r"CurrentModularMaterial", "PLY  2" )
# VCmd.SetStringValue( var5, r"SelectDb", r"User" )
# VCmd.SetStringValue( var5, r"ActiveCategoryTab", r"General" )
# VCmd.SetStringValue( var5, r"Filter", r"Ply" )
# VCmd.SetStringValue( var5, r"ActiveMaterial", r"L_PLY" )
# VCmd.SetStringValue( var5, r"ActiveFolderClassID", r"Ply" )
# VCmd.SetStringValue( var5, r"FolderPath", r"Ply" )
# VCmd.SetStringValue( var5, r"ActiveClass", r"Ply" )
# VCmd.SetStringValue( var5, r"ActiveMaterial", r"L_PLY" )
# VCmd.SetStringValue( var5, r"ActiveCategoryTab", r"General" )
# VCmd.SetStringValue( var5, r"ActiveProperty", r"Compute properties..." )
# VCmd.SetStringValue( var5, r"ActiveModelID", r"LaminaCharacterizationMacro" )
# ret=VCmd.ExecuteCommand( var5, r"UpdateComputeCb" )
# ret=VCmd.ExecuteCommand( var5, r"ExecuteCompute" )
# VCmd.Quit( var5 )
#__________________ GenericMaterialEditor END __________________
#__________________ GenericMaterialEditor BEGIN __________________
# var5=VCmd.Activate( 1, r"VMaterial.VMaterialInterface", r"GenericMaterialEditor" )
# VCmd.SetStringValue( var5, r"SelectDb", r"Model" )
# VCmd.SetStringValue( var5, r"ActiveCategoryTab", r"General" )
# #__________________ GenericMaterialEditor BEGIN __________________
# var6=VCmd.Activate( 1, r"VMaterial.VMaterialInterface", r"GenericMaterialEditor" )
# VCmd.SetStringValue( var6, r"SelectDb", r"User" )
# ret=VCmd.ExecuteCommand( var6, r"ClearSearchPtr" )
# VCmd.SetStringValue( var6, r"ActiveCategoryTab", r"General" )
# VCmd.SetStringValue( var6, r"Filter", r"All" )
# VCmd.SetStringValue( var6, r"FolderPath", r"All" )
# VCmd.SetStringValue( var6, r"ActiveMaterial", '' )
# VCmd.SetStringValue( var6, r"ActiveCategoryTab", r"General" )
# VCmd.SetStringValue( var6, r"ActiveFolderClassID", r"Ply" )
# VCmd.SetStringValue( var6, r"FolderPath", r"Ply" )
# VCmd.SetStringValue( var6, r"ActiveClass", r"Ply" )
# VCmd.SetStringValue( var6, r"ActiveMaterial", r"Ply_New_1" )
# VCmd.SetStringValue( var6, r"ActiveCategoryTab", r"General" )
# VCmd.SetStringValue( var6, r"RecentMaterialList", r"User/Ply_New_1" )
# VCmd.SetStringValue( var6, r"ActiveProperty", r"Compute properties..." )
# VCmd.SetStringValue( var6, r"ActiveModelID", r"LaminaCharacterizationMacro" )
# ret=VCmd.ExecuteCommand( var6, r"UpdateComputeCb" )
# ret=VCmd.ExecuteCommand( var6, r"ExecuteCompute" )
# VCmd.Quit( var6 )
print('First caracterization')
print('First caracterization')
print('First caracterization')
# #__________________ GenericMaterialEditor BEGIN __________________
# var6=VCmd.Activate( 1, r"VMaterial.VMaterialInterface", r"GenericMaterialEditor" )
# VCmd.SetStringValue( var6, r"SelectDb", r"User" )
# ret=VCmd.ExecuteCommand( var6, r"ClearSearchPtr" )
# VCmd.SetStringValue( var6, r"ActiveCategoryTab", r"General" )
# VCmd.SetStringValue( var6, r"Filter", r"All" )
# VCmd.SetStringValue( var6, r"FolderPath", r"All" )
# VCmd.SetStringValue( var6, r"ActiveMaterial", '' )
# VCmd.SetStringValue( var6, r"ActiveCategoryTab", r"General" )
# VCmd.SetStringValue( var6, r"ActiveFolderClassID", r"Ply" )
# VCmd.SetStringValue( var6, r"FolderPath", r"Ply" )
# VCmd.SetStringValue( var6, r"ActiveClass", r"Ply" )
# VCmd.SetStringValue( var6, r"ActiveMaterial", r"Ply_New_1" )
# VCmd.SetStringValue( var6, r"ActiveCategoryTab", r"General" )
# VCmd.SetStringValue( var6, r"RecentMaterialList", r"User/Ply_New_1" )
# VCmd.SetStringValue( var6, r"ActiveProperty", r"Compute properties..." )
# VCmd.SetStringValue( var6, r"ActiveModelID", r"LaminaCharacterizationMacro" )
# ret=VCmd.ExecuteCommand( var6, r"UpdateComputeCb" )
# ret=VCmd.ExecuteCommand( var6, r"ExecuteCompute" )
# VCmd.Quit( var6 )

#__________________ GenericMaterialEditor BEGIN __________________
var4=VCmd.Activate( 1, r"VMaterial.VMaterialInterface", r"GenericMaterialEditor" )
VCmd.SetStringValue( var4, r"SelectDb", r"Model" )
VCmd.SetStringValue( var4, r"ActiveCategoryTab", r"General" )
VCmd.SetStringValue( var4, r"Filter", r"All" )
VCmd.SetStringValue( var4, r"FolderPath", r"All" )
VCmd.SetStringValue( var4, r"ActiveMaterial", '' )
VCmd.SetStringValue( var4, r"ActiveCategoryTab", r"General" )
VCmd.SetStringValue( var4, r"SelectDb", r"Public" )
ret=VCmd.ExecuteCommand( var4, r"ClearSearchPtr" )
VCmd.SetStringValue( var4, r"ActiveCategoryTab", r"General" )
VCmd.SetStringValue( var4, r"SelectDb", r"User" )
ret=VCmd.ExecuteCommand( var4, r"ClearSearchPtr" )
VCmd.SetStringValue( var4, r"ActiveCategoryTab", r"General" )
VCmd.SetStringValue( var4, r"ActiveFolderClassID", r"Ply" )
VCmd.SetStringValue( var4, r"FolderPath", r"Ply" )
VCmd.SetStringValue( var4, r"ActiveClass", r"Ply" )
VCmd.SetStringValue( var4, r"ActiveMaterial", r"Ply_New_1" )
VCmd.SetStringValue( var4, r"ActiveCategoryTab", r"General" )
VCmd.SetStringValue( var4, r"RecentMaterialList", r"User/Ply_New_1" )
VCmd.SetStringValue( var4, r"ActiveProperty", r"rein_resin_selection" )
VCmd.SetStringValue( var4, r"PropertySValue", r"L_RTM" )
VCmd.SetStringValue( var4, r"ActiveProperty", r"rein_fiber_selection" )
VCmd.SetStringValue( var4, r"PropertySValue", r"L_FIBER" )
VCmd.SetStringValue( var4, r"ActiveProperty", r"Distorotion_Fiber_Content" )
VCmd.SetStringValue( var4, r"ActiveModelID", r"Distortion_rein_fiber_reference" )
VCmd.SetStringValue( var4, r"PropertySValue", r"             0.5" )
VCmd.SetStringValue( var4, r"ActiveProperty", r"Compute properties..." )
VCmd.SetStringValue( var4, r"ActiveModelID", r"LaminaCharacterizationMacro" )
ret=VCmd.ExecuteCommand( var4, r"UpdateComputeCb" )
ret=VCmd.ExecuteCommand( var4, r"ExecuteCompute" )
VCmd.Quit( var4 )
#__________________ GenericMaterialEditor END __________________
#__________________ GenericMaterialEditor BEGIN __________________
var5=VCmd.Activate( 1, r"VMaterial.VMaterialInterface", r"GenericMaterialEditor" )
VCmd.SetStringValue( var5, r"SelectDb", r"Model" )
VCmd.SetStringValue( var5, r"ActiveCategoryTab", r"General" )
VCmd.Quit( var5 )

print('First caracterization finished')

#__________________ GenericMaterialEditor END __________________
VExpMngr.ExportFile( VdbDistortionFilePath, 0 )
VExpMngr.ExportFile( r'/nishome/smo/CAELESTIS/2024_RTMDIST_test/Results/line_1/zzPly.vdb', 0 )
# ret=VE.ModelDestroy( "M  @0" )
# VE.SetCurrentPage( 1 )
# VE.SetCurrentPage( 1 )
# VE.SetActiveWindow( r"p1w1" )
# VE.NewSession(  )
