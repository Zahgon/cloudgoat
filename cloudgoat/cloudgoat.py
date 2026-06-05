#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK
import argparse
import os
import re
import subprocess
import sys




def parse_args():
    parser = argparse.ArgumentParser(add_help=False, usage="cloudgoat.py help")

    parser.add_argument(
        "command", nargs="*", action="store"
    ).completer = command_completer
    parser.add_argument(
        "-a", "--auto", required=False, action="store_true", help=argparse.SUPPRESS
    )
    parser.add_argument(
        "-p", "--profile", help=argparse.SUPPRESS
    )
    parser.add_argument(
        "-h", "--help", action='store_true', help=argparse.SUPPRESS
    )

    try:
        import argcomplete

        argcomplete.autocomplete(parser)
    except ImportError:
        pass

    return parser.parse_args()


def main():
    # This should come before version checking because argcomplete suppresses
    # all non-completion output and exits early.
    args = parse_args()

    if sys.version_info[0] < 3 or (
        sys.version_info[0] >= 3 and sys.version_info[1] < 6
    ):
        print("CloudGoat requires Python 3.6+ to run.")
        sys.exit(1)

    try:        
        terraform_version_process = subprocess.Popen(["terraform", "--version"], stdout=subprocess.PIPE, text=True)
        output, _ = terraform_version_process.communicate()

    except FileNotFoundError:
        print("Terraform not found. Please install Terraform before using CloudGoat.")
        sys.exit(1)

    version_number = re.search(r'Terraform v(\d+\.\d+\.\d+)', output)

    if not version_number:
        print("Terraform not found. Please install Terraform before using CloudGoat.")
        sys.exit(1)

    terraform_version = version_number.group(1)
    major_version, minor_version, sub_minor = terraform_version.split(".")
    if int(major_version) == 0 and int(minor_version) < 11:
        print(
            "Your version of Terraform is v{}. CloudGoat requires Terraform v0.12 or"
            " higher to run.".format(version_number[0])
        )

    try:
        from cloudgoat.core.python.commands import CloudGoat

        base_dir = os.path.dirname(os.path.abspath(__file__))
        cloudgoat = CloudGoat(base_dir)
        cloudgoat.parse_and_execute_command(args)
    except KeyboardInterrupt:
        print("\nBye!")

if __name__ == "__main__":
    main()
