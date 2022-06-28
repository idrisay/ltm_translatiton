from dotenv import load_dotenv
import os
import json
import translators as trns
from datetime import datetime
import deepl

from functions import consoleInfo, consoleSuccess, consoleError, replaceSpecChars, returnSpecChars

load_dotenv()
now = datetime.now()

dbColumns = os.getenv("DB_COLUMNS_FOR_TRANSLATE")
fromLang = os.getenv("FROM_LANG")
toLang = os.getenv("TO_LANG")
locale = os.getenv("LOCALE")

## YOU NEED TO UNCOMMENT THIS PART FOR DEEPL TRANSLATE
# deeplTranslator = deepl.Translator(os.getenv("DEEPL_API_KEY"))

dbColumns = dbColumns.split(",")
columnList = list(map(int, dbColumns))

orgContentName = 'originalContent/ltm_translations_' + fromLang + '_'+ toLang + '.json'
with open(orgContentName, "r", encoding="utf-8") as read_file:
    tableContent = json.load(read_file)

## Get the dictionary
dictionary = {}
dictPath = 'dictionaries/dictionary_' + fromLang + '_'+ toLang + '.json'
try:
    with open(dictPath, "r", encoding="utf-8") as read_file:
        dictionary = json.load(read_file)
except:
    with open(dictPath, "w") as outfile:
        outfile.write('{}')

## TRANSLATE
for index, line in enumerate(tableContent, start=0):
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
                    ##########################################################################################
                    consoleError("From Bing Translate...")
                    result = trns.bing(text, from_language=fromLang, to_language=toLang)
                    
                    ##########################################################################################
                 
                    ## YOU NEED TO UNCOMMENT THIS PART FOR DEEPL TRANSLATE
                    # consoleError("From Deep Translate...")
                    # result = deeplTranslator.translate_text(text, source_lang=fromLang, target_lang=toLang)
                    ##########################################################################################
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
resultPath = 'results/ltm_translations_' + fromLang + '_'+ toLang + '.json'
with open(resultPath, "w", encoding="utf-8") as write_file:
    json.dump(
        tableContent,
        write_file,
        ensure_ascii=False,
        indent=4,
        sort_keys=True,
        default=str,
    )

# result = deeplTranslator.translate_text(text, target_lang="ES")