"""
15-110 Hw6 - Protein Sequencing Project
Name:
AndrewID:
"""

import hw6_protein_tests as test

project = "Protein" # don't edit this

### WEEK 1 ###

'''
readFile(filename)
#1 [Check6-1]
Parameters: str
Returns: str
'''
def readFile(filename):
    with open(filename, 'r') as file:
        content = file.read()
    # Remove any newlines from the text
        content = content.replace('\n', '')
    # Return the modified content
    return content

'''
dnaToRna(dna, startIndex)
#2 [Check6-1]
Parameters: str ; int
Returns: list of strs
'''
def dnaToRna(dna, startIndex):
    codons=[]
    i=startIndex
    while i<len(dna):
        codon=dna[i:i+3]
        if codon in ["TAA","TAG","TGA"]:
            codon=codon.replace("T","U")
            codons.append(codon)
            break
        codon=codon.replace("T","U")
        codons.append(codon)
        i+=3
    return codons


'''
makeCodonDictionary(filename)
#3 [Check6-1]
Parameters: str
Returns: dict mapping strs to strs
'''
def makeCodonDictionary(filename):

    import json

    with open(filename, 'r') as file:
        amino_acid_to_codons = json.load(file)

    # Create a new dictionary to map codons to amino acids
    codon_to_amino_acid = {}

    # Iterate through the amino acid to codons mapping
    for amino_acid, codon_list in amino_acid_to_codons.items():
        # Change all Ts in the codons to Us
        modified_codons = [codon.replace('T', 'U') for codon in codon_list]

        # Map each codon to the corresponding amino acid
        for codon in modified_codons:
            codon_to_amino_acid[codon] = amino_acid

    return codon_to_amino_acid
    


'''
generateProtein(codons, codonD)
#4 [Check6-1]
Parameters: list of strs ; dict mapping strs to strs
Returns: list of strs
'''
def generateProtein(codons, codonD):

    proteins=[]
    if codons[0]=="AUG":
        proteins.append("Start")
    
    for i in range(1,len(codons)):
        if codons[i]=="UAA" or codons[i]=="UAG" or codons[i]=="UGA":
            proteins.append("Stop") 
            return proteins
        else:
            proteins.append(codonD[codons[i]])

    return proteins


'''
synthesizeProteins(dnaFilename, codonFilename)
#5 [Check6-1]
Parameters: str ; str
Returns: 2D list of strs
'''
def synthesizeProteins(dnaFilename, codonFilename):
  # Read DNA sequence from the file
    dna = readFile(dnaFilename)

    # Generate codon dictionary from the provided file
    codonD = makeCodonDictionary(codonFilename)

    proteins = []  # List to store synthesized proteins
    unused_bases_count = 0  # Count of unused bases

    i = 0
    while i < len(dna):
        # Look for the start codon "ATG"
        if dna[i:i + 3] == 'ATG':
            # Call dnaToRna with the correct parameters
            rna = dnaToRna(dna, i)
            # Call generateProtein on the resulting RNA and codon dictionary to produce a protein
            protein = generateProtein(rna, codonD)
            proteins.append(protein)
            # Update the index to skip past all the already-checked bases
            i += 3 * len(rna)
        else:
            # If no start codon is found, move to the next base and increment the unused base count
            i += 1
            unused_bases_count += 1

    total_bases = len(dna)
    total_proteins = len(proteins)


    # Print the results
    print(f"Total number of bases: {total_bases}")
    print(f"Unused base count: {unused_bases_count}")
    print(f"Total number of proteins synthesized: {total_proteins}")

    return proteins



def runWeek1():
    print("Human DNA")
    humanProteins = synthesizeProteins("data/human_p53.txt", "data/codon_table.json")
    print("Elephant DNA")
    elephantProteins = synthesizeProteins("data/elephant_p53.txt", "data/codon_table.json")



### WEEK 2 ###

'''
commonProteins(proteinList1, proteinList2)
#1 [Check6-2]
Parameters: 2D list of strs ; 2D list of strs
Returns: 2D list of strs
'''
def commonProteins(proteinList1, proteinList2):
    common_proteins = []
    
    for protein1 in proteinList1:
        for protein2 in proteinList2:
            # Check if the proteins are equal
            if protein1 == protein2 and protein1 not in common_proteins:
                common_proteins.append(protein1)
    
    return common_proteins

