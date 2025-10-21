# Naive implementation
import sys
import os
from itertools import combinations
from collections import defaultdict
import time

def read_dataset(file_name: str, k: int): 
    full_file_path = os.path.join(os.path.dirname(__file__), file_name)

    subset_counts = defaultdict(int)
    max_count = 0
    max_subsets = []

    with open(full_file_path, 'r') as file:
        for line in file:
            line = line.removesuffix("\n")
            authors = line.split(",")

            if len(authors) >= k:
                for subset in combinations(authors, k):
                    subset = tuple(sorted(subset))
                    subset_counts[subset] += 1
                    count = subset_counts[subset]
                    
                    if count > max_count:
                        max_count = count
                        max_subsets = [subset]
                    elif count == max_count:
                        max_subsets.append(subset)

    print(f"{len(max_subsets)} set(s) found for k = {k} with max = {max_count}: ")
    for subset in max_subsets:
        print(subset)


def main():
    if len(sys.argv) < 2:
        print("Give file to read")
        sys.exit(1)
    file_name = sys.argv[1]
    k = sys.argv[2]

    start = time.time()
    read_dataset(file_name, int(k))
    end = time.time()
    print(f"Total time: {end - start:.4f} seconds")


if __name__ == '__main__':
    main()