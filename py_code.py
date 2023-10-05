import argparse
from dirsync import sync
import schedule
import time

# Parse command line arguments
def parse_args():
    parser = argparse.ArgumentParser(description="Folder synchronization script")
    parser.add_argument("source_path", help="Path to the source folder")
    parser.add_argument("replica_path", help="Path to the replica folder")
    parser.add_argument("sync_interval", type=int, help="Synchronization interval in seconds")
    parser.add_argument("log_file_path", help="Path to the log file")
    return parser.parse_args()

# Set up and run the synchronization
def run_sync(source_path, replica_path, sync_interval, log_file_path):
    # Open the file in append mode
    with open(log_file_path, 'a') as logger_file:

        class Logger:
            def info(self, message):
                print(message)
                logger_file.write(message + '\n')

        my_logger = Logger()

        def custom_sync():
            my_logger.info("Sync started.")
            sync(source_path, replica_path, 'sync', purge=True, logger=my_logger)  # sync one way
            my_logger.info("Sync completed.")

        schedule.every(sync_interval).seconds.do(custom_sync)

        while True:
            schedule.run_pending()
            time.sleep(1)

if __name__ == "__main__":
    
    # Parse command line arguments
    args = parse_args()

    # Run the synchronization with provided arguments
    run_sync(args.source_path, args.replica_path, args.sync_interval, args.log_file_path)