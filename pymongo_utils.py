from pymongo import ReplaceOne
from tqdm import tqdm


def apply_function(collection, function, filter_dict={}, batch=100000):
    """
    Apply the given function on the elements of a MongoDB collection.

    :param collection: a mongodb collection
    :param filter_dict: a filter to mongodb find function
    :param function: a function to be applied to every element that pass the filter
    :param batch: the size of BulkWrite operation in mongodb
    :return: void
    """
    new_entries_batch = []
    for entry in tqdm(collection.find(filter_dict)):
        if len(new_entries_batch) >= batch:
            requests = [ReplaceOne({"_id": new_entry["_id"]}, new_entry) for new_entry in new_entries_batch]
            collection.bulk_write(requests, ordered=False)
            new_entries_batch = []
        new_entries_batch.append(function(entry))
    requests = [ReplaceOne({"_id": new_entry["_id"]}, new_entry) for new_entry in new_entries_batch]
    collection.bulk_write(requests, ordered=False)
 
    
class KeyFunctions(object):
    """
    Stores functions to be used for given key values of a MongoDb collection entry
    """
    def __init__(self, key_function_tuples=[]):
        self.key_function_tuples = key_function_tuples

    def add(self, key, function):
        self.key_function_tuples.append((key, function))

    def apply(self, entry):
        new_entry = entry.copy()
        for key, function in self.key_function_tuples:
            new_entry[key] = function(entry[key])
        return new_entry
        

def obtain_collection_keys(collection, filter={}):
    """
    Function used to obtain all the keys of entries in a MongoDb collection

    :param collection: a mongodb collection
    :param filter: a filter for mongodb find function
    :return: a dictionary containing all the keys of all the entries obtained by the find function,
        with the number of ocurrences of the key in the value
    """
    keys = {}
    for entry in collection.find(filter):
        for key in entry:
            keys[key] = keys.setdefault(key, 0) + 1
    return keys

