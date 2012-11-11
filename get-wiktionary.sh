dump="http://dumps.wikimedia.org/enwiktionary/20121104/enwiktionary-20121104-pages-articles.xml.bz2"
wget -qO- $dump | pv -s 350m| bunzip2 > enwik.xml
