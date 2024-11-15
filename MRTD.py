

#BEFORE
#FIRST REQUIREMENT
def scanMRZ(input):
    #THIS DOES STUFF WITH HARDWARE, FOR NOW IGNORE
    inputRETURN = input.replace("<","")
    return inputRETURN


#AFTER
def scanMRZMUT(input):
    #THIS DOES STUFF WITH HARDWARE, FOR NOW IGNORE
    inputRETURN = input.replace("<",",")
    final = ""
    for a in input:
        if (a.isdigit()) or  a != " " or (a.isalpha()):
            final += a
    if(final == inputRETURN):
        return final
    elif(final == input.replace("<",",")):
        return final
    elif((inputRETURN == input.replace("<",","))):
        return

def checkInput(input):
    if(len(input) == len("P<UTOERIKSSON<<ANNA<MARIA<<<<<<<<<<<<<< L898902C36UT07408122F1204159ZE184226B<<<<<<1")):
        return "Good"
    elif (len(input) < len("P<UTOERIKSSON<<ANNA<MARIA<<<<<<<<<<<<<< L898902C36UT07408122F1204159ZE184226B<<<<<<1")):
        return "INVALID SCAN: NOT ENOUGH CHARACTERS"
    elif (len(input) > len("P<UTOERIKSSON<<ANNA<MARIA<<<<<<<<<<<<<< L898902C36UT07408122F1204159ZE184226B<<<<<<1")):
        return "INVALID SCAN: TOO MANY CHARACTERS"

def checkValues(input):
    for value in input:
        if not(value.isdigit()) and value != " " and not(value.isalpha()):
            return "INVALID SCAN: INVALID CHARACTERS"
    return "Works Out"

#Before
#THIS GETS THE SECOND LINE
def getSecond(input):
    list = input.split(" ")
    stringOne = list[0]
    stringTwo = list[1]
    return stringTwo

#After
def getSecondMut(input):
    list = input.split(" ")
    stringOne = 0
    stringTwo = list[1]
    if stringTwo in input:

        return stringTwo
    else:
        return input.split(" ")[0]

#SECOND REQUIREMENT

#THIS FINDS THE SECURITY DIGITS
def getDigits(input):
    #print(input)
    #print([input[9], input[19], input[27],input[37]])
    return [input[9], input[19], input[27],input[37]]







#THIRD REQUIREMENT

#THIS IS A MOCK FOR THE DATABASE. RIGHT NOW, IT ONLY CHECKS IF ABRAHAM LINCOLN IS TRYING TO GET PAST SECURITY.
def databaseRequest(input, DEBUGGING_MODE):
    if(DEBUGGING_MODE):
        return "Good, Return Original"
    else:

        if(input[4:22] == "LINCOLNABRAHAM"):
            return "THIS IS A FAKE ID, REPORT IT IMMEDIATELY"
        else:
            return "Good, Return Original"

#THIS GETS THE INFORMATION READY FOR THE DATABASE
def getDatabase(input, SERVERCONNECTION):
    list = input.split(" ")
    stringOne = list[0]
    stringTwo = list[1]
    dataFound = databaseRequest(stringOne, SERVERCONNECTION)
    if(dataFound == "Good, Return Original"):
        return stringTwo
    else:
        return dataFound
    return input

#Before
#THIS GETS THE MOD VALUE
def getMod(input):
    return input % 10

#THIS GETS THE MOD VALUE
#After
def getModMut(input):
    modONE = input % 10
    modTWO = input % 10
    modTHREE = input % 10
    if (modONE == modTWO):
        return modONE
    elif(modONE == modTHREE):
        return modONE
    elif(modTWO == modTHREE):
        return modTWO

#THIS IS THE FLETCHER16 CODE
def fletcher16(data):
    #code inspired by https://ozeki.hu/p_1613-fletcher-16-checksum-generator.html
    sum1 = 0xff
    sum2 = 0xff
    x = data.find("&s=")
    bytes_remaining = x if x != -1 else len(data)
    i = 0
    while bytes_remaining:
        tlen = min(20, bytes_remaining)
        bytes_remaining -= tlen
        while tlen:
            sum1 = (sum1 + ord(data[i])) & 0xffff
            sum2 = (sum2 + sum1) & 0xffff
            i += 1
            tlen -= 1
        sum1 = (sum1 & 0xff) + (sum1 >> 8)
        sum2 = (sum2 & 0xff) + (sum2 >> 8)
    sum1 = (sum1 & 0xff) + (sum1 >> 8)
    sum2 = (sum2 & 0xff) + (sum2 >> 8)
    checksum = (sum2 << 8) | sum1
    return checksum


