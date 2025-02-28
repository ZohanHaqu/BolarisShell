import os
import sys
import platform
import shutil
import subprocess
import time
import psutil
import getpass

def show_help():
    help_text = """
    Welcome to the Bolaris Shell Help!

    Available commands:

    1. exit              - Exits the shell.
    2. cd <path>         - Change the current directory.
    3. ls                - List files in the current directory.
    4. pwd               - Print the current working directory.
    5. mkdir <dir_name>  - Create a directory.
    6. rmdir <dir_name>  - Remove a directory.
    7. rm <file_name>    - Remove a file with a confirmation prompt.
    8. cp <src> <dst>    - Copy a file.
    9. mv <src> <dst>    - Move a file.
    10. df               - Show disk usage.
    11. ps               - Show current running processes.
    12. kill <pid>       - Kill a process.
    13. sysinfo          - Show system information.
    14. uptime           - Show system uptime.
    15. date             - Show current date and time.
    16. env              - Show environment variables.
    17. free             - Show memory information.
    18. find <file>      - Search for a file in the current directory.
    19. lsof             - Show open files.
    20. proc <pid>       - Show information about a specific process.
    
    Note:
    - All commands are similar to typical Unix-like shell commands.
    - Windows-specific commands like `dir`, `cls` are blocked for this shell.

    """
    print(help_text)

def bolaris_shell():
    username = getpass.getuser()  # Get the current username
    print(f"Welcome to The Bolaris Shell")
    
    while True:
        try:
            # Get the current working directory
            current_directory = os.getcwd()

            # Custom prompt with Username@bolaris and full path
            prompt = f"{username}@bolaris$-{current_directory.replace(os.getcwd().split(os.sep)[0], '')}"
            command = input(f"{prompt} ")

            # Block Windows commands
            if command in ["dir", "cls", "echo"]:
                print(f"Error: '{command}' is not a valid command in this shell.")
                continue

            # Exit Command
            elif command == "exit":
                print("Exiting Bolaris Shell...")
                break

            # Show Help
            elif command == "help":
                show_help()

            # Change Directory
            elif command.startswith("cd "):
                path = command[3:]
                try:
                    os.chdir(path)
                    print(f"Changed directory to {path}")
                except FileNotFoundError:
                    print(f"No such directory: {path}")

            # List Files and Directories
            elif command == "ls":
                for item in os.listdir(os.getcwd()):
                    print(item)

            # Show current working directory
            elif command == "pwd":
                print(os.getcwd())

            # Make a directory
            elif command.startswith("mkdir "):
                dir_name = command[6:]
                try:
                    os.mkdir(dir_name)
                    print(f"Directory '{dir_name}' created.")
                except FileExistsError:
                    print(f"Directory '{dir_name}' already exists.")

            # Remove a file with confirmation
            elif command.startswith("rm "):
                file_name = command[3:]
                confirm = input(f"Are you sure you want to remove '{file_name}'? (y/n): ")
                if confirm.lower() == 'y':
                    try:
                        os.remove(file_name)
                        print(f"File '{file_name}' removed.")
                    except FileNotFoundError:
                        print(f"File '{file_name}' not found.")
                else:
                    print(f"File '{file_name}' not removed.")

            # Remove a directory
            elif command.startswith("rmdir "):
                dir_name = command[6:]
                try:
                    os.rmdir(dir_name)
                    print(f"Directory '{dir_name}' removed.")
                except FileNotFoundError:
                    print(f"Directory '{dir_name}' not found.")
                except OSError:
                    print(f"Directory '{dir_name}' is not empty.")

            # Copy a file
            elif command.startswith("cp "):
                args = command[3:].split(" ")
                if len(args) == 2:
                    src, dst = args
                    try:
                        shutil.copy(src, dst)
                        print(f"Copied '{src}' to '{dst}'.")
                    except FileNotFoundError:
                        print(f"File '{src}' not found.")
                else:
                    print("Usage: cp <source> <destination>")

            # Move a file
            elif command.startswith("mv "):
                args = command[3:].split(" ")
                if len(args) == 2:
                    src, dst = args
                    try:
                        shutil.move(src, dst)
                        print(f"Moved '{src}' to '{dst}'.")
                    except FileNotFoundError:
                        print(f"File '{src}' not found.")
                else:
                    print("Usage: mv <source> <destination>")

            # Show disk usage
            elif command == "df":
                total, used, free = shutil.disk_usage("/")
                print(f"Total: {total // (2**30)} GiB")
                print(f"Used: {used // (2**30)} GiB")
                print(f"Free: {free // (2**30)} GiB")

            # Show current processes
            elif command == "ps":
                for proc in psutil.process_iter(['pid', 'name', 'status']):
                    print(proc.info)

            # Kill a process
            elif command.startswith("kill "):
                try:
                    pid = int(command[5:])
                    os.kill(pid, 9)  # Send SIGKILL
                    print(f"Process {pid} killed.")
                except ValueError:
                    print("Invalid process ID.")
                except ProcessLookupError:
                    print("No such process.")

            # Show system information
            elif command == "sysinfo":
                uname = platform.uname()
                print(f"System: {uname.system}")
                print(f"Node Name: {uname.node}")
                print(f"Release: {uname.release}")
                print(f"Version: {uname.version}")
                print(f"Machine: {uname.machine}")
                print(f"Processor: {uname.processor}")

            # Show uptime
            elif command == "uptime":
                uptime = time.time() - psutil.boot_time()
                hours, remainder = divmod(uptime, 3600)
                minutes, seconds = divmod(remainder, 60)
                print(f"Uptime: {int(hours)} hours, {int(minutes)} minutes, {int(seconds)} seconds")

            # Show current date and time
            elif command == "date":
                print(time.strftime("%Y-%m-%d %H:%M:%S"))

            # Show environment variables
            elif command == "env":
                for key, value in os.environ.items():
                    print(f"{key}={value}")

            # Show system memory info
            elif command == "free":
                memory = psutil.virtual_memory()
                print(f"Total: {memory.total // (1024 ** 2)} MB")
                print(f"Used: {memory.used // (1024 ** 2)} MB")
                print(f"Free: {memory.available // (1024 ** 2)} MB")

            # Search for a file
            elif command.startswith("find "):
                path = command[5:]
                result = subprocess.run(["find", ".", "-name", path], stdout=subprocess.PIPE)
                print(result.stdout.decode())

            # Show the number of open files
            elif command == "lsof":
                result = subprocess.run(["lsof"], stdout=subprocess.PIPE)
                print(result.stdout.decode())

            # Show process info for a specific pid
            elif command.startswith("proc "):
                pid = command[5:]
                try:
                    process = psutil.Process(int(pid))
                    print(f"Process ID: {process.pid}")
                    print(f"Name: {process.name()}")
                    print(f"Status: {process.status()}")
                    print(f"Memory Info: {process.memory_info()}")
                    print(f"CPU Times: {process.cpu_times()}")
                except psutil.NoSuchProcess:
                    print(f"No such process with PID {pid}.")

            # Handle unknown command
            else:
                print(f"Command '{command}' not found. Try 'exit' to quit.")

        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    bolaris_shell()

