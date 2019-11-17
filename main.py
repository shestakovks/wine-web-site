import datetime

from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape


def get_wines_from_file(filename):
    products = dict()
    product = dict()
    mapping = {
        'Название': 'name',
        'Сорт': 'grape',
        'Цена': 'price',
        'Картинка': 'image',
    }
    with open(filename) as f:
        products_file = f.read().strip().split('\n')
    for line in products_file:
        if line.startswith('#'):
            product_line = line.split(' ', 1)[-1]
            products[product_line] = products.setdefault(product_line, [])
        elif line:
            if line.startswith('Выгодное предложение'):
                product['profitable'] = True
            else:
                key, value = line.split(':')
                product[mapping[key]] = value.strip()
        elif not line and product:
            products[product_line].append(product)
            product = dict()
    products[product_line].append(product)
    return products


env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')

products = get_wines_from_file('wine.txt')
rendered_page = template.render(
    years_since_founded=str(datetime.date.today().year - 1920),
    products=products
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
