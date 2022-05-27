# -*- coding: utf-8 -*


def format_table(table, format):
    if format == "xml":
        return table2xml(keyphrases_table)
    elif format == "csv":
        return table2csv(keyphrases_table)
    else:
        raise Exception("Unknown table format: '%s'. "
                        "Please use one of: 'xml', 'csv'." % format)


def table2xml(keyphrases_table):
    res = "<table>\n"
    for keyphrase in sorted(keyphrases_table.keys()):
        res += '  <keyphrase value="%s">\n' % keyphrase
        for text in sorted(keyphrases_table[keyphrase].keys()):
            res += '    <text name="%s">' % text
            res += '%.3f' % keyphrases_table[keyphrase][text]
            res += '</text>\n'
        res += '  </keyphrase>\n'
    res += "</table>\n"
    return res


def table2csv(keyphrases_table):

    def quote(s):
        return '"' + s.replace('"', "'") + '"'

    keyphrases = sorted(keyphrases_table.keys())
    texts = sorted(keyphrases_t