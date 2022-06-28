## LTM Translator


1. Add environment keywords to .env file
```
DB_COLUMNS_FOR_TRANSLATE = column index to translate (5) 
DB_HOST = host credential for db(localhost)
DB_USER = user credential for db(root)
DB_PASSWORD = password for db(root)
DB_PORT = port for db(8889)
DB_NAME = db name to translate
DB_TABLE = db table to translate(ltm_translations)
NEW_DB_TABLE = new db table name to create(result)
FROM_LANG = which lang translate from(de)
TO_LANG = which lang translate from(it)
LOCALE = which rows will be translated(it_IT)(condition)
```

2. Run ```py dbToJson.py``` to get all database table to json file. After run this command  will be created a file 
in ```originalContent```.

3. Run ```py deeplTrns.py``` command to translate all columns you selected before in ```.env``` 
```DB_COLUMNS_FOR_TRANSLATE``` file.

4. Run ```py jaonToDb.py``` command to write the result to database.

Feel free to contact me fot any kind of support about this repo. <a href='mailto:idris@evulpo.com?subject=%5BGitHub%5D%20LTM%20Translator'>Idris Ay</a>