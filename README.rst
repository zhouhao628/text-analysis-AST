EAST
====

**EAST** stands for the *Enhanced Annotated Suffix Tree* method for text analysis.


Installation
------------

To install EAST, run:

::

    $ pip install EAST

This may require admin permissions on your machine (and should then be run with *sudo*).

EAST comes both as a *CLI application* and as a *python library* (which can be imported and used in python code).


CLI application
------------------------

Keyphrases table
~~~~~~~~~~~~~~~~

The basic use case for the AST method is to calculate matching scores for a set of keyphrases against a set of text files (the so-called **keyphrase table**). To do that with **east**, launch it as fo