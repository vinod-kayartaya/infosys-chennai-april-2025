"""
This module contains custom utility functions
"""

def dirr(obj):
    """
    This function returns a list of non-dunder attributes of the input object
    
    To import this, open python REPL shell from the current folder
    `from myutils import dirr`
    """
    return [a for a in dir(obj) if not a.startswith('_')]
