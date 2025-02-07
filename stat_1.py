# я хз зачем оно))

import os
import re
import statistics

# Путь к папке с файлами
folder_path = './test'

# Регулярные выражения для поиска данных в файлах
cluster_pattern = re.compile(r'Кластер (\d+):')
good_pattern = re.compile(r'хорошая:\s+(\д+)')
no_record_pattern = re.compile(r'нет записи:\s+(\д+)')
trash_pattern = re.compile(r'мусор:\s+(\д+)')
fail_pattern = re.compile(r'не по./test
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        clusters = cluster_pattern.findall(content)
        
        for cluster in clusters:
            if cluster not in data_dict:
                data_dict[cluster] = {'good': [], 'no_record': [], 'trash': [], 'fail': []}
            
            good_match = good_pattern.search(content)
            no_record_match = no_record_pattern.search(content)
            trash_match = trash_pattern.search(content)
            fail_match = fail_pattern.search(content)
            
            good = int(good_match.group(1)) if good_match else 0
            no_record = int(no_record_match.group(1)) if no_record_match else 0
            trash = int(trash_match.group(1)) if trash_match else 0
            fail = int(fail_match.group(1)) if fail_match else 0
            
            data_dict[cluster]['good'].append(good)
            data_dict[cluster]['no_record'].append(no_record)
            data_dict[cluster]['trash'].append(trash)
            data_dict[cluster]['fail'].append(fail)

# Чтение всех файлов в папке
for filename in os.listdir(folder_path):
    if filename.endswith('.txt'):
        parse_file(os.path.join(folder_path, filename))

# Функция для расчета статистики и выводов
def analyze_data(data_dict, group_name):
    total_clusters = len(data_dict)
    high_variability_count = 0

    print(f"Анализ {group_name}:")
    for cluster, data in data_dict.items():
        print(f"Кластер {cluster}:")
        for key in data:
            values = data[key]
            if len(values) > 1:  # Только если есть больше одного значения
                mean = statistics.mean(values)
                stdev = statistics.stdev(values)
                coef_variation = (stdev / mean) * 100 if mean != 0 else 0
                print(f"  {key}: среднее = {mean:.2f}, стд. откл. = {stdev:.2f}, коэф. вариации = {coef_variation:.2f}%")
                if coef_variation > 50:  # Условие для высокой вариативности (можно настроить)
                    high_variability_count += 1
            else:
                print(f"  {key}: недостаточно данных для анализа")
        print()

    # Выводы
    print(f"Итог по {group_name}:")
    print(f"  Всего кластеров: {total_clusters}")
    print(f"  Кластеров с высокой вариативностью: {high_variability_count} ({(high_variability_count/total_clusters)*100:.2f}%)\n")

# Анализ данных
analyze_data(short_range_data, "короткого диапазона")
analyze_data(full_range_data, "полного диапазона (200-2000)")
