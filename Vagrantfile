# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|

  config.vm.define "shell", primary: true do |shell|

    shell.vm.box = "picoCTF/shell-base"
    shell.vm.network "private_network", ip: "192.168.2.3"

    shell.vm.synced_folder ".", "/vagrant", disabled: true
    shell.vm.synced_folder ".", "/picoCTF"

    # Directly use shell provisioner until Vagrant fix lands in 1.8.2, issue #6740
    shell.vm.provision "shell", path: "vagrant/provision_scripts/install_ansible.sh"
    shell.vm.provision "shell" do |s|
        s.inline = "cd $1 && ansible-playbook -i $2 --limit $3 site.yml"
        s.args   = ["/picoCTF/ansible/","inventories/local_development", "shell"]
    end
    # Replace above with this once vagrant 1.8.2 is released
    #shell.vm.provision :ansible_local do |ansible|
    #    ansible.playbook            = "site.yml"
    #    ansible.limit               = "shell"
	#    ansible.provisioning_path   = "/picoCTF/ansible/"
    #    ansible.inventory_path      = "/picoCTF/ansible/inventories/local_development"
    #end

    shell.vm.provider "virtualbox" do |vb|
        vb.name = "picoCTF-shell-dev"
        vb.customize ["modifyvm", :id, "--memory", "2048"]
    end
  end

  config.vm.define "web", primary: true do |web|
    
    web.vm.box = "picoCTF/web-base"
    web.vm.network "private_network", ip: "192.168.2.2"

    web.vm.synced_folder ".", "/vagrant", disabled: true
    web.vm.synced_folder ".", "/picoCTF"

    # Directly use shell provisioner until Vagrant fix lands in 1.8.2, issue #6740
    web.vm.provision "shell", path: "vagrant/provision_scripts/install_ansible.sh"
    web.vm.provision "shell" do |s|
        s.inline = "cd $1 && ansible-playbook -i $2 --limit $3 site.yml"
        s.args   = ["/picoCTF/ansible/","inventories/local_development", "db,web"]
    end
    # Replace above with this once vagrant 1.8.2 is released
    #web.vm.provision :ansible_local do |ansible|
    #    ansible.playbook            = "site.yml"
    #    ansible.limit               = ["db","web"]
	#    ansible.provisioning_path   = "/picoCTF/ansible/"
    #    ansible.inventory_path      = "/picoCTF/ansible/inventories/local_development"
    #end

    web.vm.provider "virtualbox" do |vb|
        vb.name = "picoCTF-web-dev"
        vb.customize ["modifyvm", :id, "--memory", "1024"]
    end
  end

end
