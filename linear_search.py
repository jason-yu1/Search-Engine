# Got slate magazine data from http://www.anc.org/data/oanc/contents/
# rm'd .xml, .anc files, leaving just .txt
# 4534 files in like 55 subdirs

from words import get_text, words


def linear_search(files, terms):
    """
    Given a list of fully-qualified filenames, return a list of them
    whose file contents has all words in terms as normalized by your words() function.
    Parameter terms is a list of strings.
    Perform a linear search, looking at each file one after the other.
    """
    match = []
    # loop through each file
    for file in files:
        # open file
        f = open(file, "r")
        s = words(f.read())
        f.close()

        # check if all terms are in file
        if all([term in s for term in terms]):
            match.append(file)

    # list of matching documents
    return match