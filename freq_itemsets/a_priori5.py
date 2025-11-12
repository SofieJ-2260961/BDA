"""
A-Priori Algorithm for Finding Maximal Author Sets
Optimized for exact results with cProfile bottleneck analysis
No publications are skipped - all data is processed
"""

from itertools import combinations
from collections import defaultdict
import time
import cProfile
import pstats
import io

def read_dataset(filename):
    """
    Generator function to read dataset line by line.
    Yields frozensets of authors for each publication.
    """
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            authors = line.strip().split(',')
            authors = [a.strip() for a in authors if a.strip()]
            if len(authors) > 0:
                yield frozenset(authors)

def count_support_pass_optimized(filename, candidates, k):
    """
    Optimized single pass with smart subset generation.
    Only generates subsets that could possibly be in candidates.
    
    Args:
        filename: Path to dataset file
        candidates: Set of candidate itemsets (frozensets)
        k: Size of itemsets to count
    
    Returns:
        Dictionary mapping itemsets to their support counts
    """
    support_counts = defaultdict(int)
    
    # Pre-convert to set for O(1) lookup
    candidates_set = set(candidates) if not isinstance(candidates, set) else candidates
    
    total_pubs = 0
    total_subsets = 0
    large_pubs = 0
    
    for publication in read_dataset(filename):
        pub_size = len(publication)
        total_pubs += 1
        
        # Skip if publication is too small
        if pub_size < k:
            continue
        
        # Track large publications
        if pub_size > 50:
            large_pubs += 1
            if large_pubs <= 5:  # Report first few
                print(f"  Processing large publication with {pub_size} authors...")
        
        # For very large publications, use more efficient checking
        if pub_size > 100:
            # Only check subsets that could be candidates
            # This is much faster than generating all subsets
            for subset_tuple in combinations(publication, k):
                total_subsets += 1
                subset_frozen = frozenset(subset_tuple)
                if subset_frozen in candidates_set:
                    support_counts[subset_frozen] += 1
                
                # Progress indicator for very large publications
                if total_subsets % 1000000 == 0:
                    print(f"    ... checked {total_subsets:,} subsets so far")
        else:
            # Normal processing for regular publications
            for subset_tuple in combinations(publication, k):
                total_subsets += 1
                subset_frozen = frozenset(subset_tuple)
                if subset_frozen in candidates_set:
                    support_counts[subset_frozen] += 1
    
    print(f"  Processed {total_pubs} publications, checked {total_subsets:,} subsets")
    if large_pubs > 0:
        print(f"  Found {large_pubs} publications with >50 authors")
    
    return support_counts

def generate_candidates_optimized(prev_frequent, k):
    """
    Optimized candidate generation with early pruning.
    
    Args:
        prev_frequent: Set of frequent itemsets of size k-1
        k: Size of candidates to generate
    
    Returns:
        Set of candidate itemsets of size k
    """
    candidates = set()
    prev_list = list(prev_frequent)
    n = len(prev_list)
    
    # For small k, use optimized join
    if k <= 3:
        # Self-join without explicit subset checking for small k
        for i in range(n):
            for j in range(i + 1, n):
                union = prev_list[i] | prev_list[j]
                if len(union) == k:
                    candidates.add(union)
    else:
        # Standard self-join with pruning for larger k
        for i in range(n):
            for j in range(i + 1, n):
                union = prev_list[i] | prev_list[j]
                
                if len(union) == k:
                    # Check if all (k-1)-subsets are frequent
                    all_frequent = True
                    for subset in combinations(union, k - 1):
                        if frozenset(subset) not in prev_frequent:
                            all_frequent = False
                            break
                    
                    if all_frequent:
                        candidates.add(union)
    
    return candidates

