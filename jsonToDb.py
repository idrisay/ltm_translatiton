from dotenv import load_dotenv
import os
import mysql.connector
import json

from datetime import datetime
now = datetime.now()

## Get env variables
load_dotenv()
dbName = os.getenv("DB_NAME")
dbHost = os.getenv("DB_HOST")
dbUser = os.getenv("DB_USER")
dbPassword = os.getenv("DB_PASSWORD")
dbPort = os.getenv("DB_PORT")
dbTableName = os.getenv("DB_TABLE")
newDbTableName = os.getenv("NEW_DB_TABLE")
fromLang = os.getenv("FROM_LANG")
toLang = os.getenv("TO_LANG")

newDbTableName = newDbTableName + '_' + now.strftime("%H:%M:%S").replace(":", "_", 1000) + '_' + fromLang + '_' + toLang

db = mysql.connector.connect(
    host=dbHost, user=dbUser, password=dbPassword, port=dbPort, database=dbName
)
resultPath = 'results/ltm_translations_' + fromLang + '_'+ toLang + '.json'
with open(resultPath, "r", encoding="utf-8") as read_file:
    tableContent = json.load(read_file)

dbCursor = db.cursor()
tableColumnNumber = len(tableContent[0])

sql = (
    """INSERT INTO """
    + newDbTableName
    + " ("
    + ", ".join(dbCursor.column_names)
    + ") VALUES "
    + "("
    + "".join(["%s, " for i in range(tableColumnNumber)])
    + ")"
).replace(", )", ")")



dbCursor.execute(f"CREATE TABLE IF NOT EXISTS {newDbTableName} LIKE {dbTableName}")

for index, line in enumerate(tableContent, start=0):
    print(line[0])
    dbCursor.execute(sql, line)

db.commit()