previousName = None

with open('commentors_by_suggestion.txt', 'r') as file:
    with open('commentors.txt', 'w') as newFile:
        commentorAmount = 0
        currentSuggestion = None

        for line in file:
            line = line.strip()

            # If line is a suggestionId (number)
            if line.isdigit():
                # If switching from a previous suggestion, write the final count
                if previousName is not None:
                    newFile.write(f'{previousName} {commentorAmount}\n')

                currentSuggestion = line
                newFile.write(f'{currentSuggestion}\n')

                previousName = None
                commentorAmount = 0

            else:
                # Author line
                if previousName is None:
                    previousName = line
                    commentorAmount = 1
                elif previousName == line:
                    commentorAmount += 1
                else:
                    newFile.write(f'{previousName} {commentorAmount}\n')
                    previousName = line
                    commentorAmount = 1

        # After the loop ends, write the last author group
        if previousName is not None:
            newFile.write(f'{previousName} {commentorAmount}\n')
