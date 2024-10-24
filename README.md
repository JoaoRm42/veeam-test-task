# Folder Synchronization Script

This project is a Python script that synchronizes two folders: a source directory and a replica directory.
It monitors changes, updates the replica with new or modified files from the source, and deletes files from the replica that no longer exist in the source.
The synchronization happens periodically, and all file operations are logged in both the terminal (with color-coded messages) and a log file.

## Table of Contents
- [Features](#features)
- [Prerequisites](#prerequisites)
- [How It Works](#howItWorks)
- [Command-Line Arguments](#command-linesrguments)
- [Usage](#usage)
- [Example Workflow](#exampleworkflow)
- [Logging](#logging)
- [Handling Errors](#handlingerrors)
- [Customization](#customization)

## Features
Real-time synchronization: Ensures that the replica folder always mirrors the source folder.
File and folder creation: New files or directories in the source are copied to the replica.
File modification: Files in the replica are updated if their source counterpart is modified.
File deletion: Files or directories removed from the source are also removed from the replica.
Logging: All file operations (creation, update, deletion) are logged in both the terminal and a log file.
Customizable synchronization interval: You can set how often the synchronization occurs (in seconds).
Graceful shutdown: The program can be safely stopped with ```Ctrl+C```.

## Prerequisites
- Python 3.x
- Basic understanding of Python command-line arguments.


## How It Works
The script is made up of two main classes:

1. **Log**: This class is responsible for logging messages to both the terminal and a log file. Terminal messages are color-coded for better readability:

- Green for successful folder creation
- Yellow for newly created files in the source
- Blue for successful file or folder copies
- Red for errors or deletions

2. **Sync**: This class handles the synchronization process. It compares the contents of the source and replica directories:

- Copies files and directories from the source to the replica if they don't exist or have been modified.
- Deletes files from the replica if they've been removed from the source.

## Command-Line Arguments
The script takes four arguments:

- ```source``` - The path to the source directory that you want to sync from.
- ```replica``` - The path to the replica directory that will mirror the source.
- ```interval``` - The synchronization interval in seconds (how often the script will sync the two directories).
- ```log_file``` - The path to the log file where all file operations will be recorded.


## Usage
1. **Clone the repository**:

```bash
git clone https://github.com/JoaoRm42/veeam-test-task.git
cd veeam-test-task
```

2. **Run the script**:

You can run the script using Python by passing the required arguments like so:

```bash
python test_task.py <source_directory> <replica_directory> <interval_seconds> <log_file>
```

**Example**:

```bash
python test_task.py /path/to/source /path/to/replica 60 /path/to/log.txt
```
In this example:

- ```/path/to/source```: The folder you want to keep as the source.
- ```/path/to/replica```: The folder that will mirror the source.
- ```60```: The synchronization interval (in seconds).
- ```/path/to/log.txt```: The file where logs will be saved.

3. Stop the script:

The script will run continuously, synchronizing the two folders at the given interval. To stop it, press ```Ctrl+C```.

# Example Workflow
1. Initial Sync:

- The replica folder is created if it doesn't exist.
- All files and subdirectories from the source folder are copied to the replica.
- Any changes (new files, modifications, or deletions) are logged.

2. Subsequent Syncs:

- The script will detect any new files or modifications in the source and update the replica accordingly.
- Files or directories removed from the source will also be deleted from the replica.

# Logging
All operations (copying, deleting, etc.) are logged in two ways:

1. Terminal: Color-coded messages make it easy to see what actions are being performed:
   
- **Green**: Folder creation
- **Yellow**: New files in the source
- **Blue**: Files and directories copied
- **Red**: Errors or deletions

2. Log File: The same messages are written to the log file without colors for easy review later.

# Handling Errors
If there are any issues with copying or deleting files (such as permission errors), the error will be logged in both the terminal and the log file with a red message.

# Customization
You can modify the synchronization interval by adjusting the value of the ```interval``` argument when running the script. By default, the synchronization happens every 60 seconds, but you can change this to any value you prefer.
