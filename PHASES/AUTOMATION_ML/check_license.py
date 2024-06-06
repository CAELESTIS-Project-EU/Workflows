from pycompss.api.task import task
from pycompss.api.parameter import *
from pycompss.api.container import container
from pycompss.api.binary import binary
import subprocess


@task(returns=1)
def check_license():
    script = "/gpfs/projects/bsce81/check_license_server.sh"

    try:
        # Execute the shell script and capture the output
        result = subprocess.run([script], capture_output=True, text=True, check=True)

        # Check if the expected output is in the script's output
        if "License Server is already running" in result.stdout:
            print("License Server is already running")
            return True
        else:
            raise Exception("Unexpected output: License Server is not running")

    except subprocess.CalledProcessError as e:
        raise Exception(f"Script execution failed: {e}")