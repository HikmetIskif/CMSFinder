import requests
import argparse
import random
import string
from concurrent.futures import ThreadPoolExecutor, as_completed

def trialResponse(domain):
    trialUrl = f"{domain}/{generateRandomString()}"
    try:
        response = requests.get(trialUrl, allow_redirects=True, timeout=5)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def generateRandomString(length=10):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def detectCms(domain):
    if trialResponse(domain):
        return []

    cmsList = {
        "wordpress": ["/wp-content/", "/wp-admin/"],
        "jenkins": ["/jenkins/login", "/jenkins/script"],
        "joomla": ["/administrator/"],
        "umbraco": ["/umbraco/", "/umbraco/backoffice"],
        "nginx": ["/nginx-status"],
        "phpmyadmin": ["/phpmyadmin/"],
        "ghost": ["/ghost/"],
        "mediawiki": ["/wiki/"],
        "modx": ["/manager/"],
        "drupal": ["/sites/default/"],
        "magento": ["/app/etc/"],
        "prestashop": ["/admin-dev/"]
    }

    detectedCms = []
    futures = []
    with ThreadPoolExecutor() as executor:
        for cms, directories in cmsList.items():
            for directory in directories:
                url = f"{domain}{directory}"
                future = executor.submit(requests.get, url, allow_redirects=True, timeout=5)
                futures.append((future, cms))

    for future, cms in futures:
        try:
            response = future.result()
            if response.status_code == 200:
                detectedCms.append(cms)
                break
        except requests.exceptions.RequestException:
            pass

    return detectedCms

def printHeader():
    header = r"""
 ██████╗███╗   ███╗███████╗███████╗██╗███╗   ██╗██████╗ ███████╗██████╗ 
██╔════╝████╗ ████║██╔════╝██╔════╝██║████╗  ██║██╔══██╗██╔════╝██╔══██╗
██║     ██╔████╔██║███████╗█████╗  ██║██╔██╗ ██║██║  ██║█████╗  ██████╔╝
██║     ██║╚██╔╝██║╚════██║██╔══╝  ██║██║╚██╗██║██║  ██║██╔══╝  ██╔══██╗
╚██████╗██║ ╚═╝ ██║███████║██║     ██║██║ ╚████║██████╔╝███████╗██║  ██║
 ╚═════╝╚═╝     ╚═╝╚══════╝╚═╝     ╚═╝╚═╝  ╚═══╝╚═════╝ ╚══════╝╚═╝  ╚═╝
                                                                        
                                            
 Detect Content Management Systems (CMS) and more!
"""

    print(header)

def main():
    parser = argparse.ArgumentParser(description="Detect CMS of domains.")
    parser.add_argument("-d", "--domains-file", required=True, help="Path to the file containing domains.")
    parser.add_argument("-s", "--silent", action="store_true", help="Only print sites with detected CMS.")
    args = parser.parse_args()

    printHeader()

    with open(args.domains_file, "r") as file:
        domains = file.read().splitlines()

    with ThreadPoolExecutor() as executor:
        cmsResults = {executor.submit(detectCms, domain): domain for domain in domains}

        for future in as_completed(cmsResults):
            domain = cmsResults[future]
            cmsList = future.result()
            if cmsList:
                if args.silent:
                    print(f"{domain} is using: {', '.join(cmsList)}")
                else:
                    print(f"{domain} is using: {', '.join(cmsList)}")
            elif not args.silent:
                print(f"{domain} is not using a known CMS.")

if __name__ == "__main__":
    main()
