# scitextool

Some routines for the preparation of scientific paper submissions.

## Dependences:
bibtexparser, requests, lxml

## bibtex_abbr.py
Convert the name of journals in bibtex file to corresponding abbreviations.
The abbreviation rules is taken from [ADS](http://adsabs.harvard.edu/abs_doc/journals1.html).

### Usage:
```bash
bibtex_abbr input.bib [output.bib]
```

Modify `ads_journal_abbr.json` to add your custom abbreviations.


## bibtex_keep_surname.py
Protect the surname of the authors to prevent possible mis-interpretation by Chinese journal templates.

### Usage:
```bash
bibtex_keep_surname input.bib [output.bib]
```

## To be continue
