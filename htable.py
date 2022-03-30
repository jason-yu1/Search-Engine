"""
A hashtable represented as a list of lists with open hashing.
Each bucket is a list of (key,value) tuples
"""


def htable(nbuckets):
    """Return a list of nbuckets lists"""
    buckets = [[] for i in range(nbuckets)]
    return buckets


def hashcode(o):
    """
    Return a hashcode for strings and integers; all others return None
    For integers, just return the integer value.
    For strings, perform operation h = h*31 + ord(c) for all characters in the string
    """
    if type(o) is str:
        h = 0
        for c in o:
            h = h * 31 + ord(c)
        return h
    elif type(o) is int:
        return o
    else:
        return None


def bucket_indexof(table, key):
    """
    You don't have to implement this, but I found it to be a handy function.
    Return the index of the element within a specific bucket; the bucket is:
    table[hashcode(key) % len(table)]. You have to linearly
    search the bucket to find the tuple containing key.
    """
    bucket = table[hashcode(key) % len(table)]
    for index, element in enumerate(bucket):
        if element[0] == key:
            return index
    raise ValueError("key not in list")


def htable_put(table, key, value):
    """
    Perform the equivalent of table[key] = value
    Find the appropriate bucket indicated by key and then append (key,value)
    to that bucket if the (key,value) pair doesn't exist yet in that bucket.
    If the bucket for key already has a (key,value) pair with that key,
    then replace the tuple with the new (key,value).
    Make sure that you are only adding (key,value) associations to the buckets.
    The type(value) can be anything. Could be a set, list, number, string, anything!
    """
    bucket = table[hashcode(key) % len(table)]
    if bucket:
        # replace tuple if pair does exist
        for index, pair in enumerate(bucket):
            if key == pair[0]:
                bucket[bucket_indexof(table, key)] = (key, value)
                break
            # append to list if pair doesnt exist
            if index == len(bucket) - 1:
                bucket.append((key, value))
    # if bucket is empty, initialize one
    else:
        bucket.append((key, value))


def htable_get(table, key):
    """
    Return the equivalent of table[key].
    Find the appropriate bucket indicated by the key and look for the
    association with the key. Return the value (not the key and not
    the association!). Return None if key not found.
    """
    bucket = table[hashcode(key) % len(table)]
    try:
        return bucket[bucket_indexof(table, key)][1]
    except ValueError:
        return None


def htable_buckets_str(table):
    """
    Return a string representing the various buckets of this table.
    The output looks like:
        0000->
        0001->
        0002->
        0003->parrt:99
        0004->
    where parrt:99 indicates an association of (parrt,99) in bucket 3.
    """
    s = ''
    for num, bucket in enumerate(table):
        temp_s = ''
        ind = str(num).zfill(4)
        temp_s = "".join([temp_s, ind, '->'])
        if bucket:
            for i, pair in enumerate(bucket):
                key = pair[0]
                if type(key) != str:
                    key = str(key)
                temp_s = "".join([temp_s, key, ':', str(pair[1])])
                # if not end of list, add comma and space
                if i != len(bucket) - 1:
                    temp_s = "".join([temp_s, ', '])
                # if end of list, add new line
                else:
                    temp_s = "".join([temp_s, '\n'])
        else:
            temp_s = "".join([temp_s, '\n'])
        s = "".join([s, temp_s])

    return s


def htable_str(table):
    """
    Return what str(table) would return for a regular Python dict
    such as {parrt:99}. The order should be in bucket order and then
    insertion order within each bucket. The insertion order is
    guaranteed when you append to the buckets in htable_put().
    """
    # get number of elements in all table
    count = sum([len(elements) for elements in table])

    s = '{'
    for num, bucket in enumerate(table):
        temp_s = ''
        for i, pair in enumerate(bucket):
            key = pair[0]
            if type(key) != str:
                key = str(key)
            temp_s = "".join([temp_s, key, ':', str(pair[1])])
            # if add real object to string, decrease counter
            if bucket:
                count -= 1
            # if last item added, do not add comm
            if count == 0:
                break
            temp_s = "".join([temp_s, ', '])

        if num == len(table) - 1:
            temp_s = "".join([temp_s, '}'])
        s = "".join([s, temp_s])

    return s
