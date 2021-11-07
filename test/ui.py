# Import the modules needed to run the script.
import sys, os, time

# Main definition - constants
menu_actions  = {}  

# =======================
#     MENUS FUNCTIONS
# =======================

def getAgents():
    #Vasu fix this kthx bye!
    #Select IP, HOSTNAME, LASTCHECKED where lastseen < 5 mins
    #print in format hostname@IP, last see @ LASTCHECKED
    print("This is an agent")

def doCommand(command):
    print("Running command: " + command)
    time.sleep(3)
    main_menu()

# Main menu
def main_menu():
    os.system('clear')
    
    print("Welcome,\n")
    print("Please choose what you want to do:")
    print("1. View agents")
    print("2. Run command against all")
    print("\n0. Quit")
    choice = input(" >>  ")
    exec_menu(choice)

    return

# Execute menu
def exec_menu(choice):
    os.system('clear')
    ch = choice.lower()
    if ch == '':
        menu_actions['main_menu']()
    else:
        try:
            menu_actions[ch]()
        except KeyError:
            print("Invalid selection, please try again.\n")
            menu_actions['main_menu']()
    return

# Menu 1
def menu1():
    print("List of all active agents!\n")
    print("9. Back")
    print("0. Quit")
    print('\n')
    getAgents()
    choice = input(" >>  ")
    exec_menu(choice)
    return


# Menu 2
def menu2():
    print ("Type a command, or return to the main menu!\n")
    print ("9. Back")
    print ("0. Quit" )
    choice = input(" >>  ")
    if(choice != "9" or choice != "0"):
        doCommand(choice)
    else:
        exec_menu(choice)
    return

# Back to main menu
def back():
    menu_actions['main_menu']()

# Exit program
def exit():
    sys.exit()

# =======================
#    MENUS DEFINITIONS
# =======================

# Menu definition
menu_actions = {
    'main_menu': main_menu,
    '1': menu1,
    '2': menu2,
    '9': back,
    '0': exit,
}

# =======================
#      MAIN PROGRAM
# =======================

# Main Program
if __name__ == "__main__":
    # Launch main menu
    main_menu()

