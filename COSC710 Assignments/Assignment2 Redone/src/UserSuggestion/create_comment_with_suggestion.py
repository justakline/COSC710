import pymysql     



conn = pymysql.connect(
    host='127.0.0.1',
    user='root',
    password='12345',
    db='set_local',
    port=3306
)

cursor = conn.cursor()



# 3) Fetch all comments with their suggestion’s author
query = """
SELECT
  c.author       AS commenter,
  s.author       AS sugg_author,
  c.body         AS text
FROM sbf_comment c
JOIN sbf_suggestion s
  ON c.suggestionId = s.suggestionId;
"""
cursor.execute(query)

with open('commenter_author_text.txt', 'w') as f:
     i = 0
     for commenter, sugg_author,text in cursor:
           # Add replacement for '\r' to handle different newline types
          cleaned_commenter = commenter.replace('\r', '').replace('\n', '').replace('\t', '').strip()
          cleaned_sugg_author = sugg_author.replace('\r', '').replace('\n', '').replace('\t', '').strip()
          cleaned_text = text.replace('\r', '').replace('\n', '').replace('\t', '').strip()




          f.write(f"{cleaned_commenter} {cleaned_sugg_author} {cleaned_text}\n")
          
          