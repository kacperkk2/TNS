import random
import sys

def extract(filename:str, sample_size:int):
    rows = []
    file_parts = filename.split('.')
    extension = file_parts[-1]
    filename_noext = '.'.join(file_parts[0:-1])
    print("Opening:", filename, filename_noext, extension)
    with open(f"experiments/number_data/{filename}", mode='r') as inputfile:
        rows = inputfile.readlines()
    
    extracted_sample = random.sample(rows, sample_size)
    with open(f"experiments/number_data/{filename_noext}-{sample_size}rows.{extension}", mode='w') as outputfile:
        outputfile.writelines(extracted_sample)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: filename sample_size")
        exit(1)

    extract(sys.argv[1], int(sys.argv[2]))