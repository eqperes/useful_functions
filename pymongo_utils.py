from pymongo import ReplaceOne


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
