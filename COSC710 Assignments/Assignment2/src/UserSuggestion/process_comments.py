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
    author_to_index = load_mapping(author_to_index_file)
    suggestion_to_author = load_mapping(suggestions_owner_file)
    unique_suggestions = set()
    with open(commentors_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line.isdigit():
                unique_suggestions.add(line)
    suggestion_indices = {sugg_id: str(index + len(author_to_index) + 1) for index, sugg_id in
                          enumerate(sorted(unique_suggestions))}
    edges = []
    with open(commentors_file, 'r') as f:
        current_suggestion = None
        commenter_counts = defaultdict(int)

        # Generate a distinct set of indices for suggestions to avoid clashes with author IDs


        for line in f:
            line = line.strip()
            # This is a section id
            if line.isdigit():
                if current_suggestion is not None:
                    total_comments = sum(commenter_counts.values())
                    num_commenters = len(commenter_counts)
                    avg_comments = total_comments / num_commenters if num_commenters else 0

                    suggestion_index = suggestion_indices[current_suggestion]
                    # Create edges from commenters to the suggestion
                    for commenter, count in commenter_counts.items():
                        commenter_index = author_to_index.get(commenter)
                        if commenter_index:
                            edges.append((commenter_index, suggestion_index, count))

                    # Create an edge from the suggestion to its author with average comments as weight
                    owner_name = suggestion_to_author.get(current_suggestion)
                    owner_index = author_to_index.get(owner_name)
                    if owner_index:
                        edges.append((suggestion_index, owner_index, avg_comments))

                current_suggestion = line
                commenter_counts.clear()
            else:
                # Parse commenter and comment count, accumulating counts for each commenter
                commenter, count = line.split()
                commenter_counts[commenter] += int(count)

        # Process the last suggestion
        if current_suggestion is not None:
            total_comments = sum(commenter_counts.values())
            num_commenters = len(commenter_counts)
            avg_comments = total_comments / num_commenters if num_commenters else 0

            suggestion_index = suggestion_indices[current_suggestion]

            for commenter, count in commenter_counts.items():
                commenter_index = author_to_index.get(commenter)
                if commenter_index:
                    edges.append((commenter_index, suggestion_index, count))

            owner_name = suggestion_to_author.get(current_suggestion)
            owner_index = author_to_index.get(owner_name)
            if owner_index:
                edges.append((suggestion_index, owner_index, avg_comments))


    #Write the edges to the output file, each edge as source, target, and weight
    with open(output_file, 'w') as f_out:
        for source, target, weight in edges:
            f_out.write(f"{source} {target} {weight}\n")

# Example usage
process_comments('commentors.txt', 'authorToIndex.txt', 'suggestions_owner.txt', 'finalUserSuggestionGraph.txt')
