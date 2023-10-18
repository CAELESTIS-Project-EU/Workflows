#!/bin/bash
#
#  Submit jobs in MN4
#     sbatch < job.sh
#
#SBATCH --job-name=oht-udg
#SBATCH --chdir=.
#SBATCH --error=%j.err
#SBATCH --output=%j.out
#SBATCH --qos=debug
#SBATCH --ntasks=144
#SBATCH --cpus-per-task=1
#SBATCH --ntasks-per-node=48
##SBATCH --constraint=highmem
#SBATCH --time=00:05:00
#
# Load modules for the executable
#
#module purge
#module load oneapi/2021.4
#module load impi/2018.4
#module load ALYA/mpio

#ALYAPATH="/home/bsc21/bsc21946/alya/master/build_x/src/alya/alya"
ALYAPATH="/home/bsc21/bsc21946/alya/1792-alya-single-precision/build_x_mn4/src/alya/alya"
PROBLEMNAME=OHT_Validation_D2
#
# Launches ALYA
#
srun $ALYAPATH $PROBLEMNAME
