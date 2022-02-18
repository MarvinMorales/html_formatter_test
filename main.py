import os
import json
import sys

jsonFolder = "json_files"
outputFolder = "output"
textEncoding = "utf-8"

json_files_path = f"{os.getcwd()}/{jsonFolder}"
txt_files_path = f"{os.getcwd()}/{outputFolder}"
config_path = f"{os.getcwd()}/configuration.json"

def createFile(template:str, jsonF:str, jsonObj:dict):
    try:
        with open(f"{os.getcwd()}/{template}_header_template.txt", 'r', 
        encoding=textEncoding) as templateText:
            fileData = templateText.read()
            replaced = fileData.replace("|column_name|", jsonF).replace("|question_type|", 
            template).replace("|column_name_cammelCase|", 
            "".join([x for x in jsonF.title().split("_")]))
            optionsFile = open(f"{template}_template.txt", 'r', encoding=textEncoding)
            option = optionsFile.read()
            optionsFile.close()
            with open(f"{os.getcwd()}/{outputFolder}/{jsonF}.txt", "w", 
            encoding=textEncoding) as finalFile:
                finalFile.write(replaced + "\n")
                for index, value in jsonObj.items():
                    finalFile.write(option.replace("|option_name|", 
                    f"{jsonF}_{index}").replace("|value|", 
                    f"{index}").replace("|inner_html|", value) + "\n")
            finalFile.close()
        templateText.close()
    except (OSError, ValueError, IndexError, TypeError) as err: 
        print(f"There was an error: {err}")
        print(f"There was an error: {sys.exc_info()[0]}")

try: 
    jsonFilesList = os.listdir(json_files_path)
    mainFile = open(config_path, 'r', encoding=textEncoding)
    dataRead = mainFile.read()
    mainFile.close()
except OSError as err: print(f"There was an error: {sys.exc_info()[0]}")

for obj in json.loads(dataRead):
    try:
        jsonF = obj['column_name']
        if jsonF != "" and f"{jsonF}.json" in jsonFilesList:
            jsonObj = open(f"{json_files_path}/{jsonF}.json", 'r', encoding=textEncoding)
            dataJson = jsonObj.read()
            jsonObj.close()
            jsonObj = json.loads(dataJson)
            if obj['sort_alphabetically'] == "True": 
                jsonObj = dict(sorted(jsonObj.items(), key = lambda kv:(kv[1], kv[0])))
            createFile(obj['question_type'], jsonF, jsonObj)
    except OSError as err: print(f"There was an error: {err}") 
        
print("Process accomplished!!!")