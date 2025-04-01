import os
import subprocess
import sys
from colorama import Fore, Style, init
import logo

Version = 0.1

# Initialize colorama
init(autoreset=True)

def banner():
    """Display the banner information."""
    print(f"{Fore.CYAN}version: {Version}")
    print(f"{Fore.GREEN}[✨] Do you wanna buy me a coffee☕? > https://ko-fi.com/lose_sec")
    print("")

def john_install():
    """Check if John the Ripper is installed."""
    try:
        subprocess.run(["john", "--help"], check=True)
        os.system('cls' if os.name == 'nt' else 'clear')
    except subprocess.CalledProcessError:
        print(f"{Fore.RED}Error: John the Ripper is not installed.")
        sys.exit(1)

def extract_zip_hash(file_path):
    """Extract the hash from a ZIP file using zip2john."""
    if not os.path.exists(file_path):
        print(f"{Fore.RED}Error: File {file_path} does not exist.")
        sys.exit(1)

    try:
        # Extract the hash using zip2john
        hash_file = file_path + ".hash"
        subprocess.run(["zip2john", file_path], stdout=open(hash_file, "w"), check=True)
        print(f"{Fore.GREEN}Hash for {file_path} extracted successfully to {hash_file}.")
        return hash_file
    except subprocess.CalledProcessError:
        print(f"{Fore.RED}Error: Failed to extract hash from {file_path}.")
        sys.exit(1)

def run_john(hash_file):
    """Run John the Ripper on the extracted hash."""
    try:
        subprocess.run(["john", hash_file], check=True)
        print(f"{Fore.GREEN}John the Ripper is running...")
    except subprocess.CalledProcessError:
        print(f"{Fore.RED}Error: Failed to run John the Ripper on {hash_file}.")
        sys.exit(1)

def show_password(hash_file):
    """Show the cracked password."""
    try:
        result = subprocess.run(["john", "--show", hash_file], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = result.stdout.decode("utf-8").strip()
        if output:
            print(f"{Fore.GREEN}Cracked password: {output}")
        else:
            print(f"{Fore.YELLOW}No password found or John the Ripper could not crack it.")
    except subprocess.CalledProcessError:
        print(f"{Fore.RED}Error: Failed to retrieve cracked password for {hash_file}.")
        sys.exit(1)

def main():
    john_install()

    # Display logo
    logo.root()

    # Display banner
    banner()

    # Get the file path from the user
    file_path = input("Enter the full path of the encrypted file: ").strip()

    # Extract the hash and run John the Ripper
    hash_file = extract_zip_hash(file_path)
    run_john(hash_file)

    # Display the cracked password
    show_password(hash_file)

if __name__ == "__main__":
    main()