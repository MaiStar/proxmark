import os
import re

# Путь к папке с файлами
folder_path = './test'

# Регулярные выражения для поиска данных в файлах
good_pattern = re.compile(r'хорошая:\s+(\d+)\s+\([\d\.]+%\)')
no_record_pattern = re.compile(r'нет записи:\s+(\d+)\s+\([\d\.]+%\)')
trash_pattern = re.compile(r'мусор:\s+(\d+)\s+\([\d\.]+%\)')
fail_pattern = re.compile(r'не получилось:\s+(\d+)\s+\([\d\.]+%\)')

# Итоговые значения
total_good = 0
total_no_record = 0
total_trash = 0
total_fail = 0

total_clusters = 0

# Функция для парсинга данных из файла
def parse_file(file_path):
    global total_good, total_no_record, total_trash, total_fail, total_clusters
    
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        
        total_good += sum(int(match) for match in good_pattern.findall(content))
        total_no_record += sum(int(match) for match in no_record_pattern.findall(content))
        total_trash += sum(int(match) for match in trash_pattern.findall(content))
        total_fail += sum(int(match) for match in fail_pattern.findall(content))

        # Подсчет общего количества кластеров
        total_clusters += content.count('Кластер')

# Чтение всех файлов в папке
for filename in os.listdir(folder_path):
    if filename.endswith('.txt'):
        parse_file(os.path.join(folder_path, filename))

# Подсчет общего количества всех записей
total_all = total_good + total_no_record + total_trash + total_fail

# Вывод итогов в терминал
print(f"Все файлы \\ все кластеры:")
print(f"  хорошая: {total_good} ({total_good/total_all*100:.2f}%)")
print(f"  нет записи: {total_no_record} ({total_no_record/total_all*100:.2f}%)")
print(f"  мусор: {total_trash} ({total_trash/total_all*100:.2f}%)")
print(f"  не получилось: {total_fail} ({total_fail/total_all*100:.2f}%)")
