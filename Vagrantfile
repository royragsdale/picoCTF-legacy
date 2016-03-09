# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|

  config.vm.define "shell", primary: true do |shell|
    shell.vm.box_url = "https://cloud-images.ubuntu.com/vagrant/vivid/current/vivid-server-cloudimg-amd64-vagrant-disk1.box"
    shell.vm.box = "ubuntu/vivid64"

    # Bug fixed in 1.7.4
    # shell.vm.hostname = "shell"
    shell.vm.provision :shell, inline: "hostnamectl set-hostname shell"

    shell.ssh.forward_agent = true

    shell.vm.network "private_network", ip: "192.168.2.3"

    shell.vm.provision :shell, :path => "scripts/shell_setup.sh"

    shell.vm.synced_folder ".", "/vagrant",
        owner: "vagrant",
        group: "root",
        mount_options: ["dmode=1710"]

    shell.vm.provider "virtualbox" do |vb|
        vb.customize ["modifyvm", :id, "--memory", "3072"]
    end
  end

  config.vm.define "web", primary: true do |web|
    web.vm.box_url = "https://cloud-images.ubuntu.com/vagrant/vivid/current/vivid-server-cloudimg-amd64-vagrant-disk1.box"
    web.vm.box = "ubuntu/vivid64"

    # web.vm.hostname = "web"
    web.vm.provision :shell, inline: "hostnamectl set-hostname web"

    web.vm.network "private_network", ip: "192.168.2.2"

    web.vm.provision :shell, :path => "scripts/web_setup.sh"
    web.ssh.forward_agent = true

    web.vm.provider "virtualbox" do |vb|
        vb.customize ["modifyvm", :id, "--memory", "2048"]
    end
  end

end
