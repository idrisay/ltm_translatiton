from dotenv import load_dotenv
import os
import mysql.connector
import json
load_dotenv()

dbName = os.getenv("DB_NAME")
dbHost = os.getenv("DB_HOST")
dbUser = os.getenv("DB_USER")
dbPassword = os.getenv("DB_PASSWORD")
dbPort = os.getenv("DB_PORT")
dbTableName = os.getenv("DB_TABLE")
# newDbTableName = os.getenv("NEW_DB_TABLE")
dbColumns = os.getenv("DB_COLUMNS_FOR_TRANSLATE")
fromLang = os.getenv("FROM_LANG")
toLang = os.getenv("TO_LANG")

## Get the database table
db = mysql.connector.connect(
    host=dbHost, user=dbUser, password=dbPassword, port=dbPort, database=dbName
)
dbCursor = db.cursor()
dbCursor.execute(f"SELECT * FROM {dbTableName}")
tableContentOrg = dbCursor.fetchall()

# Write the database table to a json file
orgContentName = 'originalContent/ltm_translations_' + fromLang + '_'+ toLang + '.json'
with open(orgContentName, "w", encoding="utf-8") as write_file:
    json.dump(
        tableContentOrg,
        write_file,
        ensure_ascii=False,
        indent=4,
        sort_keys=True,
        default=str,
    )