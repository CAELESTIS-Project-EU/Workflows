# Gnuplot script file for plotting data f-t curve
# Created by G.Guillamet <gerard.guillamet@bsc.es>

#set terminal aqua dashed enhanced
#set terminal x11 dashed nopersist enhanced font "arial,15"
#set terminal wxt dashed nopersist enhanced font "arial,12"
set terminal wxt dashed nopersist enhanced font "helvetica, 9"

set   autoscale                        # scale axes automatically
unset log                              # remove any log-scaling
unset label                            # remove any previous labels
set xtic auto                          # set xtics automatically
set ytic auto                          # set ytics automatically
set xlabel "Time (ms)"
set ylabel "STI (s)"
set xr [0:0.65]
#set yr [6e-9:9.9e-9]
set key right top
set grid
set size square
#
# define line styles using explicit rgbcolor names
#
#set for [i=1:3] linetype i dashtype i
set style line 1 lt 1 lc rgb "black" lw 2
set style line 2 lt 1 lc rgb "red" lw 2
set style line 3 lt 1 lc rgb "blue" lw 2
set style line 4 lt 1 lc rgb "green" lw 1
set style line 5 lt 1 lc rgb "orange" lw 1
set style line 6 lt 2 lc rgb "grey" lw 1
set style line 7 lt 2 lc rgb "green" lw 1
   
plot "./base/1p/OHT_Validation_D2.sld.cvg" using (1e+3*$5):($6) title 'STI no-vecto' with lines ls 1, \
     "OHT_Validation_D2.sld.cvg" using (1e+3*$5):($6) title 'STI vecto' with lines ls 2
