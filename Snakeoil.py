import os
import subprocess
import urllib.request
print("Operating System = " + os.name)

# Setting the current directory to the current working directory
current_directory = os.getcwd()
print("Current directory = " + current_directory)

# Define the install directory path
install_directory = os.path.join(current_directory, "install")

# Create the install directory if it doesn't exist
if not os.path.exists(install_directory):
    os.mkdir(install_directory)

# Printing the install directory
print(f"Install directory = {install_directory}")

# URLs and their descriptive names
urls = [
    ('Arch Linux', 'https://packages.oth-regensburg.de/archlinux/iso/latest/archlinux-x86_64.iso'),
    ('Ubuntu', 'https://ftp.halifax.rwth-aachen.de/ubuntu-releases/noble/ubuntu-24.04-desktop-amd64.iso'),
    ('Debian', 'https://cdimage.debian.org/debian-cd/current/amd64/iso-cd/debian-12.5.0-amd64-netinst.iso'),
    ('Gentoo', 'https://distfiles.gentoo.org/releases/amd64/autobuilds/20240526T163557Z/livegui-amd64-20240526T163557Z.iso'),
    ('Kali Linux', 'https://cdimage.kali.org/kali-2024.2/kali-linux-2024.2-installer-amd64.iso'),
    ('Linux Mint', 'https://ftp.rz.uni-frankfurt.de/pub/mirrors/linux-mint/iso/stable/21.3/linuxmint-21.3-cinnamon-64bit.iso'),
    ('Pop!_OS', 'https://iso.pop-os.org/22.04/amd64/nvidia/41/pop-os_22.04_amd64_nvidia_41.iso'),
    ('Kubuntu', 'https://cdimage.ubuntu.com/kubuntu/releases/24.04/release/kubuntu-24.04-desktop-amd64.iso'),
    ('CentOS Stream', 'https://mirrors.centos.org/mirrorlist?path=/9-stream/BaseOS/x86_64/iso/CentOS-Stream-9-latest-x86_64-dvd1.iso&redirect=1&protocol=https'),
    ('Parrot Security', 'https://deb.parrot.sh/parrot/iso/6.1/Parrot-security-6.1_amd64.iso'),
    ('Qubes OS', 'https://ftp.halifax.rwth-aachen.de/qubes/iso/Qubes-R4.2.1-x86_64.iso'),
    ('Manjaro KDE', 'https://download.manjaro.org/kde/24.1.0/manjaro-kde-24.1.0-241001-linux610.iso'),
    ('EndeavourOS', 'https://mirror.alpix.eu/endeavouros/iso/EndeavourOS_Endeavour_neo-2024.09.22.iso'),
    ('Test', 'https://archive.org/download/tiny-iso-test/TinyIsoTest.iso')
]

# Prompt the user to choose a Distribution
print("Please choose a distribution to download:")
for i, (name, url) in enumerate(urls, start=1):
    print(f"{i}. {name}")

choice = int(input("Enter the number of your choice: ")) - 1

# Validate the user's choice
if 0 <= choice < len(urls):
    name, url = urls[choice]
    print(f"Download URL = {url}")

    # Path where the file will be saved
    file_path = os.path.join(install_directory, 'notwindows.iso')

    # Define a callback function to show download progress
    def show_progress(block_num, block_size, total_size):
        downloaded = block_num * block_size
        percentage = downloaded / total_size * 100
        print(f"\rDownloading: {percentage:.2f}%", end='')

    # Downloading the file with progress display
    urllib.request.urlretrieve(url, file_path, show_progress)

    # Process output
    print(f"\nFile downloaded and saved to {file_path}")
else:
    print("Invalid choice. Exiting.")

# End of Download

# List all the drives
if os.name == 'nt':
    drive_list = subprocess.run('wmic logicaldisk get name', shell=True, capture_output=True, text=True)
    drives = drive_list.stdout.split()[1:]  # Skip the header
else:
    drive_list = subprocess.run('lsblk -o NAME,SIZE,TYPE,MOUNTPOINT', shell=True, capture_output=True, text=True)
    drives = [line.split()[0] for line in drive_list.stdout.splitlines() if 'disk' in line]

# Display the drives with numeric choices
print("Please choose a drive to partition and format:")
for i, drive in enumerate(drives, start=1):
    print(f"{i}. {drive}")

drive_choice = int(input("Enter the number of your choice: ")) - 1

# Validate the user's choice
if 0 <= drive_choice < len(drives):
    drive = drives[drive_choice]
    print(f"Selected drive: {drive}")

    # Partition and format the drive
    def partition_and_format_drive(drive):
        if os.name == 'nt':
            # Create a script for diskpart
            diskpart_script = f"""
            select disk {drive}
            clean
            create partition primary
            select partition 1
            format fs=fat32 quick
            assign letter={drive}
            exit
            """
            # Save the script to a temporary file
            with open("diskpart_script.txt", "w") as file:
                file.write(diskpart_script)

            # Run diskpart with the script
            subprocess.run("diskpart /s diskpart_script.txt", shell=True, check=True)
            print(f"Drive {drive} has been partitioned and formatted to FAT32.")
            
            
            subprocess.run(f"C:\\ProgramFiles\\7-Zip\\7z.exe x {file_path} -o {target}", shell=True, check=True)
        else:
            # Linux-specific commands
            subprocess.run(f"sudo parted /dev/{drive} mklabel msdos", shell=True, check=True)
            subprocess.run(f"sudo parted -a optimal /dev/{drive} mkpart primary fat32 0% 100%", shell=True, check=True)
            subprocess.run(f"sudo mkfs.vfat -F 32 /dev/{drive}1", shell=True, check=True)
            print(f"/dev/{drive} has been partitioned and formatted to FAT32.")

            # Make the partition bootable with the ISO using dd
            subprocess.run(f"sudo dd if={file_path} of=/dev/{drive} bs=4M status=progress", shell=True, check=True)
            print(f"The ISO has been written to /dev/{drive} and made bootable.")

    partition_and_format_drive(drive)
else:
    print("Invalid choice. Exiting.")

print("Snakeoil.py has finished running.")