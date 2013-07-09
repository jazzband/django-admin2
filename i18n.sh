#!/bin/bash

### Helper functions

function assert_django {
    hash django-admin.py 2>/dev/null ||
        { echo >&2 "django-admin.py not found. Please install Django."; exit 1; }
}

function assert_tx {
    hash tx 2>/dev/null ||
        { echo >&2 "tx not found. Please install transifex-client."; exit 1; }
}

function are_you_sure {
    read -r -p "$1 Are you sure? [y/n] " response
    if [[ $response =~ ^([yY][eE][sS]|[yY])$ ]]
    then
        :
    else
        exit 1
    fi
}


### Command functions

function makemessages {
    assert_django
    echo "### Processing djadmin2..."
    ( cd djadmin2; django-admin.py makemessages -a )
    echo "### Processing example app..."
    ( cd example/blog; django-admin.py makemessages -a )
    echo "### Processing example2 app..."
    ( cd example2/polls; django-admin.py makemessages -a )
}

function compilemessages {
    assert_django
    echo "### Processing djadmin2..."
    ( cd djadmin2; django-admin.py compilemessages )
    echo "### Processing example app..."
    ( cd example/blog; django-admin.py compilemessages )
    echo "### Processing example2 app..."
    ( cd example2/polls; django-admin.py compilemessages )
}

function checkmessages {
    ls -1 djadmin2/locale/*/LC_MESSAGES/django.po | xargs -I {} msgfmt -c {}
    ls -1 example/blog/locale/*/LC_MESSAGES/django.po | xargs -I {} msgfmt -c {}
    ls -1 example2/polls/locale/*/LC_MESSAGES/django.po | xargs -I {} msgfmt -c {}
}

function pulltx {
    assert_tx
    echo "### Pulling new translations from Transifex..."
    tx pull -a
}

function pushtx {
    assert_tx
    are_you_sure "Warning: This might destroy existing translations."
    echo "### Pushing translations and sources to Transifex..."
    tx push -s
}


### Parse arguments

case $1 in
    "")
        echo "Available commands:"
        echo "--- makemessages: Generate or update .po files"
        echo "--- compilemessages: Compile .po files to .mo files";
        echo "--- checkmessages: Check .po files for syntax errors";
        echo "--- pulltx: Pull new translations from Transifex";
        echo "--- pushtx: Push translations and sources to Transifex";
    ;;
    "makemessages")
        makemessages
    ;;
    "compilemessages")
        compilemessages
    ;;
    "checkmessages")
        checkmessages
    ;;
    "pulltx")
        pulltx
    ;;
    "pushtx")
        pushtx
    ;;
    *)
        echo "Unknown command: $1"
    ;;
esac
