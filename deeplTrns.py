from dotenv import load_dotenv
import os
import mysql.connector
import json
import translators as trns
from datetime import datetime
import deepl


from functions import consoleInfo, consoleSuccess, consoleError, replaceSpecChars, returnSpecChars

load_dotenv()
now = datetime.now()

dbName = os.getenv("DB_NAME")
dbHost = os.getenv("DB_HOST")
dbUser = os.getenv("DB_USER")
dbPassword = os.getenv("DB_PASSWORD")
dbPort = os.getenv("DB_PORT")
dbTableName = os.getenv("DB_TABLE")
newDbTableName = os.getenv("NEW_DB_TABLE")
dbColumns = os.getenv("DB_COLUMNS_FOR_TRANSLATE")
fromLang = os.getenv("FROM_LANG")
toLang = os.getenv("TO_LANG")
locale = os.getenv("LOCALE")

deeplTranslator = deepl.Translator(os.getenv("DEEPL_API_KEY"))

newDbTableName = newDbTableName + now.strftime("%H:%M:%S").replace(":", "_", 1000)
dbColumns = dbColumns.split(",")
columnList = list(map(int, dbColumns))


## Get the database table
# db = mysql.connector.connect(
#     host=dbHost, user=dbUser, password=dbPassword, port=dbPort, database=dbName
# )

newDbTableName = newDbTableName + now.strftime("%H:%M:%S").replace(":", "_", 1000)

# with open("ltm_translations_org.json", "r", encoding="utf-8") as read_file:
orgContentName = 'originalContent/ltm_translations_' + fromLang + '_'+ toLang + '.json'
with open(orgContentName, "r", encoding="utf-8") as read_file:
    tableContent = json.load(read_file)

# dbCursor = db.cursor()
tableColumnNumber = len(tableContent[0])

## Write sql query for insert into new database
# sql = (
#     """INSERT INTO """
#     + newDbTableName
#     + " ("
#     + ", ".join(dbCursor.column_names)
#     + ") VALUES "
#     + "("
#     + "".join(["%s, " for i in range(tableColumnNumber)])
#     + ")"
# ).replace(", )", ")")

## Get the dictionary
dictionary = {}
# with open("dictionary.json", "r", encoding="utf-8") as read_file:
dictPath = 'dictionaries/dictionary_' + fromLang + '_'+ toLang + '.json'
try:
    with open(dictPath, "r", encoding="utf-8") as read_file:
        dictionary = json.load(read_file)
except:
    with open(dictPath, "w") as outfile:
        outfile.write('{}')

## TRANSLATE
for index, line in enumerate(tableContent, start=0):
    # print(
    #     "------------------------------------------------------   ",
    #     'id : ',line[0],' - ', index, '/', len(tableContent),
    #     "   -----------------------------------------------------",
    # )
    for i in columnList:
        if line[2] == locale:
            print("Translating: ", line[0], line[2])
            orgText = str(line[i])
            text = str(line[i])
            text = replaceSpecChars(text)
            result = ""
            if orgText in dictionary:
                consoleInfo("From Dictionary...")
                result = dictionary[orgText]
            else:
                if text.strip():
                    ## Will translate in here
                    consoleError("From Deepl Translate...")
                    result = trns.bing(text, from_language=fromLang, to_language=toLang)
                    # result = deeplTranslator.translate_text(text, target_lang="ES")
                    # result = deeplTranslator.translate_text(text, source_lang=fromLang, target_lang=toLang)
                    result = str(result)
                    result = returnSpecChars(result)
                    dictionary[orgText] = result
                else:
                    result = text
            checkResult = str(i) + " - " + orgText + " - " + result
            consoleSuccess(checkResult)
            tableContent[index][i] = str(returnSpecChars(result))
            with open(dictPath, "w", encoding="utf-8") as write_file:
                json.dump(dictionary, write_file, ensure_ascii=False)


########################
resultPath = 'result/ltm_translations_' + fromLang + '_'+ toLang + '.json'
with open(resultPath, "w", encoding="utf-8") as write_file:
    json.dump(
        tableContent,
        write_file,
        ensure_ascii=False,
        indent=4,
        sort_keys=True,
        default=str,
    )





        