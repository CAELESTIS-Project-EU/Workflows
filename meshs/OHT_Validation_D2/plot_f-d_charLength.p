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
set key left top
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
set style line 4 lt 2 lc rgb "green" lw 1.7
set style line 5 lt 2 lc rgb "orange" lw 1.7
set style line 6 lt 2 lc rgb "grey" lw 1.7
#set style line 7 lt 2 lc rgb "green" lw 1.5

plot "./base/1p/OHT_Validation_D2-reaction-MIN.sld.res" using (1*$3):(1e-3*$6) title 'MIN' with lines ls 2, \
     "./base/1p/OHT_Validation_D2-reaction-MAX.sld.res" using (1*$3):(1e-3*$6) title 'MAX' with lines ls 3, \
     "./base/1p/OHT_Validation_D2-reaction-LFACE.sld.res" using (1*$3):(1e-3*$6) title 'LFACE=MIN' with lines ls 4, \
     "./base/1p/OHT_Validation_D2-reaction-VOLUME.sld.res" using (1*$3):(1e-3*$6) title 'VOLUME' with lines ls 5, \
     "./base/1p/OHT_Validation_D2-reaction-AVERAGE.sld.res" using (1*$3):(1e-3*$6) title 'AVERAGE' with lines ls 6
