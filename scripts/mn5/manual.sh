USER=bsc19518
NAMEFILE=test.yaml
WORKFLOW_FOLDER=/home/bsc/bsc019518/experiment
EXECUTION_FOLDER=/home/bsc/bsc019518/experiment/execution
NUM_NODES=2
EXEC_TIME=120
QOS=gp_debug
INSTALL_DIR=/home/bsc/bsc019518/install_workflow/
DATA_DIR=/home/bsc/bsc019518/data/

export ALYA_BIN=/gpfs/projects/cns100/examples/cantilever/Executables/Alya_mn5g.x
export ALYA_PROCS=56
export ALYA_PPN=16

module purge
# alya modules
module load ucx/1.15.0-gcc openmpi/4.1.5-gcc
# python modules
module load mkl hdf5/1.14.1-2-gcc-openmpi python/3.12.1-gcc
# gmesh modules
module load intel gmsh/4.12.2
# COMPSs module
module load COMPSs/3.3

export COMPSS_MPIRUN_TYPE=ompi


export PYTHONPATH=$INSTALL_DIR:$PYTHONPATH

# shellcheck disable=SC2164
cd $EXECUTION_FOLDER
enqueue_compss -g -t -d --worker_working_dir=$PWD --scheduler=es.bsc.compss.scheduler.orderstrict.fifo.FifoTS --job_execution_dir=$EXECUTION_FOLDER --qos=$QOS --exec_time=$EXEC_TIME --pythonpath=$PYTHONPATH --num_nodes=$NUM_NODES --worker_in_master_cpus=112 /home/bsc/bsc019518/install_workflow/Workflows/WORKFLOWS/api.py $WORKFLOW_FOLDER/$NAMEFILE $EXECUTION_FOLDER $DATA_DIR

echo DONEEE

