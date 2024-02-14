

def writeJobLauncher(path, fileName, queue, numCPUs):
    """ Job Launcher for Nord3v3
    """

    stream = open(path+'queueNO3.sh', 'w', newline='\n')

    stream.write('#!/bin/bash\n')
    stream.write('##\n')
    stream.write('##  Submit jobs in Nord3v2\n')
    stream.write('##     sbatch < job.sh\n')
    stream.write('##\n')
    stream.write(f'#SBATCH --job-name={fileName:s}\n')
    stream.write('#SBATCH --chdir=.\n')
    stream.write('#SBATCH --error=%j.err\n')
    stream.write('#SBATCH --output=%j.out\n')
    stream.write(f'#SBATCH --qos={queue:s}\n')
    stream.write(f'#SBATCH --ntasks={numCPUs:g}\n')
    stream.write('#SBATCH --cpus-per-task=1\n')
    stream.write('#SBATCH --ntasks-per-node=16\n')
    stream.write('#SBATCH --time=02:00:00\n')
    stream.write('##\n')
    stream.write('## Load modules for the executable\n')
    stream.write('##\n')
    stream.write('module purge\n')
    stream.write('module load oneapi/2021.4.0\n')
    stream.write('module load intel/2021.4.0\n')
    stream.write('module load impi/2021.4.0\n')
    stream.write('module load ALYA/mpio\n')
    stream.write('##\n')
    stream.write('ALYAPATH="/gpfs/projects/bsce81/alya/builds/Alya_no3.x"\n')
    stream.write(f'PROBLEMNAME={fileName:s}\n')
    stream.write('##\n')
    stream.write('## Launches ALYA\n')
    stream.write('##\n')
    stream.write('srun $ALYAPATH $PROBLEMNAME\n')
