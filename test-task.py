import os
import shutil
import time
import argparse

# Define color codes for terminal output
RED = "\033[91m"
GREEN = "\033[32m"
BLUE = "\033[34m"
YELLOW = "\033[33m"
RESET = "\033[0m"

class Log:
    def __init__(self, log_file_path):
        self.running = True
        self.log_file_path = log_file_path
        try:
            open(log_file_path, "x")  # Attempt to create the log file
        except FileExistsError:
            print(f"{RED}Error: File \"{log_file_path}\" already exists{RESET}")

    def log_message(self, message, color):
        # Print to the terminal with color
        colored_message = f"{color}{message}{RESET}"
        print(colored_message)

        # Write to the log file without color
        with open(self.log_file_path, "a") as log_file:
            log_file.write(message + "\n")  # Write the plain message to the log file

class Sync:
    def __init__(self, source_dir, replica_dir, logger):
        self.source_dir = source_dir
        self.replica_dir = replica_dir
        self.logger = logger

    def synchronize(self):
        """Synchronize the replica folder to match the source folder."""

        # Create source folder if it doesn't exist
        if not os.path.exists(self.source_dir):
            os.makedirs(self.source_dir)
            self.logger.log_message(f"Folder created: {self.source_dir}", GREEN)

        # Create replica folder if it doesn't exist
        if not os.path.exists(self.replica_dir):
            os.makedirs(self.replica_dir)
            self.logger.log_message(f"Folder created: {self.replica_dir}", GREEN)

        # Create a set of existing files in the replica
        replica_files = {item: os.path.join(self.replica_dir, item) for item in os.listdir(self.replica_dir)}

        # Copy files from source to replica
        for item in os.listdir(self.source_dir):
            src_path = os.path.join(self.source_dir, item)
            dest_path = os.path.join(self.replica_dir, item)

            if os.path.isdir(src_path):
                # If the item is a directory
                if not os.path.exists(dest_path):
                    try:
                        shutil.copytree(src_path, dest_path)
                        self.logger.log_message(f"Copied directory: {src_path} to {dest_path}", BLUE)
                    except Exception as e:
                        self.logger.log_message(f"Error copying directory {src_path}: {e}", RED)
                else:
                    # If the directory exists, recursively synchronize it
                    self.synchronize_directory(src_path, dest_path)
            else:
                # If the item is a file
                try:
                    if not os.path.exists(dest_path) or os.path.getmtime(src_path) > os.path.getmtime(dest_path):
                        shutil.copy2(src_path, dest_path)
                        self.logger.log_message(f"Copied file: {src_path} to {dest_path}", BLUE)
                except Exception as e:
                    self.logger.log_message(f"Error copying file {src_path}: {e}", RED)

        # Remove files from the replica that are no longer in the source
        for item in replica_files.keys():
            replica_path = replica_files[item]
            source_path = os.path.join(self.source_dir, item)

            if not os.path.exists(source_path):  # If item doesn't exist in the source
                try:
                    if os.path.isdir(replica_path):
                        shutil.rmtree(replica_path)  # Remove the directory
                        self.logger.log_message(f"Removed directory: {replica_path}", RED)
                    else:
                        os.remove(replica_path)  # Remove the file
                        self.logger.log_message(f"Removed file: {replica_path}", RED)
                except Exception as e:
                    self.logger.log_message(f"Error removing {replica_path}: {e}", RED)

    def synchronize_directory(self, source_dir, dest_dir):
        """Recursively synchronize contents of a directory."""
        for item in os.listdir(source_dir):
            src_path = os.path.join(source_dir, item)
            dest_path = os.path.join(dest_dir, item)

            if os.path.isdir(src_path):
                if not os.path.exists(dest_path):
                    try:
                        shutil.copytree(src_path, dest_path)
                        self.logger.log_message(f"Copied directory: {src_path} to {dest_path}", BLUE)
                    except Exception as e:
                        self.logger.log_message(f"Error copying directory {src_path}: {e}", RED)
                else:
                    self.synchronize_directory(src_path, dest_path)  # Recursively synchronize
            else:
                try:
                    if not os.path.exists(dest_path) or os.path.getmtime(src_path) > os.path.getmtime(dest_path):
                        shutil.copy2(src_path, dest_path)
                        self.logger.log_message(f"Copied file: {src_path} to {dest_path}", BLUE)
                except Exception as e:
                    self.logger.log_message(f"Error copying file {src_path}: {e}", RED)

def main():
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="Synchronize two folders: source and replica.")
    parser.add_argument("source", help="Path to the source directory.")
    parser.add_argument("replica", help="Path to the replica directory.")
    parser.add_argument("interval", type=int, help="Synchronization interval in seconds.")
    parser.add_argument("log_file", help="Path to the log file.")

    args = parser.parse_args()

    logger = Log(args.log_file)
    sync = Sync(args.source, args.replica, logger)

    while True:
        sync.synchronize()
        time.sleep(args.interval)

if __name__ == "__main__":
    main()
