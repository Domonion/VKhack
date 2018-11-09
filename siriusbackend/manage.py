#!/usr/bin/env python
import os
import sys

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'siriusbackend.settings')

    GRAPH_PATH = os.environ['GRAPH_PATH']
    SUBCATEGORIES_GRAPH_FILE = 'subcategories_graph.json'
    EVENTS_GRAPH_FILE = 'events_graph.json'

    SUBCATEGORIES_GRAPH = os.path.join(GRAPH_PATH, SUBCATEGORIES_GRAPH_FILE)
    EVENTS_GRAPH = os.path.join(GRAPH_PATH, EVENTS_GRAPH_FILE)

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
