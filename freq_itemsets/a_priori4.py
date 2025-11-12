#  A-priori implementation

import sys
import os
from itertools import combinations
import cProfile

def identify_max_author_sets(frequent_itemsets: dict, k: int):
    mx = max(frequent_itemsets.values())
    result = ([combo for combo, v in frequent_itemsets.items() if v == mx], mx)
    print(f"\nResult: Most frequent {k}-author combination(s) appear in {result[1]} books")
    print(f"Combinations: {result[0]}")

def count_frequent_itemsets(frequent: dict, baskets: list, k: int, threshold: int):
    candidate_counts = {}
    
    for basket in baskets:
        for combo in combinations(sorted(basket), k):
            # Check if all (k-1)-subsets are frequent
            all_subsets_frequent = True
            for subset in combinations(combo, k - 1):
                if subset not in frequent:
                    all_subsets_frequent = False
                    break          

            if all_subsets_frequent:
                if combo in candidate_counts:
                    candidate_counts[combo] += 1
                else:
                    candidate_counts[combo] = 1
    
    # Check threshold
    frequent_next = {combo: count for combo, count in candidate_counts.items() 
                if count >= threshold}
    
    return frequent_next


def a_priori(frequent_itemsets: dict, baskets: list, k: int, threshold: int):
    current_size = 1
    result = ([], 0)
    new_frequent_itemset = True

    while new_frequent_itemset:

        if len(frequent_itemsets) == 0:
            break
        frequent_next = count_frequent_itemsets(frequent_itemsets, baskets, current_size + 1, threshold)
        if len(frequent_next) == 0:
            new_frequent_itemset = False
            print(f"No frequent itemsets at level {current_size + 1}, stopping")
            break
        identify_max_author_sets(frequent_itemsets, k)    
        frequent_itemsets = frequent_next
        current_size += 1
            

def read_dataset(file_name, k, threshold): 
    full_file_path: str = os.path.join(os.path.dirname(__file__), file_name)
    author_counts = {} 
    baskets = []

    print(f"Reading dataset: {file_name}")
    print(f"Looking for {k}-itemsets with threshold {threshold}")
    
    with open(file_name, 'r', encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            authors = line.split(",")
            baskets.append(authors)
                
            for author in authors:
                if author in author_counts:    
                    author_counts[author] += 1
                else:
                    author_counts[author] = 1
    
    # remove authors that don't meet the threshold
    author_counts = {(author,): count for author, count in author_counts.items() 
                     if count >= threshold}

    print(f"Frequent authors (support >= {threshold}): {len(author_counts)}")
    
    if len(author_counts) == 0:
        print("No frequent authors found!")
  
    return author_counts, baskets


def main():
    if len(sys.argv) < 4:
        print("Usage: python script.py <filename> <k> <threshold>")
        sys.exit(1)
    
    file_name = sys.argv[1]
    k = int(sys.argv[2])
    threshold = int(sys.argv[3])

    if k < 1:
        print("Error: k must be at least 1")
        sys.exit(1)
    
    if threshold < 1:
        print("Error: threshold must be at least 1")
        sys.exit(1)

    author_counts, baskets = read_dataset(file_name, k, threshold)
    result = a_priori(author_counts, baskets, k, threshold)
    
if __name__ == '__main__':
    main()