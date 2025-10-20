# Naive implementation
import sys
import os
from itertools import combinations
from collections import defaultdict

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
            
            for k in range(1, n):
                for subset in combinations(authors, k):
                    subset = frozenset(subset)
                    subset_counts[subset] += 1
                    count = subset_counts[subset]
                    
                    if count > max_count_per_k[k]:
                        max_count_per_k[k] = count
                        max_subsets_per_k[k] = {subset}
                    elif count == max_count_per_k[k]:
                        max_subsets_per_k[k].add(subset)

    print(f"Found sets: {list(max_subsets_per_k.items())}")
    print(f"Maximal occurrences: {max_count_per_k}")


def main():
    if len(sys.argv) < 3:
        print("Give file to read")
        sys.exit(1)
    file_name = sys.argv[1]

    read_dataset(file_name)


if __name__ == '__main__':
    main()