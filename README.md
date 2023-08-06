# CMSFinder

CMSfinder - Detect Content Management Systems (CMS) and more!

CMSfinder is a Python tool that helps you detect Content Management Systems (CMS) and other known systems like Nginx and Jenkins. It takes a list of domains from a file as input and checks for the presence of known directories (e.g., /wp-content, /umbraco, /phpmyadmin) that indicate the use of specific CMS platforms. If a CMS is detected, the tool will display the name of the CMS used for each domain in the input file.

**Installation**
1. git clone https://github.com/HikmetIskif/CMSFinder
2. cd CMSfinder
3. pip install -r requirements.txt

**Usage**
The default usage is:
>**python3 cmsfinder.py -d (path to domains file)**
This will print the results for both domains using and not using CMS.
To print the results that are using CMS only, use silent mode by adding -s or --silent parameter:
>**python3 cmsfinder.py -d (path to domains file) -s**
>**python3 cmsfinder.py -d (path to domains file) --silent**

- Some websites may return a 200 response for all directories. CMSfinder includes a trial request to check for such cases. However, false negatives are still possible.
- This tool is not foolproof and may not detect every CMS or system accurately.
- Use this tool responsibly and only on domains that you have proper authorization to scan.
