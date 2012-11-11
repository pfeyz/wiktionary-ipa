#!/usr/bin/env python3

"""

Not handled

  * {{a|[[w:Canadian English|CA]]; US, in accents with the [[cot-caught
      merger]]}} {{IPA|/ˈdɪfθɑŋ/|/ˈdɪpθɑŋ/}}

  * {{a|RP|[[antepenultimate]] [[stress]]}}
    {{IPA|/trɑːnsˈleɪtɹɪsiːz/|/trænsˈleɪtɹɪsiːz/|/trɑːnzˈleɪtɹɪsiːz/|/trænzˈleɪtɹɪsiːz/}}

  * {{a|RP|[[penultimate]] stress}}
    {{IPA|/ˌtrɑːnsleɪˈtɹaɪsiːz/|/ˌtrænsleɪˈtɹaɪsiːz/|/ˌtrɑːnzleɪˈtɹaɪsiːz/|/ˌtrænzleɪˈtɹaɪsiːz/}}

"""

from xml import sax
import re

class IpaParser(sax.handler.ContentHandler):

    special_chars = '"&<>'
    region_regex = r"{{a\|(.*?)}}"
    ipa_regex = r"{{IPA\|(.*?)}}"

    def __init__(self, *args, **kwargs):
        super(sax.handler.ContentHandler, self).__init__(*args, **kwargs)
        self.depth = 0
        self.reading_page = False
        self.reading_ns = False
        self.reading_title = False
        self.reading_text = False
        self.reading_english = False
        self.reading_phonetics = False
        self.reading_entry = False
        self.title = None
        self.entry = None
        self.lines = 0

    def emit_entry(self):
        ipa = re.search(self.ipa_regex, self.entry)
        region = re.search(self.region_regex, self.entry)
        if ipa and not re.search("lang=", ipa.group(1)):
            print(self.title, end=", ")
            if region:
                regions = region.group(1).split("|")
                print("regions={0}".format(", ".join(regions)), end=" - ")
            transcriptions = re.findall(r"/(.*?)/", ipa.group(1))
            print("ipa={0}".format(", ".join(transcriptions)))

    def startElement(self, name, attrs):
        if name == "page":
            self.reading_page = True
        if self.reading_page and name == "title":
            self.reading_title = True
        if self.reading_page and name == "ns":
            self.reading_ns = True
        if self.reading_page and name == "text":
            self.reading_text = True
        #print("{0}start {1}".format("|  " * self.depth, name))
        self.depth += 1

    def characters(self, content):
        if self.reading_ns and content != "0":
            self.reading_page = False
        if self.reading_title:
            self.title = content
        if self.reading_text:
            if self.lines == 0 :
                print(">>>", self.title)
            if content == "==English==":
                self.reading_english = True
            elif re.match("^==[^=]", content):
                self.reading_english = False
            if self.reading_english and content == "===Pronunciation===":
                self.reading_phonetics = True
            elif content.startswith("==="):
                self.reading_phonetics = False
            self.lines += 1
        if self.reading_phonetics:
            if content.startswith("*"):
                if self.entry:
                    self.emit_entry()
                self.entry = content
            elif self.entry and content[0] in self.special_chars:
                self.entry += content
            elif self.entry and self.entry[-1] in self.special_chars:
                self.entry += content
            elif not content.strip():
                if self.entry:
                    self.emit_entry()
                self.entry = None
                self.reading_entry = False

    def endElement(self, name):
        self.depth -= 1
        if name == "page":
            self.reading_page = False
            self.title = None
        if name == "ns":
            self.reading_ns = False
        if name == "title":
            self.reading_title = False
        if name == "text":
            self.reading_text = False
            self.reading_phonetics = False
            self.reading_english = False
            self.lines = 0

        #print("{0}end {1}".format("|  " * self.depth, name))


parser = sax.make_parser()
parser.setContentHandler(IpaParser())
parser.parse(open("enwik.xml"))
