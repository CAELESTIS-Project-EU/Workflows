#!/bin/bash
#
#  Submit jobs in NO3
#     sbatch < job.sh
#
#SBATCH --job-name=oht-udg
#SBATCH --chdir=.
#SBATCH --error=%j.err
#SBATCH --output=%j.out
#SBATCH --qos=debug
#SBATCH --ntasks=672
#SBATCH --cpus-per-task=1
#SBATCH --ntasks-per-node=48
##SBATCH --constraint=highmem
#SBATCH --time=00:40:00
#
# Load modules for the executable
#
#module purge
#module load oneapi/2021.4.0
#module load intel/2021.4.0
#module load impi/2021.4.0
#module load ALYA/mpio
#module load intel/2017.4
#module load impi/2017.4
#module load mkl/2017.4
#module load ALYA/mpio

PROBLEMNAME=FEM_OHT_nom

#ALYAPATH="/gpfs/projects/bsce81/alya/builds/Alya_mn4.x"
#ALYAPATH="/home/bsc21/bsc21946/alya/master/build_x/src/alya/alya"
ALYAPATH="/home/bsc21/bsc21946/alya/1792-alya-single-precision/build_x_mn4/src/alya/alya"
#
# Launches ALYA
#
srun $ALYAPATH $PROBLEMNAME
