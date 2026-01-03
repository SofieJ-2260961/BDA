import sys
from row_processor import parse, process_post

def main(input_path, output_path):
    with open(output_path, mode="w") as output:
        for attrs in parse(input_path):
            pid, shingles = process_post(attrs, k=5)
            if pid is None:
                continue
            output.write(pid)
            for shingle in shingles:
                output.write(",")
                output.write(shingle)
            output.write("\n")


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: python convert_xml.py input.xml output.txt')
        sys.exit(1)
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    main(input_path, output_path)