#!/usr/bin/env python
import bibtexparser
import io
import sys


def convert(bibtex_input, bibtex_output=None):
    bibtex_database = bibtexparser.load(io.open(bibtex_input))

    for entry in bibtex_database.entries:
        if 'author' in entry:
            authors = entry['author'].split(' and ')
            for i, _ in enumerate(authors):
                fulname = authors[i].strip().split(',')
                surname = fulname[0].strip()
                if surname.startswith('{'):
                    pass
                else:
                    surname = "{%s}" % surname
                fulname[0] = surname
                authors[i] = ",".join(fulname)
            entry['author'] = " and ".join(authors)

        # entry['language'] = '{en}'
        if 'language' in entry:
            del entry['language']

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
        print("usage: bibtex_keep_surname input.bib [output.bib]")
