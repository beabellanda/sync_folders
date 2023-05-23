import os
import shutil
import datetime
import sys
import time
import argparse
import signal


def synchronize_folders(source, replica):
    # Create the replica folder if it doesn't exist
    if not os.path.exists(replica):
       os.makedirs(replica)

    # Iterate over all entries in the source folder
    for item in os.listdir(source):
        source_path = os.path.join(source, item)
        replica_path = os.path.join(replica, item)
        
        # Check if the entry is a directory
        if os.path.isdir(source_path):
            # Recursively synchronize the subfolders
         synchronize_folders(source_path, replica_path)
        else:
            # Copy the file from source to replica
         shutil.copy2(source_path, replica_path)

    filelog = open("logfile.txt", "a")
    x = datetime.datetime.now()
    filelog.write(x.strftime("%c")) 
    filelog.write("  Folders synchronized successfully. \n")
    filelog.close()
   

def start_synchronization(source_folder, replica_folder, interval):
    # Check if source folder exists
    if not os.path.exists(source_folder):
        print(f"Error: Source folder '{source_folder}' does not exist.")
        sys.exit(1)

    # Check if replica folder exists, create it if necessary
    if not os.path.exists(replica_folder):
        os.makedirs(replica_folder)
        print(f"Replica folder '{replica_folder}' created.")

    # Start the synchronization process
    while True:
        synchronize_folders(source_folder, replica_folder)
        # Sleep interval
        time.sleep(interval)


def stop_synchronization(signal, frame):
    print("\nSynchronization stopped.")
    sys.exit(0)



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Folder Synchronization Script')
    parser.add_argument('source_folder', help='path to the source folder')
    parser.add_argument('replica_folder', help='path to the replica folder')
    parser.add_argument('command', choices=['start', 'stop', 'log'], help='command to start or stop synchronization')
    parser.add_argument('--interval', type=int, default=10, help='synchronization interval in seconds')

    args, extra_args = parser.parse_known_args()

    source_folder = args.source_folder
    replica_folder = args.replica_folder
    command = args.command
    interval = args.interval

    if command == 'start':
        signal.signal(signal.SIGINT, stop_synchronization)
        start_synchronization(source_folder, replica_folder, interval)
        print("\nSynchronization started.")
    elif command == 'stop':
        stop_synchronization(None, None)
        print("\nSynchronization stopped.")
    if command == 'log':
        filelog= open("logfile.txt", "r")
        print(filelog.read())

# Set the paths for the source and replica folders
source_folder = 'source'
replica_folder = 'replica'


# Synchronize the folders
synchronize_folders(source_folder, replica_folder)

