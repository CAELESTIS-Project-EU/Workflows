from pycompss.api.task import task
from pycompss.api.parameter import *
from pycompss.api.container import container
from pycompss.api.binary import binary
import subprocess


def check_license():
    script = "/gpfs/projects/bsce81/check_license_server.sh"

    try:
        # Execute the shell script
        result = subprocess.run([script], capture_output=True, text=True)

        # Check the exit code of the script
        if result.returncode == 0:
            print("License Server is already running or started successfully.")
            return True
        else:
            print("License Server is not running and could not be started. Check the log file for details.")
            print(result.stdout)
            print(result.stderr)
            return False
    except subprocess.CalledProcessError as e:
        print(f"Script execution failed: {e}")
        return False
