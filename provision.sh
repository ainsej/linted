export VE_DIR=/home/vagrant/.envs/linted
export CODE_DIR=/vagrant

#install dependencies
apt-get update
apt-get install -y build-essential git
apt-get install -y python-software-properties
apt-get install -y libpq-dev
apt-get install -y postgresql postgresql-contrib

#Install redis
add-apt-repository -y ppa:chris-lea/redis-server
apt-get update
apt-get install -y redis-server

#Install python packages
apt-get install -y python python-dev python-setuptools
easy_install pip
pip install setuptools --no-use-wheel --upgrade
pip install virtualenv

#Create postgres user / database
sudo -u postgres psql -c "CREATE USER linted WITH NOCREATEDB NOCREATEUSER ENCRYPTED PASSWORD 'development'"
sudo -u postgres psql -c "CREATE DATABASE linted WITH OWNER linted"

#Create virtualenv
virtualenv --no-site-packages $VE_DIR
$VE_DIR/bin/pip install -r $CODE_DIR/requirements.txt
chown -R vagrant $VE_DIR
chgrp -R vagrant $VE_DIR

#Run syncdb to create south specific databases
if [ ! -e /home/vagrant/.provisioned ]
then
    (cd $CODE_DIR && $VE_DIR/bin/python manage.py syncdb --noinput)
    touch /home/vagrant/.provisioned
fi

#Perform migrations for application
(cd $CODE_DIR && $VE_DIR/bin/python manage.py migrate linted)
