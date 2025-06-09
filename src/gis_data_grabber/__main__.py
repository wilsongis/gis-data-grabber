from .downloader import RESTDownloader

def mainMenu() -> bool:
    """Displays Main Menu and prompts for choice.

    Returns:
        bool: True if user needs to run again, False if not.
    """    
    print("1. CMD Line Mode\n2. File Source Mode\n Enter Q or q to quit.")
    myinput = input()
    if myinput=='1':
        return runCmdLineMode()
    elif myinput =='2':
        # TODO: upgrade this to show a basic file browser window.
        filename = input("Input location of file containing list of services")
        return runFilesourceMode(filename)
    elif myinput == 'Q' or myinput == 'q':
        print("Quitting... ")
        return False
    else:
        print ("Could not understand. Please choose from the menu options.")
        return True

def rerunProgramPrompt() -> bool:
    """Basic prompt, asks users if they want to re-run the program and checks their input

    Returns:
        bool: True if they want to run again, elif False
    """    

    userinput = input("Do you want to run REST Downloader again? (Enter Y to rerun)")

    if userinput == "Y" or userinput == "y":
        return True
    else:
        return False

def runFilesourceMode(filename) -> bool:
    """Looks at filename and attempts to download each listed service.

    Args:
        filename (string): A full file path to a json file that contains a list
        of services to be downloaded.
    
    Returns:
        bool: True if user needs to run again, False if not.
    """

    # estimate progress, create progress bar
    # Run through each service.
    #    If a service fails to download, ask user if they want to try again or skip?
    # Output final report?
    
def runCmdLineMode() -> bool:
    """Prompts user for REST URL, File Geodatabase Location, and Feature Class Name

    Returns:
        bool: True if user needs to run again, False if not.
    """    
    url = input("Please enter the full URL of the REST service you want to download: ")
    path = input("Please enter the full path of the file geodatabase (ending with .gdb): ")
    filename = input("Please enter name to save dataset as: ")

    RESTDownloader(url, path+"/"+filename,verbose=True)

    print (f"""Finished downloading service at {url}\nAt location {path} with name {filename}.""")
    return rerunProgramPrompt()

def main():
    print("Welcome to the REST Service Downloader")
    continueyn = True
    while continueyn == True:
        continueyn = mainMenu()
    quit()

if __name__ == "__main__":
    main()
