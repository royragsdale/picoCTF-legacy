# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|

  config.vm.define "shell", primary: true do |shell|

    # Vanilla debian base box from: https://atlas.hashicorp.com/debian/
    # includes vboxsf module for synchronization
    shell.vm.box = "debian/contrib-jessie64"
    shell.vm.network "private_network", ip: "192.168.2.3"

    shell.vm.synced_folder ".", "/vagrant", disabled: true
    shell.vm.synced_folder ".", "/picoCTF"

    shell.vm.provision "shell", path: "ansible/scripts/install_ansible.sh"
	shell.vm.provision :ansible_local do |ansible|
        ansible.playbook            = "site.yml"
        ansible.limit               = "shell"
	    ansible.provisioning_path   = "/picoCTF/ansible/"
        ansible.inventory_path      = "/picoCTF/ansible/inventories/dev_servers"
    end

    shell.vm.provider "virtualbox" do |vb|
        vb.name = "picoCTF-shell-dev"
        vb.customize ["modifyvm", :id, "--memory", "2048"]
    end
  end

  config.vm.define "web", primary: true do |web|
    
    web.vm.box = "debian/contrib-jessie64"
    web.vm.network "private_network", ip: "192.168.2.2"

    web.vm.synced_folder ".", "/vagrant", disabled: true
    web.vm.synced_folder ".", "/picoCTF"

    web.vm.provision "shell", path: "ansible/scripts/install_ansible.sh"
	web.vm.provision :ansible_local do |ansible|
        ansible.playbook            = "site.yml"
        ansible.limit               = ["db","web"]
	    ansible.provisioning_path   = "/picoCTF/ansible/"
        ansible.inventory_path      = "/picoCTF/ansible/inventories/dev_servers"
    end

    web.vm.provider "virtualbox" do |vb|
        vb.name = "picoCTF-web-dev"
        vb.customize ["modifyvm", :id, "--memory", "1024"]
    end
  end

end
