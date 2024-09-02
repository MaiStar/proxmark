import matplotlib.pyplot as plt

# Функция для анализа строк
def analyze_line(line):
    if "00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F" in line:
        return "хорошая"
    elif "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00" in line:
        return "нет записи"
    elif "FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF" in line:
        return "мусор"
    else:
        return "не получилось"

# Функция для чтения файла и подсчета строк
def analyze_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    clusters = {}
    current_cluster = None

    for line in lines:
        line = line.strip()

        # Проверяем начало нового кластера
        if line.isdigit():
            current_cluster = line
            clusters[current_cluster] = {"хорошая": 0, "нет записи": 0, "мусор": 0, "не получилось": 0}
        elif line.startswith("[=]"):
            # Анализируем строку
            result = analyze_line(line)
            if current_cluster is not None:
                clusters[current_cluster][result] += 1

    return clusters

# Функция для построения графика
def plot_results(clusters):
    cluster_names = list(clusters.keys())
    good = [clusters[c]["хорошая"] / sum(clusters[c].values()) * 100 for c in cluster_names]
    no_data = [clusters[c]["нет записи"] / sum(clusters[c].values()) * 100 for c in cluster_names]
    junk = [clusters[c]["мусор"] / sum(clusters[c].values()) * 100 for c in cluster_names]
    failed = [clusters[c]["не получилось"] / sum(clusters[c].values()) * 100 for c in cluster_names]

    plt.figure(figsize=(10, 6))
    plt.barh(cluster_names, good, color='green', label='хорошая')
    plt.barh(cluster_names, no_data, color='blue', left=good, label='нет записи')
    plt.barh(cluster_names, junk, color='red', left=[i+j for i, j in zip(good, no_data)], label='мусор')
    plt.barh(cluster_names, failed, color='grey', left=[i+j+k for i, j, k in zip(good, no_data, junk)], label='не получилось')

    plt.xlabel('Процент')
    plt.ylabel('Кластеры')
    plt.title('Анализ строк в кластерах')
    plt.legend()
    plt.show()

# Основная часть
if __name__ == "__main__":
    filename = "output.txt"
    clusters = analyze_file(filename)
    plot_results(clusters)