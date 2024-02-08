#.................................................
#   PROMPT_INPUT_FILE.PY, v2.0.0, January 2024, Domenico Lanza.
#.................................................
#   This project file is needed to check if the
#   default input file provided in the settings file
#   exists, otherwise it will prompt the user to choose
#   another file. After that, the input file name and
#   the output file name will be returned.
#.................................................
def prompt_input_file(settings): #function to prompt the input file
    #.................................................
    #   This function prompts the input file and returns the input and output file names
    #.................................................
    #   INPUTS:
    #   settings: the settings object containing the settings of the program
    #.................................................
    #   OUTPUTS:
    #   input_file_name: the name of the input file
    #   output_file_name: the name of the output file
    #.................................................
    print("Prompting input file...") #we print the message to the user
    #we now initialize the variables that will be returned
    input_file_name=None #name of the input file
    output_file_name=None #name of the output file
    # we first check if the default file exists, otherwise we will prompt the user to choose a file
    default=settings.default_input_file #default name of the input file
    try: #we try to open the file
        f=open(default,"r") 
        f.close()
        input_file_name=default #if the file exists, we save the name of the file in the variable input_file_name
        print("The default file:",default," exists, so it will be used") #we print the message to the user
    except: #if the file does not exist, we prompt the user to choose a file
        print("The default file:",default," does not exist") #we print the message to the user
        print("Please choose an input file(.in)") #we ask the user to choose an input file
        input_file_name=input("Input the file name: ") 
        #we now check if the user provided the extension, otherwise we will add it
        if input_file_name[-3:]!=".in": #if the extension is not .in
            input_file_name=input_file_name+".in" #we add the extension
        #we now check if the input file exists, otherwise we will throw an error
        try:  #we try to open the file
            f=open(input_file_name,"r")
            f.close()
        except: #if the new provided file does not exist
            print("The input file does not exist, the program will end") #we print the message to the user
            exit() #we exit the program
            #in the future we could implement a loop to ask the user to choose another file
        print("The input file will be:",input_file_name) #if the file exits, we use it
    # we now want to save in the variable output_file_name the name of the output file, which is the one of the input file, but with
    # the extension changed to .out from .in
    output_file_name=input_file_name[:-2]+"out" #we change the extension
    print("The output file will be:",output_file_name) #we print the message to the user
    print("Prompting input file...done")
    return input_file_name,output_file_name #we return the input and output file names
#.................................................
#   Possible improvements:
#   - we could implement a loop to ask the user to choose another file if the file does not exist
#   - we could implement a loop to ask the user to choose another file if the file does not have the right extension
#.................................................
# EXECUTION TIME: 6.985664367675781e-05=0 seconds, acceptable.
#.................................................
#   KNOW PROBLEMS:
#   None.
#.................................................