DEST_PATH="$1"
export ALYA_BIN=/gpfs/projects/bsc19/CAELESTIS/alya/builds/Alya_no3.x
export ALYA_PROCS=32
export ALYA_PPN=16
export RVEGEN_CUS=16
export gmshBinFile=/gpfs/projects/bsce81/gmsh/gmsh-4.11.1-Linux64/bin/gmsh
export gmsh2alya=/gpfs/projects/bsc19/CAELESTIS/alya/builds/gmsh2alya.pl
PAMHOME=/gpfs/projects/bsce81/MN4/bsce81/esi
PAMENV=$PAMHOME/env-`uname`
export PAMHOME PAMENV
if [ -r $PAMENV/psi.Baenv ]; then
    . $PAMENV/psi.Baenv
fi


module purge
module load intel/2021.4.0
module load mkl/2021.4
module load impi/2021.4.0
module load oneapi/2021.4.0
module load boost/1.78.0
module load ALYA/mpio
module load dislib/master
module load python/3.9.10
module load compss/3.3.1

export PYTHONPATH=$DEST_PATH:$PYTHONPATH


