
def writeAlyaKer(debug, path, fileName, nmate, densi, visco):
    """ Alya caseName.ker.dat file
    """
    
    stream = open(path + fileName+'.ker.dat', 'w', newline='\n')
    
    stream.write('$-------------------------------------------------------------------\n')
    stream.write('PHYSICAL_PROBLEM\n')
    stream.write('  PROPERTIES\n')
    for i in range(nmate):
        stream.write(f'    MATERIAL= {i+1}\n')
        stream.write(f'      DENSITY:     CONSTANT, PARAMETERS= {densi:1.4e}\n')
        stream.write(f'      VISCOSITY:   CONSTANT, PARAMETERS= {visco:1.4e}\n')
        stream.write('      ANIPOROSITY: FIELD,    PARAMETERS= 1\n')
        stream.write('    END_MATERIAL \n')
    stream.write('  END_PROPERTIES\n')
    stream.write('END_PHYSICAL_PROBLEM\n')
    stream.write('$-------------------------------------------------------------------\n')
    stream.write('NUMERICAL_TREATMENT\n')
    stream.write('  MESH\n')
    stream.write('    MULTIPLICATION\n')
    stream.write('      LEVEL= 0\n')
    stream.write('    END_MULTIPLICATION\n')
    stream.write('    SAVE_ELEMENT_DATA_BASE: OFF\n')
    stream.write('  END_MESH\n')
    stream.write('END_NUMERICAL_TREATMENT\n')
    stream.write('$-------------------------------------------------------------------\n')
    stream.write('OUTPUT_&_POST_PROCESS\n')
    if debug:
        stream.write('  ON_LAST_MESH\n')
        stream.write('  STEPS= 1e+6\n')
        stream.write('  POSTPROCESS ELNUM\n')
        stream.write('  POSTPROCESS PONUM\n')
        stream.write('  POSTPROCESS MATER\n')
        stream.write('  POSTPROCESS PERIO\n')
        stream.write('  POSTPROCESS ELSET\n')
        stream.write('  POSTPROCESS BOSET\n')
        stream.write('  POSTPROCESS ANIPO\n')
    else:
        stream.write('  NO_MESH\n')
    stream.write('END_OUTPUT_&_POST_PROCESS\n')
    stream.write('$-------------------------------------------------------------------\n')

    stream.close()

    
