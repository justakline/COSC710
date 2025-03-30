import time
from io import TextIOWrapper
from typing import TextIO


def go():
    with open("finalGraph.txt", 'w') as file:
        commentors = open("commentors.txt")
        suggestionsIdToCommentorName = open("suggestions_owner.txt")
        commentorNameToId = open("authorToIndex.txt")
        previousPostion = 0

        buffer = []
        bufferSize = 1000

        count = 0
        while(True):
            commentorsToWeight:list[tuple[int, int]] =[]
            repeat = True

            ownerId = 0
            line = commentors.readline()

            while(line):

                if(line.strip().isdigit()):
                    if(not repeat):
                        commentors.seek(previousPostion)
                        break
                    ownerId = findOwnerById(int(line), suggestionsIdToCommentorName, commentorNameToId)
                    repeat = False
                else:
                    commentorName, weight = line.strip().split(" ")
                    commentorId = findCommentorIdByName(commentorName, commentorNameToId)
                    commentorsToWeight.append((commentorId, weight))
                    previousPostion = commentors.tell()

                line = commentors.readline()
                if(not line):
                    break
                count += 1

            # Add all of the connections to the file, inbound edges will be the amount comments made in the suggestion
            for i in range(len(commentorsToWeight)):
                for j in range(len(commentorsToWeight)):
                    if(i == j):
                        continue
                    buffer.append(f'{commentorsToWeight[j][0]} {commentorsToWeight[i][0]} {commentorsToWeight[i][1]}'.replace("\n", "")+"\n")
            if (not line):
                break

            # Some of the suggestions were made by people who no longer have an account
            if(not ownerId):
                continue

            # There is an owner still there so give them an inbound edge
            for com in commentorsToWeight:
                buffer.append(f"{com[0]} {ownerId} {len(commentorsToWeight)}".strip()+"\n")

            if(len(buffer) >= bufferSize):
                file.writelines(buffer)
                buffer = []
                print("Reset the buffer " )

            #  Need to process the last couple of nodes... previously we did a readline, so if we hit none then we are at the end
            if(not line):
                break






        commentors.close()
        suggestionsIdToCommentorName.close()
        commentorNameToId.close()

def findCommentorIdByName(name: str, commentorNameToIdFile: TextIO ):
    id = ""
    for line in commentorNameToIdFile:
        if(name in line):
            id = line.split(" ")[1]
            break
    commentorNameToIdFile.seek(0)
    return None if id == "" else id.strip()

def findOwnerById(id:int, suggestionsIdToCommentorNameFile: TextIO, commentorNameToIdFile: TextIO):
    for i in range(id-1):
        suggestionsIdToCommentorNameFile.readline()
    ownerName = suggestionsIdToCommentorNameFile.readline().split(" ")[1]
    suggestionsIdToCommentorNameFile.seek(0)


    return findCommentorIdByName(ownerName, commentorNameToIdFile)


if(__name__ == '__main__'):
    go()