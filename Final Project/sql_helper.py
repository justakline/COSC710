import pymysql

conn = pymysql.connect(
    host='127.0.0.1',
    user='root',
    password='12345',
    db='set_local',
    port=3306
)

cursor = conn.cursor()


# Get the top 500 authors by total vote count, made the mistake earlier of doing by just one suggestion vote count
cursor.execute("""
    select author, sum(abs(votes)) as vote_total
    from sbf_suggestion
    group by author
    order by vote_total desc
    limit 500
""")

results = cursor.fetchall()

top_authors = []
with open("suggestions_owner.txt", "w") as f:
    current_id = None
    for author in results:
        a = author[0].strip().replace("\n", "").replace("\t","")
        top_authors.append(a)
        f.write(f"{a}\n")

# Create a mapping from author to index... the regex i used chat because i ketp getting duplicates, turns out there is a 0-width charachter
cursor.execute(
        """
        SELECT DISTINCT
       LOWER(
         REGEXP_REPLACE(
           author,           -- raw text
           '[[:space:][:cntrl:]]+',  -- any whitespace or control char
           ''
         )
       ) AS author
FROM (
    SELECT author FROM sbf_comment
    UNION ALL
    SELECT author FROM sbf_suggestion
) AS all_authors
ORDER BY author;

        """,
    )
results = cursor.fetchall()

with open("authorToIndex.txt", "w") as f:
    for idx, author in enumerate(results):
        f.write(f"{author[0].strip().replace("\n", "").replace("\t","")} {idx}\n")
print(f"Wrote authorToIndex.txt")

top_indicies = []
with open("authorToIndex.txt", "r") as f:
    for line in f.readlines():
        split_line = line.split()
        author = split_line[0].strip().replace("\n", "").replace("\t", "")
        index = split_line[1].strip().replace("\n", "").replace("\t", "")
        if(author in top_authors):
            top_indicies.append(index)

with open("top_owners_index.txt", "w") as f:
    for i in top_indicies:
        f.write(f"{i}\n")




cursor.close()
conn.close()