#THIS SPLITS THE STRING INTO IT'S NON SECURITY NUMBER PARTS
def splitTheString(input):
    return [input[0:9], input[13:19], input[21:27], input[28:len(input) - 1]]





#FOURTH REQUIREMENT

def securityCheck(codeGiven, codeGenerated, listGiven, listGenerated):
    messageToReturn = ""

    for a in range(len(codeGiven)):
        if(int(codeGiven[a]) != int(codeGenerated[a])):
            if(a == 0):
                messageToReturn += "Passport Number SECURITY NUMBER FAILED: Expected: " + str(codeGenerated[a]) + " Received: " + str(codeGiven[a]) + "\n"
            elif(a==1):
                messageToReturn += "DATE OF BIRTH SECURITY NUMBER FAILED: Expected: " + str(codeGenerated[a]) + " Received: " + str(codeGiven[a]) + "\n"
            elif(a==2):
                messageToReturn += "EXPIRATION DATE SECURITY NUMBER FAILED: Expected: " + str(codeGenerated[a]) + " Received: " + str(codeGiven[a]) + "\n"
            elif(a==3):
                messageToReturn += "PERSONAL NUMBER SECURITY NUMBER FAILED: Expected: " + str(codeGenerated[a]) + " Received: " + str(codeGiven[a]) + "\n"

    for a in range(len(listGiven)):
        if((listGiven[a]) != (listGenerated[a])):
            if(a == 0):
                messageToReturn += "Passport Number FIELD FAILED: Expected: " + str(listGenerated[a]) + " Received: " + str(listGiven[a]) + "\n"
            elif(a==1):
                messageToReturn += "DATE OF BIRTH FIELD FAILED: Expected: " + str(listGenerated[a]) + " Received: " + str(listGiven[a]) + "\n"
            elif(a==2):
                messageToReturn += "EXPIRATION DATE FIELD FAILED: Expected: " + str(listGenerated[a]) + " Received: " + str(listGiven[a]) + "\n"
            elif(a==3):
                messageToReturn += "PERSONAL NUMBER FIELD FAILED: Expected: " + str(listGenerated[a]) + " Received: " + str(listGiven[a]) + "\n"

    if(len(messageToReturn) == 0):
        messageToReturn = "Record came up clean"
    return messageToReturn


#THIS PUTS IT ALL TOGETHER
def FULLSYSTEM(input, SERVERCONNECTION):
    lenCheck = checkInput(input)
    if(lenCheck != "Good"):
        return lenCheck

    scanned = scanMRZ(input)
    #print(scanned)
    validCharCheck = checkValues(scanned)
    if(validCharCheck ==  "INVALID SCAN: INVALID CHARACTERS"):
        return "INVALID SCAN: INVALID CHARACTERS"


    secondString = getSecond(scanned)
    digits = getDigits(secondString)
    database = getDatabase(scanned, SERVERCONNECTION)
    if(database == "THIS IS A FAKE ID, REPORT IT IMMEDIATELY"):
        return "THIS IS A FAKE ID, REPORT IT IMMEDIATELY"
    stringSplitted = splitTheString(database)
    originalStringSplitted = splitTheString(secondString)
    #print(stringSplitted)
    securityNumsFound = []
    for a in stringSplitted:
        checksum = fletcher16(a)

        checksumFinal = getMod(checksum)

        securityNumsFound.append(checksumFinal)
    #print(securityNumsFound)
    finalSecurity = securityCheck(digits, securityNumsFound, originalStringSplitted, stringSplitted)
    return finalSecurity

"""
print(FULLSYSTEM("P<UTOERIKSSON<<ANNA<MARIA<<<<<<<<<<<<<< L898902C36UT07408122F1204159ZE184226B<<<<<<1", True))
print(FULLSYSTEM("P<UTOERIKSSON<<ANNA<MARIA<<<<<<<<<<<<<< L898902C32UT07408123F1204154ZE184226B<<<<<<6", False))
print(FULLSYSTEM("P<USALINCOLN<<ABRAHAM<<<<<<<<<<<<<< L898902C32UT07408123F1204154ZE184226B<<<<<<6", False))
"""
