#!/bin/bash

# Make sure `django-admin.py` is available

hash django-admin.py 2>/dev/null ||
    { echo >&2 "django-admin.py not found. Please install Django."; exit 1; }


# Functions

function makemessages() {
    echo "### Processing djadmin2..."
    ( cd djadmin2; django-admin.py makemessages -a )
    echo "### Processing example app..."
    ( cd example/blog; django-admin.py makemessages -a )
    echo "### Processing example2 app..."
    ( cd example2/polls; django-admin.py makemessages -a )
}

function compilemessages() {
    echo "### Processing djadmin2..."
    ( cd djadmin2; django-admin.py compilemessages )
    echo "### Processing example app..."
    ( cd example/blog; django-admin.py compilemessages )
    echo "### Processing example2 app..."
    ( cd example2/polls; django-admin.py compilemessages )
}


# Parse arguments

case $1 in
    "")
        echo "Available commands:"
        echo "--- makemessages"
        echo "--- compilemessages";
    ;;
    "makemessages")
        makemessages
    ;;
    "compilemessages")
        compilemessages
    ;;
esac
