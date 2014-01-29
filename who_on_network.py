#!/usr/bin/env python
from subprocess import Popen, PIPE
import os

known_devices = {'MAC address 1': 'Device 1 name', 'MAC adress 2': 'Device 2 name'}

def get_local_ip():
	ifconfig = Popen(["ifconfig"], stdout = PIPE).communicate()[0].split()

	# The IP's for the computer is written after the inet string
	ip_s = [ifconfig[i] for i in range(len(ifconfig)) if ifconfig[i-1] == "inet"]

	# The second are the local computer IP
	this_IP = ip_s[1]

	# The broadcasting ip is set to 255
	base = this_IP[0:this_IP.rfind('.')+1]
	broadcast_ip = base+'255'
	return [base,this_IP,broadcast_ip]

def find_connections(base,ran):
	ip_s = [base+str(i) for i in ran]
	os.system('cls' if os.name=='nt' else 'clear')
	print 'Checking for connections..'

	for item in ip_s: # Because apparently pinging the broadcast ip does not always work
		p = Popen(['ping','-c 2','-t 1',item],stdout = PIPE)
		p.wait()

	p = Popen(['arp','-a'],stdout=PIPE).communicate()[0].split('\n')
	active_arp = [item for item in p if not ('(incomplete)' in item)]
	connections = [ [item[item.find(base):item.find('at')-2], item[item.find('at')+3:item.find('at')+20]] for item in active_arp[1:-2] ] # Convoluted yes. This was mostly an excercise in list comprehension
	return connections

def update_connections():
	[base,this_IP,broadcast_IP] = get_local_ip()
	connections = find_connections(base, range(0,14))
	connected = [ [known_devices[item[1]],item] if item[1] in known_devices else ['Unknown Device',item] for item in connections ]
	return connected

def print_connections(connections):
	os.system('cls' if os.name=='nt' else 'clear')
	print 'Connected Devices (Other than this computer): '
	for item in connections:
		print item[0] + ':\n IP: ' + item[1][0] + '\nMAC: ' + item[1][1] + '\n'

print_connections(update_connections())
done = False
while not done:
	try:
		a = raw_input('Enter 1 to update: ')
		print a
		if str(a) == '1':
			print_connections(update_connections())
		else:
			done = True

	except:
		print 'error'




