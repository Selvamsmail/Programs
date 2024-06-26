import subprocess
import multiprocessing
import time

def run_script(script_name):
    subprocess.run(["python", script_name])

if __name__ == "__main__":
    # List of script names to run concurrently
    script_names = [
        "extractor1.py",
        "extractor2.py",
        "extractor3.py",  
    ]

    # Create a list to store process objects
    processes = [] 
    
    # Start a separate process for each script
    for script_name in script_names:
        process = multiprocessing.Process(target=run_script, args=(script_name,))
        processes.append(process)
        process.start()

    try:
        while True:
            # Count the number of running processes
            running_processes = sum(1 for process in processes if process.is_alive())
            print(f"Number of scripts running: {running_processes}")
            time.sleep(30)

    except KeyboardInterrupt:
        # Handle keyboard interrupt (Ctrl+C) to gracefully terminate the processes
        for process in processes:
            process.terminate() 

    finally:
        # Wait for all processes to complete
        for process in processes:
            process.join()
