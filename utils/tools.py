from utils import constants


def load_page_text(filepath):
	with open(filepath) as infile:
		page_text = infile.read()
	return page_text