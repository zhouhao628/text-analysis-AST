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

The basic use case for the AST method is to calculate matching scores for a set of keyphrases against a set of text files (the so-called **keyphrase table**). To do that with **east**, launch it as follows:

*$ east [-f <table_format>] [-l <language>] [-s] [-d] [-a <ast_algorithm>] [-w <term_weighting>] [-v <vector_space>] [-y] keyphrases table <keyphrases_file> <directory_with_txt_files>*

- The *-s* option determines the similarity measure to be used while computing the matching score. Its value is *"ast"* by default (as this package has been developed primarily as an implementation of the Annotated Suffix Tree method), but it can be also set to *"cosine"*: the cosine similary will be used then to compute the relevance of keyphrases to documents (the text in the collection will be represented as vectors then). 
- Depending on which relevance measure is used while computing the table, there are some auxiliary options to further specify the computation:
    - For the *AST* relevance measure:
        - The *-a* option defines the actual AST method implementation to be used. Possible arguments are *"easa"* (Enhanced 