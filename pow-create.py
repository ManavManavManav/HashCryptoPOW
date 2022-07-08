#!/usr/bin/python3 

import sys
import hashlib
from os.path import exists
import time
import itertools

def generateSuffix(initialHash,nbits):
    

    if getLeadingZeroes(initialHash)>=nbits:
        return ["",initialHash,0]

    itCt=0

    for i in range(5000):
        for guess in itertools.product("!#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^`abcdefghijklmnopqrstuvwxyz{|}~", repeat=i):
            if itCt>=1000000000:
                print("REACHED A BILLION")
                return ["",initialHash,1000000000]

            itCt+=1
            guess="".join(guess)
            guess=guess.strip()
            newData=initialHash+guess
            sha=hashlib.sha256(newData.encode()).hexdigest()
            if(getLeadingZeroes(sha)>=nbits):
                return [guess,sha,itCt]



def getLeadingZeroes(hash):
    index=0
    for i in hash:
        if(int(i,16)>0):
            index+=str(format(int(i,16),"04b")).index('1')
            return index
        else:
            index+=4

def initialHashGenerator(file):
    sha256hash = hashlib.sha256()
    with open(file, "rb") as f:
        while True:
            data=f.read(65536)
            if not data:
                break
            sha256hash.update(data)
    return (sha256hash)


def main():
    if(len(sys.argv)!=3):
        print("INVALID ARG COUNT")
        exit()

    nbits = (int)(sys.argv[1])
    if(nbits<0):
        print("Cannot have negative nbits")
        exit()

    file = sys.argv[2]
    if not (exists(file)):
        print("File not found!")
        exit()

    initialHash=initialHashGenerator(file).hexdigest()
    
   

    computeTime=time.time()
    data=generateSuffix(initialHash,nbits)
    computeTime=time.time()-computeTime

    proofOfWork=data[0]
    finalHash=data[1]
    leadingZeroBits=getLeadingZeroes(finalHash)
    iterationCounter=data[2]  
    print("File: ",file)
    print("Initial-hash: ",initialHash)
    print("Proof-of-work: ",proofOfWork)
    print("Hash: ",finalHash)
    print("Leading-zero-bits: ",leadingZeroBits)
    print("Iterations: ",iterationCounter)
    print("Compute-time: ",computeTime)


if(__name__=='__main__'):
    main()


