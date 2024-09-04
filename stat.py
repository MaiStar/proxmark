import os
import re
import statistics

# Путь к папке с файлами
folder_path = './test'

# Регулярные выражения для поиска данных в файлах
cluster_pattern = re.compile(r'Кластер (\d+):')
good_pattern = re.compile(r'хорошая:\s+(\d+)')
no_record_pattern = re.compile(r'нет записи:\s+(\d+)')
trash_pattern = re.compile(r'мусор:\s+(\d+)')
fail_pattern = re.compile(r'не получилось:\s+(\d+)')

# Данные для анализа
short_range_data = {}
full_range_data = {}

# Функция для парсинга данных из файла
def parse_file(file_path):
    # Определение группы по имени файла
    if '200-2000' in file_path:
        data_dict = full_range_data
    else:
        data_dict = short_range_data
    
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        clusters = cluster_pattern.findall(content)
        
        for cluster in clusters:
            if cluster not in data_dict:
                data_dict[cluster] = {'good': [], 'no_record': [], 'trash': [], 'fail': []}
            
            good = int(good_pattern.search(content).group(1))
            no_record = int(no_record_pattern.search(content).group(1))
            trash = int(trash_pattern.search(content).group(1))
            fail = int(fail_pattern.search(content).group(1))
            
            data_dict[cluster]['good'].append(good)
            data_dict[cluster]['no_record'].append(no_record)
            data_dict[cluster]['trash'].append(trash)
            data_dict[cluster]['fail'].append(fail)

# Чтение всех файлов в папке
for filename in os.listdir(folder_path):
    if filename.endswith('.txt'):
        parse_file(os.path.join(folder_path, filename))

# Функция для расчета статистики
def analyze_data(data_dict):
    for cluster, data in data_dict.items():
        print(f"Кластер {cluster}:")
        for key in data:
            values = data[key]
            if len(values) > 1:  # Только если есть больше одного значения
                mean = statistics.mean(values)
                stdev = statistics.stdev(values)
                coef_variation = (stdev / mean) * 100 if mean != 0 else 0
                print(f"  {key}: среднее = {mean:.2f}, стд. откл. = {stdev:.2f}, коэф. вариации = {coef_variation:.2f}%")
            else:
                print(f"  {key}: недостаточно данных для анализа")
        print()

# Анализ данных
print("Анализ короткого диапазона:")
analyze_data(short_range_data)

print("Анализ полного диапазона (200-2000):")
analyze_data(full_range_data)
