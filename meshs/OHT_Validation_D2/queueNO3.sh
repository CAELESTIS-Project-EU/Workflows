#!/bin/bash
#
#  Submit jobs in NO3
#     sbatch < job.sh
#
#SBATCH --job-name=oht-aravind
#SBATCH --chdir=.
#SBATCH --error=%j.err
#SBATCH --output=%j.out
#SBATCH --qos=debug
#SBATCH --ntasks=64
#SBATCH --cpus-per-task=1
#SBATCH --ntasks-per-node=16
##SBATCH --constraint=highmem
#SBATCH --time=01:00:00
#
# Load modules for the executable
#
module purge
module load oneapi/2021.4.0
module load intel/2021.4.0
module load impi/2021.4.0
module load ALYA/mpio

ALYAPATH="/gpfs/projects/bsce81/alya/builds/Alya_no3.x"
#ALYAPATH="/home/bsc21/bsc21946/alya/1792-alya-single-precision/build_x_no3/src/alya/alya"
#ALYAPATH="/home/bsc21/bsc21946/alya/1792-alya-single-precision/build_x_no3_sp/src/alya/alya"
#ALYAPATH="/home/bsc21/bsc21946/alya/1792-alya-single-precision/build_x_no3_sp_fix/src/alya/alya"
PROBLEMNAME=OHT_Validation_D2

#
# Launches ALYA
#
srun $ALYAPATH $PROBLEMNAME
