from collections import defaultdict

# Load mappings from file
def load_mapping(filename):
    mapping = {}
    with open(filename, 'r') as f:
        for line in f:
            parts = line.strip().split()
            mapping[parts[0]] = parts[1]
    return mapping


# Main function to process comments and create graph edges
def process_comments(commentors_file, author_to_index_file, suggestions_owner_file, output_file):

    # {"myAuthor": 0, "nextAuthor": 1}
    author_to_index = load_mapping(author_to_index_file)

    # {1 : "broAuthor", 2: "otherAuthor"}
    suggestion_to_author = load_mapping(suggestions_owner_file)

    total_suggestions = len(suggestion_to_author)

    user_user_count: defaultdict = defaultdict(int)



    with open(commentors_file, 'r') as f:
        current_suggestion = None

        for i, line in enumerate(f):
            line = line.strip()

            if line.isdigit():
                current_suggestion = int(line)
                continue
            if current_suggestion is not None:
                owner_name = suggestion_to_author.get(str(current_suggestion))
                owner_index = author_to_index.get(owner_name)
                # if(i > 100): break

                # print(f"{owner_name=} {owner_index=}")
                split_line = line.split(" ")
                commenter_name = split_line[0]
                commenter_index = author_to_index.get(commenter_name)
                # if(i > 10): break
                if owner_index is None or commenter_index is None:
                    continue

                owner_index = int(owner_index)
                commenter_index = int(commenter_index)
                number_of_comments = int(split_line[1])

                # Ensure ordering
                user_user = tuple(sorted([owner_index, commenter_index]))

                user_user_count[user_user] += number_of_comments

        # Process the last suggestion
        if current_suggestion is not None:
            owner_name = suggestion_to_author.get(str(current_suggestion))
            owner_index = author_to_index.get(owner_name)

            split_line = line.split(" ")
            commenter_name = split_line[0]
            commenter_index = author_to_index.get(commenter_name)

            if owner_index is not None and  commenter_index is not None:
                owner_index = int(owner_index)
                commenter_index = int(commenter_index)
                number_of_comments = int(split_line[1])

                # Ensure ordering
                user_user = tuple(sorted([owner_index, commenter_index]))

                user_user_count[user_user] += number_of_comments


    #Write the edges to the output file, each edge as source, target, and weight/total number of suggestions
    # The new weight will give
    maxx = 0
    minn = float('inf')
    with open(output_file, 'w') as f_out:
        scale_factor = 10**5
        min_value = 0.857
        for (user1, user2), weight in user_user_count.items():
            # print(f"{user1} {user2} {weight}\n")
            new_weight = round(round(weight/total_suggestions * scale_factor, 3)/min_value, 3)
            f_out.write(f"{user1} {user2} {new_weight}\n")
            maxx = max(maxx,new_weight )
            minn = min(minn, new_weight)

    print(f"{maxx=}")
    print(f"{minn=}")

# Example usage
process_comments('commentors.txt', 'authorToIndex.txt', 'suggestions_owner.txt', 'finalUserUserGraph.txt')
print("Done")