# Gnuplot script file for plotting data f-t curve
# Created by G.Guillamet <gerard.guillamet@bsc.es>

#set terminal aqua dashed enhanced
#set terminal x11 dashed nopersist enhanced font "arial,15"
#set terminal wxt dashed nopersist enhanced font "arial,12"
#set terminal wxt dashed nopersist enhanced font "helvetica, 9"

set   autoscale                        # scale axes automatically
unset log                              # remove any log-scaling
unset label                            # remove any previous labels
set xtic auto                          # set xtics automatically
set ytic auto                          # set ytics automatically
set xlabel "Time steps (-)"
set ylabel "dtcri (s)"
#set xr [0:5.0]
#set yr [0:9.0]
#set format y "%2.0t{/Symbol \327}10^{%L}"
#set format y "10^{%L}"
set format y "%.1t*10^%+03T"
set key right bottom
set grid
set size square
#
# define line styles using explicit rgbcolor names
#
#set for [i=1:3] linetype i dashtype i
set style line 1 lt 1 lc rgb "black" lw 1.5
set style line 2 lt 1 lc rgb "red" lw 1.5
set style line 3 lt 1 lc rgb "blue" lw 1.5
set style line 4 lt 1 lc rgb "green" lw 1.5
set style line 5 lt 1 lc rgb "orange" lw 1.5
set style line 6 lt 1 lc rgb "pink" lw 1.5
set style line 7 lt 1 lc rgb "cyan" lw 1.5

plot "./base/1p/OHT_Validation_D2.sld.cvg" using ($1):($6) title 'dtcri novecto' with lines ls 1, \
     "OHT_Validation_D2.sld.cvg" using ($1):($6) title 'dtcri vecto' with lines ls 2
