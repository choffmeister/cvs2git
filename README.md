# cvs2git

A convenient wrapper script to migrate CVS repositories to GIT.

## Usage

First make sure you have VirtualBox and Vagrant installed. Then clone the project and provision the virtual machine by executing:

~~~ bash
$ git clone https://github.com/choffmeister/cvs2git.git
$ cd cvs2git
$ vagrant up
~~~

Then put some ZIP files containing your CVS repository files (the ones from the server) into the `modules/` folder. Make sure that the ZIP files contain the content in the root directory. Then log into the VM and run the migration script:

~~~
$ vagrant ssh
$ /vagrant/bin/migrate.py
~~~
