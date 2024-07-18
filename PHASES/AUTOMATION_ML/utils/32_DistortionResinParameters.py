# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 14:25:28 2023

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
#	Date				:  	Thu Mar 30 14:04:06 2023
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
print('DISTORTION, resin parameters. p32')
print('Reading list of variables')

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
        if 'VdbDistortionFilePath' in line:
            linesplit = line.partition('= ')
            #Extract Variable name, value and IDnumber identificator                           
            VdbDistortionFilePath = linesplit[2]
            

ret=VExpMngr.LoadFile( VdbDistortionFilePath, 0 )
ret=VE.ModelChange( "M  @0" )
#__________________ GenericMaterialEditor BEGIN __________________
var4=VCmd.Activate( 1, r"VMaterial.VMaterialInterface", r"GenericMaterialEditor" )
ret=VCmd.ExecuteCommand( var4, r"MaterialNamingSystem" )
VCmd.SetStringValue( var4, r"ActiveDomain", r"Visual Distortion" )
VCmd.SetStringValue( var4, r"SelectDb", r"Public" )
ret=VCmd.ExecuteCommand( var4, r"ClearSearchPtr" )
VCmd.SetStringValue( var4, r"ActiveCategoryTab", r"General" )
VCmd.SetStringValue( var4, r"SelectDb", r"User" )
ret=VCmd.ExecuteCommand( var4, r"ClearSearchPtr" )
VCmd.SetStringValue( var4, r"ActiveCategoryTab", r"General" )
VCmd.SetStringValue( var4, r"ActiveFolderClassID", r"Reinforcement" )
VCmd.SetStringValue( var4, r"FolderPath", r"Reinforcement" )
VCmd.SetStringValue( var4, r"ActiveClass", r"Reinforcement" )
VCmd.SetStringValue( var4, r"ActiveMaterial", r"RTM_DIST" )
VCmd.SetStringValue( var4, r"ActiveCategoryTab", r"General" )
VCmd.SetStringValue( var4, r"RecentMaterialList", r"User/RTM_DIST" )
VCmd.SetStringValue( var4, r"ActiveFolderClassID", r"Resin" )
VCmd.SetStringValue( var4, r"FolderPath", r"Resin" )
VCmd.SetStringValue( var4, r"ActiveClass", r"Resin" )
VCmd.SetStringValue( var4, r"ActiveMaterial", r"L_RTM" )
VCmd.SetStringValue( var4, r"ActiveCategoryTab", r"General" )
VCmd.SetStringValue( var4, r"RecentMaterialList", r"User/L_RTM" )
VCmd.SetStringValue( var4, r"ActiveCategoryTab", r"Glassy" )
VCmd.SetStringValue( var4, r"ActiveProperty", r"ResinGlassyTensileYoungsModulus" )
VCmd.SetStringValue( var4, r"ActiveModelID", r"composite_resin_glassy" )
VCmd.SetStringValue( var4, r"PropertyValueUnit", r"Pa" )
ret=VCmd.ExecuteCommand( var4, r"UpdateParamForUnit" )
VCmd.SetStringValue( var4, r"PropertySValue", r"            4.24" )
VCmd.SetStringValue( var4, r"ActiveProperty", r"ResinGlassyTensileYoungsModulus" )
VCmd.SetStringValue( var4, r"ActiveModelID", r"composite_resin_glassy" )
VCmd.SetStringValue( var4, r"PropertyValueUnit", r"GPa" )
ret=VCmd.ExecuteCommand( var4, r"UpdateParamForUnit" )
VCmd.SetStringValue( var4, r"ActiveProperty", r"ResinGlassyTensileYoungsModulus" )
VCmd.SetStringValue( var4, r"ActiveModelID", r"composite_resin_glassy" )
VCmd.SetStringValue( var4, r"ActiveProperty", r"ResinGlassyTensileYoungsModulus" )
VCmd.SetStringValue( var4, r"ActiveModelID", r"composite_resin_glassy" )
VCmd.SetStringValue( var4, r"PropertyValueUnit", r"GPa" )
ret=VCmd.ExecuteCommand( var4, r"UpdateParamForUnit" )
VCmd.SetStringValue( var4, r"PropertySValue", r"            4.24" )
VCmd.SetStringValue( var4, r"ActiveProperty", r"ResinGlassyPoissonsRatio" )
VCmd.SetStringValue( var4, r"ActiveModelID", r"composite_resin_glassy" )
VCmd.SetStringValue( var4, r"PropertySValue", r"           0.365" )
VCmd.SetStringValue( var4, r"ActiveProperty", r"ResinGlassyShearModulus" )
VCmd.SetStringValue( var4, r"ActiveModelID", r"composite_resin_glassy" )
VCmd.SetStringValue( var4, r"PropertyValueUnit", r"GPa" )
ret=VCmd.ExecuteCommand( var4, r"UpdateParamForUnit" )
VCmd.SetStringValue( var4, r"ActiveProperty", r"ResinGlassyShearModulus" )
VCmd.SetStringValue( var4, r"ActiveModelID", r"composite_resin_glassy" )
VCmd.SetStringValue( var4, r"ActiveProperty", r"ResinGlassyShearModulus" )
VCmd.SetStringValue( var4, r"ActiveModelID", r"composite_resin_glassy" )
VCmd.SetStringValue( var4, r"PropertyValueUnit", r"GPa" )
ret=VCmd.ExecuteCommand( var4, r"UpdateParamForUnit" )
VCmd.SetStringValue( var4, r"PropertySValue", r"            1.55" )
VCmd.SetStringValue( var4, r"ActiveProperty", r"ResinGlassyCoefThermalExpansion" )
VCmd.SetStringValue( var4, r"ActiveModelID", r"composite_resin_glassy" )
VCmd.SetStringValue( var4, r"PropertyValueUnit", r"1/K" )
ret=VCmd.ExecuteCommand( var4, r"UpdateParamForUnit" )
VCmd.SetStringValue( var4, r"PropertySValue", r"         4.4e-05" )
VCmd.SetStringValue( var4, r"ActiveProperty", r"AutoComputeRubberyProperties" )
VCmd.SetStringValue( var4, r"ActiveModelID", r"composite_resin_glassy" )
VCmd.SetStringValue( var4, r"PropertySValue", r"true" )
VCmd.SetStringValue( var4, r"ActiveProperty", r"GlassyChemicalShrinkage" )
VCmd.SetStringValue( var4, r"ActiveModelID", r"composite_resin_glassy" )
VCmd.SetStringValue( var4, r"PropertySValue", r"          -0.018" )
VCmd.SetStringValue( var4, r"ActiveCategoryTab", r"Rubbery" )
VCmd.SetStringValue( var4, r"ActiveProperty", r"RubberyChemicalShrinkage" )
VCmd.SetStringValue( var4, r"ActiveModelID", r"composite_resin_rubbery" )
VCmd.SetStringValue( var4, r"PropertySValue", r"          -0.018" )
VCmd.SetStringValue( var4, r"ActiveCategoryTab", r"Chemical" )
VCmd.SetStringValue( var4, r"ActiveProperty", r"ResinChemicalDegreeofcureatgelation" )
VCmd.SetStringValue( var4, r"ActiveModelID", r"composite_resin_chemical" )
VCmd.SetStringValue( var4, r"PropertySValue", r"             0.6" )
VCmd.SetStringValue( var4, r"ActiveProperty", r"Resin_Tg0" )
VCmd.SetStringValue( var4, r"ActiveModelID", r"composite_resin_chemical" )
VCmd.SetStringValue( var4, r"PropertyValueUnit", r"K" )
ret=VCmd.ExecuteCommand( var4, r"UpdateParamForUnit" )
VCmd.SetStringValue( var4, r"PropertySValue", r"             -11" )
VCmd.SetStringValue( var4, r"ActiveProperty", r"Resin_Tg0" )
VCmd.SetStringValue( var4, r"ActiveModelID", r"composite_resin_chemical" )
VCmd.SetStringValue( var4, r"PropertyValueUnit", r"C" )
ret=VCmd.ExecuteCommand( var4, r"UpdateParamForUnit" )
VCmd.SetStringValue( var4, r"ActiveProperty", r"Resin_Tg0" )
VCmd.SetStringValue( var4, r"ActiveModelID", r"composite_resin_chemical" )
VCmd.SetStringValue( var4, r"ActiveProperty", r"Resin_Tg0" )
VCmd.SetStringValue( var4, r"ActiveModelID", r"composite_resin_chemical" )
VCmd.SetStringValue( var4, r"PropertyValueUnit", r"C" )
ret=VCmd.ExecuteCommand( var4, r"UpdateParamForUnit" )
VCmd.SetStringValue( var4, r"PropertySValue", r"             -11" )
VCmd.SetStringValue( var4, r"ActiveProperty", r"Resin_Lambda" )
VCmd.SetStringValue( var4, r"ActiveModelID", r"composite_resin_chemical" )
VCmd.SetStringValue( var4, r"PropertySValue", r"             206" )
VCmd.SetStringValue( var4, r"ActiveProperty", r"Resin_Tginf" )
VCmd.SetStringValue( var4, r"ActiveModelID", r"composite_resin_chemical" )
VCmd.SetStringValue( var4, r"PropertyValueUnit", r"C" )
ret=VCmd.ExecuteCommand( var4, r"UpdateParamForUnit" )
VCmd.SetStringValue( var4, r"ActiveProperty", r"Resin_Tginf" )
VCmd.SetStringValue( var4, r"ActiveModelID", r"composite_resin_chemical" )
VCmd.SetStringValue( var4, r"ActiveProperty", r"Resin_Tginf" )
VCmd.SetStringValue( var4, r"ActiveModelID", r"composite_resin_chemical" )
VCmd.SetStringValue( var4, r"PropertyValueUnit", r"C" )
ret=VCmd.ExecuteCommand( var4, r"UpdateParamForUnit" )
VCmd.SetStringValue( var4, r"PropertySValue", r"             206" )
VCmd.SetStringValue( var4, r"ActiveProperty", r"Resin_Lambda" )
VCmd.SetStringValue( var4, r"ActiveModelID", r"composite_resin_chemical" )
VCmd.SetStringValue( var4, r"PropertySValue", r"            0.44" )
ret=VCmd.ExecuteCommand( var4, r"Save" )
VCmd.Accept( var4 )
VCmd.Quit( var4 )

