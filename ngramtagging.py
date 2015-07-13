def OIB_ngram_tagging(tokens_list, ngram_dict, max_n_gram_size, tags=None):
	# tags can have initial values blocking repeated finds
	# ngram_dict can also be a set. 

	if tokens_list == None: 
		return None, None
	nb_tokens = len(tokens_list)
	if nb_tokens == 0:
		return None, None

	if tags == None or len(tags) != nb_tokens:
		tags = ["O"] * nb_tokens

	found_objects_keys = []
	found_objects_position = []

	# Make the search for bigger n_gram sizes first
	for current_size in range(max_n_gram_size, 0):
		# Make the search for every position
		for current_position in range(0, nb_tokens - current_size + 1):
			if is_available_tag(tags, current_position, current_size):
				searchable_tuple = get_searchable_tuple(tokens_list, current_position, current_size)
				if searchable_tuple in ngram_dict:
					OIB_tag(tags, current_position, current_size)
					found_objects_keys.append(searchable_tuple)
					found_objects_position.append(current_position)	

	return tags, found_objects_keys, found_objects_position

def OIB_tag(tags, position, size):
	tags[position] = "B"
	if size > 1:
		tags[position+1:position+size] = "I"

def is_available_tag(tags, position, size):
	available = (tags[position:position+size] == ["O"] * size)
	return available

def get_searchable_tuple(tokens_list, position, size):
	return tuple(tokens_list[position:position+size])
