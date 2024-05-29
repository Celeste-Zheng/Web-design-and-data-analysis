def find_max(theFile):
    max_length = 0
    current = 0
    sequence_started = False

    infile = open(theFile, 'r')
    for aline in infile:
        if aline.startswith('>'):
            if sequence_started:
                max_length = max(max_length, current)
            current = 0
            sequence_started = True
        elif sequence_started:
            current = current + len(aline.strip()) 

        if sequence_started:
            max_length = max(max_length, current)          
    return max_length

if __name__ == "__main__":
    theFile = "honeybee_gene_sequences.txt"
    max_length = find_max(theFile)
    print(f"The maximum sequence length is: {max_length}")