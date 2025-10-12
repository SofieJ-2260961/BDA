#  A-priori implementation

import sys
import os
from itertools import combinations

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

    print(author_counts)


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
