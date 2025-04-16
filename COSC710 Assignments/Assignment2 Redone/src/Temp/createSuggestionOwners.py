import pymysql

conn = pymysql.connect(
    host='127.0.0.1',
    user='root',
    password='12345',
    db='set_local',
    port=3306
)

cursor = conn.cursor()
cursor.execute("""
    SELECT suggestionId, author
    FROM set_local.sbf_suggestion
    ORDER BY suggestionId, author
""")

results = cursor.fetchall()

with open("suggestions_owner.txt", "w") as f:
    current_id = None
    for suggestionId, author in results:
        f.write(f"{suggestionId} {author.strip()}\n")

cursor.close()
conn.close()
