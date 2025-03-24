import os
import sys
import requests
import socket
import nmap
import colorama
from colorama import Fore, Style
from bs4 import BeautifulSoup

colorama.init()

# Banner
def banner():
    print(Fore.RED + """
    ███╗   ███╗ █████╗ ███████╗████████╗███████╗██████╗     ██╗  ██╗ █████╗  ██████╗██╗  ██╗
    ████╗ ████║██╔══██╗██╔════╝╚══██╔══╝██╔════╝██╔══██╗    ██║  ██║██╔══██╗██╔════╝██║ ██╔╝
    ██╔████╔██║███████║███████╗   ██║   █████╗  ██████╔╝    ███████║███████║██║     █████╔╝ 
    ██║╚██╔╝██║██╔══██║╚════██║   ██║   ██╔══╝  ██╔══██╗    ██╔══██║██╔══██║██║     ██╔═██╗ 
    ██║ ╚═╝ ██║██║  ██║███████║   ██║   ███████╗██║  ██║    ██║  ██║██║  ██║╚██████╗██║  ██╗
    ╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝    ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝
    """ + Style.RESET_ALL)
    print(Fore.CYAN + "Advanced Security Testing Framework\n" + Style.RESET_ALL)

# Website Information Gathering
def website_info(url):
    if not url.startswith("http"):
        url = "https://" + url  # Auto-fix missing schema
    try:
        response = requests.get(url, timeout=5)
        print(Fore.YELLOW + "[+] Website Status Code:", response.status_code)
        print("[+] Server:", response.headers.get("Server"))
        print("[+] Content Type:", response.headers.get("Content-Type"))
    except requests.exceptions.RequestException as e:
        print(Fore.RED + "[-] Error:", e)

# Port Scanner
def port_scanner(target, ports):
    nm = nmap.PortScanner()
    print(Fore.YELLOW + f"Scanning {target} for open ports...")
    for port in ports:
        nm.scan(target, str(port))
        if nm[target].has_tcp(port):
            print(Fore.GREEN + f"[+] Port {port} is open")
        else:
            print(Fore.RED + f"[-] Port {port} is closed")

# Admin Panel Finder (Fixed)
def admin_panel_finder(url):
    if not url.startswith("http"):
        url = "https://" + url  # Auto-fix missing schema

    admin_paths = ["admin", "admin.php", "login.php", "admin/login"]
    print(Fore.YELLOW + "[+] Searching for admin panel...")
    for path in admin_paths:
        test_url = f"{url}/{path}"
        try:
            response = requests.get(test_url, timeout=5)
            if response.status_code == 200:
                print(Fore.GREEN + f"[+] Found Admin Panel: {test_url}")
        except requests.exceptions.RequestException:
            pass  # Ignore errors (timeouts, bad URLs)

# Subdomain Scanner
def subdomain_scanner(domain):
    subdomains = ["www", "mail", "ftp", "blog", "dev"]
    print(Fore.YELLOW + "[+] Scanning for subdomains...")
    for sub in subdomains:
        subdomain = f"{sub}.{domain}"
        try:
            ip = socket.gethostbyname(subdomain)
            print(Fore.GREEN + f"[+] Found Subdomain: {subdomain} -> {ip}")
        except socket.gaierror:
            pass  # Ignore if subdomain doesn't exist

# Main Menu
def menu():
    banner()
    print(Fore.CYAN + "[1] Website Information")
    print("[2] Port Scanner")
    print("[3] Admin Panel Finder")
    print("[4] Subdomain Scanner")
    print("[99] Exit" + Style.RESET_ALL)

    choice = input(Fore.YELLOW + "\nEnter your choice: " + Style.RESET_ALL)

    if choice == "1":
        url = input("Enter website URL: ")
        website_info(url)
    elif choice == "2":
        target = input("Enter target IP/Domain: ")
        ports = [21, 22, 80, 443, 8080]
        port_scanner(target, ports)
    elif choice == "3":
        url = input("Enter website URL: ")
        admin_panel_finder(url)
    elif choice == "4":
        domain = input("Enter domain: ")
        subdomain_scanner(domain)
    elif choice == "99":
        sys.exit()
    else:
        print(Fore.RED + "Invalid choice!" + Style.RESET_ALL)
        menu()

# Run the script
if __name__ == "__main__":
    menu()