# File: xml_diff.py

# Copyright 2004-2014 Adaptive Insights, Inc.  
# All Rights Reserved.

# This work contains trade secrets and confidential material of 
# Adaptive Insights, Inc., and its use or disclosure in whole or in part 
# without the express written permission of Adaptive Insights, Inc., is prohibited.

import difflib
from pprint import pprint
import time
import diff_match_patch
import webbrowser

text1 = '''  1. Beautiful is better than ugly.
2. Explicit is better than implicit.
3. Simple is better than complex.
4. Complex is better than complicated.
'''
text2 = '''  1. Beautiful is better than ugly.
3.   Simple is better than complex.
4. Complicated is better than complex.
5. Flat is better than nested.
'''

def get_file_lists(path_a, path_b):
    """Take two string paths to specific files, and converts them to two lists 
    of strings from the files, separated by lines.

    Args:
      path_a: path to file a.
      path_b: path to file b.

    Returns:
      A tuple of two lists of strings.
    """
    file_a = open(path_a, 'r')
    a = file_a.readlines()
    file_b = open(path_b, 'r')
    b = file_b.readlines()
    return a, b

def get_file_string(path_a, path_b):
    """Take two string paths to specific files, and converts them to string 
    representations of the files.

    Args:
      path_a: path to file a.
      path_b: path to file b.

    Returns:
      A tuple of two strings.
    """
    file_a = open(path_a, 'r')
    a = file_a.read()
    file_b = open(path_b, 'r')
    b = file_b.read()
    return a, b

def get_example_text():
    """Returns two example lists of strings.

    Returns:
      A tuple of two lists of strings.
    """
    a = text1.strip().split("\n")
    b = text2.strip().split("\n")
    return a, b

def display_html(text, file):
    """Opens a web browser tab to display a string as an html file.

    Args:
      text: A string representation of the html text.
      file: the name of the html tab to be opened.
    """
    f = open(file,'w')
    f.write(text)
    f.close()
    webbrowser.open_new_tab(file)

def htmldiff(path_a, path_b):
    """Creates a diff between file a and file b and displays them
    in an html page

    Args:
      path_a: path to file a.
      path_b: path to file b.
    """
    d = difflib.HtmlDiff()
    a, b = get_file_lists(path_a, path_b)
    result = d.make_file(a, b, context=True, numlines=0)
    display_html(result, 'diff.html')

def htmldiff_example():
    """Creates a diff between two sample strings and displays them
    in an html page

    Args:
      path_a: path to file a.
      path_b: path to file b.
    """
    text1, text2 = get_example_text()
    d = difflib.HtmlDiff()
    result = d.make_file(text1, text2, context=True, numlines=0)
    display_html(result, 'diff.html')

def difflib_context_diff(path_a, path_b):
    """Diffs two files, and only returns the deltas,
    or the specific changes in the diff.
    
    Args:
      path_a: path to file a.
      path_b: path to file b.

    Returns:
      A list of strings representing the deltas.
    """
    a, b = get_file_lists(path_a, path_b)
    return list(difflib.context_diff(a, bcontext=True, numlines=0))

def difflib_context_diff_example():
    """Diffs two sample strings and only returns the deltas,
    or the specific changes in the diff.

    Returns:
      A list of strings representing the deltas.
    """
    a, b = get_example_text()
    result = list(difflib.context_diff(a, b, context=True, numlines=0))
    pprint(result)
    print(len(result))

def differ_compare(path_a, path_b):
    """Diffs two files, and returns a list representation of the diff.
    
    Args:
      path_a: path to file a.
      path_b: path to file b.

    Returns:
      A list of strings representing the deltas.
    """
    d = difflib.Differ()
    a, b = get_file_lists(path_a, path_b)
    return list(d.compare(a, b))

def differ_compare_example(path_a, path_b):
    """Diffs two sample strings and returns a list representation of the diff.

    Returns:
      A list of strings representing the deltas.
    """
    d = difflib.Differ()
    a, b = get_example_text()
    return list(d.compare(a, b))


def changes_diffs(diff_match_patch, diffs):
    """Takes in a diff representation, and returns a diff representation that
    contains only the changes in the diff.

    Args:
      diff_match_patch: a diff_match_patch object
      diffs: a list of diff tuples, for example
      [(DIFF_DELETE, "Hello"), (DIFF_INSERT, "Goodbye"), (DIFF_EQUAL, " world.")]

    Returns:
      A list of tuples of updates in the diff.
    """
    e = diff_match_patch.DIFF_EQUAL
    changes = list()
    for delta, text in diffs:
        if delta != e:
            changes.append((delta, text))
    return changes

def diff_smart(path_a, path_b, flag="basic"):
    """Creates a diff between file a and file b and displays them
    in an html page. Gives the option of doing a basic, efficient,
    or semantic diff.

    Args:
      path_a: path to file a.
      path_b: path to file b.
      flag:  basic, efficient, or semantic.
    """
    a, b = get_file_string(path_a, path_b)
    d = diff_match_patch.diff_match_patch()
    diffs = d.diff_main(a, b)
    diffs = changes_diffs(d, diffs)
    if flag == "efficient":
        d.diff_cleanupEfficiency(diffs)
    elif flag == "semantic":
        d.diff_cleanupSemantic(diffs)
    elif flag != "basic":
        raise Exception("{} is not a valid option".format(flag))
    html = d.diff_prettyHtml(diffs)
    display_html(html, 'smart_diff_{}.html'.format(flag))

def diff_smart_example(flag="basic"):
    """Creates a diff between two sample strings and displays them
    in an html page. Gives the option of doing a basic, efficient,
    or semantic diff. 

    Args:
      flag:  basic, efficient, or semantic.
    """
    d = diff_match_patch.diff_match_patch()
    diffs = d.diff_main(text1, text2)
    diffs = changes_diffs(d, diffs)
    if flag == "efficient":
        d.diff_cleanupEfficiency(diffs)
    elif flag == "semantic":
        d.diff_cleanupSemantic(diffs)
    elif flag != "basic":
        flag = "basic"
        raise Warning("running basic diff")
    html = d.diff_prettyHtml(diffs)
    display_html(html, 'smart_diff_{}.html'.format(flag))

def run():
    t0 = time.time()
    f1 = "xmldump_with_diffs/pre/XCA3I63K2U3B3K7LUF2FJXO37JE-6841.xml"
    f2 = "xmldump_with_diffs/post/XCA3I63K2U3B3K7LUF2FJXO37JE-6841.xml"
    diff_smart(f1, f2, flag="basic")
    print(time.time() - t0)

if __name__ == '__main__' :
    run()