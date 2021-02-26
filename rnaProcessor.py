class ProcessorRna:
    stopCodonList = [['U', 'A', 'G'], ['U', 'G', 'A'],['U', 'A', 'A']]
    validCharacters = ['A', 'C', 'G', 'U']
    nonRelevantCharacters = [' ', '\t', '\n', '\r']
    currentCharacter = None

    def __init__(self, dataSource):
        self.incomingRna = open(dataSource, mode="r", buffering=-1, encoding=None, errors=None, newline=None, closefd=True)

    def __iter__(self):
        return self

    def __next__(self):
        resultingGenChain = None
        currentGen = []
        currentCodon = []

        self.readNextCharacter()
        while(resultingGenChain == None and self.currentCharacter != ''):
            # Check comment
            if self.isCommentStart(self.currentCharacter):
                self.readCharacterAfterComment()

            # Validate characters
            if self.isNonRelevantCharacter(self.currentCharacter):
                self.readNextCharacter()
                continue

            if not self.isValidCharacter(self.currentCharacter):
                self.skipUntilNextStopCodon()
                raise StopIteration

            # Apply logic
            currentCodon.append(self.currentCharacter)
            if len(currentCodon) == 3:
                currentGen.append(currentCodon)
                if self.isStopCodon(currentCodon):
                    if len(currentGen) > 1:
                        resultingGenChain = currentGen
                        currentGen = []
                        currentCodon = []
                        break
                    currentGen = []
                currentCodon = []

            self.readNextCharacter()
            continue

        if currentGen != []:
            print('Last chain length was not valid')
            self.incomingRna.close()
            raise StopIteration

        if currentCodon != []:
            print('No ending stop codon was found')
            self.incomingRna.close()
            raise StopIteration

        return resultingGenChain

    def skipUntilNextStopCodon(self):
        codon = []
        while not self.isStopCodon(codon) and self.currentCharacter != '':
            codon.append(self.currentCharacter)
            if len(codon) > 3:
                codon.pop(0)
            self.readNextCharacter()

    def isValidCharacter(self, character):
        return character in self.validCharacters
    
    def isNonRelevantCharacter(self, character):
        return character in self.nonRelevantCharacters

    def isStopCodon(self, codon):
        return codon in self.stopCodonList

    def isCommentStart(self, character):
        return character == ">"
    
    def readCharacterAfterComment(self):
        self.currentCharacter = self.incomingRna.readline() 
        self.readNextCharacter()

    def readNextCharacter(self):
        self.currentCharacter = self.incomingRna.read(1)
        self.currentCharacter = self.currentCharacter.capitalize()
