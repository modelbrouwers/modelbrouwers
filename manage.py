#!/usr/bin/env python2.7
import os, sys

if __name__ == "__main__":
    sys.path.append('/home/modelbrouw/brouwers/')
    #sys.path.append('/home/modelbrouw/brouwers/brouwers/')
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "brouwers.settings")
    from django.core.management import execute_from_command_line
    
    execute_from_command_line(sys.argv)
