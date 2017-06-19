# File: lxml_diff.py

# Copyright 2004-2014 Adaptive Insights, Inc.  
# All Rights Reserved.

# This work contains trade secrets and confidential material of 
# Adaptive Insights, Inc., and its use or disclosure in whole or in part 
# without the express written permission of Adaptive Insights, Inc., is prohibited.

from lxml import etree as ET
import time
import diff

def differ(path_a, path_b):
    tree_a = ET.parse(path_a)
    root_a = tree_a.getroot()
    tree_b = ET.parse(path_b)
    root_b = tree_b.getroot()
    return diff.diff(root_a, root_b)

def test(path):
    tree_a = ET.parse(path)
    root_a = tree_a.getroot()
    for c in root_a.iter("Val"):
        print(c.tag, c.attrib)
        for key in c.keys():
            print(c.get(key))

def run():
    t0 = time.time()
    f1 = "xmldump_with_diffs/pre/XCA3I63K2U3B3K7LUF2FJXO37JE-6841.xml"
    f2 = "xmldump_with_diffs/post/XCA3I63K2U3B3K7LUF2FJXO37JE-6841.xml"
    print(differ("sample.xml", "changes.xml"))
    # test(f1)
    print(time.time() - t0)


if __name__ == '__main__' :
    run()