import json
import subprocess
import os

# Function to write json to files
def writeFiles(value, fileName):
    with open(fileName, 'w') as file:
        file.write(json.dumps(value))

# Check if mapping has all the required parameters
def checkMapping(map):
    if len(map) != 3:
        quit("Invalid mapping. Mapping must be <path> <parameter> <value>")
    return map

# Load variables
try:
    lastCommit      = json.load(open("lastCommit.json"))
except:
    print("Last commit file wasn't found in cache. Creating a new one.\n")
    lastCommit      = dict()

parameters          = dict()
updateLastCommit    = dict()
mapping             = os.environ.get('MAPPING')
mappings            = [ m.split() for m in mapping.splitlines() if m.strip() != "" ]

for map in mappings:
    # Get mapping parameters
    path, param, value = checkMapping(map)

    # Get current commit from the path
    currentCommit = subprocess.run(['git', 'rev-list', '-1', 'HEAD', '--', path], capture_output=True, text=True).stdout.strip()
    
    print("\n# Checking for changes in the path %s" % path)
    print("Current commit: %s" % currentCommit)
    print("Last commit:    %s" % lastCommit.get(path))

    if currentCommit != lastCommit.get(path):
        print("The current commit differs from the last one")
        parameters[param] = json.loads(value)           # Set parameter that was mapped to that path
        updateLastCommit[path] = currentCommit          # Update path to the current commit 
    else:
        print("No changes found in %s" % path)
        updateLastCommit[path] = lastCommit.get(path)   # Keep path with the last commit from cache

writeFiles(parameters, "parameters.json")
writeFiles(updateLastCommit, "lastCommit.json")