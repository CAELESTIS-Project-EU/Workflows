from pycompss.api.task import task
import subprocess
import time
from datetime import datetime

@task()
def check_license(max_retries=3, retry_delay=30):

    script = "/gpfs/projects/bsce81/check_license_server_new.sh"
    
    for attempt in range(max_retries):
        try:
            print(f"{datetime.now()} - License check attempt {attempt + 1}/{max_retries}")
            result = subprocess.run(
                [script],
                capture_output=True,
                text=True,
                check=True,
                timeout=120  # Add timeout to prevent hanging
            )
            
            if result.returncode == 0:
                print(f"{datetime.now()} - License verified successfully")
                print(result.stdout)
                return True
                
            print(f"{datetime.now()} - License check failed (attempt {attempt + 1}):")
            print(result.stderr)
            
        except subprocess.TimeoutExpired:
            print(f"{datetime.now()} - License check timed out (attempt {attempt + 1})")
            
        except subprocess.CalledProcessError as e:
            print(f"{datetime.now()} - License check failed (attempt {attempt + 1}):")
            print(f"Exit code: {e.returncode}")
            print(f"Error output: {e.stderr}")
        
        if attempt < max_retries - 1:
            print(f"{datetime.now()} - Waiting {retry_delay} seconds before retry...")
            time.sleep(retry_delay)
    
    print(f"{datetime.now()} - Maximum retries reached. License server unavailable.")
    return False