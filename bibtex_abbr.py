#!/usr/bin/env python
from __future__ import print_function
import bibtexparser
import re
import io
import sys
import os
import json


def reduce_name(string):
    """Lower the article name, and strip the unwanted characters.
    """
    string = string.strip().lower()
    string = re.sub(r'^the\s|:|&|-|\\', '', string)
    return string


def reduce_abbr(string):
    """Convert `&` to LaTeX `\&`.
    """
    string = string.strip().replace("&", "\&")
    return string


def get_journal_dict():
    import requests
    from lxml import etree

    urls = ["http://adsabs.harvard.edu/abs_doc/journals1.html",
            "http://ads.bao.ac.cn/abs_doc/journals1.html"]

    r = requests.get(urls[0])
    p = etree.HTML(r.content)
    xpaths = p.xpath('body/pre/a')

    journal_dict = {reduce_name(journal.tail): reduce_abbr(journal.text)
                    for journal in xpaths if journal.tail is not None}

    # special cases
    journal_dict.update({
        'astrophysical journal letters': 'APJ',
        'monthly notices of the royal astronomical society letters': 'MNRAS',
        'journal of physics conference series': 'JPhCS',
        'journal of statistical computation and simulation': 'JSCS',
    })

    return journal_dict


def convert(journal_dict, bibtex_input, bibtex_output=None):
    bibtex_database = bibtexparser.load(io.open(bibtex_input))

    for entry in bibtex_database.entries:
        if 'journal' in entry:
            journal = entry['journal']
            journal = reduce_name(journal)

            if journal in journal_dict:
                entry['journal'] = journal_dict[journal]
            elif journal in journal_dict.values():
                pass
            else:
                print(u"Warning: No abbreviation for '{}'".format(journal), file=sys.stderr)

    if bibtex_output:
        bibtexparser.dump(bibtex_database, io.open(bibtex_output, 'w'))
    else:
        bibtexparser.dump(bibtex_database, sys.stdout)


if __name__ == "__main__":
    journal_dict_file = "ads_journal_abbr.json"

    if os.path.exists(journal_dict_file):
        journal_dict = json.load(open(journal_dict_file))
    else:
        journal_dict = get_journal_dict()
        json.dump(journal_dict, open(journal_dict_file, 'w'), indent=4, sort_keys=True)

    if len(sys.argv) == 2:
        convert(journal_dict, sys.argv[1])
    elif len(sys.argv) == 3:
        convert(journal_dict, sys.argv[1], sys.argv[2])
    else:
        print("usage: bibtex_abbr input.bib [output.bib]")
