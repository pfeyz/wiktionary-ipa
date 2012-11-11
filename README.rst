================
 Wiktionary IPA
================

This is a script I'm writing to extract all the IPA transcriptions of dictionary
words present in the Wiktionary. I'm using a sax XML parser because the xml file
is ~ 3 gigs and I don't have enough ram to use a tree-based parser on something
that big.

Run get-wiktionary.sh to download and decompress the wiktionary dump of all
articles, and parse-wiktionary.py (python3!) to extract the transcriptions.

Still a work in progress.
