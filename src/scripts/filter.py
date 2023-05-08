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

def checkBool(s):
    if s.lower() == 'true': return True
    elif s.lower() == 'false': return False
    else: return s  

# Load variables
parameters          = dict()
updateLastCommit    = dict()
extra_params        = os.environ.get('EXTRA_PARAMS').replace(" ","")
mapping             = os.environ.get('MAPPING')

try:
    lastCommit      = json.load(open("lastCommit.json"))
except:
    print("Last commit file wasn't found in cache. Creating a new one.\n")
    lastCommit      = dict()

if os.path.exists(mapping):
    with open(mapping) as f:
        mappings    = [ m.split() for m in f.read().splitlines() if m.strip() != "" ]
else:
        mappings    = [ m.split() for m in mapping.splitlines() if m.strip() != "" ]

extra_params        = dict([ map(checkBool,p.split(":")) for p in extra_params.splitlines() if p.strip() != "" ])

for map in mappings:
    # Get mapping parameters
    path, param, value = checkMapping(map)

    # Get current commit from the path
    currentCommit = subprocess.run(['git', 'rev-list', '-1', 'HEAD', '--', path], capture_output=True, text=True).stdout.strip()
    
    print("\n# Checking for changes in the path %s" % path)
    print("Current commit: %s" % currentCommit)
    print("Last commit:    %s" % lastCommit.get(path))

    if currentCommit != lastCommit.get(path):
        print("The current commit differs from the last one. Setting parameter {} to {}.".format(param, value))
        parameters[param] = checkBool(value)            # Set parameter that was mapped to that path
        updateLastCommit[path] = currentCommit          # Update path to the current commit 
    else:
        print("No changes found in %s" % path)
        updateLastCommit[path] = lastCommit.get(path)   # Keep path with the last commit from cache

if (extra_params):
    print("\nSetting extra parameters: %s" % extra_params)
    parameters.update(extra_params)

writeFiles(parameters, "parameters.json")
writeFiles(updateLastCommit, "lastCommit.json")