import csv

import pandas
import requests
import yaml
from lxml import html

affinity_position = ['Ascendant', 'Chaos', 'Eldritch', 'Order', 'Primordial']
ability_position = ['on Block', 'Critical Attack', 'when Hit', 'on Attack', 'Chance at', 'on Enemy Death']


class Constellation:
    def __init__(self, name, tier, ability, star, take, give, description):
        self.name = name
        self.tier = tier
        self.ability = ability
        self.star = star
        self.take = take
        self.give = give
        self.description = description

    def get_csv_row(self):
        return [self.name, self.tier, self.ability, self.star] + self.take + self.give + [self.description]

    def __repr__(self):
        return str([self.name, self.tier, self.ability, self.star, self.take, self.give, self.description]) + '\n'


def download():
    with open('gdd.yaml', 'r') as f:
        destination = yaml.load(f)['link']
    page = requests.get(destination)

    with open('gdd.txt', 'w') as f:
        f.write(page.content.decode('utf-8'))


def process():
    with open('/home/misa/PycharmProjects/test_only/test/gdd/gdd.txt', 'r') as f:
        data = f.read()

    tree = html.fromstring(data)
    tables = tree.cssselect('.wikitable')[1:]
    data = []
    for table in tables:
        tbl_data = read_table(table, get_tier(tables.index(table)))
        data = data + tbl_data
        print()
    with open('/home/misa/PycharmProjects/test_only/test/gdd/gdd.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Tier", "Ability", "Star", "Ascendant_1", "Chaos_1", "Eldritch_1", "Order_1", "Primordial_1",
                         "Ascendant_2", "Chaos_2", "Eldritch_2", "Order_2", "Primordial_2", "Description"])
        for d in data:
            writer.writerow(d.get_csv_row())


def read_table(table, tier=0):
    rows = table.getchildren()[0].getchildren()[1:]
    result = []
    for row in rows:
        cells = row.getchildren()
        name = cells[0].text_content().strip().split('\xa0')[0]
        ability = get_ability(cells[1].cssselect('li')[-1].text_content())
        star = len(cells[1].cssselect('li')) or len(cells[1].cssselect('ul'))
        take = get_star_in_cell(cells[2])
        give = get_star_in_cell(cells[3])
        description = cells[1].text_content()
        constellation = Constellation(name, tier, ability, star, take, give, description)
        result.append(constellation)
    return result


def get_star_in_cell(cell):
    result = [0, 0, 0, 0, 0]
    img_lst = cell.cssselect('img')
    numbers = [x.tail.strip() for x in img_lst]
    if len(img_lst) == 0:
        return result
    affinity = [x.get('alt') for x in img_lst]
    for i in range(len(numbers)):
        position = affinity_position.index(affinity[i])
        result[position] = numbers[i]
    return result


def get_ability(text: str):
    for ability in ability_position:
        if ability in text:
            return ability_position.index(ability) + 1
    return 0


def get_tier(idx):
    if idx < 5:
        return 1
    if idx == 5:
        return 2
    if idx == 6:
        return 3
    return -1


def calculate():
    data = pandas.read_csv('/home/misa/PycharmProjects/test_only/test/gdd/gdd.csv')
    print(data)


if __name__ == '__main__':
    process()
    calculate()
