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


def make_journal_dict():
    urls = ["http://adsabs.harvard.edu/abs_doc/journals1.html",
            "http://ads.bao.ac.cn/abs_doc/journals1.html"]

    print('making journal abbreviation list...')

    import requests
    from lxml import etree
    r = requests.get(urls[0])
    p = etree.HTML(r.content)
    xpaths = p.xpath('body/pre/a')

    journal_dict = {reduce_name(journal.tail): reduce_abbr(journal.text)
                    for journal in xpaths if journal.tail is not None}

    print('done.')
    return journal_dict


def load_journal_dict():
    dir = os.path.dirname(os.path.realpath(__file__))
    journal_dict_file = "%s/ads_journal_abbr.json" % dir
    journal_dict_custom_file = "%s/ads_journal_abbr_custom.json" % dir

    if not os.path.exists(journal_dict_file):
        journal_dict = make_journal_dict()
        json.dump(journal_dict, open(journal_dict_file, 'w'),
                  indent=4, sort_keys=True)

    journal_dict = json.load(open(journal_dict_file))
    if os.path.exists(journal_dict_custom_file):
        journal_dict_custom = json.load(open(journal_dict_custom_file))
        journal_dict.update(journal_dict_custom)
    return journal_dict


def convert(bibtex_input, bibtex_output=None):
    parser = bibtexparser.bparser.BibTexParser(
        ignore_nonstandard_types=True,
        homogenize_fields=False,
        common_strings=True,
    )
    bibtex_database = parser.parse_file(io.open(bibtex_input))
    journal_dict = load_journal_dict()

    for entry in bibtex_database.entries:
        if 'journal' in entry:
            journal_raw = entry['journal']
            journal = reduce_name(journal_raw)

            if journal.startswith('arxiv'):
                pass
            elif journal in journal_dict:
                entry['journal'] = journal_dict[journal]
            elif journal in journal_dict.values():
                pass
            else:
                print(u"Warning: No abbreviation for '{}'".format(journal_raw), file=sys.stderr)

    if bibtex_output:
        bibtexparser.dump(bibtex_database, io.open(bibtex_output, 'w'))
    else:
        bibtexparser.dump(bibtex_database, sys.stdout)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        convert(sys.argv[1])
    elif len(sys.argv) == 3:
        convert(sys.argv[1], sys.argv[2])
    else:
        print("usage: bibtex_abbr input.bib [output.bib]")
