'''
Useful NLP simple functions
'''

def remove_oe(raw_text):
	return raw_text.replace(u"œ", u"oe")
