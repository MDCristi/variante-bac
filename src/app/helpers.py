def boolean_value(correctness):
	if correctness == 'true':
		return True
	return False

def get_number_of_checked_items(form):
	checked = 0
	for field in form:
		if field.data == True:
			checked += 1
	return checked