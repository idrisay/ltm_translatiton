def consoleSuccess(text):
    print("\033[92m" + text + "\033[0m")

def consoleInfo(text):
    print("\033[94m" + text + "\033[0m")

def consoleError(text):
    print("\033[91m" + text + "\033[0m")


def replaceSpecChars(text):
    newText = (
        text.replace("«", "<X>", 1000)
        .replace("»", "<X/>", 1000)
        .replace("„", "<Y>", 1000)
        .replace("“", "<Y/>", 1000)
    )
    return newText


def returnSpecChars(text):
    newText = (
        text.replace("<X>", "«", 1000)
        .replace("<X/>", "»", 1000)
        .replace("<Y>", "„", 1000)
        .replace("<Y/>", "“", 1000)
        .replace(" &gt;",">" ,1000 )
        .replace("].","]",1000)
        .replace("& quot;","\"",1000)
        .replace(" & APOs; ","'",1000)
        .replace("&lt; ","<",1000)
        .replace("</ ","</",1000)
    )
    return newText


        # .replace(" & APOs; ","'",1000)
        # .replace(" & APOs; ","'",1000)
        # .replace(" & APOs; ","'",1000)