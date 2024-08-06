# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 14:31:21 2023

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
#	Date				:  	Thu Mar 30 14:28:02 2023
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
print('DISTORTION, fiber parameters. p33')
print('Reading list of variables')

#SMO: read macro directory from temporary file
Scriptsfolder = os.getcwd()
VariablesList = os.path.join(Scriptsfolder, 'VariablesList.txt')

print('setting fibers')

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
VCmd.SetStringValue( var4, r"ActiveFolderClassID", r"Fiber" )
VCmd.SetStringValue( var4, r"FolderPath", r"Fiber" )
VCmd.SetStringValue( var4, r"ActiveClass", r"Fiber" )
VCmd.SetStringValue( var4, r"ActiveCategoryTab", r"General" )
VCmd.SetStringValue( var4, r"ActiveClass", r"Fiber" )
VCmd.SetStringValue( var4, r"ActiveClass", r"Fiber" )
VCmd.SetStringValue( var4, r"ActiveFolderClassID", r"Fiber" )
VCmd.SetStringValue( var4, r"ActiveMaterial", r"L_FIBER" )
VCmd.SetStringValue( var4, r"FolderPath", r"Fiber" )
VCmd.SetIntValue( var4, r"MTXSetIOFlag", 256 )
VCmd.SetStringValue( var4, r"ActiveProperty", '' )
ret=VCmd.ExecuteCommand( var4, r"Save" )
VCmd.SetStringValue( var4, r"ActiveFolderClassID", r"Fiber" )
VCmd.SetStringValue( var4, r"FolderPath", r"Fiber" )
VCmd.SetStringValue( var4, r"ActiveClass", r"Fiber" )
VCmd.SetStringValue( var4, r"ActiveMaterial", r"L_FIBER" )
VCmd.SetStringValue( var4, r"ActiveCategoryTab", r"General" )
VCmd.SetIntValue( var4, r"CleaFlag", 256 )
VCmd.SetStringValue( var4, r"ActiveProperty", r"Density" )
VCmd.SetStringValue( var4, r"ActiveModelID", r"Distortion_General" )
VCmd.SetStringValue( var4, r"PropertyValueUnit", r"kg/m^3" )
ret=VCmd.ExecuteCommand( var4, r"UpdateParamForUnit" )
VCmd.SetStringValue( var4, r"PropertySValue", r"            1800" )
VCmd.SetStringValue( var4, r"ActiveCategoryTab", r"Fiber Properties" )
VCmd.SetStringValue( var4, r"ActiveProperty", r"FiberYoungsModulusInLengthDirection" )
VCmd.SetStringValue( var4, r"ActiveModelID", r"composite_fiber_properties" )
VCmd.SetStringValue( var4, r"PropertyValueUnit", r"GPa" )
ret=VCmd.ExecuteCommand( var4, r"UpdateParamForUnit" )
VCmd.SetStringValue( var4, r"ActiveProperty", r"FiberYoungsModulusInLengthDirection" )
VCmd.SetStringValue( var4, r"ActiveModelID", r"composite_fiber_properties" )
VCmd.SetStringValue( var4, r"ActiveProperty", r"FiberYoungsModulusInLengthDirection" )
VCmd.SetStringValue( var4, r"ActiveModelID", r"composite_fiber_properties" )
VCmd.SetStringValue( var4, r"PropertyValueUnit", r"GPa" )
ret=VCmd.ExecuteCommand( var4, r"UpdateParamForUnit" )
VCmd.SetStringValue( var4, r"PropertySValue", r"             230" )
VCmd.SetStringValue( var4, r"ActiveProperty", r"FiberYoungsModulusInTransverseDirection" )
VCmd.SetStringValue( var4, r"ActiveModelID", r"composite_fiber_properties" )
VCmd.SetStringValue( var4, r"PropertyValueUnit", r"GPa" )
ret=VCmd.ExecuteCommand( var4, r"UpdateParamForUnit" )
VCmd.SetStringValue( var4, r"ActiveProperty", r"FiberYoungsModulusInTransverseDirection" )
VCmd.SetStringValue( var4, r"ActiveModelID", r"composite_fiber_properties" )
VCmd.SetStringValue( var4, r"ActiveProperty", r"FiberYoungsModulusInTransverseDirection" )
VCmd.SetStringValue( var4, r"ActiveModelID", r"composite_fiber_properties" )
VCmd.SetStringValue( var4, r"PropertyValueUnit", r"GPa" )
ret=VCmd.ExecuteCommand( var4, r"UpdateParamForUnit" )
VCmd.SetStringValue( var4, r"PropertySValue", r"              15" )
VCmd.SetStringValue( var4, r"ActiveProperty", r"FiberPoissonsRatioInLengthDirection" )
VCmd.SetStringValue( var4, r"ActiveModelID", r"composite_fiber_properties" )
VCmd.SetStringValue( var4, r"PropertySValue", r"             0.3" )
VCmd.SetStringValue( var4, r"ActiveProperty", r"FiberShearModulusInLengthDirection" )
VCmd.SetStringValue( var4, r"ActiveModelID", r"composite_fiber_properties" )
VCmd.SetStringValue( var4, r"PropertyValueUnit", r"Pa" )
ret=VCmd.ExecuteCommand( var4, r"UpdateParamForUnit" )
VCmd.SetStringValue( var4, r"PropertySValue", r"               3" )
VCmd.SetStringValue( var4, r"ActiveProperty", r"FiberPoissonsRatioInTransverseDirection" )
VCmd.SetStringValue( var4, r"ActiveModelID", r"composite_fiber_properties" )
VCmd.SetStringValue( var4, r"PropertySValue", r"             0.3" )
VCmd.SetStringValue( var4, r"ActiveProperty", r"FiberShearModulusInLengthDirection" )
VCmd.SetStringValue( var4, r"ActiveModelID", r"composite_fiber_properties" )
VCmd.SetStringValue( var4, r"PropertyValueUnit", r"GPa" )
ret=VCmd.ExecuteCommand( var4, r"UpdateParamForUnit" )
VCmd.SetStringValue( var4, r"ActiveProperty", r"FiberShearModulusInLengthDirection" )
VCmd.SetStringValue( var4, r"ActiveModelID", r"composite_fiber_properties" )
VCmd.SetStringValue( var4, r"ActiveProperty", r"FiberShearModulusInLengthDirection" )
VCmd.SetStringValue( var4, r"ActiveModelID", r"composite_fiber_properties" )
VCmd.SetStringValue( var4, r"PropertyValueUnit", r"GPa" )
ret=VCmd.ExecuteCommand( var4, r"UpdateParamForUnit" )
VCmd.SetStringValue( var4, r"PropertySValue", r"              25" )
VCmd.SetStringValue( var4, r"ActiveProperty", r"FiberShearModulusInTransverseDirection" )
VCmd.SetStringValue( var4, r"ActiveModelID", r"composite_fiber_properties" )
VCmd.SetStringValue( var4, r"PropertyValueUnit", r"GPa" )
ret=VCmd.ExecuteCommand( var4, r"UpdateParamForUnit" )
VCmd.SetStringValue( var4, r"ActiveProperty", r"FiberShearModulusInTransverseDirection" )
VCmd.SetStringValue( var4, r"ActiveModelID", r"composite_fiber_properties" )
VCmd.SetStringValue( var4, r"ActiveProperty", r"FiberShearModulusInTransverseDirection" )
VCmd.SetStringValue( var4, r"ActiveModelID", r"composite_fiber_properties" )
VCmd.SetStringValue( var4, r"PropertyValueUnit", r"GPa" )
ret=VCmd.ExecuteCommand( var4, r"UpdateParamForUnit" )
VCmd.SetStringValue( var4, r"PropertySValue", r"               7" )
VCmd.SetStringValue( var4, r"ActiveProperty", r"FiberCoefThermalExpansionInLengthDirection" )
VCmd.SetStringValue( var4, r"ActiveModelID", r"composite_fiber_properties" )
VCmd.SetStringValue( var4, r"PropertyValueUnit", r"1/K" )
ret=VCmd.ExecuteCommand( var4, r"UpdateParamForUnit" )
VCmd.SetStringValue( var4, r"PropertySValue", r"        -6.3e-07" )
VCmd.SetStringValue( var4, r"ActiveProperty", r"FiberCoefThermalExpansionInTransverseDirection" )
VCmd.SetStringValue( var4, r"ActiveModelID", r"composite_fiber_properties" )
VCmd.SetStringValue( var4, r"PropertyValueUnit", r"1/K" )
ret=VCmd.ExecuteCommand( var4, r"UpdateParamForUnit" )
VCmd.SetStringValue( var4, r"PropertySValue", r"         6.3e-06" )
ret=VCmd.ExecuteCommand( var4, r"Save" )
VCmd.Accept( var4 )
VCmd.Quit( var4 )
#__________________ GenericMaterialEditor END __________________
VExpMngr.ExportFile( VdbDistortionFilePath, 0 )
VExpMngr.ExportFile( r'/nishome/smo/CAELESTIS/2024_RTMDIST_test/Results/line_1/zzFiber.vdb', 0 )
# VE.DeleteWindow(  )
# VE.SetCurrentPage( 1 )
# VE.SetCurrentPage( 1 )
# VE.SetActiveWindow( r"p1w1" )
# VE.NewSession(  )
