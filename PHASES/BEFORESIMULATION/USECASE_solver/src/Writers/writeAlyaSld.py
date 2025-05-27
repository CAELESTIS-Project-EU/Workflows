from math import pi, cos
from utils.insitu_strengths import in_situ_strengths
from utils.interf_strengths import interface_strengths_Turon2018_with_engineering_solution

def writeAlyaSldDat(file, filename, nmate, params, kfl_ori, debug, kfl_matconv, material_output):
    """ Alya caseName.sld.dat file
    """

    geometry        = params['General']['Geometry']
    
    # Get properties
    E11  = float(params['Material']['Elastic']['E11'])
    E11C = float(params['Material']['Elastic']['E11c'])
    E22  = float(params['Material']['Elastic']['E22'])
    E33  = E22
    NU12 = float(params['Material']['Elastic']['nu12'])
    NU13 = NU12
    NU23 = float(params['Material']['Elastic']['nu23'])
    G12  = float(params['Material']['Elastic']['G12'])
    G13  = G12
    G23  = E22/2.0/(1+NU23)

    T_LAY   = float(params['OGV_features']['Layup']['tply'])
    DENSITY = float(params['Material']['Other']['rho'])
    
    XT    = float(params['Material']['Strength']['XT'])
    XC    = float(params['Material']['Strength']['XC'])
    YT_UD = float(params['Material']['Strength']['YT'])
    YC_UD = float(params['Material']['Strength']['YC'])
    SL_UD = float(params['Material']['Strength']['SL'])
    YBT   = float(params['Material']['Strength']['YBT'])
    YBC   = float(params['Material']['Strength']['YBC'])
    
    fxT = float(params['Material']['Other']['fxT'])
    fxC = float(params['Material']['Other']['fxC'])
    fgT = float(params['Material']['Other']['fgT'])
    fgC = float(params['Material']['Other']['fgC'])

    ALPHA_O = float(params['Material']['Other']['ALPHA_O'])
    
    GSL = float(params['Material']['Energies']['GSL'])
    GXT = float(params['Material']['Energies']['GXT'])
    GXC = float(params['Material']['Energies']['GXC'])
    GYT = float(params['Material']['Energies']['GYT'])
    try:
        GYC = float(params['Material']['Energies']['GYC'])
    except:
        GYC = float(GSL/cos(ALPHA_O*pi/180.))

    SPLAS = float(params['Material']['Other']['Splas'])
    KPLAS = float(params['Material']['Other']['Kplas'])
    muGSL = float(params['Material']['Other']['muGSL'])
    mufXC = float(params['Material']['Other']['mufXC'])

    ALPHA_11 = float(params['Material']['Hygrothermal']['a11'])
    ALPHA_22 = float(params['Material']['Hygrothermal']['a22'])
    BETA_11  = float(params['Material']['Hygrothermal']['b11'])
    BETA_22  = float(params['Material']['Hygrothermal']['b22'])
    
    DenCoh = float(params['Material']['Cohesive']['rhoc'])
    G_IC   = float(params['Material']['Cohesive']['GIc'])
    G_IIC  = float(params['Material']['Cohesive']['GIIc'])
    tauI   = float(params['Material']['Cohesive']['tauI'])
    tauII  = float(params['Material']['Cohesive']['tauII'])
    etaBK  = float(params['Material']['Cohesive']['etaBK'])
    Kcoh   = float(params['Material']['Cohesive']['Kp'])
    NCE    = int(params['Material']['Cohesive']['nce'])

    kfl_coh  = bool(params['OGV_features']['Other']['kfl_coh'])
    layupCLU = params['OGV_features']['Layup']['clu']*40          # Hardcoded for OGV   
    layupLOC = params['OGV_features']['Layup']['loc']*40          # Hardcoded for OGV  
    le       = float(params['OGV_features']['Mesh']['le']) 

    nlgeom = bool(params['OGV_solver']['nlgeom'])
    ms     = float(params['OGV_solver']['ms'])

    try:
        d1MaxList = params['OGV_features']['Layup']['d1max']
    except:
        d1MaxList = [1.0]*len(params['OGV_features']['Layup']['ori'])
    try:
        d2MaxList = params['OGV_features']['Layup']['d2max']
    except:
        d2MaxList = [1.0]*len(params['OGV_features']['Layup']['ori'])
    try:
        d3MaxList = params['OGV_features']['Layup']['d3max']
    except:
        d3MaxList = [1.0]*len(params['OGV_features']['Layup']['ori'])
    try:
        d4MaxList = params['OGV_features']['Layup']['d4max']
    except:
        d4MaxList = [1.0]*len(params['OGV_features']['Layup']['ori'])
    try:
        d5MaxList = params['OGV_features']['Layup']['d5max']
    except:
        d5MaxList = [1.0]*len(params['OGV_features']['Layup']['ori'])
    try:
        d6MaxList = params['OGV_features']['Layup']['d6max']
    except:
        d6MaxList = [1.0]*len(params['OGV_features']['Layup']['ori'])
    try:
        dcMax = params['OGV_features']['Layup']['dcohmax']
    except:
        dcMax = 1.0
        
    
    stream = open(file, 'w')

    stream.write('$-------------------------------------------------------------------\n')
    stream.write('$\n')
    stream.write(f'$ {filename:s}\n')
    stream.write('$\n')
    stream.write('$ Dimensions:\n')
    stream.write('$\n')
    stream.write('$ Boundary conditions:\n')
    stream.write('$\n')
    stream.write('$   ^ y\n')
    stream.write('$   |\n')
    stream.write('$   |      x\n')
    stream.write('$   o----->\n')
    stream.write('$    \ \n')
    stream.write('$    _\/ z\n')
    stream.write('$\n')
    stream.write('$   CODE 1: ENCASTRE FACE,  X= -L/2\n')
    stream.write('$   CODE 2: PRESCRIBED LOAD FACE, X= L/2\n')
    stream.write('$   CODE 3: PRESSURE FACE, Z= 0 and Z= T_LAM\n')
    stream.write('$\n')
    stream.write('$\n')
    stream.write('$ Materials:\n')
    stream.write('$    CODE   1: PLY-1\n')
    stream.write('$    CODE   2: PLY-2\n')
    stream.write('$     ...\n')
    stream.write('$    CODE N-1: COHESIVE\n')
    stream.write('$    CODE   N: GAP\n')
    stream.write('$\n')
    stream.write('$ Units:     SI (-)\n')
    stream.write('$\n')
    stream.write('$ Reference: X project\n')
    stream.write('$\n')
    stream.write('$-------------------------------------------------------------------\n')
    stream.write('PHYSICAL_PROBLEM\n')
    stream.write('  PROBLEM_DEFINITION\n')
    stream.write('    TEMPORAL_DERIVATIVES: DYNAMIC\n')
    if nlgeom:
        stream.write('    NLGEOM:               ON\n')
    else:
        stream.write('    NLGEOM:               OFF\n')
    stream.write('    THERMAL_ANALYSIS:     OFF\n')
    stream.write('  END_PROBLEM_DEFINITION\n')
    stream.write('  PROPERTIES\n')
    nmate_bulk = nmate
    if kfl_coh:
        nmate_bulk = nmate - 1
        
    if kfl_matconv:

        for i in range(nmate_bulk):

            # Get elastic prop for each group
            E11 = material_output['material_groups'][i]['E11_MT']
            #E11C = params['Material']['Elastic']['E11c']
            E22 = material_output['material_groups'][i]['E22_MT']
            E33 = E22
            NU12 = material_output['material_groups'][i]['NU12_MT']
            NU13 = NU12
            NU23 = material_output['material_groups'][i]['NU23_MT']
            G12 = material_output['material_groups'][i]['G12_MT']
            G13 = G12
            G23 = E22 / 2.0 / (1 + NU23)
        
            # TO REVISE: Calculate insitus
            tclus = T_LAY*int(layupCLU[i])
            loc   = layupLOC[i]
            YT, YC, SL = in_situ_strengths(tclus, loc, E11, E22, NU12, G12, YT_UD, YC_UD, SL_UD, KPLAS, SPLAS, GSL, G_IC, G_IIC)

            
            # Max. damaged variable per ply
            d1Max = float(d1MaxList[i])
            d2Max = float(d2MaxList[i])
            d3Max = float(d3MaxList[i])
            d4Max = float(d4MaxList[i])
            d5Max = float(d5MaxList[i])
            d6Max = float(d6MaxList[i])
        
            stream.write(f'    MATERIAL          = {i+1}\n')
            stream.write(f'    DENSITY           = {DENSITY:1.4e}\n' )
            stream.write('    CONSTITUTIVE_MODEL: MAIMI \\\n')
            stream.write(f'      {E11:1.3f} {E22:1.3f}     {NU12:1.3f}   {NU23:1.3f} {G12:1.3f}                   \\\n')
            stream.write(f'        {XT:1.3f}    {fxT:1.3f}  {XC:1.3f}   {fxC:1.3f}   {YT:1.3f}    {YC:1.3f} {SL:1.3f} \\\n')
            stream.write(f'           {ALPHA_O*pi/180.:1.3f}                                                       \\\n')
            stream.write(f'         {GXT:1.3f}    {fgT:1.3f}    {GXC:1.3f}   {fgC:1.3f}    {GYT:1.3f}      {GYC:1.3f}  {GSL:1.3f} \\\n')
            stream.write(f'          {SPLAS:1.3f}    {KPLAS:1.3f}                                              \\\n')
            stream.write(f'           {0.0:1.3f}                                                       \\\n')
            stream.write(f'          {ALPHA_11:1.2e} {ALPHA_22:1.2e}  {0.0:1.3f}   {BETA_11:1.2e} {BETA_22:1.2e}   {0.0:1.3f} \\\n')
            stream.write(f'           {d1Max:1.4f}    {d2Max:1.4f}     {d3Max:1.4f}   {d4Max:1.4f}    {d5Max:1.4f}      {d6Max:1.4f} \\\n')
            stream.write(f'           {T_LAY:1.3f}    {muGSL:1.3f}    {YBT:1.3f} {YBC:1.3f}    {mufXC:1.3f} {E11C:1.3f}\n')
        
            #stream.write('    CONSTITUTIVE_MODEL: ORTHOTROPIC \\ \n')
            #stream.write(f'      {E11:1.3f} {E22:1.3f} {E33:1.3f} {NU12:1.3f} {NU13:1.3f} {NU23:1.3f} {G12:1.3f}  {G13:1.3f} {G23:1.3f}\n')
    else:
            
        for i in range(nmate_bulk):
            # Calculate insitus
            tclus = T_LAY*int(layupCLU[i])
            loc   = layupLOC[i]
            YT, YC, SL = in_situ_strengths(tclus, loc, E11, E22, NU12, G12, YT_UD, YC_UD, SL_UD, KPLAS, SPLAS, GSL, G_IC, G_IIC)
            # Max. damaged variable per ply
            d1Max = float(d1MaxList[i])
            d2Max = float(d2MaxList[i])
            d3Max = float(d3MaxList[i])
            d4Max = float(d4MaxList[i])
            d5Max = float(d5MaxList[i])
            d6Max = float(d6MaxList[i])
        
            stream.write(f'    MATERIAL          = {i+1}\n')
            stream.write(f'    DENSITY           = {DENSITY:1.4e}\n' )
            stream.write('    CONSTITUTIVE_MODEL: MAIMI \\\n')
            stream.write(f'      {E11:1.3f} {E22:1.3f}     {NU12:1.3f}   {NU23:1.3f} {G12:1.3f}                   \\\n')
            stream.write(f'        {XT:1.3f}    {fxT:1.3f}  {XC:1.3f}   {fxC:1.3f}   {YT:1.3f}    {YC:1.3f} {SL:1.3f} \\\n')
            stream.write(f'           {ALPHA_O*pi/180.:1.3f}                                                       \\\n')
            stream.write(f'         {GXT:1.3f}    {fgT:1.3f}    {GXC:1.3f}   {fgC:1.3f}    {GYT:1.3f}      {GYC:1.3f}  {GSL:1.3f} \\\n')
            stream.write(f'          {SPLAS:1.3f}    {KPLAS:1.3f}                                              \\\n')
            stream.write(f'           {0.0:1.3f}                                                       \\\n')
            stream.write(f'          {ALPHA_11:1.2e} {ALPHA_22:1.2e}  {0.0:1.3f}   {BETA_11:1.2e} {BETA_22:1.2e}   {0.0:1.3f} \\\n')
            stream.write(f'           {d1Max:1.4f}    {d2Max:1.4f}     {d3Max:1.4f}   {d4Max:1.4f}    {d5Max:1.4f}      {d6Max:1.4f} \\\n')
            stream.write(f'           {T_LAY:1.3f}    {muGSL:1.3f}    {YBT:1.3f} {YBC:1.3f}    {mufXC:1.3f} {E11C:1.3f}\n')
        
            #stream.write('    CONSTITUTIVE_MODEL: ORTHOTROPIC \\ \n')
            #stream.write(f'      {E11:1.3f} {E22:1.3f} {E33:1.3f} {NU12:1.3f} {NU13:1.3f} {NU23:1.3f} {G12:1.3f}  {G13:1.3f} {G23:1.3f}\n')

        if kfl_coh:
            # Calculate interface strength based on engineering solution
            tauI, tauII  = interface_strengths_Turon2018_with_engineering_solution(E22, G12, YT_UD, SL_UD, G_IC, G_IIC, NCE, le)
            stream.write(f'    MATERIAL          = {nmate}\n')
            stream.write(f'    DENSITY           = {DenCoh:1.4e} {Kcoh:1.1e}\n')
            stream.write('    COHESIVE_MODEL: TURON, CURRENT \ \n')
            stream.write(f'      {G_IC:1.4f} {G_IIC:1.4f} {tauI:1.4f} {tauII:1.4f} {etaBK:1.4f} {Kcoh:1.1e} {0.0:1.4f} {0.0:1.4f} {dcMax:1.4f}\n')
        
    stream.write('  END_PROPERTIES\n')
    stream.write('  PARAMETERS\n')
    if kfl_ori == 'uniform':
        stream.write('    CSYS_MATERIAL: FIELD= 1, ORIENTATION, TYPE= ELEMENT_NORMAL, REFAXIS= 2\n')
        #stream.write('    CSYS_MATERIAL: FIELD= 1, ORIENTATION, TYPE= USER, ROTAX= 3\n')
        #stream.write('    COORDINATE_SYSTEM: BASIS= CARTESIAN \ \n')
        #stream.write('      0.0 0.0 0.0  0.30901699437494745 0.9510565162951535 0.0  -0.9510565162951535 0.30901699437494745 0.0\n')
    else:
        stream.write('    CSYS_MATERIAL: FIELD= 1, VECTOR\n')
    stream.write('  END_PARAMETERS\n')
    stream.write('END_PHYSICAL_PROBLEM\n')
    stream.write('$-------------------------------------------------------------------\n')
    stream.write('NUMERICAL_TREATMENT\n')
    stream.write('  TIME_TREATMENT:       EXPLICIT\n')
    stream.write('  TIME_INTEGRATION:     TCHAMWA_WIELGOSZ, PHITW= 1.033\n')
    stream.write('  STEADY_STATE:         OFF\n')
    stream.write(f'  MASS_SCALING=         {ms:1.4e}\n')
    stream.write('  SAFETY_FACTOR=        0.9\n') 
    stream.write('  TIME_STEP_STRATEGY:   MIN_LENGTH, UPDATED\n') 
    stream.write('  DTCRI_MIN=            5.0E-9\n') 
    stream.write('  ELEMENT_LENGTH:       VOLUME\n') 
    stream.write('  VECTORIZED_ASSEMBLY:  ON\n') 
    stream.write('END_NUMERICAL_TREATMENT\n')
    stream.write('$-------------------------------------------------------------------\n')
    stream.write('OUTPUT_&_POST_PROCESS\n')
    stream.write('  START_POSTPROCESS_AT: STEP= 0\n')
    if debug:
        stream.write('  POSTPROCESS PARTI\n')
        stream.write('  POSTPROCESS PMATE\n')
        stream.write('  POSTPROCESS FIXNO\n')
        stream.write('  POSTPROCESS BOCOD\n')
        stream.write('  POSTPROCESS NPOIN\n')
        stream.write('  POSTPROCESS NELEM\n')
        stream.write('  POSTPROCESS BOSET\n')
        stream.write('  POSTPROCESS ELSET\n')
        stream.write('$  POSTPROCESS NOSET\n')
        stream.write('  POSTPROCESS CELEN\n')
        stream.write('  POSTPROCESS FEXTE\n')
        stream.write('  POSTPROCESS PRESS\n')
        stream.write('  POSTPROCESS AXIS1\n')
        stream.write('  POSTPROCESS AXIS2\n')
        stream.write('  POSTPROCESS AXIS3\n')
        stream.write('  POSTPROCESS ORIEN\n')
        stream.write('  POSTPROCESS ELNOR\n')
        stream.write('  POSTPROCESS STACK\n')
        stream.write('  POSTPROCESS PELCH\n')
        stream.write('  POSTPROCESS PELTY\n')
        stream.write('  POSTPROCESS SRPRO\n')
        stream.write('  POSTPROCESS BVESS\n')
        stream.write('  POSTPROCESS DISPL\n')
        stream.write('  POSTPROCESS DAMAG\n')
        stream.write('  POSTPROCESS DCOHE\n')
    if geometry == 'OGV':
        stream.write('  REACTION_SET, NUMBER= 1, FORCE_DROP_PERCENTAGE= 30.0, TOLERANCE=1E+3, ON_REACTION_SET= 1\n')
        stream.write('    REACTION_SET= 1, PLANE: AXIS= 2, GREATER_THAN= 150.0,\n')
        stream.write('  END_REACTION_SET\n')
    elif geometry == 'POC1':
        stream.write('  REACTION_SET, NUMBER= 1, FORCE_DROP_PERCENTAGE= 30.0, TOLERANCE=1E+3, ON_REACTION_SET= 1\n')
        stream.write('    REACTION_SET= 1, PLANE: AXIS= 1, GREATER_THAN= 305.0,\n')
        stream.write('  END_REACTION_SET\n')
    elif geometry == 'POC2':
        stream.write('  REACTION_SET, NUMBER= 1, FORCE_DROP_PERCENTAGE= 30.0, TOLERANCE=1E+3, ON_REACTION_SET= 1\n')
        stream.write('    REACTION_SET= 1, PLANE: AXIS= 2, GREATER_THAN= 273.0,\n')
        stream.write('  END_REACTION_SET\n')
    stream.write('END_OUTPUT_&_POST_PROCESS\n')
    stream.write('$-------------------------------------------------------------------\n')
    stream.write('BOUNDARY_CONDITIONS, TRANSIENT\n')
    stream.write('  CODES, NODES\n')
    stream.write('    1     111 0.0 0.0 0.0 \n')
    stream.write('    2     111 1.0 1.0 1.0, DISCRITE_FUNCTIONS= UDISP\n')
    stream.write('  END_CODES\n')
    stream.write('END_BOUNDARY_CONDITIONS\n')
    stream.write('$-------------------------------------------------------------------\n')
    
    stream.close()
