#!/usr/bin/python3

import argparse
import sys
import os
import subprocess

"""
    This script was born out of a very specific use case of having to frequently run the commands:
        vagrant destroy -f
        vagrant up
        vagrant ssh -c "ansible-playbook /vagrant/ansible/kubernetesConfiguration.yml"
    Do not expect this to be a general use case python wrapper for the Vagrant CLI 
"""


# define functions
def main():
    options_error_checking()

    # change working directory to where Vagrantfile is located
    change_working_directory_to_vagrantfile()

    # sanity check; check for Vagrantfile
    check_for_vagrantfile()

    if args.provision:
        provision_vm()
        display_status()
    if args.reloadvm:
        destroy_vm()
        provision_vm()
        display_status()
    if args.delete:
        destroy_vm()
        display_status()
    if args.status:
        display_status()
    exit(0)


def check_for_vagrantfile():
    print("Checking for Vagrantfile")
    print(os.path.abspath(os.path.curdir))
    if not os.path.exists('Vagrantfile'):
        print("ERROR: Vagrantfile not found")
        exit(1)


def options_error_checking():
    flag = False        # default value
    help_flag = False   # default value
    if '-h' in sys.argv or '--help' in sys.argv:
        help_flag = True
    if len(sys.argv) == 1:
        parser.print_help()
        flag = True
    elif len(sys.argv) == 3 and args.file:
        # print(args.file)
        print("Error, the -f and --file flags require other options specified")
        parser.print_help()
        flag = True
    elif len(sys.argv) == 4 and args.file and help_flag:
        print("Error, the -f and --file flags require other options specified")
        parser.print_help()
        flag = True
    if flag:
        exit(0)


def change_working_directory_to_vagrantfile():
    if args.file:
        folder_path = os.path.dirname(os.path.abspath(args.file))
        # print(f"folder_path = {folder_path}")
        os.chdir(folder_path)
        # print(os.path.curdir)   # present for testing
    else:
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        os.chdir("..")


def provision_vm():
    """
        Provisions vagrant box defined in Vagrantfile.\n
        This is for a specific use case where "vagrant ssh -c ${command}" needs to run after vagrant up\n
        Assumes:
            * Vagrantfile is located in current working directory
            * the ansible gets installed on the vagrant box
            * the specified ansible playbook exists and doesn't error
    :return:
    """
    print("provision_vm function placeholder")
    vm_name = get_vagrant_box()
    if get_status():
        print(f"{vm_name} is already provisioned")
        exit(1)
    else:
        subprocess.run(['vagrant', 'up'], stdout=sys.stdout)
        subprocess.run(['vagrant', 'ssh', '-c', '"ansible-playbook /vagrant/ansible/kubernetesConfiguration.yml"'],
                       stdout=sys.stdout)


def destroy_vm():
    """
        Forcefully destroys vagrant box defined in Vagrantfile.\n
        Assumes:
            * Vagrantfile located in current working directory
    :return:
    """
    print("destroy_vm function placeholder")
    vm_name = get_vagrant_box()
    if get_status():
        print(f"{vm_name} is provisioned.\nDestroying {vm_name}")
        subprocess.run(['vagrant', 'destroy', '-f'], stdout=sys.stdout)
    else:
        print(f"{vm_name} not found. Nothing to destroy.")


def display_status():
    """
        Prints to stdout results of 'vagrant status'.\n
        Assumes:
            * Vagrantfile in current working directory
    """
    os.system('vagrant status')     # os.system used for easier stdout


def get_status():
    """
        Checks if vagrant box is present.\n
        Assumes:
            * only one vagrant box defined in Vagrantfile\n
            * current working directory contains Vagrantfile
        :returns: True if vagrant box is present, else false
    """
    vm_name = get_vagrant_box()
    vagrant_status = subprocess.run(['vagrant', 'status'], stdout=subprocess.PIPE)
    print(type(vagrant_status.stdout.decode('utf-8')))
    if 'not created' in vagrant_status.stdout.decode('utf-8').lower():
        print(f"{vm_name} is not created")
        return False
    else:
        print(f"{vm_name} is created")
        return True


def get_vagrant_box():
    """
        Returns name of Vagrant Box defined by Vagrantfile.\n
        Assumes:
            * only 1 vm is defined in Vagrantfile,
            * that it should check for Vagrantfile in working directory
        :returns: str - name of Vagrant Box defined by Vagrantfile
    """
    # in vagrantfile, the vm name is between two quotation marks after "config.vm.define"
    if os.path.exists('Vagrantfile'):
        with open('Vagrantfile', mode='r') as f:
            lines = f.readlines()
            for line in lines:
                if "config.vm.define" in line:
                    marker = '"'
                    vm_name = line[line.find(marker)+len(marker):line.rfind(marker)]
                    return vm_name
        print("ERROR: Could not find name of Vagrant Box in Vagrantfile")
        exit(1)
    else:
        print("ERROR: Could not find Vagrantfile")
        exit(1)


# define arguments
parser = argparse.ArgumentParser(description='Script helps control lifecycle of vagrant box')
parser.add_argument('-f', '--file', metavar='', help='Filepath to Vagrantfile. Default is "../Vagrantfile". '
                                                     'Requires other options specified that are not -h or --help')
parser.add_argument('-r', '--reloadvm', action='store_true', help='Destroys vagrant box and then provisions it again')
parser.add_argument('-p', '--provision', action='store_true', help='Provisions and configures vm with Vagrant')
parser.add_argument('-d', '--delete', action='store_true', help='destroys vagrant box')
parser.add_argument('-s', '--status', action='store_true', help='displays results of "vagrant status" command')
args = parser.parse_args()


if __name__ == "__main__":
    main()
