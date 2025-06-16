def writePosOGV(file, ux, uy, uz, jobName):
    """ Gnuplot plot_f-d.p file
    """
    
    stream = open(file, 'w')

    stream.write('set   autoscale                        # scale axes automatically\n')
    stream.write('unset log                              # remove any log-scaling\n')
    stream.write('unset label                            # remove any previous labels\n')
    stream.write('set xtic auto                          # set xtics automatically\n')
    stream.write('set ytic auto                          # set ytics automatically\n')

    stream.write('set xlabel "Displacement (mm)"\n')
    stream.write('set ylabel "Force (kN)"\n')
    
    stream.write('set key right top\n')
    stream.write('set grid\n')
    stream.write('set size square\n')

    stream.write('#\n')
    stream.write('# define line styles using explicit rgbcolor names\n')
    stream.write('#\n')
    stream.write('#set for [i=1:3] linetype i dashtype i\n')
    stream.write('set style line 1 lt 1 lc rgb "black" lw 3.5 pt 2\n')
    stream.write('set style line 2 lt 1 lc rgb "red" lw 3.5 pt 2\n')
    stream.write('set style line 3 lt 1 lc rgb "blue" lw 1.5 pt 2\n')


    if ux > 0 and ux != 0.0:
        stream.write(f'plot "{jobName}-reaction.sld.res" using ($2):($5*1e-3) title "Alya" with lines ls 1\n')
    elif ux < 0 and ux != 0.0:
        stream.write(f'plot "{jobName}-reaction.sld.res" using (-1*$2):(-1*$5*1e-3) title "Alya" with lines ls 1\n')

    if uy > 0 and uy != 0.0:  
        stream.write(f'plot "{jobName}-reaction.sld.res" using ($3):($6*1e-3) title "Alya" with lines ls 1\n')
    elif uy < 0 and uy != 0.0:
        stream.write(f'plot "{jobName}-reaction.sld.res" using (-1*$3):(-1*$6*1e-3) title "Alya" with lines ls 1\n')

    stream.close()

    return
