import matplotlib.pyplot as plt
from datetime import datetime

def analyze_line(line):
    if "00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F" in line:
        return "хорошая"
    elif "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00" in line:
        return "нет записи"
    elif "FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF" in line:
        return "мусор"
    else:
        return "не получилось"

def analyze_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    clusters = {}
    current_cluster = None

    for line in lines:
        line = line.strip()

        if line.isdigit():
            current_cluster = line
            clusters[current_cluster] = {"хорошая": 0, "нет записи": 0, "мусор": 0, "не получилось": 0}
        elif line.startswith("[=]"):
            result = analyze_line(line)
            if current_cluster is not None:
                clusters[current_cluster][result] += 1

    all_totals = {"хорошая": 0, "нет записи": 0, "мусор": 0, "не получилось": 0}
    for cluster in clusters.values():
        for key in all_totals:
            all_totals[key] += cluster[key]
    clusters["all"] = all_totals

    return clusters

def calculate_percentages(cluster_data):
    total = sum(cluster_data.values())
    return {key: (value / total * 100) if total > 0 else 0 for key, value in cluster_data.items()}

def plot_results(clusters):
    cluster_names = list(clusters.keys())
    good = [clusters[c]["хорошая"] / sum(clusters[c].values()) * 100 for c in cluster_names]
    no_data = [clusters[c]["нет записи"] / sum(clusters[c].values()) * 100 for c in cluster_names]
    junk = [clusters[c]["мусор"] / sum(clusters[c].values()) * 100 for c in cluster_names]
    failed = [clusters[c]["не получилось"] / sum(clusters[c].values()) * 100 for c in cluster_names]

    plt.figure("Тест ключей", figsize=(10, 6))
    plt.barh(cluster_names, good, color='green', label='хорошая')
    plt.barh(cluster_names, no_data, color='blue', left=good, label='нет записи')
    plt.barh(cluster_names, junk, color='red', left=[i+j for i, j in zip(good, no_data)], label='мусор')
    plt.barh(cluster_names, failed, color='yellow', left=[i+j+k for i, j, k in zip(good, no_data, junk)], label='не получилось')

    plt.xlabel('Процент')
    plt.ylabel('Кластеры')
    plt.title('Анализ строк в кластерах')
    plt.legend()
    plt.show()

def write_results_to_file(clusters, base_filename):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    cluster_range = f"{min(clusters.keys())}-{max(clusters.keys())}"
    output_filename = f"{base_filename}_{timestamp}_{cluster_range}.txt"

    with open(output_filename, 'w') as file:
        for cluster, data in clusters.items():
            percentages = calculate_percentages(data)
            file.write(f"Кластер {cluster}:\n")
            for key, value in data.items():
                file.write(f"  {key}: {value} ({percentages[key]:.2f}%)\n")
            file.write("\n")

def print_results(clusters):
    for cluster, data in clusters.items():
        percentages = calculate_percentages(data)
        print(f"Кластер {cluster}:")
        for key, value in data.items():
            print(f"  {key}: {value} ({percentages[key]:.2f}%)")
        print()

if __name__ == "__main__":
    filename = "output.txt"
    base_filename = "results"
    clusters = analyze_file(filename)
    plot_results(clusters)
    write_results_to_file(clusters, base_filename)
    print_results(clusters)
