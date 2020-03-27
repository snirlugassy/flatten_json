import json
import csv

INPUT_FILE_NAME = 'data.json'
OUTPUT_FILE_TYPE = 'tsv'
OUTPUT_FILE_NAME = 'data' + OUTPUT_FILE_TYPE
JSON_PRIMARY_KEY = 'ID'
DELIMITER = '\t'

def load_data(file_name):
    with open(file_name, 'r') as data_file:
        return json.load(data_file)


def flatten(item, prefix):
    flat = {}

    for key in item.keys():
        if type(item[key]) is dict:
            flat.update(flatten(item[key], key + '.'))
        elif type(item[key]) is list:
            for i in item[key]:
                if type(i) is dict:
                    flat.update(flatten(i, key + '.'))
                else:
                    if key in flat.keys():
                        flat[key] += "," + str(i)
                    else:
                        flat[key] = str(i)
        else:
            flat[prefix + key] = item[key]

    return flat


def write_data_to_tsv(data, keys):
    keys = list(keys)
    keys.sort()
    with open(OUTPUT_FILE_NAME, 'w', newline='') as output_file:
        writer = csv.DictWriter(output_file, delimiter=DELIMITER, fieldnames=keys)
        writer.writeheader()
        for x in data:
            writer.writerow(x)


if __name__ == '__main__':
    data = load_data(INPUT_FILE_NAME)
    flat_data = []
    flat_keys = set({JSON_PRIMARY_KEY})
    for key in data.keys():
        flat_item = {JSON_PRIMARY_KEY: key}
        flat_item.update(flatten(data[key], ''))
        flat_data.append(flat_item)
        flat_keys.update(flat_item.keys())
    write_data_to_tsv(flat_data, flat_keys)
