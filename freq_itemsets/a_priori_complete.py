#  A-priori implementation

import sys
import os
from itertools import combinations
import time

def count_frequent_itemsets(frequent: dict, baskets: list, k: int, threshold: int):
    candidate_counts = {}
    
    # Test to see how far along the program is
    print(f"{len(frequent)} itemsets for k = {k}")

    frequent_set = set(frequent.keys())
    
    # Get all authors that appear in the current frequent itemsets
    frequent_items = set()
    for itemset in frequent_set:
        frequent_items.update(itemset)

    for basket in baskets:
        # Filter all authors from basket that are not frequent anymore (-> less combinations)
        filtered_basket = [item for item in basket if item in frequent_items]
        
        # Skip (filtered) basket if too small
        if len(filtered_basket) < k:
            continue
                    
        for combo in combinations(sorted(filtered_basket), k):
            # Check if all subsets are frequent
            all_subsets_frequent = True
            for subset in combinations(combo, k - 1):
                if subset not in frequent_set:
                    all_subsets_frequent = False
                    break          

            if all_subsets_frequent:
                if combo in candidate_counts:
                    candidate_counts[combo] += 1
                else:
                    candidate_counts[combo] = 1
    
    # Select itemsets that reach the threshold
    frequent_next = {combo: count for combo, count in candidate_counts.items() 
                if count >= threshold}
    
    return frequent_next


def a_priori(frequent_itemsets: dict, baskets: list, threshold: int):
    current_size = 1
    result = ([], 0)

    # Keep looking for maximal k-author sets until none are found
    while True:
        if len(frequent_itemsets) == 0:
            break
        frequent_next = count_frequent_itemsets(frequent_itemsets, baskets, current_size + 1, threshold)
        if len(frequent_next) == 0:
            print(f"No frequent itemsets at k = {current_size + 1}, stopping")
            break
        
        frequent_itemsets = frequent_next
        current_size += 1
            
        mx = max(frequent_itemsets.values())
        result = ([combo for combo, v in frequent_itemsets.items() if v == mx], mx)
        print(f"Most frequent {current_size}-author combination(s) appear in {result[1]} books")
        print(f"Combinations: {result[0]}")
   

def read_dataset(file_name, threshold): 
    full_file_path: str = os.path.join(os.path.dirname(__file__), file_name)
    author_counts = {} 
    baskets = []

    print(f"Reading dataset: {file_name}")
    
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
    
    # Remove authors that don't meet the threshold
    author_counts = {(author,): count for author, count in author_counts.items() 
                     if count >= threshold}

    print(f"Frequent authors (support >= {threshold}): {len(author_counts)}")
  
    return author_counts, baskets


def main():
    if len(sys.argv) < 3:
        print("Usage: python a_priori6.py <filename> <threshold>")
        sys.exit(1)
    
    file_name = sys.argv[1]
    threshold = int(sys.argv[2])
    
    if threshold < 1:
        print("Threshold must be at least 1")
        sys.exit(1)

    start = time.time()
    author_counts, baskets = read_dataset(file_name, threshold)
    a_priori(author_counts, baskets, threshold)
    end = time.time()
    print(f"Total time: {end - start:.4f} seconds")

    
if __name__ == '__main__':
    main()