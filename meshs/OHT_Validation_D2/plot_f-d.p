# Gnuplot script file for plotting data f-d curve
# Created by G.Guillamet <gerard.guillamet@bsc.es>
set   autoscale                        # scale axes automatically
unset log                              # remove any log-scaling
unset label                            # remove any previous labels
set xtic auto                          # set xtics automatically
set ytic auto                          # set ytics automatically
set xlabel "Displacement (mm)"
set ylabel "Load (kN)"
set xr [0:0.5]
set yr [0:30.0]
set key right top
set grid
set size square
#
# define line styles using explicit rgbcolor names
#
#set for [i=1:3] linetype i dashtype i
set style line 1 lt 1 lc rgb "black" lw 1.7
set style line 2 lt 1 lc rgb "red" lw 1.7
set style line 3 lt 1 lc rgb "blue" lw 1.7
set style line 4 lt 2 lc rgb "green" lw 1.7
set style line 5 lt 2 lc rgb "orange" lw 1.5
#set style line 6 lt 2 lc rgb "grey" lw 1.5
#set style line 7 lt 2 lc rgb "green" lw 1.5

execution_id = "execution_d93d431a-3bf2-4d3b-807c-072a43da0d69"
caseName = "OHT_Validation_D2"
sampleId = "s159"

jobName = caseName . "-" . sampleId
#pathJobFile = "/gpfs/projects/bsce81/alya/tests/test_Aravind/" . execution_id . "/execution/SIMULATIONS/" . jobName . "/" . jobName
pathJobFile = caseName
pathRefFile = "/gpfs/projects/bsce81/alya/tests/workflow_stable/meshs/" . caseName . "/base/1p/" . caseName

plot "./base/1p/experiment.txt" using (1*$1):(1e-3*$2) title 'Experiment' with lines ls 1, \
     "./base/1p/Abaqus-".caseName.".txt" using (1*$1):(1e-3*$2) title 'Baseline (Abaqus)' with lines ls 2, \
     pathRefFile."-reaction.sld.res" using (1*$3):(1e-3*$6) title 'Baseline (Alya)' with lines ls 3, \
     pathJobFile."-reaction.sld.res" using (1*$3):(1e-3*$6) title 'Current' with lines ls 4
