# UsbHound

&nbsp;
&nbsp;
## Description
---
This is a tool that gathers information of usb devices connected to your windows system. The information is gathered from the registry of your machine. All this tool does is automate the process of looking up the information of each usb device connected to your machine and present it as a list. 

## Features 
---
* Prints "extra information" about devices that were connected to your machine by extracting volume names. This information may be helpful in some situations
* Save the output into a file the user specifies.
* Create a hash of the output file.

## Usage
---
* -h,--help	&emsp;&emsp;&emsp;&emsp; Shows this help message and exit
* -v &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; Verbose 
* -o &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; Save the output to a file  
* -e &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; Outputs extra information     
* -s &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; Saves the hash value of the output file   

##### For example :
&nbsp;

```
py usbhound.py -o output.txt -v -e -s 
```

##### Sample output :
&nbsp;
```
Accessing the registry hive : HKEY_LOCAL_MACHINE           
Accessing the subkey : SYSTEM\CurrentControlSet\Enum\USBSTOR      

2  Devices identified.  

Accessing the subkey : SYSTEM\CurrentControlSet\Enum\USB   
Accessing the subkey : SOFTWARE\Microsoft\Windows Portable Devices\Devices    
Accessing the subkey : SYSTEM\MountedDevices    
Accessing the registry hive : HKEY_CURRENT_USER                  
Accessing the subkey : Software\Microsoft\Windows\CurrentVersion\Explorer\Mountpoints2    
---------------------------------------------                        
Vendor ::  WD                           
Product ::  Virtual_CD_25E1                                    
Version ::  1021             
Serial Number ::  57584B314143374336415034             
Product ID ::  1058         
Vendor ID ::  25E1         
Drive Letter ::  H         
GUID ::  dfd8366d-d072-11eb-9f6d-c0e43427b576       
Volume Name :: KALI                          
Alternate Volume name ::  ['linux']         
Used by current user ::  True               
---------------------------------------------     
Vendor ::  hp                                     
Product ::  v236w                                
Version ::  PMAP                                
Serial Number ::  6E00082CA1F6EC21          
Product ID ::  03F0                      
Vendor ID ::  7D40                    
Drive Letter ::  F                      
GUID ::  d230d5ef-e0a2-11eb-9f85-502b73c02dd1   
Volume Name ::  Abhi                          
Alternate Volume name ::  []                               
Used by current user ::  True 
----------------------------------------------------------------                   
These devices/volumes were also connected/mounted on this device                        
 ----------------------------------------------------------------   
G:\                         
Galaxy A50          
POCO F1                                                                               
-----------------------------------------------------------------                      
Outputting to the file ::  hello.txt                        
Storing the hash to the file ::  hello.txt.sha256                                                 
----------------------------------------------------------------- 
```
### Explaination
---
 The alternate volume name is the name of a partition that was seen in the device at some point in time. 
 The rest is self explanatory

### Stability
---
This tool has been tested with Windows 10 and python 3.9 and currently doesnt have any dependencies.

### References 
---
* [SANS Digital Forensics and Incident Response - USB Forensics Series](https://www.youtube.com/watch?v=rHeDb8fgOdw)
* [Start learning Python - Python For Everybody](https://www.py4e.com/)




