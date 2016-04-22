# Windows

The platform is primarily developed from a linux guest, but there should be nothing preventing development on Windows.  There are a few gotchas and common errors related to the underlying tools like [Vagrant](https://www.vagrantup.com/), but once you have those components working it should be a smooth process.

## Errors

- `The box 'picoCTF/shell-base' could not be found or could not be accessed in the remote catalog.`
    - Experienced on Windows 10
    - Related to [Vagrant Issue #6754](https://github.com/mitchellh/vagrant/issues/6754)
    - Tested solution. Install [Microsoft Visual C++ 2010 SP1 Redistributable Package (x86)](https://www.microsoft.com/en-us/download/confirmation.aspx?id=8328)

- ```ansible local provisioner: * `playbook` does not exist on the guest: C:/picoCTF/ansible/site.yml```
    - Experienced on Windows 10
    - Occurs when a machine was unsuccessfully created and the necessary inventory files were not synced over.
    - Related to [Vagrant PR #6800](https://github.com/mitchellh/vagrant/pull/6800) and should be fixed in Vagrant 1.8.2
    - Tested solution. Open Virtualbox and manually destroy the machine.