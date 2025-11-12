# Naive implementation
import sys
import os
from itertools import combinations

def read_dataset(file_name, k): 
    full_file_path: str = os.path.join(os.path.dirname(__file__), file_name)

    subsets = {}

    with open(full_file_path, 'r') as file:
        for line in file:
            line = line.removesuffix("\n")
            authors = line.split(",")
                
            if len(authors) > k:
                combination = combinations(authors, k)
                for subset in combination:
                    subset = frozenset(subset)
                    if subset in subsets.keys():
                        subsets[subset] += 1
                    else:
                        subsets[subset] = 1
                        
            elif len(authors) == k:
                subset = frozenset(authors)
                if subset in subsets.keys():
                    subsets[subset] += 1
                else:
                    subsets[subset] = 1


    mx = max(subsets.values())
    print(f"Found sets: {[k for k, v in subsets.items() if v == mx]}")
    print(f"Maximal occurences: {mx}")

def main():
    if len(sys.argv) < 3:
        print("Give file to read")
        sys.exit(1)
    file_name = sys.argv[1]
    k = int(sys.argv[2])

    read_dataset(file_name, k)
    
    pass

    
if __name__ == '__main__':
    main()
