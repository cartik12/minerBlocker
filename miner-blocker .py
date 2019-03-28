#import statements
import os
from time import sleep
import tkinter
#from tkinter import tkMessageBox
from tkinter import messagebox
import psutil
import time
import shutil
from subprocess import check_output
import datetime
from datetime import timedelta

# process to check the processes running by the process name and kill it 
def processcheck(seekitem):
	for proc in psutil.process_iter():
		if proc.name() == seekitem:
			print ("miner process " + seekitem + " is running")
			proc.kill()
			print (" process " + seekitem +" is now killed")

def cpuUsageCheck():
	
	highUsage = True;
	start = datetime.datetime.now()
	a = 0;
	while True:
		print ('==========')
		#print('inside methos while check')	
		a = a + 1
		print(a)
		values = psutil.cpu_percent(percpu=True)
		#print(values)
		cores = len(values)
		j1 = [load for load in values if load >= 90] #change to 100 if required
		print(j1)
		if (len(j1) >= 2):
			#print('cpu more utilization inside method')
			sleep(1)
			end = datetime.datetime.now()
			time_difference = end - start
			time_difference_in_minutes = int(time_difference / timedelta(minutes=1))
			print('time_difference_in_minutes')
			print(time_difference_in_minutes)
			if (time_difference_in_minutes >= 4):  #set time here
				pid_list = psutil.pids();
				for pids in pid_list:
					try:
						process = psutil.Process(pids)
						if(psutil.pid_exists(pids)):
							#if (process.name() == 'chrome'): # add more browser process like microsoftedge, safari and firefox if u want to 
							pCpu = process.cpu_percent(interval=1.2)
							print(pCpu)
							print(process.name())
							if (pCpu >= 90):
								#process.terminate();
								window = tkinter.Tk()
								window.wm_withdraw()
								result = messagebox.askquestion("Kill the process " + process.name(),
									 "Two or more core are running the cores have CPU usage over " + str(pCpu/cores) + " %", icon='warning')
								if result == 'yes':
								 	print('killing the process')
								 	process.terminate();
								 	break;
					except psutil.NoSuchProcess:
						continue

# miner process that are under scrunity
miner_process = ["Silence","Carbon","xmrig32","nscpucnminer64","mrservicehost","servisce","svchosts3","svhosts","system64","systemiissec",
"taskhost","vrmserver","vshell","winlogan","winlogo","logon","win1nit","wininits","winlnlts","taskngr","tasksvr","mscl","cpuminer","sql31",
"taskhots", "svchostx","xmr86","xmrig","xmr","win1ogin","win1ogins","ccsvchst","nscpucnminer64","update_windows"]

# block website - start (this needs root privileges)
# read the hosts file and create a back up

file = open("/etc/hosts", "r") 
rawContent = file.read()
backup = open("/etc/hostBackup","w+")
backup.write(rawContent);

# clear the data in hosts
open("/etc/hosts","w").close()
changedContent = ''

# get the block website list and write it in the hosts file
with open('blacklist.txt', 'r') as myfile:
	for line in myfile: 
		changedContent = '127.0.0.1\t' + line + changedContent
fullContent = rawContent + changedContent

# write the changed data into hosts
with open("/etc/hosts","a") as f:
	f.write(fullContent)
print('host file updated with the miner websites')
# block website - end

#continious loop to check for the miner process and the cpu utilization 
# check if cpu load for more than two cores are over 90%
while True:
	try:
		for process in miner_process:
			processcheck(process)
		values = psutil.cpu_percent(percpu=True)
		j2 = [load for load in values if load >= 90] #change to 100 if required
		if (len(j2) >= 2):
			print('cpu more utilization')
			cpuUsageCheck();
		sleep(2) #checks every 2 seconds for the process running and utilization
	except KeyboardInterrupt:
		print('stopping')
		break

# to break ctrl +c in the command line
# host file again will be copied with orginal data
##clear the hosts
open("/etc/hosts","w").close()

# write back the raw data into hosts
with open("/etc/hosts","a") as f:
    f.write(rawContent)
print('host file changed to previous version')
#end