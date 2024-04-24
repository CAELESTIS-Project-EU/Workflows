#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#-------------------------------------------------------------------------------
#                          Session File
#                           ESI Group
#                      https://www.esi-group.com
#        Copyright (C) ESI Group 2022.  All rights reserved.
#-------------------------------------------------------------------------------
#	Product				:  	Visual-Environment 18.5
#	Date				:  	Fri Mar 31 16:36:46 2023
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

#SMO: read macro directory from temporary file
Scriptsfolder = os.getcwd()
VariablesList = os.path.join(Scriptsfolder, 'VariablesList.txt')

print(100*'_')
print('DISTORTION, preparing model. p31')
print('Reading list of variables')

#SMO: read macro directory from temporary file
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
            VdbCuringFilePath = linesplit[2]
            print('vdb curing file found')
        if 'VdbDistortionFilePath' in line:
            linesplit = line.partition('= ')
            #Extract Variable name, value and IDnumber identificator                           
            VdbDistortionFilePath = linesplit[2]
    
ret=VE.ChangeContext( r"Visual-RTM" )
ret=VExpMngr.LoadFile( VdbCuringFilePath, 0 )

lst1_count,lst1 =  VScn.List( "  P 10001:10004 "  )
VCmd.SetObjectArrayValue( var1, r"ExplorerSelection", lst1_count, lst1 )
ret=VCmd.ExecuteCommand( var1, r"DeleteEntities" )
lst1_count,lst1 =  VScn.List( "  P 10000 "  )
VCmd.SetObjectArrayValue( var1, r"ExplorerSelection", lst1_count, lst1 )
ret=VCmd.ExecuteCommand( var1, r"ShowSelected" )
ret=VE.ChangeContext( r"Visual-Distortion" )
#__________________ SimulationControl BEGIN __________________
var6=VCmd.Activate( 1, r"VCompUtils.VCompUtilsCmdInterface", r"SimulationControl" )
VCmd.SetObjectValue( var6, r"CurrentModel", "M  @0" )
VE.SetActiveWindow( r"p1w1" )
VCmd.Quit( var6 )
#__________________ SimulationControl END __________________
#__________________ CompositeLayerDesignManager BEGIN __________________
var7=VCmd.Activate( 1, r"VCompUtils.VCompUtilsCmdInterface", r"CompositeLayerDesignManager" )
VCmd.SetIntValue( var7, r"Part2D3DOption", 3 )
VCmd.SetGuStringValue( var7, r"LayerLaminateListFlag", r"LaminateList" )
VCmd.SetGuStringValue( var7, r"SuppressMaterialNames", r"LAMINATE_6 LAMINATE_3 LAMINATE_4 LAMINATE_5" )
VCmd.SetIntValue( var7, r"Part2D3DOption", 2 )
VCmd.Quit( var7 )
#__________________ CompositeLayerDesignManager END __________________
ret=VE.ChangeContext( r"Visual-Mesh" )
ret=VE.ChangeSkin( r"General" )
VE.SetActiveWindow( r"p1w1" )
VCmd.SetStringValue( var1, r"TargetName", r"Element" )
lst1_count,lst1 =  VScn.List( "  T 1921:6432 "  )
VCmd.SetObjectArrayValue( var1, r"GraphicSelection",  lst1_count , lst1 )
ret=VCmd.ExecuteCommand( var1, r"DeleteEntities" )
var9=VCmdGui.Create( r"VModelValidate.VCommandEleGeom" )
VCmdGui.SetIntValue( var9, r"QualParaType", 2 )
VCmdGui.SetIntValue( var9, r"ElemGeomGuiType", 1 )
VCmdGui.Activate( var9, 0 )
VCmdGui.SetIntValue( var9, r"QualParaType", 1 )
lst1_count,lst1 =  VScn.StringList( r" 1 | 2.000000 | 1 | 4.000000 | 1 | 2.000000 | 1 | 2.000000  "  )
VCmdGui.SetStringArrayValue( var9, r"1DParameterInfo", lst1_count, lst1 )
VCmdGui.SetIntValue( var9, r"QualParaType", 2 )
lst1_count,lst1 =  VScn.StringList( r" 1 | 8.000000 | 1 | 30.000000 | 1 | 4.000000 | 1 | 45.000000 | 1 | 135.000000 | 1 | 30.000000 | 1 | 120.000000 | 1 | 8.000000 | 1 | 0.700000 | 1 | 45.000000 | 1 | 0.700000 | 1 | 8.000000 | 0 | 0.001000  "  )
VCmdGui.SetStringArrayValue( var9, r"2DParameterInfo", lst1_count, lst1 )
VCmdGui.SetIntValue( var9, r"QualParaType", 3 )
lst1_count,lst1 =  VScn.StringList( r" 1 | 8.000000 | 1 | 30.000000 | 1 | 8.000000 | 1 | 45.000000 | 1 | 135.000000 | 1 | 30.000000 | 1 | 120.000000 | 1 | 8.000000 | 1 | 0.700000 | 1 | 45.000000 | 1 | 0.700000 | 1 | 0.500000 | 1 | 8.000000 | 1 | 0.500000 | 1 | 8.000000 | 0 | 0.001000  "  )
VCmdGui.SetStringArrayValue( var9, r"3DParameterInfo", lst1_count, lst1 )
VCmdGui.Quit( var9 )
#__________________ TopologyMesh BEGIN __________________
var13=VCmd.Activate( 1, r"VMeshModeler.VmmICommandGui", r"TopologyMesh" )
VCmd.SetObjectValue( var13, r"CurrentModel", "M  @0" )
VCmd.SetIntValue( var13, r"MeshType", 1 )
ret=VCmd.ExecuteCommand( var13, r"MeshAllFaces" )
VCmd.Cancel( var13 )
ret=VE.ChangeContext( r"Visual-Distortion" )
#__________________ SimulationControl BEGIN __________________
var14=VCmd.Activate( 1, r"VCompUtils.VCompUtilsCmdInterface", r"SimulationControl" )
VCmd.SetObjectValue( var14, r"CurrentModel", "M  @0" )
VE.SetActiveWindow( r"p1w1" )
VCmd.Quit( var14 )
#__________________ SimulationControl END __________________
#__________________ CompositeLayerDesignManager BEGIN __________________
var15=VCmd.Activate( 1, r"VCompUtils.VCompUtilsCmdInterface", r"CompositeLayerDesignManager" )
VCmd.SetIntValue( var15, r"Part2D3DOption", 3 )
VCmd.SetIntValue( var15, r"Part2D3DOption", 2 )
VCmd.Quit( var15 )
#__________________ CompositeLayerDesignManager END __________________
#__________________ LaminateMesh BEGIN __________________
var16=VCmd.Activate( 1, r"VCompUtils.VCompUtilsCmdInterface", r"LaminateMesh" )
VCmd.SetIntValue( var16, r"MeshOptions", 0 )
VCmd.SetIntValue( var16, r"NoOfLayers", 3 )
VCmd.SetIntValue( var16, r"NoOfLayers", 3 )
VCmd.SetObjectValue( var16, r"Model", "M  @0" )
VCmd.Accept( var16 )
VCmd.Quit( var16 )
#__________________ LaminateMesh END __________________
#__________________ PartOrientationDefinition BEGIN __________________
var17=VCmd.Activate( 1, r"VCompUtils.VCompUtilsCmdInterface", r"PartOrientationDefinition" )
VCmd.SetObjectValue( var17, r"CurrentModel", "M  @0" )
VCmd.SetObjectValue( var17, r"SelectedOrientationObj", "ORI  2" )
lst1_count,lst1 =  VScn.StringList( r" 10001/PART_Layer_1 | 10002/PART_Layer_2 | 10003/PART_Layer_3 | 10004/PART_Layer_4  "  )
VCmd.SetStringArrayValue( var1, r"ListSelection", lst1_count, lst1 )
VCmd.SetIntValue( var17, r"SimulationCheck", 1 )
ret=VCmd.ExecuteCommand( var17, r"SimulateOrientMethod" )
lst1_count,lst1 =  VScn.StringList( r" 10000/Level_10000  "  )
VCmd.SetStringArrayValue( var1, r"ListSelection", lst1_count, lst1 )
lst1_count,lst1 =  VScn.List( "  P 10000 "  )
VCmd.SetObjectArrayValue( var17, r"PartSelection", lst1_count, lst1 )
ret=VCmd.ExecuteCommand( var17, r"TransferPartsToOriList" )
VCmd.SetIntValue( var17, r"SimulationCheck", 1 )
ret=VCmd.ExecuteCommand( var17, r"SimulateOrientMethod" )
lst1_count,lst1 =  VScn.StringList( r" All  "  )
VCmd.SetStringArrayValue( var1, r"ListSelection", lst1_count, lst1 )
VCmd.SetIntValue( var17, r"YDisplayFlag", 1 )
lst1_count,lst1 =  VScn.List( "  ORI 1 "  )
VCmd.SetDbsVectorValue( var17, r"InnerOrientation", lst1_count, lst1 )
VCmd.SetIntValue( var17, r"SimulationCheck", 1 )
ret=VCmd.ExecuteCommand( var17, r"SimulateOrientMethod" )
ret=VCmd.ExecuteCommand( var17, r"TransferAxisPtCrvToOriList" )
VCmd.Accept( var17 )
VCmd.SetIntValue( var17, r"PartSelectedFlag", 3 )
ret=VCmd.ExecuteCommand( var17, r"RefreshOrientationList" )
ret=VCmd.ExecuteCommand( var17, r"ClearListSel" )
VCmd.SetIntValue( var17, r"XDisplayFlag", 0 )
VCmd.SetIntValue( var17, r"YDisplayFlag", 0 )
VCmd.SetIntValue( var17, r"ZDisplayFlag", 0 )
ret=VCmd.ExecuteCommand( var17, r"CreateNewOrientation" )
VCmd.SetIntValue( var17, r"OrientMethod", 4 )
lst1_count,lst1 =  VScn.StringList( r" All  "  )
VCmd.SetStringArrayValue( var1, r"ListSelection", lst1_count, lst1 )
lst1_count,lst1 =  VScn.List( "  P 10001:10004 "  )
VCmd.SetObjectArrayValue( var17, r"PartSelection", lst1_count, lst1 )
ret=VCmd.ExecuteCommand( var17, r"TransferPartsToOriList" )
VCmd.SetIntValue( var17, r"SimulationCheck", 1 )
ret=VCmd.ExecuteCommand( var17, r"SimulateOrientMethod" )
lst1_count,lst1 =  VScn.StringList( r" All  "  )
VCmd.SetStringArrayValue( var1, r"ListSelection", lst1_count, lst1 )
lst1_count,lst1 =  VScn.List( "  ORI 2 "  )
VCmd.SetDbsVectorValue( var17, r"InnerOrientation", lst1_count, lst1 )
VCmd.SetIntValue( var17, r"SimulationCheck", 1 )
ret=VCmd.ExecuteCommand( var17, r"SimulateOrientMethod" )
ret=VCmd.ExecuteCommand( var17, r"TransferAxisPtCrvToOriList" )
VCmd.Accept( var17 )
VCmd.Quit( var17 )
#__________________ PartOrientationDefinition END __________________
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
#__________________ CompositeLayerDesignManager END __________________
var4=VCmd.Activate( 0, r"VCompUtils.VCompUtilsCmdInterface", r"RTMtoDistortionProperties" )
VCmd.Quit( var4 )

VExpMngr.ExportFile( VdbDistortionFilePath, 0 )
# ret=VE.ModelDestroy( "M  @0" )
# VE.SetCurrentPage( 1 )
# VE.SetActiveWindow( r"p1w1" )
# VE.NewSession(  )

