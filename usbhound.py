import winreg 
import re
import argparse 
import hashlib


parser = argparse.ArgumentParser(prog="usbhound.py",description="Gives you the list of storage devices that has been connected to your device")
parser.add_argument("-v",help="verbose",action="store_true")
parser.add_argument("-o",help="save the output to a file ",action="store",type=str,default="")
parser.add_argument("-e",help="Outputs extra information",action="store_true")
parser.add_argument("-s",help="Saves the hash value of the output file",action="store_true")
args = parser.parse_args()


def store(*argv):
	global output
	for op in argv:
		output+=op 
		print(op,end=" ")
	print("")
	output+="\n"

def hash_file(filename):
   hash = hashlib.sha256()
   with open(filename,'rb') as file:
       chunk = 0
       while chunk != b'':
           chunk = file.read(1024)
           hash.update(chunk)
   return hash.hexdigest()


output=""
hashing = args.s
file=args.o
users=[]
paths=[]
dev=[]
extra_dev=[]
extra_flag=True

def sniff():
	global file
	global output
	global hashing 
	global file
	global users
	global paths
	global dev
	global extra_dev
	global extra_flag

	subkey=r"SYSTEM\CurrentControlSet\Enum\USBSTOR"
	try:
		if file != "":
			fhandle=open(file,"w")
	except:
		print("Couldnt open file\nExitting...")
		quit()



	try:
		if args.v:
			store("\n\nAccessing the registry hive : HKEY_LOCAL_MACHINE")

			store(r"Accessing the subkey : SYSTEM\CurrentControlSet\Enum\USBSTOR")
		hive_handle = winreg.ConnectRegistry(None,winreg.HKEY_LOCAL_MACHINE)
		path = winreg.OpenKey(hive_handle,subkey)
	except OSError:
		store("\nCould not open the given hive")
		quit()

	#FINDING BASIC INFO
	try:
		for i in range(winreg.QueryInfoKey(path)[0]):
			curr_dev={'ven':'','prod':'','ver':'','serial_no':'','vid':'','pid':'','vol':'','letter':'','alt_name':[],'guid':'','curr_user':True,'users':[]}
			value=winreg.EnumKey(path,i)
			temp_path = subkey+"\\"+value
			paths.append(temp_path)
			path = winreg.OpenKey(hive_handle,subkey)
			curr_dev['ven']=re.findall('Ven_(.+?)&',value)[0]
			curr_dev['prod']=re.findall('Prod_(.+?)&',value)[0]
			curr_dev['ver']=re.findall('Rev_(.*)?',value)[0]
			dev.append(curr_dev)

	except OSError:
		store("Some Error Occured while accessing the registry")

	store("\n",str(i+1)," Devices identified.\n")

	#FINDING SERIAL NUMBERS 
	j=0
	try:
		for i in paths:
			temp_path = winreg.OpenKey(hive_handle,i)
			dev[j]['serial_no'] = re.findall('(.+?)&',winreg.EnumKey(temp_path,0))[0]
			j+=1
	except OSError:
		store("Error Occured while accessing the serial numbers")

	winreg.CloseKey(path)
	winreg.CloseKey(temp_path)

	subkey =r"SYSTEM\CurrentControlSet\Enum\USB"
	path = winreg.OpenKey(hive_handle,subkey)

	if args.v:
		store(r"Accessing the subkey : SYSTEM\CurrentControlSet\Enum\USB")

	for i in range(winreg.QueryInfoKey(path)[0]):
		try:
			value=winreg.EnumKey(path,i)
			temp_path=winreg.OpenKey(hive_handle,subkey+"\\"+value)
			for j in range(len(dev)):
				if(winreg.EnumKey(temp_path,0)==dev[j]['serial_no']):
					dev[j]['vid'] = re.findall('VID_(.+?)&',value)[0]
					dev[j]['pid'] = re.findall('PID_(....)',value)[0]
		except OSError:
			store("Some Error Occured while accessing the registry")

	winreg.CloseKey(path)
	winreg.CloseKey(temp_path)

	subkey = r"SOFTWARE\Microsoft\Windows Portable Devices\Devices"
	try:
		if args.v:
			store(r"Accessing the subkey : SOFTWARE\Microsoft\Windows Portable Devices\Devices")
		path = winreg.OpenKey(hive_handle,subkey)
		for i in range(winreg.QueryInfoKey(path)[0]):
			extra_flag=True
			for j in dev:
				value=(winreg.EnumKey(path,i))
				temp_path=winreg.OpenKey(hive_handle,subkey+"\\"+value)
				info=winreg.EnumValue(temp_path,0)
				if re.search(j['serial_no'],value):
					j['vol']=info[1]
					extra_flag=False
					break
			temp=re.findall("{(.*)}",value)
			if extra_flag:
				if temp!=[]:
					extra_dev.append([re.findall(".*-.*-.*-.*-(.*)",temp[0])[0],info[1]])
				else:
					extra_dev.append(["",info[1]])
	except OSError:
		store("Error Occured while accessing the registry")

	winreg.CloseKey(path)
	winreg.CloseKey(temp_path)

	subkey = r"SYSTEM\MountedDevices"
	try:
		if args.v:
			store(r"Accessing the subkey : SYSTEM\MountedDevices")
		path = winreg.OpenKey(hive_handle,subkey)
		for i in range(winreg.QueryInfoKey(path)[1]):
			value=winreg.EnumValue(path,i)[1]
			value=str(value)
			data = ''.join([str(i) for i in re.findall(r".*?x00(.)",value)])
			drive=winreg.EnumValue(path,i)[0]	
			for j in dev:
				if j['serial_no'] != "":
					if re.search(j['serial_no'],data):
						temp=re.findall(r"(.):",drive)
						if temp !=[] :
							j['letter']=temp[0]
						else:
							if j['letter']=="":
								j['letter']="N/A"
						guid = re.findall("{(.*)}",drive)
						if guid !=[]:
							j['guid'] = guid[0]
						for k in extra_dev:
							if re.search(k[0].upper(),drive.upper()):
								if k[0] != "":
									j['alt_name'].append(k[1])
									extra_dev.remove(k)
								
	except OSError:
		store("Error Occured while accessing the registry")														
	winreg.CloseKey(path)

	#CURRENT USER
	if args.v:
				store("Accessing the registry hive : HKEY_CURRENT_USER")
				store(r"Accessing the subkey : Software\Microsoft\Windows\CurrentVersion\Explorer\Mountpoints2")
	hive_handle_user = winreg.ConnectRegistry(None,winreg.HKEY_CURRENT_USER)
	subkey = r"Software\Microsoft\Windows\CurrentVersion\Explorer\Mountpoints2"
	path = winreg.OpenKey(hive_handle_user,subkey)
	for i in range(winreg.QueryInfoKey(path)[1]):
		for j in dev:
			guid = re.findall("{(.*)}")
			if guid != []:
				if guid[0] == j['guid']:
					print("guid :: ",guid[0])
					j['curr_user']=True
	store("\n")
	for i in dev:
		store("---------------------------------------------")
		store("Vendor :: ",i['ven'])
		store("Product :: ",i['prod'])
		store("Version :: ",i['ver'])
		store("Serial Number :: ",i['serial_no'])
		store("Product ID :: ",i['vid'])
		store("Vendor ID :: ",i['pid'])
		store("Drive Letter :: ",i['letter'])
		store("GUID :: ",i['guid'])
		if i['vol'] =="":
			store("Volume Name :: ","N/A")
		else:
			store("Volume Name :: ",i['vol'])
		store("Alternate Volume name :: ",str(i['alt_name']))
		store("Used by current user :: ",str(i['curr_user']),"\n")
	if args.e:
		if extra_dev == []:
			store("-------------------------------------------------")
			store("No extra information to display")
			store("-------------------------------------------------")
		else:
			store("-------------------------------------------------")
			store("These devices were also connected on this device")
			store("-------------------------------------------------")
			for i in extra_dev:
				store(str(i[1]))

	if file != "":
		try:
			if args.v:
				print("\n------------------------------------------------------------------") 
				print("Outputting to the file :: ",file)
			fhandle.write(output)
			fhandle.close()
			if hashing:
				hash=hash_file(file)
				file=file+".sha256"
				if args.v:
					print("Storing the hash to the file :: ",file)
					print("------------------------------------------------------------------")
				fhandle=open(file,"w")
				fhandle.write(hash)
				fhandle.close()
		except:
			print("Couldnt open file\n")


sniff()