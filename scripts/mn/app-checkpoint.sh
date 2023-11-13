USER=$1
NAMEFILE=$2
WORKFLOW_FOLDER=$3
EXECUTION_FOLDER=$4
NUM_NODES=$5
EXEC_TIME=$6
QOS=$7
INSTALL_DIR=$8
BRANCH=$9
module load compss/3.2
# shellcheck disable=SC2164
cd $EXECUTION_FOLDER
enqueue_compss -d -g -t --worker_working_dir=$PWD --scheduler=es.bsc.compss.scheduler.orderstrict.fifo.FifoTS --job_execution_dir=$EXECUTION_FOLDER --qos=$QOS --exec_time=$EXEC_TIME --pythonpath=$PYTHONPATH --num_nodes=$NUM_NODES --worker_in_master_cpus=16 --checkpoint_params=instantiated.group:1 --checkpoint=es.bsc.compss.checkpoint.policies.CheckpointPolicyInstantiatedGroup --checkpoint_folder=$EXECUTION_FOLDER/tmp/checkpointing/ $INSTALL_DIR/$BRANCH/BACKEND/api.py $WORKFLOW_FOLDER/$NAMEFILE $EXECUTION_FOLDER

echo DONEEE

