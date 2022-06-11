import os
import platform
import getopt, sys

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
        found.add(os.path.join(root, name))

  if len(found) < 1:
    errorHandler("no browser.html")

  # in some rare instances, there could be more than one file found, so only use the latest version
  return max(found)
# 
def errorHandler(type):
  message = ""

  match type:
    case "bad directory":
      message = "The provided install path is not a valid directory.\n \
        Please enter the install path manually with the INSTALL_PATH variable."
    case "no browser.html":
      message = "The browser.html file was not found under the install path used.\n \
        Consider manually setting the INSTALL_PATH variable with a known good path."
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
      INSTALL_PATH = os.path.expandvars('')
    case "Linux":
      # TODO: Figure out default install directory for Linux
      INSTALL_PATH = os.path.expandvars('')
    case "Windows":
      INSTALL_PATH = os.path.expandvars('%LOCALAPPDATA%\Vivaldi\Application')
    case "Custom":
      INSTALL_PATH = os.path.expandvars(INSTALL_PATH)


  browserHtml = getCurrentVersionPath(INSTALL_PATH)
  VERBOSE and print(browserHtml)