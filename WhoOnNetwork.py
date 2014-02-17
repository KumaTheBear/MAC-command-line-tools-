#!/usr/bin/env python
from subprocess import Popen, PIPE
import os

KNOWN_DEVICES = {'MAC address 1': 'Device 1 name', 'MAC adress 2': 'Device 2 name'}

def getLocalIp():
	ifconfig = Popen(["ifconfig"], stdout = PIPE).communicate()[0].split()

	# The IP's for the computer is written after the inet string
	ip_s = [ifconfig[i] for i in range(len(ifconfig)) if ifconfig[i-1] == "inet"]

	# The second are the local computer IP
	this_IP = ip_s[1]

	# The broadcasting ip is set to 255
	base = this_IP[0:this_IP.rfind('.')+1]
	broadcast_ip = base+'255'
	return [base,this_IP,broadcast_ip]

def findConnections(base,ran):
	ip_s = [base+str(i) for i in ran]

	for item in ip_s: # Because apparently pinging the broadcast ip does not always work
		p = Popen(['ping','-c 2','-t 1',item],stdout = PIPE)
		p.wait()

	p = Popen(['arp','-a'],stdout=PIPE).communicate()[0].split('\n')
	active_arp = [item for item in p if not ('(incomplete)' in item)]
	connections = [ [ item.split()[1][1:-1], item.split()[3] ] for item in active_arp[1:-2] ] # Convoluted yes. This was mostly an excercise in list comprehension
	return connections

def updateConnections(ran):
	[base,this_IP,broadcast_IP] = getLocalIp()
	connections = findConnections(base, ran)
	connected = [ [known_devices[item[1]],item] if item[1] in known_devices else ['Unknown Device',item] for item in connections ]
	return connected

def printConnections(connections):
	os.system('cls' if os.name=='nt' else 'clear')
	print 'Connected Devices (Other than this computer): '
	for item in connections:
		print item[0] + ':\n IP: ' + item[1][0] + '\nMAC: ' + item[1][1] + '\n'

printConnections(updateConnections(range(2,6)))
done = False
while not done:
	try:
		printConnections(updateConnections(range(2,6)))
		time.sleep(5.5)

	except:
		print 'error'





