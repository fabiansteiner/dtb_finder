from analysis.YaraPluginBase import YaraBasePlugin
from typing import List
from helperFunctions.database import ConnectTo
from storage.db_interface_common import MongoInterfaceCommon

import base64
import requests
import json
import pymongo
import subprocess
import os


class AnalysisPlugin(YaraBasePlugin):
    '''
    A Short description
    '''
    NAME = 'dtb_finder'
    DESCRIPTION = 'finds, extracts and saves the Flattended Device Tree into analysis result.'
    DEPENDENCIES = []
    VERSION = '0.1.1'
    FILE = __file__

    debuggingPrints = False

    def __init__(self, plugin_administrator, config=None, recursive=True):
        super().__init__(plugin_administrator, config=config, recursive=recursive, plugin_path=__file__)

    def println(self, text):
        if self.debuggingPrints == True:
            print(text)

    def validateDTB(self, filename, content):
        with open(filename, "wb") as fp:
            fp.write(content)

        process = subprocess.run(['dtc', '-I','dtb','-O','dts','-q',filename], stdout=subprocess.DEVNULL)
        os.remove(filename)

        return process.returncode

    def getFromMongodb(self, _uid):

        dbObject = None
        with ConnectTo(MongoInterfaceCommon, self.config) as connection:
            dbObject = connection.get_object(uid=_uid, analysis_filter=[])

        return dbObject

    def process_object(self, file_object):

        file_object = super().process_object(file_object)
        analysis = file_object.processed_analysis[self.NAME]
        if len(analysis) > 1:
            self.println("Flattened Device Tree found!!")
            analysis['summary'] = list(set({"Flattend Device Tree"}))

            #save device tree binary to file_object
            filebegin = analysis['flattened_device_tree']['strings'][0][0]
            matchingBase64 = analysis['flattened_device_tree']['strings'][0][2]
            filesize = int(str(matchingBase64)[20:22]+str(matchingBase64)[23:25],16)
            dtbFile = file_object.binary[filebegin:filebegin+filesize]
            self.println("Validity of file: "+str(self.validateDTB("validationFile.dtb", dtbFile)))

            #if dtbFile is a valid .dtb File, continue...
            if self.validateDTB("validationFile.dtb", dtbFile) == 0:
                if not file_object.parents: #no parents means its a firmware
                    self.println("IS A FIRMWARE, no parent checking todo!")
                    analysis['dtb'] = dtbFile
                    self.println("Device Tree extracted and saved!"+file_object.file_name)
                    
                else:   #has a parent so it can not be a firmware but a file_object
                    self.println("IS A FILE_OBJECT, process parent checking....")
            
                    #Get Parent
                    parentid = file_object.parents[0]
                    self.println("First Parent = " + parentid)
                    parent = self.getFromMongodb(parentid)
                    parentAnalysis = parent.processed_analysis[self.NAME]

                    #check if parents have a dtb or dtb_reference
                    if "dtb" in parentAnalysis or "dtb_reference" in parentAnalysis:
                        #if parents dtb entry is not empty, check if its the same
                        if "dtb" in parentAnalysis:
                            parentsDtb = parentAnalysis['dtb']
                            if dtbFile == parentsDtb:
                                #if its the same, save the parents _uid in analysis['dtb_reference']
                                analysis['dtb_reference'] = parentid
                                self.println("SAME DTB, SAVED REFERENCE")

                        #if parent has not empty reference:
                        
                        elif "dtb_reference" in parentAnalysis:
                            parentsDtbReference = parentAnalysis['dtb_reference']
                            #get reference object from mongodb
                            referenceObject = self.getFromMongodb(parentsDtbReference)
                            referenceObjectAnalysis = referenceObject.processed_analysis[self.NAME]
                            #check reference objects dtb with own dtb
                            referenceDTB = referenceObjectAnalysis['dtb']
                            if dtbFile == referenceDTB:
                                #if equal: save the same reference
                                analysis['dtb_reference'] = parentsDtbReference
                                self.println("SAME DTB FROM REFERENCE, SAVED REFERENCE")

                    #if parent has a different dtb or a reference to an object with a different dtb, save dtb normaly.
                    else:
                        analysis['dtb'] = dtbFile
                        self.println("Device Tree extracted and saved!"+file_object.file_name)


        return file_object