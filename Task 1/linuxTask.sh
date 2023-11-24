#!/bin/bash

# 1.1 
if [ "$EUID" -eq 0 ]; then
    echo "Script is running as root."
else
    echo "Script is not running as root."
fi

# 1.2 
echo "$(date +"%Y-%m-%d %H:%M:%S")"

# 1.3 
mkdir my_new_dir
cd my_new_dir

# 1.4 C
cp ~/my_file.txt /tmp

# 1.5 
rm ~/my_file.txt

# 1.6
echo "Files in ~/:"
ls ~/

# 1.7 
read -p "Enter the filename: " filename
if [ -e "$filename" ]; then
    echo "Contents of file $filename:"
    cat "$filename"
else
    echo "File $filename does not exist."
fi

# 1.8 
read -p "Enter the directory name: " directory
if [ -d "$directory" ]; then
    echo "Files in directory $directory:"
    ls "$directory"
else
    echo "Directory $directory does not exist."
fi

# 1.9 
read -p "Enter the filename: " filename
if [ -e "$filename" ]; then
    echo "Contents of file $filename:"
    cat "$filename"
else
    echo "Error: File $filename does not exist."
fi

# 1.10 
read -p "Enter the directory name: " directory
if [ -d "$directory" ]; then
    echo "Files in directory $directory:"
    ls "$directory"
else
    echo "Error: Directory $directory does not exist."
fi

# 1.11 
read -p "Enter the filename: " filename
if [ -e "$filename" ]; then
    sed -i 's/error/warning/g' "$filename"
    echo "Occurrences of 'error' replaced with 'warning' in $filename."
else
    echo "Error: File $filename does not exist."
fi

# 1.12 
error_files=$(grep -rl "error" /var/log)
if [ -n "$error_files" ]; then
    echo "Files containing 'error' in /var/log:"
    echo "$error_files"
else
    echo "Error: No files found with 'error' in /var/log."
fi

# 1.13 

function display_disk_space() {
    df -h
}


function check_free_space() {
    threshold=10  
    free_space=$(df -h | awk 'NR==2 {print $5}' | cut -d'%' -f1)
    
    if [ "$free_space" -lt "$threshold" ]; then
        echo "Warning: Free space is below $threshold%."
    fi
}


function clean_up_files() {
    read -p "Enter the directory to clean up: " cleanup_directory
    echo "Clean up completed in $cleanup_directory."
}

function log_event() {
    echo "$(date): $1" >> disk_space_manager.log
}


case "$1" in
    "display")
        display_disk_space
        ;;
    "check")
        check_free_space
        ;;
    "cleanup")
        clean_up_files
        ;;
    *)
        echo "Usage: $0 {display|check|cleanup}"
        exit 1
        ;;
esac


log_event "Script executed with argument: $1"

