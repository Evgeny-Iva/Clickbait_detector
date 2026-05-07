import argparse
import csv


def parse_args(args=None):
    parse = argparse.ArgumentParser()
    parse.add_argument('--files', nargs='+', required=True, help="Пути к CSV-файлам")
    parse.add_argument('--report', default='clickbait', help="Тип отчёта")
    return parse.parse_args(args)

def process_file(file_path):
    result = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = csv.reader(f)
            next(text)
            for row in text:
                if float(row[1]) > 15 and float(row[2]) < 40:
                    result.append([row[0], float(row[1]), float(row[2])])
        return result
    except FileNotFoundError:
        print(f"Ошибка: файл {file_path} не найден. Пропускаем.")
        return result

    except ValueError:
        print(f"Ошибка: файл {file_path} содержит нечисловые значения в колонках CTR или retention. Пропускаем.")
        return result

    except Exception as e:
        print(f"Ошибка при чтении {file_path}: {e}. Пропускаем.")
        return result

def print_table(data):
    sorted_data = sorted(data, key=lambda x: x[1], reverse=True)
    width_title = len("title")
    for video in data:
        if len(video[0]) > width_title:
            width_title = len(video[0])

    width_title += 2
    ctr_width = len('ctr')
    retention_width = len('retention_rate')

    print(f"+{'-' * (width_title + 2)}+{'-' * (ctr_width + 3)}+{'-' * (retention_width + 2)}+")
    print(f"| {'title':<{width_title}} | {'ctr':>{ctr_width + 1}} | {'retention_rate':>{retention_width}} |")
    print(f"+{'=' * (width_title + 2)}+{'=' * (ctr_width + 3)}+{'=' * (retention_width + 2)}+")

    for row in sorted_data:
        print(f"| {row[0]:<{width_title}} | {row[1]:>{ctr_width}} | {row[2]:>{retention_width}} |")
        print(f"+{'-' * (width_title + 2)}+{'-' * (ctr_width + 3)}+{'-' * (retention_width + 2)}+")


REPORTS = {
    "clickbait": print_table,
}

if __name__ == '__main__':
    args = parse_args()
    if args.report not in REPORTS:
        print(f"Ошибка: отчёт '{args.report}' не поддерживается. Доступны: {', '.join(REPORTS.keys())}")
        exit(1)

    all_videos = []
    for file_path in args.files:
        videos = process_file(file_path)
        all_videos.extend(videos)

    if all_videos:
        REPORTS[args.report](all_videos)
    else:
        print("Не найдено видео, удовлетворяющих условиям!")