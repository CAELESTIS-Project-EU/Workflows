USER=bsc19518
NAMEFILE=gsa_OHT_Validation_D2_add241dc-8fa9-4edc-930f-1899721e31f6.yaml
WORKFLOW_FOLDER=/gpfs/scratch/bsc19/bsc19518/results/execution_f9bc9ed1-6406-4eac-a553-0305ac27d191/workflows
EXECUTION_FOLDER=/gpfs/scratch/bsc19/bsc19518/results/execution_f9bc9ed1-6406-4eac-a553-0305ac27d191/execution 
NUM_NODES=50
EXEC_TIME=1440
QOS=bsc_cs
INSTALL_DIR=/home/bsc19/bsc19518/installWorkflow/

export ALYA_BIN=/gpfs/projects/bsce81/alya/builds/Alya_no3.x
export ALYA_PROCS=64
export ALYA_PPN=16

module purge
module load oneapi/2021.4.0
module load intel/2021.4.0
module load impi/2021.4.0
module load ALYA/mpio
module load mkl/2021.4
module load boost/1.78.0
module load python/3.9.10

export PYTHONPATH=$INSTALL_DIR:$PYTHONPATH

module load compss/TrunkRC
# shellcheck disable=SC2164
cd $EXECUTION_FOLDER
enqueue_compss -g -t -d --worker_working_dir=$PWD --checkpoint_params=instantiated.group:1 --checkpoint=es.bsc.compss.checkpoint.policies.CheckpointPolicyInstantiatedGroup --checkpoint_folder=$EXECUTION_FOLDER/tmp/checkpointing/  --scheduler=es.bsc.compss.scheduler.orderstrict.fifo.FifoTS --job_execution_dir=$EXECUTION_FOLDER --qos=$QOS --exec_time=$EXEC_TIME --pythonpath=$PYTHONPATH --num_nodes=$NUM_NODES --worker_in_master_cpus=16 $INSTALL_DIR/BACKEND/api.py $WORKFLOW_FOLDER/$NAMEFILE $EXECUTION_FOLDER

echo DONEEE

