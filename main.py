import subprocess
from colorama import Fore, init
import sys
import readline

# Initialize colorama
init(autoreset=True)

# Banner
BANNER = '''
██████╗ ███████╗██╗   ██╗      ███████╗██╗   ██╗██████╗ 
██╔══██╗██╔════╝██║   ██║      ██╔════╝██║   ██║██╔══██╗
██████╔╝█████╗  ██║   ██║█████╗███████╗██║   ██║██████╔╝
██╔══██╗██╔══╝  ╚██╗ ██╔╝╚════╝╚════██║██║   ██║██╔══██╗
██║  ██║███████╗ ╚████╔╝       ███████║╚██████╔╝██████╔╝
╚═╝  ╚═╝╚══════╝  ╚═══╝        ╚══════╝ ╚═════╝ ╚═════╝ 
 		Greets - DDLR - RemoteExecutio - XSec by SunplaceSolutions
'''

# Greets in light blue
GREETS = Fore.CYAN + "Greets = DDLR - RemoteExecution - XSec - All Security Team's" + Fore.RESET

# Main menu with rainbow-colored options
def main_menu():
    try:
        print(BANNER)
        print(GREETS)
        print()
        
        # Rainbow colors for menu
        colors = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.MAGENTA]
        menu_options = ["1. Reverse IP Lookup", "2. Buscar Subdominios"]
        
        for i, option in enumerate(menu_options):
            color = colors[i % len(colors)]
            print(color + option + Fore.RESET)
        
        choice = input("Ingresa el número de tu elección: ")
        
        if choice == '1':
            # Execute reverse_ip.py
            subprocess.run(["python3", "reverse_ip.py"])
        elif choice == '2':
            # Execute buscar_subdominios.py
            subprocess.run(["python3", "buscar_subdominios.py"])
        else:
            print("Opción no válida.")
    
    except KeyboardInterrupt:
        print("\nScript cancelado por el usuario.")

if __name__ == "__main__":
    main_menu()
