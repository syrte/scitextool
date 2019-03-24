#!/usr/bin/env python
import bibtexparser
import io
import sys
import re

"""
Create hyper links for doi, url or arxiv in `.bib` file.

- for arxiv paper:
    + insert arxiv link into 'journal'
- else:
    + insert doi link into 'journal'
    + insert url link (ads, arxiv or what ever) into 'volumne' (if any)
"""


def convert(bibtex_input, bibtex_output=None):
    parser = bibtexparser.bparser.BibTexParser(
        ignore_nonstandard_types=True,
        homogenize_fields=False,
        common_strings=True,
    )

    bibtex_database = parser.parse_file(io.open(bibtex_input))

    for entry in bibtex_database.entries:
        if entry['ENTRYTYPE'] != 'article':
            continue

        if 'journal' in entry:
            match_arxiv = (
                re.match(r'^arxiv:\s*(\d+\.\d+)', entry['journal'], re.I) or  # arXiv:1606.02694
                re.match(r'^arxiv:\s*(\D+/\d+)', entry['journal'], re.I) or  # arXiv:astro-ph/9905116
                re.match(r'^arxiv:\s*(\d+\.\d+)', entry.get('pages', ''), re.I)
            )
        elif entry.get('archiveprefix', '').lower() == 'arxiv':
            match_arxiv = (
                re.match(r'^(\d+\.\d+)', entry.get('eprint', '')) or
                re.match(r'^(\D+/\d+)', entry.get('eprint', ''))
            )
        elif 'url' in entry:
            match_arxiv = (
                re.match(r'^https?://arxiv.org/abs/(\d+\.\d+)', entry['url']) or
                re.match(r'^https?://arxiv.org/abs/(\D+/\d+)', entry['url'])
            )
        else:
            match_arxiv = None

        if match_arxiv:
            arxivid = match_arxiv.group(1)
            entry['journal'] = r"{arXiv:\href{https://arxiv.org/abs/%s}{%s}}" % (
                arxivid, arxivid)
            entry.pop('pages', None)
            entry.pop('doi', None)
            entry.pop('url', None)
        elif 'journal' in entry:
            if 'doi' in entry:
                entry['journal'] = r"{\href{https://doi.org/%s}{%s}}" % (
                    entry['doi'], entry['journal'])
                entry.pop('doi')

            if 'url' in entry and 'volume' in entry:
                entry['volume'] = r"{\href{%s}{%s}}" % (
                    entry['url'], entry['volume'])
                entry.pop('url')

        # drop eprint labels for arxiv
        if entry.get('archiveprefix', '').lower() == 'arxiv':
            entry.pop('archiveprefix', None)
            entry.pop('eprinttype', None)
            entry.pop('eprint', None)

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
        print("usage: bibtex_hyperlink input.bib [output.bib]")
