import sys
import random
from typing import Iterator, List, Sequence, Set, Tuple
import numpy as np
import matplotlib.pyplot as plt


def generate_indices(numposts: int, sample_size: int) -> List[int]:
    indices = []
    for _ in range(sample_size):
        indices.append(random.randrange(0, numposts))
    return indices


def sample_posts_from_file(path: str, numposts: int, sample_size: int = 1000) -> List[Tuple[str, Set[str]]]:
    """Sample posts from a txt file and return list of (id, shingles_set)."""
    posts = []
    indices = generate_indices(numposts, sample_size)
    count = 0
    with open(path) as dataset:
        for line in dataset:
            if count in indices:
                data = line.split(",")
                posts.append((data[0], set(data[1:])))
            count += 1
    return posts


def jaccard(a: Set[str], b: Set[str]) -> float:
    if not a and not b:
        return 1.0
    inter = a & b
    union = a | b
    if not union:
        return 0.0
    return len(inter) / len(union)


def compute_all_pairwise_sims(items: Sequence[Tuple[str, Set[str]]]) -> Iterator[Tuple[str, str, float]]:
    """Yield (id1, id2, similarity) for each pair id1 < id2 in items."""
    n = len(items)
    for i in range(n):
        id1, s1 = items[i]
        for j in range(i + 1, n):
            id2, s2 = items[j]
            yield id1, id2, jaccard(s1, s2)


def compute_similarity_list(items: Sequence[Tuple[str, Set[str]]]) -> List[float]:
    """Return list of Jaccard similarities for every pair in items."""
    return [sim for _, _, sim in compute_all_pairwise_sims(items)]


def plot_similarity_hist(similarities: List[float], name: str, output_path: str, bin_size: float = 0.02) -> None:
    bins = np.arange(0.0, 1.0 + bin_size, bin_size)
    plt.figure(figsize=(8, 6))
    plt.hist(similarities, bins=bins, edgecolor='black')
    plt.yscale('log')
    plt.xlabel('Jaccard similarity')
    plt.ylabel('Aantal paren')
    plt.title(f'Jaccard similarity per paar in {name} (totaal # paren: {len(similarities)})')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def main(dataset, output_path, num_posts, sample_size: int = 1000, bin_size: float = 0.02):
    print(f'Sampling {sample_size} posts from {dataset}')
    sampled = sample_posts_from_file(dataset, num_posts, sample_size)
    print('Computing pairwise Jaccard similarities')
    similarities = compute_similarity_list(sampled)
    print(f'Computed {len(similarities)} similarities (pairs).')
    print('Plotting histogram')
    plot_similarity_hist(similarities, dataset, output_path, bin_size=bin_size)
    print(f'Saved histogram to {output_path}')


if __name__ == '__main__':
    if len(sys.argv) < 4:
        print('Usage: python brute_force.py input.txt num_posts output.png')
        sys.exit(1)
    input_path = sys.argv[1]
    num_posts = int(sys.argv[2])
    output_path = sys.argv[3]
    main(input_path, output_path, num_posts, sample_size=1000)