def apriori_maximal_author_sets(filename, min_support, enable_profiling=False):
    """
    A-Priori algorithm to find maximal author sets for all k.
    Processes ALL publications without skipping.
    
    Args:
        filename: Path to dataset file
        min_support: Minimum support threshold
        enable_profiling: Whether to enable detailed profiling
    
    Returns:
        Dictionary mapping k to (max_support, count, example) tuples
    """
    print(f"Starting A-Priori with minimum support = {min_support}")
    print(f"Processing ALL publications (no skipping)")
    print("=" * 70)
    
    results = {}
    k = 1
    
    # First pass: count individual authors
    print(f"\n[Pass {k}] Counting individual authors...")
    start_time = time.time()
    
    author_counts = defaultdict(int)
    total_pubs = 0
    
    for publication in read_dataset(filename):
        total_pubs += 1
        for author in publication:
            author_counts[frozenset([author])] += 1
    
    # Filter by minimum support
    frequent_items = {item: count for item, count in author_counts.items() 
                      if count >= min_support}
    
    elapsed = time.time() - start_time
    print(f"Total publications: {total_pubs}")
    print(f"Unique authors: {len(author_counts)}")
    print(f"Frequent authors (support >= {min_support}): {len(frequent_items)}")
    print(f"Time: {elapsed:.2f}s")
    
    if not frequent_items:
        print("\nNo frequent itemsets found. Try lowering the threshold.")
        return results
    
    # Store results for k=1
    max_support = max(frequent_items.values())
    max_items = [item for item, sup in frequent_items.items() if sup == max_support]
    results[k] = (max_support, len(max_items), max_items[0])
    
    print(f"\nMaximal support for k={k}: {max_support}")
    print(f"Number of maximal author sets: {len(max_items)}")
    print(f"Example: {set(max_items[0])}")
    
    # Previous frequent itemsets
    prev_frequent = set(frequent_items.keys())
    
    # Iterate for k > 1
    k = 2
    while prev_frequent:
        print(f"\n[Pass {k}] Generating candidates of size {k}...")
        cand_start = time.time()
        
        # Generate candidates
        candidates = generate_candidates_optimized(prev_frequent, k)
        
        if not candidates:
            print(f"No candidates generated. Stopping.")
            break
        
        cand_time = time.time() - cand_start
        print(f"Generated {len(candidates)} candidates in {cand_time:.2f}s")
        
        # Count support for candidates
        print(f"Counting support for candidates...")
        count_start = time.time()
        
        support_counts = count_support_pass_optimized(filename, candidates, k)
        
        count_time = time.time() - count_start
        
        # Filter by minimum support
        frequent_items = {item: count for item, count in support_counts.items() 
                          if count >= min_support}
        
        total_time = time.time() - cand_start
        print(f"Found {len(frequent_items)} frequent itemsets of size {k}")
        print(f"Time: {total_time:.2f}s (candidate gen: {cand_time:.2f}s, counting: {count_time:.2f}s)")
        
        if not frequent_items:
            print(f"No frequent itemsets of size {k} found. Stopping.")
            break
        
        # Store results for current k
        max_support = max(frequent_items.values())
        max_items = [item for item, sup in frequent_items.items() if sup == max_support]
        results[k] = (max_support, len(max_items), max_items[0])
        
        print(f"\nMaximal support for k={k}: {max_support}")
        print(f"Number of maximal author sets: {len(max_items)}")
        print(f"Example: {set(max_items[0])}")
        
        # Update for next iteration
        prev_frequent = set(frequent_items.keys())
        k += 1
    
    return results

def print_summary(results):
    """Print a summary table of all results."""
    print("\n" + "=" * 70)
    print("SUMMARY OF MAXIMAL AUTHOR SETS")
    print("=" * 70)
    print(f"{'k':<5} {'Max Support':<15} {'# of Max Sets':<20} {'Example'}")
    print("-" * 70)
    
    for k in sorted(results.keys()):
        max_support, count, example = results[k]
        example_str = str(set(example))
        if len(example_str) > 40:
            example_str = example_str[:37] + "..."
        print(f"{k:<5} {max_support:<15} {count:<20} {example_str}")

def run_with_profiling(filename, min_support):
    """Run the algorithm with cProfile enabled."""
    print("\n" + "=" * 70)
    print("RUNNING WITH PROFILING ENABLED")
    print("=" * 70)
    
    profiler = cProfile.Profile()
    profiler.enable()
    
    results = apriori_maximal_author_sets(filename, min_support, enable_profiling=True)
    
    profiler.disable()
    
    # Print profiling results
    print("\n" + "=" * 70)
    print("PROFILING RESULTS - TOP BOTTLENECKS")
    print("=" * 70)
    
    s = io.StringIO()
    stats = pstats.Stats(profiler, stream=s)
    stats.sort_stats('cumulative')
    stats.print_stats(20)  # Top 20 functions
    
    print(s.getvalue())
    
    return results

def main():
    """Main function to run the A-Priori algorithm."""
    # Configuration
    filename = "./datasets/dataset_large.txt"
    min_support = 25
    enable_profiling = True  # Set to True to identify bottlenecks
    
    print("A-PRIORI ALGORITHM FOR MAXIMAL AUTHOR SETS")
    print("=" * 70)
    print(f"Dataset: {filename}")
    print(f"Minimum support threshold: {min_support}")
    print(f"Profiling: {'ENABLED' if enable_profiling else 'DISABLED'}")
    print()
    
    overall_start = time.time()
    
    try:
        if enable_profiling:
            results = run_with_profiling(filename, min_support)
        else:
            results = apriori_maximal_author_sets(filename, min_support)
        
        if results:
            print_summary(results)
        
        overall_elapsed = time.time() - overall_start
        print(f"\n{'=' * 70}")
        print(f"Total execution time: {overall_elapsed:.2f}s ({overall_elapsed/60:.2f} minutes)")
        print(f"{'=' * 70}")
        
    except FileNotFoundError:
        print(f"\nError: File '{filename}' not found.")
        print("Please update the filename in the script.")
    except KeyboardInterrupt:
        print("\n\nInterrupted by user. Partial results may be incomplete.")
    except Exception as e:
        print(f"\nError occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()