
#Source: http://code.activestate.com/recipes/578948-flattening-an-arbitrarily-nested-list-in-python/
def flatten(lis):
    """Given a list, possibly nested to any level, return it flattened."""
    new_lis = []
    for item in lis:
        if type(item) == type([]):
            new_lis.extend(flatten(item))
        else:
            new_lis.append(item)
    return new_lis
