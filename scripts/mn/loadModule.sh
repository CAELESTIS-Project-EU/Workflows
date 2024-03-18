DEST_PATH="$1"
export ALYA_BIN=/gpfs/projects/bsce81/alya/builds/Alya_mn4_sp.x
export ALYA_PROCS=48
export ALYA_PPN=48
export gmshBinFile=/gpfs/projects/bsce81/gmsh/gmsh-4.11.1-Linux64/bin/gmsh
export gmsh2alya=/gpfs/projects/bsce81/alya/builds/gmsh2alya.pl
module purge
module load intel/2020.1
module load impi/2018.4
module load mkl/2018.4
module load dislib/0.9.0
module load ALYA/mpio
module load python/3.9.10


export PYTHONPATH=$DEST_PATH:$PYTHONPATH

