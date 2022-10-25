'''
Author: Tao
Date: 2022-10-25 13:49:51
LastEditors: Tao
LastEditTime: 2022-10-25 13:50:40
Description: 
Email: 202203580@post.au.dk
Copyright (c) 2022 by Tao Tang, All Rights Reserved. 
'''
#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pythonProject1.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
