import sys
import os
from itertools import combinations

def generate_candidates(frequent_itemsets, k):
    """
    Generate candidate k-itemsets from frequent (k-1)-itemsets.
    Only generate candidates where all (k-1)-subsets are frequent.
    """
    candidates = set()
    frequent_list = list(frequent_itemsets.keys())
    
    if k == 2:
        # Special case: generate pairs from single items
        candidates = set(combinations(sorted(frequent_list), 2))
    else:
        # Join step: combine itemsets that differ by exactly one item
        for i in range(len(frequent_list)):
            for j in range(i + 1, len(frequent_list)):
                item_i = frequent_list[i] if isinstance(frequent_list[i], tuple) else (frequent_list[i],)
                item_j = frequent_list[j] if isinstance(frequent_list[j], tuple) else (frequent_list[j],)
                
                # Union the two itemsets
                union = tuple(sorted(set(item_i) | set(item_j)))
                
                # Only consider if the union has size k
                if len(union) == k:
                    # Prune step: check if all (k-1)-subsets are frequent
                    all_subsets_frequent = True
                    for subset in combinations(union, k - 1):
                        if subset not in frequent_itemsets:
                            all_subsets_frequent = False
                            break
                    
                    if all_subsets_frequent:
                        candidates.add(union)
    
    return candidates


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
    
    # Generate candidates for next level (size current_size + 1)
    candidates = generate_candidates(frequent_itemsets, current_size + 1)
    
    print(f"Generated {len(candidates)} candidates for level {current_size + 1}")
    
    if len(candidates) == 0:
        # No candidates generated, return current level
        print(f"No candidates at level {current_size + 1}, stopping early")
        if len(frequent_itemsets) == 0:
            return ([], 0)
        mx = max(frequent_itemsets.values())
        return ([combo for combo, v in frequent_itemsets.items() if v == mx], mx)
    
    # Count candidates in baskets
    candidate_counts = {}
    for basket in baskets:
        basket_set = set(basket)
        for candidate in candidates:
            candidate_set = set(candidate)
            if candidate_set.issubset(basket_set):
                if candidate in candidate_counts:
                    candidate_counts[candidate] += 1
                else:
                    candidate_counts[candidate] = 1
    
    # Prune: keep only frequent itemsets
    frequent_next = {combo: count for combo, count in candidate_counts.items() 
                     if count >= threshold}
    
    if len(frequent_next) == 0:
        # No frequent itemsets at next level, return current level
        print(f"No frequent itemsets at level {current_size + 1}, returning level {current_size}")
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
    
    # Start A-Priori recursion from size 1
    result = make_combinations(author_counts, baskets, k, threshold, current_size=1)
    
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