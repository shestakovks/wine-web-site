import datetime
from collections import defaultdict
from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape


def get_products_from_string(product_file_string):
    product_file_lines = product_file_string.strip().split('\n')
    mapping = {
        'Название': 'name',
        'Сорт': 'grape',
        'Цена': 'price',
        'Картинка': 'image',
    }
    products = defaultdict(list)
    product_subtitle = None
    product = {}

    for index, line in enumerate(product_file_lines):
        if line.startswith('#'):
            product_subtitle = line.split(' ', 1)[-1]
        elif line.startswith('Выгодное предложение'):
                product['profitable'] = True
        elif line:
            key, value = line.split(':')
            product[mapping[key.strip()]] = value.strip()

        if (not line and product) or (product and index == len(product_file_lines) - 1):
            if product_subtitle is None:
                return
            products[product_subtitle].append(product)
            product = {}

    return products


if __name__ == '__main__':
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    foundation_year = 1920
    with open('wine.txt') as f:
        product_file_string = f.read()
    products = get_products_from_string(product_file_string)
    rendered_page = template.render(
        years_since_founded=str(datetime.date.today().year - foundation_year),
        products=products
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()
