# cvs2git

A convenient wrapper script to migrate CVS repositories to GIT.

## Usage

First make sure you have VirtualBox and Vagrant installed. Then clone the project, provision the virtual machine and migrate your repository by executing:

~~~ bash
$ git clone https://github.com/choffmeister/cvs2git.git
$ cd cvs2git
$ vagrant up
$ vagrant ssh
$ /vagrant/bin/cvs2git.py /path/to/cvs/dir /path/to/git/dir
~~~

Tip: Put your CVS repository to the `modules/` folder. This way you can access it from within the VM and it is properly added to the gitignore rules.
