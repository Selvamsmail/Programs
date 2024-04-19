import pandas as pd
import os 
import shutil
import time

def save_data_to_disk(data, filename):
    max_attempts = 5  # Maximum number of attempts
    wait_time = 5  # Time to wait between attempts (in seconds)
    
    for _ in range(max_attempts):
        try:
            if not os.path.isfile(filename):  # Check if file exists
                # If file doesn't exist, create a new one with the data
                data.to_parquet(filename, index=False)
                break  # Break out of the loop after creating the file
            
            pd.read_parquet(filename)
            backup_filename = filename + 'bak.parquet'
            if os.path.isfile(backup_filename):
                os.remove(backup_filename)  # Remove old backup before creating a new one
            shutil.copyfile(filename, backup_filename)
            
            existing_df = pd.read_parquet(filename)
            data = pd.concat([existing_df, data], ignore_index=True)
            data.to_parquet(filename, index=False)
            break  # Break out of the loop if successful
        
        except Exception as e:
            print(f"Error: {e}")
            print(f"File '{filename}' is in use. Waiting {wait_time} seconds before trying again...")
            time.sleep(wait_time)
    else:
        raise Exception(f"Failed to save data to '{filename}' after {max_attempts} attempts.")
