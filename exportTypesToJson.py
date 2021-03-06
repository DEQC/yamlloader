# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from yaml import load
import json
import os
import ConfigParser

try:
	from yaml import CSafeLoader as SafeLoader
	print("Using CSafeLoader")
except ImportError:
	from yaml import SafeLoader
	print("Using Python SafeLoader")


fileLocation = os.path.dirname(os.path.realpath(__file__))
inifile=fileLocation+'/config.cfg'
config = ConfigParser.ConfigParser()
config.read(inifile)
sourcePath=config.get('Files','sourcePath')
destinationPath=config.get('Files','destinationPath')


print("opening Yaml")
with open(os.path.join(sourcePath,'fsd','typeIDs.yaml'),'r') as yamlstream:
    print("importing")
    typeids=load(yamlstream,Loader=SafeLoader)
    print("Yaml Processed into memory")
    with open(os.path.join(destinationPath,'typeid.json'),"w") as output:
        json.dump(typeids,output)
