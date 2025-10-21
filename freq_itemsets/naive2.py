# Naive implementation
import sys
import os
from itertools import combinations
from collections import defaultdict
import time

def read_dataset(file_name): 
    full_file_path = os.path.join(os.path.dirname(__file__), file_name)

    subset_counts = defaultdict(int)
    max_count_per_k = defaultdict(int)
    max_subsets_per_k = defaultdict(set)

    with open(full_file_path, 'r') as file:
        for line in file:
            line = line.removesuffix("\n")
            authors = line.split(",")
            n = len(authors)
            
            for k in range(1, n+1):
                for subset in combinations(authors, k):
                    subset = frozenset(subset)
                    subset_counts[subset] += 1
                    count = subset_counts[subset]
                    
                    if count > max_count_per_k[k]:
                        max_count_per_k[k] = count
                        max_subsets_per_k[k] = {subset}
                    elif count == max_count_per_k[k]:
                        max_subsets_per_k[k].add(subset)

    for k, subsets in zip(max_count_per_k.items(), max_subsets_per_k.values()):
        print(f"{len(subsets)} set(s) found for k = {k[0]} with max = {k[1]}: ")
        for subset in subsets:
            print(subset)


def main():
    if len(sys.argv) < 2:
        print("Give file to read")
        sys.exit(1)
    file_name = sys.argv[1]

    start = time.time()
    read_dataset(file_name)
    end = time.time()
    print(f"Total time: {end - start:.4f} seconds")


if __name__ == '__main__':
    main()