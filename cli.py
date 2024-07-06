import sys
import datetime
import os
import subprocess

from utils.loader import Loader

# Args: pod_name, container_name, source_file, backup_dir
# -p pod_name: args[1]
# -c container_name
# -src source_dir
# -bck backup_dir
# -l local_dir
# -f file_name 

# -d flag for only downloading a file from pod
# -u flag for only uploading a file to pod
# -b for downloading and uploading a file to pod

loader = Loader(0)

def download_and_backup_file(pod_name, container_name, source_file, backup_dir):
    """
    Downloads a file from a pod container, adds a timestamp to the name, 
    and stores it as a backup. Uploads a local file to replace the original.

    Args:
        pod_name: Name of the Kubernetes pod.
        container_name: Name of the container within the pod (optional).
        source_file: Path to the file within the pod container.
        backup_dir: Local directory to store the backup file.
    """
    loader.log(10,"")

    # Get current timestamp
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename, extension = os.path.splitext(os.path.basename(source_file))

    # Construct backup filename with timestamp before extension
    backup_filename = f"{filename}_{timestamp}{extension}"
    destination_path = f"{backup_dir}/{backup_filename}"

    # Download the file using kubectl cp
    download_cmd = f"kubectl cp {pod_name}:{source_file} {backup_dir}/{backup_filename}"
    if container_name:
        download_cmd += f" -c {container_name}"
    subprocess.run(download_cmd.split(), check=True)
    loader.log(15,"Downloaded file from pod " + pod_name + " " + source_file)
    loader.log(20,"Backup stored as" + destination_path)
    # print(f"Downloaded file from pod: {pod_name}:{source_file}")
    # print(f"Backup stored as: {destination_path}")

def upload_file(pod_name, container_name, local_file, source_file):
    """
    Uploads a local file to a pod container.

    Args:
        pod_name: Name of the Kubernetes pod.
        container_name: Name of the container within the pod (optional).
        source_file: Path to the local file to upload.
    """
    
    loader.log(10,"")

    # Upload the local file using kubectl cp
    upload_cmd = f"kubectl cp {local_file} {pod_name}:{source_file}"
    if container_name:
        upload_cmd += f" -c {container_name}"
    subprocess.run(upload_cmd.split(), check=True)
    loader.log(20,"Uploaded local file: " + source_file + " " + source_file)

def download_and_upload_file(pod_name, container_name, source_file, backup_dir, local_file):
    download_and_backup_file(pod_name, container_name, source_file, backup_dir)
    upload_file(pod_name, container_name, local_file, source_file)

def help():
    print("Use this program to easily access files from a pod in a kubernetes cluster")
    print("-p <podname>")
    print("-l <local file path>")
    print("-src <remote source file path>")
    print("-bck <destination file path on local system>")
    print("-f <filename>")
    print("\n** This program depends on kubectl tool but doesnt configure it! **")


def main():
    print("Hello World!")

    for i in range(1, len(sys.argv)):
        if sys.argv[i] == "-help":
            help()
            sys.exit(1)

    if len(sys.argv) < 6:
        print("Usage: python cli.py -p pod_name -c container_name -src source_file -bck backup_dir -lf local_file")
        sys.exit(1)
    # the arguments can be in different orders
    pod_name = ""
    container_name = ""
    source_file = ""
    backup_dir = ""
    local_file = ""
    file_name = ""

    for i in range(1, len(sys.argv), 2):
        if sys.argv[i] == "-p":
            pod_name = sys.argv[i+1]
        elif sys.argv[i] == "-c":
            container_name = sys.argv[i+1]
        elif sys.argv[i] == "-src":
            source_file = sys.argv[i+1]
        elif sys.argv[i] == "-bck":
            backup_dir = sys.argv[i+1]
        elif sys.argv[i] == "-l":
            local_file = sys.argv[i+1]
        elif sys.argv[i] == "-f":
            file_name = sys.argv[i+1]

    if file_name == "":
        print("Please provide a filename using -f <filename>")
        sys.exit(1)
    else:
        source_file += "/" + file_name
        local_file += "/" + file_name

    loader.log(2,"")

    if "-d" in sys.argv:
        download_and_backup_file(pod_name, container_name, source_file, backup_dir)
    elif "-u" in sys.argv:
        upload_file(pod_name, container_name, source_file)
    elif "-b" in sys.argv:
        download_and_upload_file(pod_name, container_name, source_file, backup_dir, local_file)
    else:
        print("Invalid arguments. Use -d for download, -u for upload, -b for both.")
        sys.exit(1)

if __name__ == "__main__":
    main()