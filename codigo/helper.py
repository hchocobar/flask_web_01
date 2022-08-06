def date_format(value):
	months = ("Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre")
	month = months[value.month-1]
	return "{} de {} de {}".format(value.day, month, value.year)

def featurepagination(page,items,per_page):
	"""Solo obtiene el numero de paginas totales"""
	resulti = items / per_page
	resultf = items % per_page
	if resultf != 0:
		resulti = resulti + 1

	pagination = []
	for x in xrange(0,resulti):
			pagination.append(x+1)
	return pagination

def extract_text(text):
	return text[0:500]

def delete_spacewith(text,reverse=False):
	if reverse == False:
		return text.replace(' ','-')
	else:
		return text.replace('-',' ')