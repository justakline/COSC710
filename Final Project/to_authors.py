


import csv
from collections import defaultdict

def author_to_index_builder():
    indexToAuthor = defaultdict(str)
    with open("authorToIndex.txt", "r") as file:
        for line in file.readlines():
            author = line.split()[0].replace("\n", "").replace("\t", "")
            index = line.split()[1].replace("\n", "").replace("\t", "")
            indexToAuthor[index] = author
    return indexToAuthor

def convert():

    with open("friend_recommendations_top500.csv","r") as file:
        csv_reader = csv.reader(file)
        indexToAuthor = author_to_index_builder()
        with open("friend_recommendations_top500_authors.csv", "w") as out:
            count = 0
            for line in csv_reader:
                if(count == 0):
                    count += 1
                    out.write(",".join(line) + "\n")
                    continue
                a0 = indexToAuthor[line[0].replace("\n", "").replace("\t", "")]
                a1 =indexToAuthor[line[1].replace("\n", "").replace("\t", "")]
                a3 =indexToAuthor[line[3].replace("\n", "").replace("\t", "")]
                a2 =indexToAuthor[line[2].replace("\n", "").replace("\t", "")]
                out.write(f"{a0},{a1},{a2},{a3}\n")

