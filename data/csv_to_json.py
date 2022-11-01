import csv
import json

ADS = 'ads'
CATEGORY = 'categories'


def convert_file(csv_file, json_file, model):
    results = []
    with open(csv_file, encoding='utf-8') as f:
        for row in csv.DictReader(f):
            to_add = {'model': model, 'pk': int(row['Id'] if 'Id' in row else row['id'])}
            if 'id' in row:
                del row['id']
            else:
                del row['Id']
            if 'is_published' in row:
                if row['is_published'] == 'TRUE':
                    row['is_published'] = True
                else:
                    row['is_published'] = False
            if 'price' in row:
                row['price']= int(row['price'])
            to_add['fields'] = row
            results.append(to_add)
    with open(json_file, 'w', encoding='utf-8') as jf:
        jf.write(json.dumps(results, ensure_ascii=False))

convert_file(f'{ADS}.csv',f'{ADS}.json', 'ads.ad')
convert_file(f'{CATEGORY}.csv',f'{CATEGORY}.json', 'ads.category')