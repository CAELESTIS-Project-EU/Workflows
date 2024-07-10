USER=$1
NAMEFILE=$2
WORKFLOW_FOLDER=$3
EXECUTION_FOLDER=$4
NUM_NODES=$5
EXEC_TIME=$6
QOS=$7
INSTALL_DIR=$8
BRANCH=$9
DATA_DIR=${10}
gOPTION=${11}
tOPTION=${12}
dOPTION=${13}
PROJECT_NAME=${14}
# shellcheck disable=SC2164
cd $EXECUTION_FOLDER

# Construct the enqueue_compss command based on user options
enqueue_compss_cmd="enqueue_compss --worker_working_dir=$PWD --project_name=$PROJECT_NAME --job_execution_dir=$EXECUTION_FOLDER --log_dir=$EXECUTION_FOLDER --qos=$QOS --exec_time=$EXEC_TIME --pythonpath=$PYTHONPATH --num_nodes=$NUM_NODES --worker_in_master_cpus=16"

# Add -g option if specified
if [ "$gOPTION" = "true" ]; then
  enqueue_compss_cmd="$enqueue_compss_cmd -g"
fi

# Add -t option if specified
if [ "$tOPTION" = "true" ]; then
  enqueue_compss_cmd="$enqueue_compss_cmd -t"
fi

# Add -d option if specified
if [ "$dOPTION" = "true" ]; then
  enqueue_compss_cmd="$enqueue_compss_cmd -d"
fi

# Add the rest of the command
enqueue_compss_cmd="$enqueue_compss_cmd $INSTALL_DIR/$BRANCH/WORKFLOWS/api.py $WORKFLOW_FOLDER/$NAMEFILE $EXECUTION_FOLDER $DATA_DIR"

# Execute the command
$enqueue_compss_cmd
echo $enqueue_compss_cmd
echo DONEEE

