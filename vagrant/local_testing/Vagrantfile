# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|

  config.vm.define "web", primary: true do |web|
    # Vanilla debian base box from:
    # https://atlas.hashicorp.com/debian/
    web.vm.box = "debian/jessie64"

    web.vm.network "private_network", ip: "10.0.1.10"

    web.vm.provider "virtualbox" do |vb|
        vb.customize ["modifyvm", :id, "--memory", "2048"]
    end

    #shell.vm.synced_folder "../private_pico/picoCTF-problems-private/", "/private-problems"
  end

  config.vm.define "shell", primary: true do |shell|
    shell.vm.box = "debian/jessie64"

    shell.vm.network "private_network", ip: "10.0.1.11"

    shell.vm.provider "virtualbox" do |vb|
        vb.customize ["modifyvm", :id, "--memory", "2048"]
    end
  end

  config.vm.define "db", primary: true do |db|
    db.vm.box = "debian/jessie64"

    db.vm.network "private_network", ip: "10.0.1.20"

    db.vm.provider "virtualbox" do |vb|
        vb.customize ["modifyvm", :id, "--memory", "1024"]
    end
  end

end
