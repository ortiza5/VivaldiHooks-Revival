from ast import match_case
import os
import platform
import getopt, sys
import shutil
import re

# The program will try to guess where Vivaldi is installed based on your operating system,
# but you can specify an install path manually
# You can use variables like: "%LOCALAPPDATA%"
INSTALL_PATH = ""
VERBOSE = False

def getCurrentVersionPath(basePath):
  if not os.path.isdir(basePath):
    errorHandler("bad directory")
  
  # Look through all files under the base directory and record the locations of browser.html files
  found = set()
  for root, dirs, files in os.walk(basePath):
    for name in files:
      if name.endswith("browser.html"):
        found.add(root)

  if len(found) < 1:
    errorHandler("no browser.html")

  # in some rare instances, there could be more than one file found, so only use the latest version
  return max(found)

def restoreBundleJsFromBackup(path):
  backupPath = os.path.join(path, "bundle.js.bak")
  dst = os.path.join(path, "bundle.js")

  if not os.path.isfile(backupPath):
    errorHandler("no backup")

  shutil.copy(backupPath, dst)
  os.remove(backupPath)

def backupBundleJs(path):
  bundlePath = os.path.join(path, "bundle.js")
  dst = os.path.join(path, "bundle.js.bak")

  if not os.path.isfile(bundlePath):
    errorHandler("no bundle")

  shutil.copy(bundlePath, dst)

# 
def errorHandler(type):
  message = ""

  match type:
    case "bad directory":
      message = """The provided install path is not a valid directory.
        Please enter the install path manually with the INSTALL_PATH variable."""
    case "no browser.html":
      message = """The browser.html file was not found under the install path used.
        Consider manually setting the INSTALL_PATH variable with a known good path."""
    case "no backup":
      message = "No backup file was found. Make sure bundle.js.bak exists."
    case "no bundle":
      message = "No bundle.js file was found. Make sure bundle.js exists."
    case _:
      message = "Unspecified error..."
  
  raise Exception(message)


if __name__ == '__main__':
  # get any command line arguments
  args = sys.argv[1:]
  shortNames = "vp:"
  longNames = ["Verbose", "InstallPath="]

  try:
    arguments, values = getopt.getopt(args, shortNames, longNames)

    for arg, value in arguments:
      if arg in ("-v", "--Verbose"):
        VERBOSE = True
      if arg in ("-p", "--InstallPath"):
        INSTALL_PATH = value
  except getopt.error as err:
    print(str(err))

  # Get the default install path for different OSs or use the user configured path 
  operatingSystem = "Custom" if INSTALL_PATH else platform.system()

  match operatingSystem:
    case "Darwin":
      # TODO: Figure out default install directory for Macs
      INSTALL_PATH = os.path.expandvars('\Applications\Vivaldi.app\Contents\Versions')
    case "Linux":
      # TODO: Figure out default install directory for Linux
      INSTALL_PATH = os.path.expandvars('')
    case "Windows":
      INSTALL_PATH = os.path.expandvars('%LOCALAPPDATA%\Vivaldi\Application')
    case "Custom":
      INSTALL_PATH = os.path.expandvars(INSTALL_PATH)

  # find the location that contains the latest bundle.js file
  currentPath = getCurrentVersionPath(INSTALL_PATH)
  if not os.path.isdir(currentPath):
    errorHandler("no browser.html")

  # prompt the user for actions to take if a backup bundle.js is found
  choice = ""
  if os.path.isfile(os.path.join(currentPath, "bundle.js.bak")):
    while True:
      choice = input(re.sub('^\s+', '', """Choose an option and enter the corresponding number:
      - (1) [Recommended] Restore bundle.js from the backup and CONTINUE
      - (2) Restore bundle.js from the backup and EXIT
      - (3) Delete the backup and create a new one before CONTINUING
      Choice: """, flags=re.MULTILINE))
      if choice in ["1", "2", "3"]:
        break
      print("Invalid choice, please only input 1, 2, or 3")

  match choice:
    case "1":
      restoreBundleJsFromBackup(currentPath)
      backupBundleJs(currentPath)
    case "2":
      restoreBundleJsFromBackup(currentPath)
      exit()
    case _:
      backupBundleJs(currentPath)