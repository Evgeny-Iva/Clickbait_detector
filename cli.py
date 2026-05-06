import argparse
import csv


def parse_args():
    parse = argparse.ArgumentParser()
    parse.add_argument('--files', nargs='+', required=True, help="Пути к CSV-файлам")
    parse.add_argument('--ctr', type=float, default=10, help="Порог CTR")
    parse.add_argument('--retention', type=float, default=50, help="Порог удержания")
    return parse.parse_args()

def process_file(file_path, ctr_threshold, retention_threshold):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = csv.reader(f)
        next(text)
        for row in text:
            if float(row[1]) > ctr_threshold and float(row[2]) < retention_threshold:
                print(row[0])


if __name__ == '__main__':
    args = parse_args()
    for file_path in args.files:
        process_file(file_path, args.ctr, args.retention)