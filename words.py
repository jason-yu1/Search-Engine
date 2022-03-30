import os
import string
from jinja2 import Template
import re


def filelist(root):
    """Return a fully-qualified list of filenames under root directory"""
    files = list()
    for (dirpath, dirnames, filenames) in os.walk(root):
        files += [os.path.join(dirpath, file) for file in filenames if file[-4:] == '.txt']

    return files

def get_text(fileName):
    f = open(fileName, encoding='latin-1')
    s = f.read()
    f.close()
    return s


def words(text):
    """
    Given a string, return a list of words normalized as follows.
    Split the string to make words first by using regex compile() function
    and string.punctuation + '0-9\\r\\t\\n]' to replace all those
    char with a space character.
    Split on space to get word list.
    Ignore words < 3 char long.
    Lowercase all words
    """
    regex = re.compile('[' + re.escape(string.punctuation) + '0-9\\r\\t\\n]')
    nopunct = regex.sub(" ", text)  # delete stuff but leave at least a space to avoid clumping together
    words = nopunct.split(" ")
    words = [w for w in words if len(w) > 2]  # ignore a, an, to, at, be, ...
    words = [w.lower() for w in words]
    # print words
    return words

def find_lines(docs, terms):
    word_lines = []
    for doc in docs:
        with open(doc) as f:
            lines = f.readlines()
        temp = []
        # find matching lines
        for line in lines:
            format_line = words(line)
            if any([term in format_line for term in terms]):
                # add boldness to key term
                for term in terms:
                    ls = [(m.start(), m.end()) for m in re.finditer(r"(?<![a-z])\b" + re.escape(term) + r"\b(?![a-z])", line.lower())]
                    i = 0
                    for l in ls:
                        line = line[:(l[0] + i*6 + i)] + '<b>' + line[(l[0] + i*6 + i):(l[1] + i*6 + i)] + '</b>' + line[(l[1] + i*6):]
                        i += 1
                # add line to list
                temp.append(line)
            # stop after we get two lines
            if len(temp) == 2:
                break

        # add list of lines if there is a match
        if len(temp) > 0:
            word_lines.append(temp)

    return word_lines


def results(docs, terms):
    """
    Given a list of fully-qualifed filenames, return an HTML file
    that displays the results and up to 2 lines from the file
    that have at least one of the search terms.
    Return at most 100 results.  Arg terms is a list of string terms.
    """
    with open('templates/template.html') as f:
        t = Template(f.read())

    # for each document
    # find up to 2 lines containing at least one search term
    lines = find_lines(docs,terms)
    length = len(lines)

    """f = open(doc, "r")
    s = words(f.read())
    f.close()"""

    return t.render(docs = docs, terms = terms, lines=lines, length = length)


def filenames(docs):
    """Return just the filenames from list of fully-qualified filenames"""
    if docs is None:
        return []
    return [os.path.basename(d) for d in docs]
