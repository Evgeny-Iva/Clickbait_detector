# Clickbait Detector

CLI-утилита для поиска кликбейтных видео из CSV-файлов.

## Пример запуска

python cli.py --files videos.csv
python cli.py --files data1.csv data2.csv --report clickbait

## Формат CSV

Ожидаются колонки: title, ctr, retention

## Условие отбора

CTR > 15% и удержание < 40%