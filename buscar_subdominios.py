import subprocess
import os
import sys  # Importar sys para usar sys.exit
from termcolor import colored

def print_banner():
    banner = '''
    
██████╗ ███████╗███╗   ██╗███████╗██╗      ██████╗ ██████╗ ███████╗
██╔══██╗██╔════╝████╗  ██║██╔════╝██║     ██╔═══██╗██╔══██╗██╔════╝
██████╔╝█████╗  ██╔██╗ ██║█████╗  ██║     ██║   ██║██████╔╝█████╗  
██╔═══╝ ██╔══╝  ██║╚██╗██║██╔══╝  ██║     ██║   ██║██╔═══╝ ██╔══╝  
██║     ███████╗██║ ╚████║███████╗███████╗╚██████╔╝██║     ███████╗
╚═╝     ╚══════╝╚═╝  ╚═══╝╚══════╝╚══════╝ ╚═════╝ ╚═╝     ╚══════╝
                                                                   
            XSec Security Team !!
    '''
    print(banner)

def run_command(command):
    """Ejecuta un comando de shell y captura la salida."""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout.splitlines()
    except Exception as e:
        print(f"Error al ejecutar el comando {command}: {e}")
        sys.exit(1)

def save_to_file(filename, data):
    """Guarda los datos en un archivo sin modificaciones."""
    with open(filename, "w") as f:
        f.write("\n".join(data))

def main(domain):
    print_banner()
    
    # Paso 1: Obtener subdominios con assetfinder
    print(f"[+] Buscando subdominios para: {domain}")
    assetfinder_cmd = f"assetfinder --subs-only {domain}"
    subdomains = run_command(assetfinder_cmd)
    
    # Guardar subdominios sin modificaciones en archivo específico
    subdomain_file = f"{domain}_subdomains.txt"
    save_to_file(subdomain_file, subdomains)
    print(f"[+] Subdominios guardados en {subdomain_file}")

    # Paso 2: Filtrar subdominios válidos con httprobe
    print(f"[+] Filtrando subdominios válidos con httprobe...")
    httprobe_cmd = f"cat {subdomain_file} | httprobe -t 40000"
    valid_subdomains = run_command(httprobe_cmd)
    
    # Guardar subdominios válidos sin modificaciones en archivo específico
    httprobe_file = f"{domain}_httprobe.txt"
    save_to_file(httprobe_file, valid_subdomains)
    print(f"[+] Subdominios válidos guardados en {httprobe_file}")

    # Paso 3: Ejecutar subzy en los subdominios válidos
    print(f"[+] Ejecutando subzy en los subdominios válidos...")
    
    # Leer y ordenar subdominios válidos, eliminando duplicados
    with open(httprobe_file, "r") as f:
        unique_sorted_valid_subdomains = sorted(set(f.read().splitlines()))
    
    # Guardar la lista ordenada y única de subdominios válidos para subzy
    sorted_httprobe_file = f"{domain}_httprobe_sorted.txt"
    save_to_file(sorted_httprobe_file, unique_sorted_valid_subdomains)
    
    # Ejecutar subzy
    subzy_cmd = f"subzy r --targets {sorted_httprobe_file}"
    vulnerable_sites = run_command(subzy_cmd)
    
    # Guardar sitios vulnerables en archivo específico
    vulnerable_file = f"{domain}_vulnerables.txt"
    save_to_file(vulnerable_file, sorted(set(vulnerable_sites)))
    
    if vulnerable_sites:
        print(f"[+] Resultados guardados en {vulnerable_file}")
        print(colored(f"[*] ¡Sitios vulnerables encontrados y guardados en {vulnerable_file}!", "red", attrs=["bold"]))
    else:
        print("[*] No se encontraron sitios vulnerables.")

if __name__ == "__main__":
    try:
        domain = input("Ingrese el dominio a analizar: ")
        main(domain)
    except KeyboardInterrupt:
        print("\nEl script fue interrumpido de manera segura.")
        sys.exit(0)  # Salida limpia sin errores
