USER=bsc19518
NAMEFILE=montecarlo_FEM_OHT_nom_daac1321-0982-43af-808e-04f415359fdf.yaml
WORKFLOW_FOLDER=/gpfs/scratch/bsc19/bsc19518/results/execution_a093561f-ad6d-4748-8c56-7bf309626f0f/workflows
EXECUTION_FOLDER=/gpfs/scratch/bsc19/bsc19518/results/execution_a093561f-ad6d-4748-8c56-7bf309626f0f/execution
NUM_NODES=12
EXEC_TIME=1440
QOS=bsc_cs
INSTALL_DIR=/home/bsc19/bsc19518/installWorkflow/
BRANCH=main
DATA_DIR=/home/bsc19/bsc19518/data_dir/

export ALYA_BIN=/gpfs/projects/bsce81/alya/builds/Alya_no3.x
export ALYA_PROCS=192
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

