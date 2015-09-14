# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "ubuntu/trusty32"
  config.ssh.forward_agent = true
  config.vm.synced_folder "../", "/home/vagrant/project"
  config.vm.provision "ansible" do |ansible|
    ansible.playbook = "provisioning/playbook.yml"
  end

  config.vm.provider "virtualbox" do |v, override|
    v.name = "twitter"
    v.memory = 1024
    v.customize ["modifyvm", :id, "--ioapic", "on"]
    v.customize ["modifyvm", :id, "--cpus", "2"]
    override.vm.network "private_network", ip: "192.168.50.4"
  end

  config.vm.provider "lxc" do |v, override|
    override.vm.box = "fgrehm/trusty64-lxc"
    override.vm.network "forwarded_port", guest: 3456, host:3456
  end
end