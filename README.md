# MiniKube-Sandbox
Sandbox repo for learning Kubernetes with MiniKube

<h1>General Usage and Branch Structure</h1>
If you wish to use this sandbox too, I will be maintaining a branch called "Vanilla" which will only automate the setup of minikube. You can clone this branch to start using and learning as you see fit. 
I will also have a dev branch to learn and get things work, and once working the changes will be merged into main.

<h1>Pre-requisites</h1>

  * Virtualized hardware will need:
      * 20 GB free storage
      * 2 GB free memory
      * 2 CPUs
  * Software
      * Vagrant: https://www.vagrantup.com/docs/installation
      * Virtualbox: https://www.virtualbox.org/wiki/Downloads
      * git for cloning the repository

All of these applications can also be installed via CLI on Windows with Chocolatey, and Mac with Homebrew

<h1>Setup Instructions</h1>

  * cd into the directory where you cloned the repository. This directory should contain the "Vagrantfile"
  * run the command "vagrant up" to provision and configure your vm
  * After the virtual machine is configured, run the command "vagrant ssh" to ssh into the vm you just provisioned and configured
  * Start minikube by running the command "minikube start"
      * This uses the Docker driver to run minikube, i.e. minikube is itself a docker container requiring the docker engine to run, and also has the docker-engine installed in the container so that Kubernetes pods can use docker as their container run-time.

When you are done with testing/working with minikube:
  * Exit your vm with the command exit
  * Power down vm with command "vagrant halt"; or,
  * Suspend vm with command "vagrant suspend". You will need to use "vagrant resume" to start vm again; or,
  * Destroy vm with command "vagrant destroy". You can easily create again with the "vagrant up" command

<h1>Technical Difficulties</h1>

To start Minikube, you need to manually run the command:

> minikube start

after ssh'ing into the vm using the "vagrant ssh" command.

I tried for about 90 minutes to get this command to work from the minikubeConfiguration.sh script, but could not do so.
Confirmed I was running script as user vagrant, not running as root (provisioner privileged:false in Vagrantfile), and added the user vagrant to the docker group, but still am not able to run the command without errors.

<h1>Next Steps</h1>

  * Convert configuration bash script to an ansible playbook
  * Utilize the Ansible/Packer/Terraform stack to automate MiniKube VM provisioning/configuration to public cloud
  * Run a Jenkins or Gitlab container
  * Run Argo CD
  * Configure CI/CD pipelines for DevOps/GitOps workflows
  * Run a simple web app 
  * Monitor with a Prometheus container 
