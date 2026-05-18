# -*- coding: utf-8 -*-
__author__ = 'Manifest Creator by ONS TDZ Technical Architects'

# IMPORTS
import hashlib
import json
import os
import datetime
import argparse
import sys
import getopt
import re

#
# FUNCTIONS
#
def GetDataSetFiles(path):
    listFiles = []
    if (os.path.isdir(path)) :
        for root, dirs, files in os.walk(path):
            for name in files:
                listFiles.append(os.path.join(root, name))

    else :
        listFiles.append(path)
    return listFiles

def getFileInfo(datasetFile):
    dictFilesHash = {}
    datasetFileMd5 = hashlib.md5(open(datasetFile, 'rb').read()).hexdigest()
    datasetFilePath = os.path.dirname(os.path.relpath(datasetFile))
    datasetFileSize = os.path.getsize(datasetFile)

    # TODO: Verify trailing colons :thinking_face:
    dictFilesHash['relativePath:'] = datasetFilePath
    dictFilesHash['name:'] = os.path.split(datasetFile)[1]
    dictFilesHash['md5sum:'] = datasetFileMd5
    dictFilesHash['sizeBytes:'] = datasetFileSize
    return dictFilesHash

def GetFileDetails(path):
    listFilesList = []

    # TODO: assigned but never used
    filesCount = 0
    datasetFiles = GetDataSetFiles(path)

    for datasetFile in datasetFiles:
        listFilesList.append(getFileInfo(datasetFile))

    return listFilesList

def isotime():
    # 2012-04-23T18:25:43.511Z
    # TODO: assigned and overwritten
    isonow = ''
    isonow = datetime.datetime.now()
    if isonow.utcoffset() is None :
        return isonow.isoformat()+"+00:00"
    else:
        return isonow.isoformat()

# MAIN MANIFEST GENERATION FUNCTION
def GenerateManifest(path, sourceName, description, version, dataset, sensitivity,iterationl1, iterationl2, iterationl3, iterationl4,schemaVersion, output_path='folder.mani'):
    """
        Generates a folder.mani JSON manifest file describing a dataset.
        Output shape::
            {
                "files": [
                    {
                        "relativePath:": "...",  # NOTE: trailing colons in keys are intentional (see TODO)
                        "name:": "...",
                        "md5sum:": "...",
                        "sizeBytes:": 123
                    }
                ],
                "schemaVersion": 1,
                "sourceName": "...",
                "description": "...",
                "manifestCreated": "2024-01-01T00:00:00+00:00",
                "dataset": "...",
                "version": 1,
                "sensitivity": "low|medium|high",
                "iterationL1": "",
                "iterationL2": "",
                "iterationL3": "",
                "iterationL4": "",
                "fullSizeMegabytes": "0.000001"  # NOTE: string, not float
            }
        """

    # TODO: assigned and overwritten
    listFilesList = []
    listFilesList = GetFileDetails(path)

    maniData = {}
    maniData['files'] = listFilesList

    totalSize=(sum(item['sizeBytes:'] for item in listFilesList))/1000000.0
    totalSize="%0.6f" % totalSize

    if (iterationl1 is None) :
        iterationl1=""
    if (iterationl2 is None) :
        iterationl2=""
    if (iterationl3 is None) :
        iterationl3=""
    if (iterationl4 is None) :
        iterationl4=""

    version=int(version)

    maniData.update({
        'schemaVersion':schemaVersion,
        'sourceName':sourceName,
        'description':description,
        'manifestCreated':isotime(),
        'dataset':dataset,
        'version':version,
        'sensitivity': sensitivity,
        'iterationL1': iterationl1,
        'iterationL2': iterationl2,
        'iterationL3': iterationl3,
        'iterationL4': iterationl4,
        'fullSizeMegabytes': totalSize
    })

    with open(output_path, 'w') as maniFile:
        json.dump(maniData, maniFile)

def validate(allargs):
    isValid=True
    #path file or dir exists
    if (not(os.path.exists(allargs.path))) :
        print("Dataset Path not found")
        isValid=False

    #dataset,iterationl1,2 & 3 valid characters
    validChars=re.compile("^[a-z0-9_]*$")

    # TODO: Extract to appropriately-named methods
    if (not(validChars.match(allargs.dataset))) :
        print("dataset name can only contain a-z 0-9 and _")
        isValid=False

    # TODO: Is this a bug? Was the desired intent to return False if "iteration1 did not contain only a-z 0-9 and _"?
    ## hasattr(allargs, "iterationl1") always returns True because the attribute exists on the Namespace object,
    ## even when its value is invalid. The 'or' short-circuits, so validChars.match() is never reached.
    if (not(hasattr(allargs,"iterationl1") or validChars.match(allargs.iterationl1) )) :
        # or validChars.match(allargs.iterationl1))) :
        print("iteration1 can only contain a-z 0-9 and _")
        isValid=False

    if (not(hasattr(allargs,"iterationl2") or validChars.match(allargs.iterationl2) )) :
        print("iterationl2 can only contain a-z 0-9 and _")
        isValid=False

    if (not(hasattr(allargs,"iterationl3") or validChars.match(allargs.iterationl3) )) :
        print("iterationl3 can only contain a-z 0-9 and _")
        isValid=False

    if (not(hasattr(allargs,"iterationl4") or validChars.match(allargs.iterationl4) )) :
        print("iterationl3 can only contain a-z 0-9 and _")
        isValid=False

    #version = integer
    try :
        version=int(allargs.version)
    except :
        version=0

    if (not (version >0 and version <100 )) :
        print("Version must be an integer 1-99")
        isValid=False

    #sensitivity = low/medium/high
    validsens=set(['low','medium','high'])
    if (not (allargs.sensitivity.lower() in validsens)):
        print("Sensitivity must be low, medium or high")
        isValid=False

    return isValid

#
# MAIN
#
#GenerateManifest (sys.argv[2],sys.argv[4],sys.argv[6],sys.argv[8],sys.argv[9])

if __name__ == "__main__":
    # SCRIPT HELP
    parser = argparse.ArgumentParser(description=__author__)
    parser.add_argument('-p', '--path', help='Dataset folder path', required=True)  # 1
    parser.add_argument('-o', '--sourceName', help='Source name', required=True)  # 2
    parser.add_argument('-d', '--description', help='Dataset description', required=True)  # 3
    parser.add_argument('-v', '--version', help='Dataset version', required=True)  # 4
    parser.add_argument('-n', '--dataset', help='Dataset name', required=True)  # 5
    parser.add_argument('-s', '--sensitivity', help='Sensitivity', required=True)  # 6
    parser.add_argument('-l', '--iterationl1', help='Iteration 1', required=False)  # 7
    parser.add_argument('-m', '--iterationl2', help='Iteration 2', required=False)  # 8
    parser.add_argument('-i', '--iterationl3', help='Iteration 3', required=False)  # 9
    parser.add_argument('-j', '--iterationl4', help='Iteration 4', required=False)  # 10
    args = parser.parse_args()

    schemaVersion = 1

    if validate(args) :
        GenerateManifest (
            args.path,
            args.sourceName,
            args.description,
            args.version,
            args.dataset,
            args.sensitivity,
            args.iterationl1,
            args.iterationl2,
            args.iterationl3,
            args.iterationl4,
            schemaVersion
        )