'''
combineProteins(proteinList)
#2 [Check6-2]
Parameters: 2D list of strs
Returns: list of strs
'''
def combineProteins(proteinList):
    # Initialize an empty list to store the combined amino acids
    combined_amino_acids = []

    # Iterate through each protein in the list
    for protein in proteinList:
        # Iterate through each amino acid in the protein
        for amino_acid in protein:
            combined_amino_acids.append(amino_acid)
    return combined_amino_acids
      
    

'''
aminoAcidDictionary(aaList)
#3 [Check6-2]
Parameters: list of strs
Returns: dict mapping strs to ints
'''
def aminoAcidDictionary(aaList):
    freq_of_aminoAcid={}
    for i in aaList:
        x=aaList.count(i)
        freq_of_aminoAcid[i]=x
    return freq_of_aminoAcid

'''
findAminoAcidDifferences(proteinList1, proteinList2, cutoff)
#4 [Check6-2]
Parameters: 2D list of strs ; 2D list of strs ; float
Returns: 2D list of values
'''
def findAminoAcidDifferences(proteinList1, proteinList2, cutoff):
    diff=[]
    protein1=combineProteins(proteinList1)
    protein2=combineProteins(proteinList2)
    freq1dict=aminoAcidDictionary(protein1)
    freq2dict=aminoAcidDictionary(protein2)
    # print(freq1dict)
    # print(freq2dict)#check y for elemsts not in anyone og lits

    for i in freq1dict:
        if i in freq2dict:
                if i not in diff and i not in ["Start","Stop"]:
                    y=abs(freq1dict[i]/len(protein1)-freq2dict[i]/len(protein2))
                    #x=round(y,3)
                    if y>cutoff:
                        diff.append([i,abs(round(freq1dict[i]/len(protein1),4)),abs(round(freq2dict[i]/len(protein2),4))],)
        else:
            if i not in diff and i not in ["Start","Stop"]:
                freq2dict[i]=0
                y=abs(freq1dict[i]/len(protein1)-freq2dict[i])
                #x=round(y,3)
                if y>cutoff:
                    diff.append([i,0,abs(round(freq2dict[i]/len(protein2),4))])
                    
    for j in freq2dict:
        if j not in diff and j not in ["Start","Stop"] and j not in freq1dict:
            freq1dict[j]=0
            y=abs(freq1dict[j]-freq2dict[j]/len(protein2))
           # x=round(y,3)
            if y>cutoff:
                diff.append([j,0,abs(round(freq2dict[j]/len(protein2),4))])
             
   # print(diff)
    return diff



'''
displayTextResults(commonalities, differences)
#5 [Check6-2]
Parameters: 2D list of strs ; 2D list of values
Returns: None
'''
def displayTextResults(commonalities, differences):
    print("Most common occured proteins ")
    for i in commonalities:
        if i !=["Start","Stop"]:
            print(i)
    print("Most different proteins")
    for j in differences:
        print(j)
    return


    
def runWeek2():
    humanProteins = synthesizeProteins("data/human_p53.txt", "data/codon_table.json")
    elephantProteins = synthesizeProteins("data/elephant_p53.txt", "data/codon_table.json")

    commonalities = commonProteins(humanProteins, elephantProteins)
    differences = findAminoAcidDifferences(humanProteins, elephantProteins, 0.005)
    displayTextResults(commonalities, differences)


### WEEK 3 ###
import numpy

import matplotlib
'''
makeAminoAcidLabels(proteinList1, proteinList2)
#2 [Hw6]
Parameters: 2D list of strs ; 2D list of strs
Returns: list of strs
'''
def makeAminoAcidLabels(proteinList1, proteinList2):

    lable=[]

    for i in proteinList1:
        for j in i:
            if j not in lable:
                lable.append(j)
    
    for i in proteinList2:
        for j in i:
            if j not in lable:
                lable.append(j)

    l=sorted(lable)        

    return l

  

