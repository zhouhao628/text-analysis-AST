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
        - The *-a* option defines the actual AST method implementation to be used. Possible arguments are *"easa"* (Enhanced Annotated Suffix Arrays), *"ast_linear"* (Linear-time and -memory implementation of Annotated Suffix Trees) and *"ast_naive"* (a slow and memory-consumptive implementation, present just for comparison).
        - The *-d* option and specifies whether the the matching score should be computed in the denormalized form (normalized by default, see *[Mirkin, Chernyak & Chugunova, 2012]*.
    - For the *Cosine* relevance measure:
        - The *-v* option specifies what elements should form the vector space, i.e. be the actual terms (these can be *"stems"*, *"lemmata"* or just *"words"*. In the first two cases, the words in the text collection get transformed into stems/lemmata automatically).
        - The *-w* option determines which term weighting scheme should be used (*"tf-idf"* or just *"tf"*).
- The *-y* option and determines whether the matching score should be computed taking into account the synonyms extracted from the text file.
- The *-l* option tells EAST about the language in which the texts in the collection and the keyphrases are written. In general, EAST does not need this information to compute the AST similarity scores. However, it is used to compute the cosine similarity scores (in case the user prefers this relevance measure type). English is the default language; all possible values of this parameter are: *"danish"* / *"dutch"* / *"english"* / *"finnish"* / *"french"* / *"german"* / *"hungarian"* / *"italian"* / *"norwegian"* / *"porter"* / *"portuguese"* / *"romanian"* / *"russian"* / *"spanish"* / *"swedish"*.
- The *-f* option specifies the format in which the table should be printed. The format is *XML* by default (see an example below); the *-f* option can also take *CSV* as its parameter.
- Please note that you can also specify the path to a single text file instead of that for a directory. In case of the path to a directory, only *.txt* files will be processed.

If you want to print the output to some file, just redirect the *EAST* output (e.g. by appending *> filename.txt* to the command in Unix).

Sample output in the XML format:

::

    <table>
      <keyphrase value="KEYPHRASE_1">
        <text name="TEXT_1">0.250</text>
        <text name="TEXT_2">0.234</text>
      </keyphrase>
      <keyphrase value="KEYPHRASE_2">
        <text name="TEXT_1">0.121</text>
        <text name="TEXT_2">0.000</text>
      </keyphrase>
      <keyphrase value="KEYPHRASE_3">
        <text name="TEXT_1">0.539</text>
        <text name="TEXT_3">0.102</text>
      </keyphrase>
    </table>

    

Keyphrases graph
~~~~~~~~~~~~~~~~

The *east* software also allows to construct a **keyphrases relation graph**, which indicates implications between different keyphrases according to the text corpus being analysed. The graph construction algorithm is based on the analysis of co-occurrences of keyphrases in the text corpus. A keyphrase is considered to imply another one if that second phrase occurs frequently enough in the same texts as the first one (that frequency is controlled by the referral confidence parameter). A keyphrase counts as occuring in a text if its presence score for that text ecxeeds some threshold *[Mirkin, Chernyak, & Chugunova, 2012]*.

*$ east [-f <graph_format>] [-c <referral_confidence>] [-r <relevance_threshold>] [-p <support_threshold>] [-s] [-d] [-a <ast_algorithm>] [-w <term_weighting>] [-v <vector_space>] [-y] keyphrases graph <keyphrases_file> <directory_with_txt_files>*

- The *-p* option configures the threshold for graph node support (the number of documents "containing" the corresponding keyphrase according to the AST method), starting with which the nodes get included into the graph.
- The *-c* option controls the *referral confidence* level above which the implications between keyphrases are considered to be strong enough to be added as graph arcs. The confidence level should be a float in [0; 1] and is 0.6 by default.
- The *-r* option controls the  *relevance threshold of the matching score* - the minimum matching score value where keyphrases start to be counted as occuring in the corresponding texts. It should be a float in [0; 1] and is 0.25 by default.
- The *-f* option determines in which format the resulting graph should come to the output. Possible values are:
    - *"gml"* (`Graph Modelling Language <http://en.wikipedia.org/wiki/Graph_Modelling_Language>`_, which can be used for graph visualization in tools like `Gephi <http://gephi.org>`_);
    - *"edges"*, which is just a list of edges in form *Keyphrase -> <List of keyphrases it points to>* (simple but convenient for a quick analysis of implications between keyphrases).
- The *-s* option, as well as its auxiliary options (*-d*, *-a*, *-v*, *-w* and *-y*) configure the relevance scores computation (exactly as for the *keyphrases table* command). Note that the relevance measure (*"ast"* / *"cosine"*) used while computing the graph usually largely influences its shape.


Sample output in the *edges* format:

::

    KEYPHRASE_1 -> KEYPHRASE_3
    KEYPHRASE_2 -> KEYPHRASE_3, KEYPHRASE_4
    KEYPHRASE_4 -> KEYPHRASE_1

The same graph in *gml*:

::

    graph
    [
      node
      [
        id 0
        label "KEYPHRASE_1"
      ]
      node
      [
        id 1
        label "KEYPHRASE_2"
