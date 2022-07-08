#!/usr/bin/python3 


from email import header
import hashlib
import sys
from os.path import exists
from typing import final


def getLeadingZeroes(hash):
    index = 0
    for i in hash:
        if(int(i, 16) > 0):
            index += str(format(int(i, 16), "04b")).index('1')
            return index
        else:
            index += 4

def main():
    fVerdict = True

    if(len(sys.argv) != 3):
        print("INVALID ARG COUNT")
        exit()

    headerFile = sys.argv[1]
    targetFile = sys.argv[2]
    
    if not exists(headerFile) or not exists(targetFile):
        print("MISSING ONE OF THE ARGUMENT FILES, CHECK INPUT")
        exit()




    headerData = open(headerFile, 'r').read().splitlines()
    targetData = open(targetFile, 'rb').read()

    targetHash = hashlib.sha256(targetData).hexdigest()

    try:
        headerHash = headerData[1][14:]
    except:
        headerHash=hashlib.sha256()
        fVerdict=False

    try:
        proofOfWork = headerData[2][15:]
    except:
        proofOfWork=""
        fVerdict=False

    try:
        finalHash = headerData[3][6:]
    except:
        finalHash=hashlib.sha256()
        fVerdict=False

    try:
        ldZeroes = int(headerData[4][19:])
    except:
        ldZeroes=-1
        fVerdict=False

    

    if(headerHash==""):
        print("ERROR: missing Initial-hash in header")
        fVerdict=False
    elif(headerHash==targetHash):
        print("PASSED: initial file hashes match")
    else:
        print("ERROR: initial hashes don't match")
        print("       hash in header: ",headerHash)
        print("       file hash: ",targetHash)
        fVerdict=False


    expectedHash=hashlib.sha256((targetHash+proofOfWork).encode()).hexdigest()

    if(ldZeroes==-1):
        print("ERROR: missing Leading-zero-bits value in header")
        fVerdict=False
    elif(ldZeroes==getLeadingZeroes(expectedHash)):
        print("PASSED: leading bits is correct")
    else:
        print("ERROR: Leading-zero-bits value:",ldZeroes,"but hash has",getLeadingZeroes(expectedHash),"leading zero bits")
        fVerdict=False


    if(finalHash==""):
        print("ERROR: missing Hash in header")
        fVerdict=False
    elif(finalHash==expectedHash):
        print("PASSED: pow hash matches Hash header")
    else:
        print("ERROR: pow hash does not match Hash header")
        print("       expected: ",expectedHash)
        print("       header has: ",finalHash)
        fVerdict=False


    if(fVerdict):
        print("pass")
    else:
        print("fail")


if(__name__ == '__main__'):
    main()
