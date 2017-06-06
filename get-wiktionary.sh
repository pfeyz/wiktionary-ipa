dump="https://dumps.wikimedia.org/enwiktionary/20170101/enwiktionary-20170101-pages-articles.xml.bz2"
wget -qO- $dump | pv -s 560m| bunzip2 > enwik.xml