'''
setupChartData(labels, proteinList)
#3 [Hw6]
Parameters: list of strs ; 2D list of strs
Returns: list of floats
'''
def setupChartData(labels, proteinList):

    Freq=[]

    combine=combineProteins(proteinList)
    dict1=aminoAcidDictionary(combine)
    length=0

    for i in proteinList:
        for j in i:
            length+=1

    for i in labels:
        if i in dict1:
            Freq.append(dict1[i]/length)
        else:
            Freq.append(0)

    return Freq

  
'''
createChart(xLabels, freqList1, label1, freqList2, label2, edgeList=None)
#4 [Hw6] & #5 [Hw6]
Parameters: list of strs ; list of floats ; str ; list of floats ; str ; [optional] list of strs
Returns: None
'''
def createChart(xLabels, freqList1, label1, freqList2, label2, edgeList=None,edgecolor="white"):
    import matplotlib.pyplot as plt
    import numpy as np

    w = 0.35  # the width of the bars
    index=np.arange(len(xLabels))
    index1 = index - w/2
    index2 = index + w/2

    if edgeList:
        plt.bar(index1, freqList1, w, label=label1,edgecolor=edgeList,linewidth=1.5)
        plt.bar(index2, freqList2, w, label=label2,edgecolor=edgeList,linewidth=1.5)
    else:
         plt.bar(index1, freqList1, w, label=label1,edgecolor=edgecolor)
         plt.bar(index2, freqList2, w, label=label2,edgecolor=edgecolor)
         



    # plt.bar(index1, freqList1, w, label=label1)
    # plt.bar(index2, freqList2, w, label=label2)

    plt.xticks(rotation="vertical")
    plt.xlabel('Amino Acids')
    plt.ylabel('Frequency')
    plt.xticks(index, xLabels)
    plt.legend()
    

    plt.show()
    return

'''
makeEdgeList(labels, biggestDiffs)
#5 [Hw6]
Parameters: list of strs ; 2D list of values
Returns: list of strs
'''
def makeEdgeList(labels, biggestDiffs):
    colors=[]
    for i in labels:
        for j in biggestDiffs:
            if i==j[0]:
                colors.append("black")
                break
        else:
            colors.append("white")
    #print(colors)
    return colors
    

'''
runFullProgram()
#6 [Hw6]
Parameters: no parameters
Returns: None
'''
def runFullProgram():
    human_proteins = synthesizeProteins("data/human_p53.txt", "data/codon_table.json")
    elephant_proteins = synthesizeProteins("data/elephant_p53.txt", "data/codon_table.json")
    
    # Step 2: Generate Text Report
    common_proteins = commonProteins(human_proteins, elephant_proteins)
    amino_acid_diffs = findAminoAcidDifferences(human_proteins, elephant_proteins, 0.005)
    displayTextResults(common_proteins, amino_acid_diffs)
    
    # Step 3: Create Bar Chart
    labels = makeAminoAcidLabels(human_proteins, elephant_proteins)
    human_data = setupChartData(labels, human_proteins)
    elephant_data = setupChartData(labels, elephant_proteins)
    edge_list = makeEdgeList(labels, amino_acid_diffs)
    createChart(labels, human_data, "Human", elephant_data, "Elephant", edge_list)

    return


### RUN CODE ###

# This code runs the test cases to check your work
if __name__ == "__main__":
    print("\n" + "#"*15 + " WEEK 1 TESTS " +  "#" * 16 + "\n")
    test.week1Tests()
    print("\n" + "#"*15 + " WEEK 1 OUTPUT " + "#" * 15 + "\n")
    runWeek1()

    ## Uncomment these for Week 2 ##
    
    print("\n" + "#"*15 + " WEEK 2 TESTS " +  "#" * 16 + "\n")
    test.week2Tests()
    print("\n" + "#"*15 + " WEEK 2 OUTPUT " + "#" * 15 + "\n")
    runWeek2()
    

    ## Uncomment these for Week 3 ##
    
    print("\n" + "#"*15 + " WEEK 3 TESTS " +  "#" * 16 + "\n")
    test.week3Tests()
    print("\n" + "#"*15 + " WEEK 3 OUTPUT " + "#" * 15 + "\n")
    runFullProgram()
    
