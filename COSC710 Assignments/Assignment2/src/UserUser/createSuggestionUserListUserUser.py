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
    FROM set_local.sbf_comment
    ORDER BY suggestionId, author
""")

results = cursor.fetchall()

with open("commentors_by_suggestion.txt", "w") as f:
    current_id = None
    for suggestionId, author in results:
        if suggestionId != current_id:
            f.write(f"{suggestionId}\n")
            current_id = suggestionId
        f.write(f"{author}\n")

cursor.close()
conn.close()
