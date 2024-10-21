# Usage: run.sh <yaml_file> <execution_name> <num_nodes> <exec_time>


if [ "$#" -ne 4 ]; then
    echo "Illegal number of parameters($#)"
    echo "Usage: run.sh <yaml_file> <execution_name> <num_nodes> <exec_time>"
    exit 1
fi


YAML=/gpfs/scratch/bsce81/BSC_FULL_WORKFLOW/install_dir/Workflows/examples/MANUFACTURING_AND_MECHANICAL/yamls/$1
EXEC_NAME=$2
NUM_NODES=$3
EXEC_TIME=$4
EXECUTION_FOLDER=/gpfs/scratch/bsce81/BSC_FULL_WORKFLOW/executions/${EXEC_NAME}/
mkdir -p $EXECUTION_FOLDER/results/
QOS=debug
PROJECT=bsce81
INSTALL_DIR=/gpfs/scratch/bsce81/BSC_FULL_WORKFLOW/install_dir
DATA_DIR=/gpfs/scratch/bsce81/BSC_FULL_WORKFLOW/data/

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

export COMPSS_MPIRUN_TYPE=impi

export PYTHONPATH=$INSTALL_DIR:$PYTHONPATH

# shellcheck disable=SC2164
cd $EXECUTION_FOLDER
enqueue_compss -d --project_name=$PROJECT --constraints=medmem --network=ethernet --output_profile=$EXECUTION_FOLDER/time --keep_workingdir --log_dir=$EXECUTION_FOLDER --worker_working_dir=$PWD --scheduler=es.bsc.compss.scheduler.orderstrict.fifo.FifoTS --job_execution_dir=$EXECUTION_FOLDER --qos=$QOS --exec_time=$EXEC_TIME --pythonpath=$PYTHONPATH --num_nodes=$NUM_NODES --worker_in_master_cpus=16 $INSTALL_DIR/WORKFLOWS/api.py $YAML $EXECUTION_FOLDER $DATA_DIR

echo DONE!

