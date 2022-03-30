# Got slate magazine data from http://www.anc.org/data/oanc/contents/
# rm'd .xml, .anc files, leaving just .txt
# 4534 files in like 55 subdirs

from htable import *
from words import get_text, words


def myhtable_create_index(files):
    """
    Build an index from word to set of document indexes
    This does the exact same thing as create_index() except that it uses
    your htable.  As a number of htable buckets, use 4011.
    Returns a list-of-buckets hashtable representation.
    """
    index = htable(4011)
    for i, file in enumerate(files):
        # open file
        s = get_text(file)
        for word in words(s):
            val = htable_get(index, word)
            if val is not None:
                val.add(i)
            else:
                val = {i}
            htable_put(index, word, val)
    return index


def myhtable_index_search(files, index, terms):
    """
    This does the exact same thing as index_search() except that it uses your htable.
    I.e., use htable_get(index, w) not index[w].
    """
    # get ids of matching docs
    ids = get_id(index, terms)

    # return list of matches
    match = [files[id] for id in ids]

    return match


def get_id(index, terms):
    temp = [htable_get(index, term) for term in terms]
    if temp[0] == None:
        return []
    # get file ids for term
    ids = temp[0].intersection(*temp)

    return ids











