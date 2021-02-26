from rnaProcessor import ProcessorRna

def main():
    path = "refMrna.fa.txt"
    processor = ProcessorRna(path)

    for gen in processor:
        print(gen)

if __name__ == "__main__":
    main()