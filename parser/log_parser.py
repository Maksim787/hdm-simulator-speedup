import os
from pathlib import Path
import re
from datetime import datetime

MONTHS_MAPPING = {
    'ЯНВ': 'Jan',
    'ФЕВ': 'Feb',
    'МАР': 'Mar',
    'АПР': 'Apr',
    'МАЙ': 'May',
    'ИЮН': 'Jun',
    'ИЮЛ': 'Jul',
    'АВГ': 'Aug',
    'СЕН': 'Sep',
    'ОКТ': 'Oct',
    'НОЯ': 'Nov',
    'ДЕК': 'Dec'
}

def parse_dates_from_file(file_path):
    dates = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            if "НАЧАЛО СЛЕДУЮЩЕГО ВРЕМЕННОГО ШАГА" in line:
                match = re.search(r'([А-Я]+) \d{4}', line)
                if match:
                    month_ru = match.group(1)
                    month_en = MONTHS_MAPPING.get(month_ru)
                    if month_en:
                        date_str = match.group(0).strip().split()
                        date_str[0] = month_en
                        date_str = ' '.join(date_str)
                        date = datetime.strptime(date_str, '%b %Y')
                        dates.append(date)
    return dates

def calculate_date_difference(file_path):
    dates = parse_dates_from_file(file_path)
    if len(dates) < 2:
        return None
    min_date = min(dates)
    max_date = max(dates)
    difference = (max_date.year - min_date.year) * 12 + (max_date.month - min_date.month)
    return difference

def find_result_logs(root_dir: Path) -> list[Path]:
    result_logs = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file == "result.log":
                result_logs.append(os.path.join(root, file))
    return result_logs

def parse_model_statistics(file_path: Path) -> dict:
    model_statistics = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        found_statistics = False
        for line in file:
            if "СТАТИСТИКА МОДЕЛИ" in line:
                found_statistics = True
                continue
            if found_statistics:
                line = line.strip()
                if ':' not in line:
                    break
                key, value = line.split(':', 1)
                model_statistics[key.strip()] = value.strip()
    return model_statistics

def get_time(file_path: Path) -> str:
    with open(file_path, 'r', encoding='utf-8') as file:
        line = file.readline()
        if line.startswith("| Время расчета"):
            return line[-9:-1]
        else:
            return None