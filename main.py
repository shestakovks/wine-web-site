from collections import defaultdict
import datetime

from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape


def get_product_file_lines(filename):
    with open(filename) as f:
        return f.read().strip().split('\n')


def get_wines_from_file(product_file_lines):
    mapping = {
        'Название': 'name',
        'Сорт': 'grape',
        'Цена': 'price',
        'Картинка': 'image',
    }
    products = defaultdict(list)
    product_subtitle = None
    default_product_subtitle = 'Другое'
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
            product_subtitle = product_subtitle or default_product_subtitle
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
    product_file_lines = get_product_file_lines('wine.txt')
    products = get_wines_from_file(product_file_lines)
    rendered_page = template.render(
        years_since_founded=str(datetime.date.today().year - foundation_year),
        products=products
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()
