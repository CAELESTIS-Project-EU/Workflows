# Gnuplot script file for plotting data f-d curve
# Created by G.Guillamet <gerard.guillamet@bsc.es>
set   autoscale                        # scale axes automatically
unset log                              # remove any log-scaling
unset label                            # remove any previous labels
set xtic auto                          # set xtics automatically
set ytic auto                          # set ytics automatically
set xlabel "Displacement (mm)"
set ylabel "Load (kN)"
#set xr [0:20.0]
#set yr [0:1500.0]
set key right top
set grid
set size square

#system("alya-sets OHT_Validation_D2-boundary.sld.set 3")
#
# define line styles using explicit rgbcolor names
#
#set for [i=1:3] linetype i dashtype i
set style line 1 lt 1 lc rgb "black" lw 1.7
set style line 2 lt 1 lc rgb "red" lw 1.7
set style line 3 lt 1 lc rgb "blue" lw 1.7
#set style line 4 lt 2 lc rgb "green" lw 1.5
#set style line 5 lt 2 lc rgb "orange" lw 1.5
#set style line 6 lt 2 lc rgb "grey" lw 1.5
#set style line 7 lt 2 lc rgb "green" lw 1.5

plot "./base/1p/abaqus.txt" using (1*$1):(1e-3*$2) title 'Abaqus' with lines ls 1, \
     "./base/1p/OHT_Validation_D2-reaction-green-v23-0.sld.res" using (1*$3):(1e-3*$6) title 'Alya Green v23=0.0' with lines ls 2, \
     "./base/1p/OHT_Validation_D2-reaction-infinitesimal-v23-0.sld.res" using (1*$3):(1e-3*$6) title 'Alya Infinitesimal v23=0.0' with lines ls 3
