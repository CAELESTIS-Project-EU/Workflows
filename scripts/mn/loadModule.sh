DEST_PATH="$1"
export ALYA_BIN=/gpfs/projects/bsce81/alya/builds/Alya_mn4.x
export ALYA_PROCS=96
export ALYA_PPN=48

module purge
module load intel/2018.4
module load impi/2018.4
module load ALYA/mpio
module load mkl/2018.4
module load boost/1.80.0
module load python/3.9.10

export PYTHONPATH=$DEST_PATH:$PYTHONPATH