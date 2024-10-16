DEST_PATH="$1"
export ALYA_BIN=/gpfs/projects/bsce81/alya/builds/Alya_no3.x
export ALYA_PROCS=32
export ALYA_PPN=16

module purge
module load oneapi/2021.4.0
module load intel/2021.4.0
module load impi/2021.4.0
module load ALYA/mpio
module load mkl/2021.4
module load boost/1.78.0
module load python/3.9.10

export PYTHONPATH=$DEST_PATH:$PYTHONPATH
