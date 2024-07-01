DEST_PATH="$1"
export ALYA_BIN=/gpfs/projects/cns100/alya/builds/Alya_mn5g.x
export ALYA_PROCS=112
export ALYA_PPN=112

module purge
# python modules
module load intel impi  mkl hdf5 python/3.12.1
module load dislib/master
module unload intel impi
# alya modules
module load gcc ucx/1.15.0-gcc openmpi/4.1.5-gcc
# gmsh modules
module load intel gmsh/4.12.2
# COMPSs module
module load COMPSs/3.3.1
module load singularity
module load dislib/master

export COMPSS_MPIRUN_TYPE=openmpi


export PYTHONPATH=$DEST_PATH:/gpfs/projects/cns100/pips/python3.12/site-packages/:$INSTALL_DIR:$PYTHONPATH:/gpfs/projects/cns100/tests/install_workflow_coupontool/
