import re
from xml.etree.cElementTree import iterparse

namespace = ""

def ns(data, namespace):
    return re.sub("^{{{0}}}".format(namespace), "", data)

for event, content in iterparse(open('enwik.xml'), ('start-ns', 'end',)):
    pass
