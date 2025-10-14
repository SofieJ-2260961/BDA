#  A-priori implementation

import sys
import os
from itertools import combinations

def make_combinations(author_dict: dict, baskets: list, k: int, threshold: int, tuple_size: int):
    if k == 0:
        # Return something
        mx = max(author_dict.values())
        return ([k for k, v in author_dict.items() if v == mx], mx)
    
    combos = combinations(list(author_dict.keys()), tuple_size)
    combo_counts = {}

    for basket in baskets:
        for combo in combos:
            if set(combo).issubset(set(basket)):
                if combo in combo_counts:
                    combo_counts[combo] += 1
                else:
                    combo_counts[combo] = 1
                
    for combo_count in list(combo_counts.keys()):
        if combo_counts[combo_count] < threshold:
            del combo_counts[combo_count]
    
    return make_combinations(combo_counts, baskets, k - 1, threshold, tuple_size + 1)


def read_dataset(file_name, k, threshold): 
    full_file_path: str = os.path.join(os.path.dirname(__file__), file_name)
    author_counts = {} 
    baskets = []

    with open(full_file_path, 'r') as file:
        for line in file:
            line = line.removesuffix("\n")
            authors = line.split(",")
            baskets.append(authors)
                
            for author in authors:
                if author in author_counts:    
                    author_counts[author] += 1
                else:
                    author_counts[author] = 1


    # Remove author count that don't meet the threshold
    for author in list(author_counts.keys()):
        if author_counts[author] < threshold:
            del author_counts[author]


    make_combinations(author_counts, baskets, k, threshold, 1)


def main():
    if len(sys.argv) < 3:
        print("Give file to read")
        sys.exit(1)
    file_name = sys.argv[1]
    k = int(sys.argv[2])
    threshold = int(sys.argv[3])

    read_dataset(file_name, k, threshold)
    
    pass

    
if __name__ == '__main__':
    main()
