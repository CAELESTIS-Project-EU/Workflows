# Usage: ./run.sh ogv.yaml test_ogv 1 120
# Usage: ./run.sh poc1.yaml test_poc1 1 60

if [ "$#" -ne 4 ]; then
    echo "Illegal number of parameters($#)"
    echo "Usage: run.sh <yaml_file> <execution_name> <num_nodes> <exec_time>"
    exit 1
fi


YAML=/gpfs/scratch/bsc21/bsc021946/CAELESTIS/full-workflow/Workflows/examples/MANUFACTURING_AND_MECHANICAL/yamls/$1
EXEC_NAME=$2
NUM_NODES=$3
EXEC_TIME=$4

EXECUTION_FOLDER=/gpfs/scratch/bsc21/bsc021946/CAELESTIS/full-workflow/Workflows/examples/MANUFACTURING_AND_MECHANICAL/execution/${EXEC_NAME}/
mkdir -p $EXECUTION_FOLDER/results/
QOS=bsc_case
PROJECT=bsc21
INSTALL_DIR=/gpfs/scratch/bsc21/bsc021946/CAELESTIS/full-workflow/Workflows/
DATA_DIR=/gpfs/scratch/bsc21/bsc021946/CAELESTIS/full-workflow/data/
COUPONTOOL=/gpfs/scratch/bsc21/bsc021946/CAELESTIS/full-workflow/COUPONtool

PAMHOME=/gpfs/projects/bsce81/MN4/bsce81/esi_25
PAMENV=$PAMHOME/env-`uname`
export PAMHOME PAMENV
if [ -r $PAMENV/psi.Baenv ]; then
    . $PAMENV/psi.Baenv
fi

export ALYA_BIN=/gpfs/projects/bsce81/alya/builds/Alya_no4i.x
export ALYA_PROCS=48
export ALYA_PPN=48
export ALYA_TIMEOUT=3600

module purge
module load intel/2018.4
module load impi/2018.4
module load mkl/2018.4
module load boost/1.78.0
module load dislib/master
module load python/3.9.10

export COMPSS_MPIRUN_TYPE=impi
export PYTHONPATH=$COUPONTOOL:$PYTHONPATH
export PYTHONPATH=$INSTALL_DIR:$PYTHONPATH

# shellcheck disable=SC2164
cd $EXECUTION_FOLDER
enqueue_compss --project_name=$PROJECT --network=ethernet --output_profile=$EXECUTION_FOLDER/time --keep_workingdir --log_dir=$EXECUTION_FOLDER --worker_working_dir=$PWD --scheduler=es.bsc.compss.scheduler.orderstrict.fifo.FifoTS --job_execution_dir=$EXECUTION_FOLDER --qos=$QOS --exec_time=$EXEC_TIME --pythonpath=$PYTHONPATH --num_nodes=$NUM_NODES --worker_in_master_cpus=48 $INSTALL_DIR/WORKFLOWS/api.py $YAML $EXECUTION_FOLDER $DATA_DIR

echo DONE!

