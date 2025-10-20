#  A-priori implementation

import sys
import os
from itertools import combinations
import time

def count_frequent_itemsets(frequent: dict, baskets: list, k: int, threshold: int):
    candidate_counts = {}
    
    print(f"Checking {len(frequent)} itemsets for k = {k}")

    frequent_set = set(frequent.keys())
    frequent_items = set()
    for itemset in frequent_set:
        frequent_items.update(itemset)
    
    checked = 0

    for basket in baskets:
        filtered_basket = [item for item in basket if item in frequent_items]
        if len(filtered_basket) >= k:
            checked += 1
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
    
    print(f"Checked baskets: {checked}")

    return frequent_next


def a_priori(frequent_itemsets: dict, baskets: list, k: int, threshold: int):
    current_size = 1
    result = ([], 0)

    while current_size < k:

        if len(frequent_itemsets) == 0:
            break
        frequent_next = count_frequent_itemsets(frequent_itemsets, baskets, current_size + 1, threshold)
        if len(frequent_next) == 0:
            print(f"No frequent itemsets at level {current_size + 1}, stopping")
            break
            
        frequent_itemsets = frequent_next
        current_size += 1

    mx = max(frequent_itemsets.values())
    result = ([combo for combo, v in frequent_itemsets.items() if v == mx], mx)
    print(f"\nResult: Most frequent {k}-author combination(s) appear in {result[1]} books")
    print(f"Combinations: {result[0]}")
            

def read_dataset(file_name, k, threshold): 
    full_file_path: str = os.path.join(os.path.dirname(__file__), file_name)
    author_counts = {} 
    baskets = []

    print(f"Reading dataset: {file_name}")
    print(f"Looking for {k}-itemsets with threshold {threshold}")
    
    with open(full_file_path, 'r') as file:
        for line in file:
            line = line.strip()
            authors = line.split(",")
            baskets.append(authors)
                
            for author in authors:
                if author in author_counts:    
                    author_counts[author] += 1
                else:
                    author_counts[author] = 1
    
    # Prune: remove authors that don't meet the threshold
    author_counts = {(author,): count for author, count in author_counts.items() 
                     if count >= threshold}

    print(f"Frequent authors (support >= {threshold}): {len(author_counts)}")
    
    if len(author_counts) == 0:
        print("No frequent authors found!")
  
    return author_counts, baskets


def main():
    if len(sys.argv) < 4:
        print("Usage: python script.py <filename> <k> <threshold>")
        print("Example: python script.py small_dataset.txt 3 5")
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

    start = time.time()
    
    author_counts, baskets = read_dataset(file_name, k, threshold)
    result = a_priori(author_counts, baskets, k, threshold)

    end = time.time()
    print(end - start)

    
if __name__ == '__main__':
    main()