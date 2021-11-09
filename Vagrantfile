# -*- mode: ruby -*-
# vi: set ft=ruby :
VAGRANT_EXPERIMENTAL="disks"

Vagrant.configure("2") do |config|
  config.vm.define "minikube" do |minikube|
    minikube.vm.box = "geerlingguy/ubuntu1804"
    minikube.vm.hostname = "minikube"
    minikube.vm.provider "virtualbox" do |v|
      v.memory = 2048
      v.cpus = 2
    end
    minikube.vm.disk :disk, size: "20GB", primary: true 
    minikube.vm.network "private_network", ip: "10.1.0.2"
    minikube.vm.network "forwarded_port", guest: 80, host: 8080
    minikube.vm.provision "shell",privileged: true, path: "scripts/installAnsible.sh"
    minikube.vm.provision "ansible_local" do |ansible|
      ansible.playbook = "ansible/minikubeConfiguration.yml"
    end
    # minikube.vm.provision "shell", privileged: false, path: "scripts/minikubeConfiguration.sh"
  end
end