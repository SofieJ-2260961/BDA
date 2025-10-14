# TODO: write some tests for the datasets

# Naive implementation
import sys
import os
from itertools import combinations

def read_dataset(file_name): 
    full_file_path: str = os.path.join(os.path.dirname(__file__), file_name)

    max_authors = 0
    num_publ = 0
    all_authors = []
    total_authors = 0

    with open(full_file_path, 'r') as file:
        for line in file:
            line = line.removesuffix("\n")
            authors = line.split(",")
            num_publ += 1
            total_authors += len(authors)
            max_authors = max(len(authors), max_authors)
            for author in authors:
                if author not in all_authors:
                    all_authors.append(author)


    print(f"# publications: {num_publ}")
    print(f"# authors: {len(all_authors)}")
    print(f"Max authors per publication: {max_authors}")
    print(f"Avg authors per publication: {total_authors / num_publ}")

def main():
    if len(sys.argv) < 2:
        print("Give file to read")
        sys.exit(1)
    file_name = sys.argv[1]

    read_dataset(file_name)
    
    pass

    
if __name__ == '__main__':
    main()