VExpMngr.ExportFile( VdbDistortionFilePath, 0 )

#__________________ GenericMaterialEditor END __________________
incfile= open(VariablesList,"r")
if incfile.mode == 'r':
    inclines = incfile.read().splitlines()
    incfile.close()
    for line in inclines:
        line_no += 1
        if 'Shrinkage' in line:
            print('shrinkage is in line')
            linesplit = line.partition('= ')
            #Extract Variable name, value and IDnumber identificator                           
            Shrinkage = linesplit[2]
            
            #__________________ GenericMaterialEditor BEGIN __________________
            var4=VCmd.Activate( 1, r"VMaterial.VMaterialInterface", r"GenericMaterialEditor" )
            VCmd.SetStringValue( var4, r"SelectDb", r"Model" )
            VCmd.SetStringValue( var4, r"ActiveCategoryTab", r"General" )
            VCmd.SetStringValue( var4, r"SelectDb", r"User" )
            ret=VCmd.ExecuteCommand( var4, r"ClearSearchPtr" )
            VCmd.SetStringValue( var4, r"ActiveCategoryTab", r"General" )
            VCmd.SetStringValue( var4, r"ActiveFolderClassID", r"Resin" )
            VCmd.SetStringValue( var4, r"FolderPath", r"Resin" )
            VCmd.SetStringValue( var4, r"ActiveClass", r"Resin" )
            VCmd.SetStringValue( var4, r"ActiveMaterial", r"L_RTM" )
            VCmd.SetStringValue( var4, r"ActiveCategoryTab", r"General" )
            VCmd.SetStringValue( var4, r"RecentMaterialList", r"User/L_RTM" )
            VCmd.SetStringValue( var4, r"ActiveCategoryTab", r"Glassy" )
            VCmd.SetStringValue( var4, r"ActiveProperty", r"GlassyChemicalShrinkage" )
            VCmd.SetStringValue( var4, r"ActiveModelID", r"composite_resin_glassy" )
            VCmd.SetStringValue( var4, r"PropertySValue", str(Shrinkage) )
            VCmd.SetStringValue( var4, r"ActiveCategoryTab", r"Rubbery" )
            VCmd.SetStringValue( var4, r"ActiveProperty", r"RubberyChemicalShrinkage" )
            VCmd.SetStringValue( var4, r"ActiveModelID", r"composite_resin_rubbery" )
            VCmd.SetStringValue( var4, r"PropertySValue", str(Shrinkage) )
            ret=VCmd.ExecuteCommand( var4, r"Save" )
            VCmd.Accept( var4 )
            VCmd.Quit( var4 )

VExpMngr.ExportFile( VdbDistortionFilePath, 0 )
VExpMngr.ExportFile( r'/nishome/smo/CAELESTIS/2024_RTMDIST_test/Results/line_1/zzResin.vdb', 0 )
# VE.DeleteWindow(  )
# VE.SetCurrentPage( 1 )
# VE.SetCurrentPage( 1 )
# VE.SetActiveWindow( r"p1w1" )
# VE.NewSession(  )
