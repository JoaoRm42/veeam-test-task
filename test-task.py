"""This is a program that synchronizes two folders: source and replica"""

# The lines `import os`, `import shutil`, `import time`, and `import argparse` are importing Python
# modules that provide various functionalities:
import os
import shutil
import time
import argparse


# The lines `RED = "\033[91m"`, `GREEN = "\033[32m"`, `BLUE = "\033[34m"`, `YELLOW = "\033[33m"`, and
# `RESET = "\033[0m"` are defining escape sequences for ANSI color codes. These escape sequences are
# used to change the text color in the terminal output.
RED = "\033[91m"
GREEN = "\033[32m"
BLUE = "\033[34m"
YELLOW = "\033[33m"
RESET = "\033[0m"


# The `Log` class initializes a log file and provides a method to log messages with color to the
# terminal and without color to the log file.
class Log:
    def __init__(self, log_file_path):
        """
        The function initializes an object with a log file path and attempts to create a new log file,
        displaying an error message if the file already exists.

        :param log_file_path: The `log_file_path` parameter in the `__init__` method is a string that
        represents the file path where the log file will be created or accessed. It is used to initialize
        the `log_file_path` attribute of the class instance
        """
        self.running = True
        self.log_file_path = log_file_path
        try:
            open(log_file_path, "x")  # Attempt to create the log file
        except FileExistsError:
            print(f'{RED}Error: File "{log_file_path}" already exists{RESET}')

    def log_message(self, message, color):
        """
        The `log_message` function prints a colored message to the terminal and writes the plain message to
        a log file.

        :param message: The `message` parameter is the text message that you want to log or display. It can
        be any string that you want to output to the terminal with color and write to a log file without
        color
        :param color: The `color` parameter in the `log_message` function is used to specify the color in
        which the message should be displayed in the terminal. It is a string that represents the color code
        or name that will be used to format the message when printing to the terminal
        """
        # Print to the terminal with color
        colored_message = f"{color}{message}{RESET}"
        print(colored_message)

        # Write to the log file without color
        with open(self.log_file_path, "a") as log_file:
            log_file.write(message + "\n")  # Write the plain message to the log file


