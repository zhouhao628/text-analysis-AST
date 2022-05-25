# -*- coding: utf-8 -*


def format_table(table, format):
    if format == "xml":
        return table2xml(keyphrases_table)
    elif format == "csv":
        return table2csv(keyphrases_table)
    else