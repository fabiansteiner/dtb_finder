import base64
import requests
import json



firmware_uuid="3a86dc3c40fc0f1818df36e0c82bd96ab0b58941a1ae94457567108cba5be457_32135"



def dump_file(filename, content):
    with open(filename, "wb") as fp:
        fp.write(content)
    print('File found, saving '+filename)

#Query for getting all files with detected Device trees within a specific firmware
query='query={"$and":[{ "parent_firmware_uids": { "$all": ["'+firmware_uuid+'"]} },{"processed_analysis.dtb_finder.dtb":{"$exists":true} }]}'
#print('My Query: '+query+'\n\n')

#Request all affected object_files with the upper query
request_url = 'http://localhost:5000/rest/file_object'
res = requests.get(request_url, params=query).json()
#print('Result: '+str(res)+'\n\n')

#dump <object_file._uid>.dtb in current location, if it exists
for item in res["uids"]:
	bin_request_url = 'http://localhost:5000/rest/file_object/'+str(item)
	result = requests.get(bin_request_url).json()
	file_path = str(item)+'.dtb'
	base64Binary = result['file_object']['analysis']['dtb_finder']['dtb'].encode("ascii")
	decoded = base64.decodebytes(base64Binary)
	#print("".join(["{:08b}".format(x) for x in decoded]))
	dump_file(file_path, decoded)



#dump <firmware._uid>.dtb in current location, if it exists
request_url_fw = 'http://localhost:5000/rest/firmware/'+firmware_uuid
result = requests.get(request_url_fw).json()
if "dtb" in result['firmware']['analysis']['dtb_finder']:
	file_path = firmware_uuid +'.dtb'
	base64Binary = result['firmware']['analysis']['dtb_finder']['dtb'].encode("ascii")
	decoded = base64.decodebytes(base64Binary)
	dump_file(file_path, decoded)



































#extract filesize out of yara match jizzle
'''
with open('example.json') as json_file:
    data = json.load(json_file)

filebegin = data['processed_analysis']['dtb_Finder']['flattened_device_tree']['strings'][0][0]
matchingBase64 = data['processed_analysis']['dtb_Finder']['flattened_device_tree']['strings'][0][2]['$binary']
matchingBytes = base64.b64decode(matchingBase64)
filesize = int(str(matchingBytes)[20:22]+str(matchingBytes)[23:25],16)



with open("firmware/ddwrt-linksys-wrt1900acs-webflash.bin", "rb") as fp:
	filebinary = fp.read()

dump_file("tree.dtb", filebinary[filebegin:filebegin+filesize])

'''


#{"$and":[{"parent_firmware_uids":["216a8aa7ff93bc235eae0dd47de2575888c825cf9be30502aac323e19c1a20dd_37228544"]},{"processed_analysis.dtb_Finder":{"$exists":true}},{"processed_analysis.dtb_Finder.summary":["Flattend Device Tree"]}]}