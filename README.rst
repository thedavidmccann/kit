Installation
============

The following is a step-by-step process for installing the development indicator
collection kit on an Ubuntu machine.

Virtual Environment
--------------------
If you're installing the collection kit on a machine with other python applications,
you'll likely want to create a "Virtual Environment" to install all dependencies.  This
keeps the copy of python in /usr clean, and also keeps you from having to run
sudo to install every dependency.  From a terminal, you'll run the following commands:

::

    sudo apt-get install python-virtualenv
    
    cd /path/to/your/virtual/environments/

    mkdir virtual_environments

    cd virtual_environments

    virtualenv --no-site-packages kit

    source kit/bin/activate

Downloading the source
----------------------
Second, you'll need the application source itself.  Unfortunately, for now, this
required a clone directly from github (rather than a download or pip install).  Check
this README on github for updates to the install process.  From a terminal, run:

::

    cd /path/to/your/projects/

    git clone git://github.com/daveycrockett/kit.git

    cd kit
    
    git submodule init
    
    git submodule update

Configuring the application
---------------------------
Once you've downloaded kit, you'll need to install kit's requirements:

    cd kit

    pip install -r requirements.pip

Run the usual database initialization steps:

    python manage.py syncdb

    python manage.py migrate

And now you should be ready to run the server:

    python manage.py runserver

Dashboard
=========
When you navigate to http://localhost:8000, you'll be walked through the process of
initializing the system to collect data.  This involves uploading locations (these
aren't GPS coordinates, but rather a tree of locations for aggregating information),
users (those reporting information), reports (SMS reports and XForms) and indicators 
(individual pieces of data to be collected). 
