import requests
import re
import os
import sys
from packaging import version
from subprocess import call

current_version = "0.1.1"
url = "https://raw.githubusercontent.com/shachar700/ink-scripts/main/py/s3/Leaderboards/util/update_checker.py"

def check_for_updates():
    '''Checks the script version against the repo, reminding users to update if available.'''
    try:
        latest_script = requests.get(url)
        new_version = re.search(r'current_version = "([\d.]*)"', latest_script.text).group(1)
        update_available = version.parse(new_version) > version.parse(current_version)

        if update_available:
            print(f"\nThere is a new version (v{new_version}) available.", end='')

            if os.path.isdir(".git"):
                update_now = input("\nWould you like to update now? [Y/n] ")
                if update_now == "" or update_now[0].lower() == "y":
                    FNULL = open(os.devnull, "w")
                    call(["git", "checkout", "."], stdout=FNULL, stderr=FNULL)
                    call(["git", "checkout", "master"], stdout=FNULL, stderr=FNULL)
                    call(["git", "pull"], stdout=FNULL, stderr=FNULL)
                    print(f"Successfully updated to v{new_version}. Please restart the script.")
                    sys.exit(0)
                else:
                    print("Please update to the latest version by running 'git pull' as soon as possible.\n")
                    sys.exit(0)
            else:
                print("Visit the site below to update:\nhttps://github.com/shachar700/ink-scripts\n")
    except Exception as e:
        print("» Couldn't connect to GitHub. Please update the script manually via `git pull`.\n")
