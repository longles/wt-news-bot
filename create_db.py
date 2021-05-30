import sqlite3

# Create DB
db = sqlite3.connect('wt_news.db')
cursor = db.cursor()

# Format DB
cursor.execute('CREATE TABLE "warthunder" ("hash" TEXT)')
cursor.commit()