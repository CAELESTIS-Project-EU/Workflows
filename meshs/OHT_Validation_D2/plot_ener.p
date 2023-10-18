# Gnuplot script file for plotting data f-d curve
# Created by G.Guillamet <gerard.guillamet@bsc.es>
set   autoscale                        # scale axes automatically
unset log                              # remove any log-scaling
unset label                            # remove any previous labels
set xtic auto                          # set xtics automatically
set ytic auto                          # set ytics automatically
set xlabel "Time (s)"
set ylabel "Energy (N·mm)"
set key right bottom
set grid
set size square

#
# define line styles using explicit rgbcolor names
#
#set for [i=1:3] linetype i dashtype i
#set style line 1 lt 1 lc rgb "black" lw 1.5
#set style line 2 lt 1 lc rgb "red" lw 1.5
#set style line 3 lt 1 lc rgb "blue" lw 1.5
#set style line 4 lt 2 lc rgb "green" lw 1.5
#set style line 5 lt 2 lc rgb "orange" lw 1.5
#set style line 6 lt 2 lc rgb "grey" lw 1.5
#set style line 7 lt 2 lc rgb "green" lw 1.5

plot "fuse.sld.cvg" using ($5):($11) title 'ALLIE' with lines, \
     "fuse.sld.cvg" using ($5):($12) title 'ALLEW' with lines, \
     "fuse.sld.cvg" using ($5):($13) title 'ALLKE' with lines, \
     "fuse.sld.cvg" using ($5):($14) title 'ETOTA' with lines