# The `Sync` class provides methods to synchronize files and directories between a source
# folder and a replica folder while logging the operations.
class Sync:
    def __init__(self, source_dir, replica_dir, logger):
        """
        The function initializes an object with source directory, replica directory, and logger
        attributes.

        :param source_dir: The `source_dir` parameter in the `__init__` method is typically used to
        specify the directory path where the source files are located. This parameter allows you to
        provide the location of the source files that will be used or manipulated within the class or
        object
        :param replica_dir: The `replica_dir` parameter in the `__init__` method is typically used to
        specify the directory where a replica or copy of the source files will be stored. This parameter
        allows the class instance to know where to create or locate the replica files during the
        execution of the program
        :param logger: The `logger` parameter in the `__init__` method is typically used to pass a
        logging object that can be used to record events, errors, and other information during the
        execution of the class methods. This allows for better debugging and monitoring of the
        application
        """
        self.source_dir = source_dir
        self.replica_dir = replica_dir
        self.logger = logger

    def synchronize(self):
        """
        The `synchronize` function synchronizes the replica folder to match the source folder by
        creating missing folders, copying files from the source to the replica, and removing files from
        the replica that are no longer in the source.
        """

        # Create source folder if it doesn't exist
        if not os.path.exists(self.source_dir):
            os.makedirs(self.source_dir)
            self.logger.log_message(f"Folder created: {self.source_dir}", GREEN)

        # Create replica folder if it doesn't exist
        if not os.path.exists(self.replica_dir):
            os.makedirs(self.replica_dir)
            self.logger.log_message(f"Folder created: {self.replica_dir}", GREEN)

        # Create a set of existing files in the replica
        replica_files = {
            item: os.path.join(self.replica_dir, item)
            for item in os.listdir(self.replica_dir)
        }

        # Copy files from source to replica
        for item in os.listdir(self.source_dir):
            src_path = os.path.join(self.source_dir, item)
            dest_path = os.path.join(self.replica_dir, item)

            if os.path.isdir(src_path):
                # If the item is a directory
                if not os.path.exists(dest_path):
                    try:
                        shutil.copytree(src_path, dest_path)
                        self.logger.log_message(
                            f"Copied directory: {src_path} to {dest_path}", BLUE
                        )
                    except Exception as e:
                        self.logger.log_message(
                            f"Error copying directory {src_path}: {e}", RED
                        )
                else:
                    # If the directory exists, recursively synchronize it
                    self.synchronize_directory(src_path, dest_path)
            else:
                # If the item is a file
                try:
                    if not os.path.exists(dest_path) or os.path.getmtime(
                        src_path
                    ) > os.path.getmtime(dest_path):
                        shutil.copy2(src_path, dest_path)
                        self.logger.log_message(
                            f"Copied file: {src_path} to {dest_path}", BLUE
                        )
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
                        self.logger.log_message(
                            f"Removed directory: {replica_path}", RED
                        )
                    else:
                        os.remove(replica_path)  # Remove the file
                        self.logger.log_message(f"Removed file: {replica_path}", RED)
                except Exception as e:
                    self.logger.log_message(f"Error removing {replica_path}: {e}", RED)

    def synchronize_directory(self, source_dir, dest_dir):
        """
        The function `synchronize_directory` recursively synchronizes the contents of a source directory
        with a destination directory, copying files and directories as needed and logging messages about
        the synchronization process.

        :param source_dir: The `source_dir` parameter in the `synchronize_directory` method represents
        the directory whose contents you want to synchronize with another directory. This method
        recursively goes through all the files and subdirectories in the `source_dir` and copies them to
        the corresponding locations in the `dest_dir`. If a file
        :param dest_dir: The `dest_dir` parameter in the `synchronize_directory` method represents the
        destination directory where the contents from the `source_dir` will be synchronized to. It is
        the directory where the files and subdirectories from the `source_dir` will be copied to or
        updated based on the comparison of modification
        """
        for item in os.listdir(source_dir):
            src_path = os.path.join(source_dir, item)
            dest_path = os.path.join(dest_dir, item)

            if os.path.isdir(src_path):
                if not os.path.exists(dest_path):
                    try:
                        shutil.copytree(src_path, dest_path)
                        self.logger.log_message(
                            f"Copied directory: {src_path} to {dest_path}", BLUE
                        )
                    except Exception as e:
                        self.logger.log_message(
                            f"Error copying directory {src_path}: {e}", RED
                        )
                else:
                    self.synchronize_directory(
                        src_path, dest_path
                    )  # Recursively synchronize
            else:
                try:
                    if not os.path.exists(dest_path) or os.path.getmtime(
                        src_path
                    ) > os.path.getmtime(dest_path):
                        shutil.copy2(src_path, dest_path)
                        self.logger.log_message(
                            f"Copied file: {src_path} to {dest_path}", BLUE
                        )
                except Exception as e:
                    self.logger.log_message(f"Error copying file {src_path}: {e}", RED)


def main():
    """
    The `main` function synchronizes two folders at a specified interval and logs the synchronization
    process.
    """
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(
        description="Synchronize two folders: source and replica."
    )
    parser.add_argument("source", help="Path to the source directory.")
    parser.add_argument("replica", help="Path to the replica directory.")
    parser.add_argument(
        "interval", type=int, help="Synchronization interval in seconds."
    )
    parser.add_argument("log_file", help="Path to the log file.")

    args = parser.parse_args()

    logger = Log(args.log_file)
    sync = Sync(args.source, args.replica, logger)

    while True:
        sync.synchronize()
        time.sleep(args.interval)


if __name__ == "__main__":
    main()
