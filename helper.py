def date_format(value):
    months = ('Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
              'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre')
    month = months[value.month - 1]
    return "{} de {} del {}".format(value.day, month, value.year)


def feature_pagination(page, items, per_page):
    # número de páginas totales
    result_i = items / per_page
    result_f = items % per_page
    if result_f != 0:
        result_i = result_i + 1

    pagination = []
    for x in range(0, result_i):
        pagination.append(x + 1)
    return pagination


def extract_text(text):
    return text[0:500]


def delete_space_with(text, reverse=False):
    if reverse is False:
        return text.replace(' ', '-')
    else:
        return text.replace('-', ' ')
