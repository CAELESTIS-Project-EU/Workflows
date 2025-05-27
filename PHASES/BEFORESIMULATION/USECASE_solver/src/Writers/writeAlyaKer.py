def writeAlyaKerDat(file, params, debug):
    """ Alya caseName.ker.dat file
    """

    tf = float(params['OGV_solver']['tf'])
    ux = float(params['OGV_solver']['ux'])
    uy = float(params['OGV_solver']['uy'])
    uz = float(params['OGV_solver']['uz'])
    mesh_div_level = int(params['OGV_solver']['mesh_div_level'])
    
    stream = open(file, 'w')
    
    stream.write('$-------------------------------------------------------------------\n')
    stream.write('PHYSICAL_PROBLEM\n')
    stream.write('END_PHYSICAL_PROBLEM\n')
    stream.write('$-------------------------------------------------------------------\n')
    stream.write('NUMERICAL_TREATMENT\n')
    stream.write('  MESH\n')
    stream.write('    MULTIPLICATION\n')
    stream.write(f'     LEVEL= {mesh_div_level}\n')
    stream.write('      ELEMENT_NORMAL_MULTIPLICATION: ON\n')
    stream.write('      PARALLELIZATION:               COORDINATES\n')
    stream.write('    END_MULTIPLICATION\n')
    stream.write('    SAVE_ELEMENT_DATA_BASE: ON\n')
    stream.write('  END_MESH\n')
    stream.write('  DISCRETE_FUNCTIONS\n')
    stream.write('    TOTAL_NUMBER= 1\n')
    stream.write('    FUNCTIONS=  UDISP, DIMENSIONS= 3\n')
    stream.write('      TIME_SHAPE: SMOOTH\n')
    stream.write('      SHAPE_DEFINITION\n')
    stream.write('        2\n')
    stream.write('        0.0  0.0 0.0 0.0\n')
    stream.write(f'        {tf:1.4e} {ux:1.4f} {uy:1.4f} {uz:1.4f}\n')
    stream.write('      END_SHAPE_DEFINITION\n')
    stream.write('    END_FUNCTIONS\n')
    stream.write('  END_DISCRETE_FUNCTIONS\n')
    stream.write('END_NUMERICAL_TREATMENT\n')
    stream.write('$-------------------------------------------------------------------\n')
    stream.write('OUTPUT_&_POST_PROCESS\n')
    if debug:
        stream.write('  ON_LAST_MESH\n')
        stream.write('  STEPS= 1e6\n')
    else:
        stream.write('  NO_MESH\n')
    stream.write('END_OUTPUT_&_POST_PROCESS\n')
    stream.write('$-------------------------------------------------------------------\n')

    stream.close()
