# Gnuplot script file for plotting data f-d curve
# Created by G.Guillamet <gerard.guillamet@bsc.es>
set   autoscale                        # scale axes automatically
unset log                              # remove any log-scaling
unset label                            # remove any previous labels
set xtic auto                          # set xtics automatically
set ytic auto                          # set ytics automatically
set xlabel "Max. displacement (mm)"
set ylabel "Energy fraction (%)"
set yr [0:6.0]
set xr [0:20.0]
set key right top
set grid
set size square

#
# define line styles using explicit rgbcolor names
#
#set for [i=1:3] linetype i dashtype i
set style line 1 lt 1 lc rgb "black" lw 1.5
set style line 2 lt 2 lc rgb "red" lw 1.5
set style line 3 lt 1 lc rgb "blue" lw 1.5
#set style line 4 lt 2 lc rgb "green" lw 1.5
#set style line 5 lt 2 lc rgb "orange" lw 1.5
#set style line 6 lt 2 lc rgb "grey" lw 1.5
#set style line 7 lt 2 lc rgb "green" lw 1.5

set arrow from 0.0,5.0 to 20.0,5.0 nohead linestyle 2

plot "fuse.sld.cvg" using ($10):($13/$14*100.) title "ALLKE/ETOTA" with lines ls 1, \
     "fuse.sld.cvg" using ($10):($13/$11*100.) title "ALLKE/ALLIE" with lines ls 3

