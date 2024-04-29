
def writeAlyaDom(path, fileName, icase, npoin, nelem, nboun, nmate, periodicityMethod, fieldFlag, Full_periodicity):
    """ Alya caseName.dom.dat file
    """
    
    stream = open(path+fileName+'.dom.dat', 'w', newline='\n')

    stream.write('$-------------------------------------------------------------------\n')
    stream.write('DIMENSIONS\n')
    stream.write('  NODAL_POINTS      = %d\n' % npoin)
    stream.write('  ELEMENTS          = %d\n' % nelem)
    stream.write('  BOUNDARIES        = %d\n' % nboun)
    stream.write('  SPACE_DIMENSIONS  = %d\n' % 3)
    stream.write('  TYPES_OF_ELEMENTS = HEX08\n')
    stream.write('  MATERIALS         = %d\n' % nmate)
    if fieldFlag:
        stream.write('  FIELDS            = 1\n')
        stream.write('    FIELD= 1, DIMENSIONS= %d, ELEMENTS\n' % (9))
        stream.write('  END_FIELDS\n')
    stream.write('END_DIMENSIONS\n')
    stream.write('$-------------------------------------------------------------------\n')
    stream.write('STRATEGY\n')
    stream.write('  INTEGRATION_RULE:                OPEN\n')
    stream.write('  DOMAIN_INTEGRATION_POINTS=       0\n')
    stream.write('  SCALE:                           XSCAL= 1.0E-3 YSCAL= 1.0E-3 ZSCAL= 1.0E-3\n')  # Acordar las unidades y volver a poner 1
    stream.write('  TRANSLATION:                     XTRAN= 0.0    YTRAN= 0.0    ZTRAN= 0.0\n')
    stream.write('  EXTRAPOLATE_BOUNDARY_CONDITIONS: ON\n')
    stream.write('  BOUNDARY_ELEMENT:                ON\n')
    stream.write('  GROUPS=                          512, SEQUENTIAL_FRONTRAL\n')
    if periodicityMethod == 'Automatic':
        if Full_periodicity == True:
            stream.write('  PERIODICITY:                     BOUNDARY_CODES, TOLER= AUTOMATIC\n')
            stream.write('    1  2\n')
            stream.write('    3  4\n')
            stream.write('    5  6\n')
        else:
            stream.write('  PERIODICITY:                     BOUNDARY_CODES, TOLER= AUTOMATIC\n')
            if icase == 'x-flow' or icase == 'y-flow':
                stream.write('    1  2\n')
                stream.write('    3  4\n')
            else:
                stream.write('    1  2\n')
                stream.write('    3  4\n')
                stream.write('    5  6\n')
        
        stream.write('  END_PERIODICITY\n')
    stream.write('END_STRATEGY\n')
    stream.write('$-------------------------------------------------------------------\n')
    stream.write('GEOMETRY\n')
    stream.write('  INCLUDE ../msh/%s.geo.dat\n' % fileName)
    stream.write('  INCLUDE ../msh/%s.bou.dat\n' % fileName)
    stream.write('  INCLUDE ../msh/%s.mat.dat\n' % fileName)
    if periodicityMethod != 'Automatic':
        stream.write('  INCLUDE ./%s.per.dat\n' % fileName)
    stream.write('END_GEOMETRY\n')
    stream.write('$-------------------------------------------------------------------\n')
    stream.write('SETS\n')
    stream.write('  INCLUDE ../msh/%s.set.dat\n' % fileName)
    stream.write('END_SETS\n')
    stream.write('$-------------------------------------------------------------------\n')
    stream.write('BOUNDARY_CONDITIONS\n')
    stream.write('  INCLUDE ../msh/%s.fix.dat\n' % fileName)
    stream.write('END_BOUNDARY_CONDITIONS\n')
    stream.write('$-------------------------------------------------------------------\n')
    stream.write('FIELDS\n')
    stream.write('  INCLUDE ../msh/%s.fie.dat\n' % fileName)
    stream.write('END_FIELDS\n')
    stream.write('$-------------------------------------------------------------------\n')
    
    stream.close()

    
