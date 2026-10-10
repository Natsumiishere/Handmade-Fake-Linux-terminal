#!/usr/bin/env python3

import os
import sys
import time
import random
import getpass
import hashlib
import hmac
from datetime import datetime


USER = "user"
HOST = "mypc"

# save password file in user's home directory
PASS_FILE = os.path.join(os.path.expanduser("~"), ".my_secure_terminal_pass")


LOGO = r"""
        _        _    _   _             _            
       | |      | |  | | | |           (_)           
       | | ___  | |  | |_| | ___ _ __   ___   _____ 
       | |/ _ \ | |  |  _  |/ _ \ '_ \ / _` | \ \ / /
       | |  __/ | |  | | | |  __/ | | | (_| | |\ V / 
       |_|\___| |_|  |_| |_|\___|_| |_|\__,_| | \_/  
                                                _/ |
                                               |__/ 
"""


def clear():
    """clear the terminal screen"""
    os.system("cls" if os.name == "nt" else "clear")


def slow_print(text, delay=0.02):
    """show text slowly, character by character"""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()


def progress(label, total=35, delay=0.015):
    """show progress bar"""
    for i in range(total + 1):
        filled = "#" * i
        empty = "-" * (total - i)
        percent = int(i / total * 100)
        sys.stdout.write(f"\r{label}: [{filled}{empty}] {percent}%")
        sys.stdout.flush()
        time.sleep(delay)
    print()


def boot_animation():
    """boot animation similar to Linux"""
    clear()

    messages = [
        "Starting MyLinux Kernel 6.10",
        "Loading kernel modules",
        "Mounting filesystems",
        "Starting network manager",
        "Applying security policies",
        "Checking user permissions",
        "Starting terminal service",
    ]

    for msg in messages:
        print(f"[  OK  ] {msg}")
        time.sleep(random.uniform(0.15, 0.45))

    print()
    progress("Loading terminal", 35, 0.012)
    print()

    # show logo slowly
    for line in LOGO.strip("\n").splitlines():
        sys.stdout.write(line + "\n")
        sys.stdout.flush()
        time.sleep(0.08)

    print()
    slow_print("Welcome to MyLinux Secure Terminal", 0.03)
    time.sleep(0.5)


def hash_password(password, salt):
    """hash the password using PBKDF2"""
    return hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        100000
    )


def setup_password():
    """set up a password for the first run"""
    slow_print("First run detected. Please set a password.", 0.01)

    while True:
        try:
            pass1 = getpass.getpass("Set a password: ")

            if len(pass1) < 4:
                print("Password must be at least 4 characters.")
                continue

            pass2 = getpass.getpass("Confirm password: ")

            if pass1 != pass2:
                print("Passwords do not match.")
                continue

            salt = os.urandom(16)
            hashed = hash_password(pass1, salt)

            with open(PASS_FILE, "wb") as f:
                f.write(salt + hashed)

            try:
                os.chmod(PASS_FILE, 0o600)
            except Exception:
                pass

            print("Password saved.\n")
            return True

        except (EOFError, KeyboardInterrupt):
            print("\nCancelled.")
            return False


def load_stored_password():
    """load the stored salt and hash"""
    try:
        with open(PASS_FILE, "rb") as f:
            data = f.read()

        if len(data) < 16 + 32:
            return None

        salt = data[:16]
        stored_hash = data[16:]
        return salt, stored_hash

    except FileNotFoundError:
        return None
    except Exception:
        return None


def ask_password():
    """get password and check if it's correct"""
    stored = load_stored_password()

    if stored is None:
        if not setup_password():
            return False

        stored = load_stored_password()
        if stored is None:
            return False

    salt, stored_hash = stored

    for attempt in range(3, 0, -1):
        try:
            password = getpass.getpass("Password: ")
        except (EOFError, KeyboardInterrupt):
            print("\nExit.")
            return False

        test_hash = hash_password(password, salt)

        if hmac.compare_digest(test_hash, stored_hash):
            print("Access granted.")
            time.sleep(0.6)
            return True

        print(f"Access denied. {attempt - 1} attempts left.")
        time.sleep(0.6)

    return False


def show_neofetch():
    """show a fake neofetch-like system info"""
    info = [
        f"{USER}@{HOST}",
        "-----------------",
        "OS: MyLinux 1.0",
        "Kernel: 6.10-custom",
        "Shell: mysh 1.0",
        "Terminal: Python Secure Terminal",
        f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "CPU: Fake CPU @ 4.20GHz",
        "Memory: 16GB DDR5",
    ]

    logo_lines = LOGO.strip("\n").splitlines()
    max_lines = max(len(logo_lines), len(info))

    for i in range(max_lines):
        left = logo_lines[i] if i < len(logo_lines) else ""
        right = info[i] if i < len(info) else ""
        print(f"{left:<60} {right}")


def run_command(command):
    """run simple internal commands"""
    parts = command.strip().split()
    if not parts:
        return True

    cmd = parts[0].lower()
    args = parts[1:]

    if cmd in ("exit", "quit"):
        print("Goodbye.")
        return False

    elif cmd == "clear":
        clear()

    elif cmd == "help":
        print("Available commands:")
        print("  help       - show this help")
        print("  clear      - clear screen")
        print("  echo       - print text")
        print("  date       - show date/time")
        print("  whoami     - show current user")
        print("  hostname   - show hostname")
        print("  ls         - fake list files")
        print("  pwd        - print working directory")
        print("  neofetch   - show logo and system info")
        print("  sudo       - try it :)")
        print("  exit       - exit terminal")

    elif cmd == "echo":
        print(" ".join(args))

    elif cmd == "date":
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    elif cmd == "whoami":
        print(USER)

    elif cmd == "hostname":
        print(HOST)

    elif cmd == "ls":
        print("Desktop  Documents  Downloads  Pictures  Music  Videos  Projects")

    elif cmd == "pwd":
        print(f"/home/{USER}")

    elif cmd == "sudo":
        print("Permission denied: nice try :)")

    elif cmd == "neofetch":
        show_neofetch()

    else:
        print(f"{cmd}: command not found")

    return True


def shell():
    """main terminal loop"""
    while True:
        try:
            command = input(f"{USER}@{HOST}:~$ ")
        except (EOFError, KeyboardInterrupt):
            print("\nExit.")
            break

        if not command.strip():
            continue

        if not run_command(command):
            break


def main():
    boot_animation()

    if ask_password():
        print("\nType 'help' to see available commands.")
        shell()
    else:
        print("Too many failed attempts.")
        time.sleep(1)


if __name__ == "__main__":
    main()