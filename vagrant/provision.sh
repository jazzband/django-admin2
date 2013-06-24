#!/bin/bash

# Script to set up a Django project on Vagrant.

# Installation settings

PROJECT_NAME=$1

DB_NAME=$PROJECT_NAME
VIRTUALENV_NAME=$PROJECT_NAME

PROJECT_DIR=/home/vagrant/$PROJECT_NAME
VIRTUALENV_DIR=/home/vagrant/.virtualenvs/$PROJECT_NAME

# Python development packages
PACKAGES="build-essential python python-dev python-distribute python-pip"

export LANGUAGE=en_US.UTF-8
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8

# Update the apt cache
apt-get update -y

apt-get install -y $PACKAGES

# virtualenv global setup
pip install virtualenv virtualenvwrapper stevedore virtualenv-clone

# bash environment global setup
cp -p $PROJECT_DIR/vagrant/bashrc /home/vagrant/.bashrc
su - vagrant -c "mkdir -p /home/vagrant/.pip_download_cache"

# ---

# virtualenv setup for project
su - vagrant -c "/usr/local/bin/virtualenv $VIRTUALENV_DIR && \
    echo $PROJECT_DIR > $VIRTUALENV_DIR/.project && \
    PIP_DOWNLOAD_CACHE=/home/vagrant/.pip_download_cache $VIRTUALENV_DIR/bin/pip install -r $PROJECT_DIR/requirements.txt"

# run setup.py develop
su - vagrant -c "cd $PROJECT_DIR && $VIRTUALENV_DIR/bin/python setup.py develop"

# add in ipython
su - vagrant -c "$VIRTUALENV_DIR/bin/pip install ipython"

# activate the virtualenv as soon as we shell in
echo "workon $VIRTUALENV_NAME" >> /home/vagrant/.bashrc
