import time
import json
import sys
from datetime import datetime
import os
os.system("title CameraMan")

Config = {
    'DaysOldTolerated': 7,
    'MonthsOldTolerated': 0,
    'YearsOldTolerated': 0,
    'RefreshRate': 300,
    'CameraDirectories': ["",""],
    'LaunchOptions': [""],
    }






## Launch Options: "skipMenu","runOnce"

CurrentDirectory = ""

InstallPath = os.path.join(os.getenv('programdata'), 'CameraMan')
if not os.path.isdir(InstallPath):
    os.makedirs(InstallPath)

try:
    with open(InstallPath+"/CameraMan.cfg", 'r') as f:
        Config = json.load(f)
except:
    with open(InstallPath+"/CameraMan.cfg", 'w') as f:
        json.dump(Config, f)

def SaveSettings():
    global Config
    with open(InstallPath+"/CameraMan.cfg", 'w') as f:
        json.dump(Config, f)

def LoadSettings():
    global Config
    with open(InstallPath+"/CameraMan.cfg", 'r') as f:
        Config = json.load(f)














def run():
    while True:
        LoadSettings()

        for i in Config["CameraDirectories"]:
            global CurrentDirectory
            CurrentDirectory = i
            clean(os.listdir(i))
        LoadSettings()
        for i in Config["LaunchOptions"]:
            if i == "runOnce":
                sys.exit(0)
        RefreshTime = Config["RefreshRate"]

        print("----------------------------------------------")
        ViewingTime = 10
        for i in range(1,10):
            time.sleep(1)
            print(str(10 - i)+" Seconds Left To View Results.")
        os.system("cls")
        print("Refreshing In: "+str(RefreshTime)+" Seconds.")
        for i in range(1,RefreshTime):
            os.system("cls")
            print(str(RefreshTime - i)+" Seconds Until Next Purge.")
            time.sleep(1)




def getDate():
    year = time.strftime("%Y")
    day = time.strftime("%d")
    month = time.strftime("%m")
    return([year,month,day])
def stringifylist(x):
    str = ""
    for i in x:
        str = str+i
    return str
def clean(listyBoi):
    LoadSettings()
    for i in listyBoi:
        date = getDate()
        year = date[0]
        month = date[1]
        day = date[2]
        i_year = i[:4]
        i_month = i[4:-2]
        i_day = i[6:]

        i_date = [i_year,i_month,i_day]
        delete = False
        reasons = []

        if int(year) - int(i_year) > Config["YearsOldTolerated"]:
            reasons.insert(len(reasons)+1,"Too Old By Years")
            delete = True
        elif int(month) - int(i_month) > Config["MonthsOldTolerated"]:
            reasons.insert(len(reasons)+1,"Too Old By Months")
            delete = True
        elif int(day) - int(i_day) > Config["DaysOldTolerated"]:
            reasons.insert(len(reasons)+1,"Too Old By Days")
            delete = True
        for i in reasons:
            print("[Deleting: ("+stringifylist(i_date)+") because of: ("+i+")")
        if len(reasons) > 0:
            for file in os.listdir(CurrentDirectory+"/"+stringifylist(i_date)):
                os.remove(CurrentDirectory+"/"+stringifylist(i_date)+"/"+file)
            os.rmdir(CurrentDirectory+"/"+stringifylist(i_date))
        else:
            print("Nothing In "+CurrentDirectory+" Matches Deletion Requirements.")


def drawSettingsMenu():
        os.system("cls")
        print("---------------------------------")
        print("\n")
        print("\n")
        print("[1]: RefreshRate")
        print("[2]: DaysOldTolerated")
        print("[3]: MonthsOldTolerated")
        print("[4]: YearsOldTolerated")
        print("[5]: CameraDirectories")
        print("[6]: Return")
        print("\n")
        print("\n")
        print("---------------------------------")
        choice = input(">: ")
        if choice == str(1):
            newValue = input("Enter a new value: ")
            Config["RefreshRate"] = newValue
            SaveSettings()
        elif choice == str(2):
            newValue = input("Enter a new value: ")
            Config["DaysOldTolerated"] = newValue
            SaveSettings()
        elif choice == str(3):
            newValue = input("Enter a new value: ")
            Config["MonthsOldTolerated"] = newValue
            SaveSettings()
        elif choice == str(4):
            newValue = input("Enter a new value: ")
            Config["YearsOldTolerated"] = newValue
            SaveSettings()
        elif choice == str(5):
            print("     ---------------------------------")
            print("     [1]: Add Item To List")
            print("     [2]: Remove Item From List")
            print("     ---------------------------------")
            newValue = input(":> ")
            if newValue == str(1):
                newValue = input("Enter New Directory: ")
                Chars = []
                it = 0
                for i in newValue:
                    it += 1
                    if it > 2:
                        print(i + " > 2")
                        char = i
                        if char == "\\": # Escape the escape character.
                            char = "/"
                        Chars.append(char)
                    else:
                        print(i + " else")
                        Chars.append(i)
                newValue = ""
                for i in Chars:
                    newValue += i
                Config["CameraDirectories"].insert(len(Config["CameraDirectories"])+1,newValue)
            elif newValue == str(2):
                for i in range(len(Config["CameraDirectories"])):
                    print("["+str(i)+"]"+":    "+Config["CameraDirectories"][i])
                newValue = input("Delete #: ")
                Config["CameraDirectories"].remove(Config["CameraDirectories"][int(newValue)])
            SaveSettings()
        elif choice == str(6):
            drawMenu()
        drawSettingsMenu()



def drawMenu():
    os.system("cls")
    print("---------------------------------")
    print("\n")
    print("\n")
    print("[1]: Settings")
    print("[2]: Run")
    print("\n")
    print("\n")
    print("---------------------------------")
    choice = input(":> ")
    errored = False
    try:
        int(choice)
        errored = False
    except ValueError:
        errored = True
        print("ValueError")
    except:
        errored = True
        print("Error")
    if errored != True:
        if int(choice) == 1:
            drawSettingsMenu()
        elif int(choice) == 2:
            run()
        else:
            print("else")
            drawMenu()
    else:
        drawMenu()



LoadSettings()

for i in Config["LaunchOptions"]:
    if i == "skipMenu":
        run()
        break
drawMenu()
