#  A-priori implementation

import sys
import os
from itertools import combinations

def count_frequent_itemsets(frequent_prev: dict, baskets: list, k: int, threshold: int):
    """
    Count k-itemsets by generating them on-the-fly from baskets.
    Only count if all (k-1)-subsets are frequent (A-Priori property).
    """
    candidate_counts = {}
    
    for basket in baskets:
        # Generate all k-combinations from this basket
        for combo in combinations(sorted(basket), k):
            # Check if all (k-1)-subsets are in frequent_prev
            all_subsets_frequent = True
            for subset in combinations(combo, k - 1):
                if subset not in frequent_prev:
                    all_subsets_frequent = False
                    break
            
            # Only count if all subsets are frequent
            if all_subsets_frequent:
                if combo in candidate_counts:
                    candidate_counts[combo] += 1
                else:
                    candidate_counts[combo] = 1
    
    # Prune: keep only itemsets that meet threshold
    frequent = {combo: count for combo, count in candidate_counts.items() 
                if count >= threshold}
    
    return frequent


def make_combinations(frequent_itemsets: dict, baskets: list, k: int, threshold: int, current_size: int):
    """
    Recursively find frequent k-itemsets using A-Priori algorithm.
    """
    # Base case: we've reached the desired k
    if current_size == k:
        if len(frequent_itemsets) == 0:
            return ([], 0)
        mx = max(frequent_itemsets.values())
        return ([combo for combo, v in frequent_itemsets.items() if v == mx], mx)
    
    print(f"Level {current_size}: {len(frequent_itemsets)} frequent itemsets")
    
    # Generate and count (current_size + 1)-itemsets from baskets
    # Only count those where all k-subsets are in frequent_itemsets
    frequent_next = count_frequent_itemsets(frequent_itemsets, baskets, 
                                           current_size + 1, threshold)
    
    print(f"Level {current_size + 1}: {len(frequent_next)} frequent itemsets")
    
    if len(frequent_next) == 0:
        # No frequent itemsets at next level, return current level
        print(f"No frequent itemsets at level {current_size + 1}, stopping")
        if len(frequent_itemsets) == 0:
            return ([], 0)
        mx = max(frequent_itemsets.values())
        return ([combo for combo, v in frequent_itemsets.items() if v == mx], mx)
    
    # Recurse to next level
    return make_combinations(frequent_next, baskets, k, threshold, current_size + 1)


def read_dataset(file_name, k, threshold): 
    full_file_path: str = os.path.join(os.path.dirname(__file__), file_name)
    author_counts = {} 
    baskets = []

    print(f"Reading dataset: {file_name}")
    print(f"Looking for {k}-itemsets with threshold {threshold}")
    
    with open(full_file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line:  # Skip empty lines
                authors = line.split(",")
                baskets.append(authors)
                    
                for author in authors:
                    if author in author_counts:    
                        author_counts[author] += 1
                    else:
                        author_counts[author] = 1

    print(f"Total baskets: {len(baskets)}")
    print(f"Total unique authors: {len(author_counts)}")
    
    # Prune: remove authors that don't meet the threshold
    author_counts = {author: count for author, count in author_counts.items() 
                     if count >= threshold}

    print(f"Frequent authors (support >= {threshold}): {len(author_counts)}")
    
    if len(author_counts) == 0:
        print("No frequent authors found!")
        return ([], 0)
    
    if k == 1:
        # Special case: return most frequent single authors
        mx = max(author_counts.values())
        result = [author for author, count in author_counts.items() if count == mx]
        print(f"\nResult: Most frequent author(s) appear in {mx} books")
        print(f"Authors: {result}")
        return (result, mx)
    
    # Convert single authors to tuples for consistency
    author_counts_tuples = {(author,): count for author, count in author_counts.items()}
    
    # Start A-Priori recursion from size 1
    result = make_combinations(author_counts_tuples, baskets, k, threshold, current_size=1)
    
    print(f"\nResult: Most frequent {k}-author combination(s) appear in {result[1]} books")
    print(f"Combinations: {result[0]}")
    return result


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

    read_dataset(file_name, k, threshold)

    
if __name__ == '__main__':
    main()