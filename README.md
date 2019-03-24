# scitextool

Some routines for the preparation of scientific paper submissions.

## Dependences:
bibtexparser

optional: requests, lxml

## bibtex_abbr.py
Convert the journal names in `.bib` file to their abbreviations.
The abbreviation rules is taken from [ADS](http://adsabs.harvard.edu/abs_doc/journals1.html).

**Usage:**
```bash
bibtex_abbr input.bib [output.bib]
```

Modify `ads_journal_abbr_custom.json` to add your custom abbreviations.

## bibtex_abbr.py
Create hyper links for doi, url or arxiv in `.bib` file.

- for arxiv paper:
    + insert arxiv link into 'journal'
- else:
    + insert doi link into 'journal'
    + insert url link (ads, arxiv or what ever) into 'volumne' (if any)

**Usage:**
```bash
bibtex_hyperlink input.bib [output.bib]
```

## bibtex_keep_surname.py
Protect the surname of the authors to prevent possible mis-interpretation by Chinese journal templates.

**Usage:**
```bash
bibtex_keep_surname input.bib [output.bib]
```

## To be continue
