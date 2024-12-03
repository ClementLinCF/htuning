import csv

def extract_values(filename):
    results = {}
    total_count = 0
    
    with open(filename, 'r') as file:
        for line in file:
            split_string = line.split(' ')
            transA = split_string[split_string.index('--transA') + 1]
            transB = split_string[split_string.index('--transB') + 1]
            m = int(split_string[split_string.index('-m') + 1])
            n = int(split_string[split_string.index('-n') + 1])
            k = int(split_string[split_string.index('-k') + 1])
            
            combination = (transA, transB, m, n, k)
            
            if combination in results:
                results[combination] += 1
            else:
                results[combination] = 1
                
            total_count += 1

    return results, total_count

log_filename = "hipblaslt.log"

results, total_count = extract_values(log_filename)

with open('freq_result.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['transA', 'transB', 'm', 'n', 'k', 'count', 'percentage']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    for combination, count in results.items():
        percentage = (count / total_count) * 100
        writer.writerow({'transA': combination[0], 'transB': combination[1], 'm': combination[2], 'n': combination[3], 'k': combination[4], 'count': count, 'percentage': percentage})

