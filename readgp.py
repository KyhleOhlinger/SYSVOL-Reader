import rp
from rp.data import data
from rp.reader import reader
import os, binascii, sys
from collections import defaultdict
import configparser
import argparse

def print_data(policy):
	# Depending on data type, will need different decoding types when printing the data
	if(isinstance(policy.data, bytes)):
		try:
			print(str(policy.key.decode('utf_16_le') + "\t\t" + policy.value.decode('utf_16_le') + "\t\t" + str(policy.data.decode('utf_16_le'))))
		except UnicodeDecodeError:
			print(str(policy.key.decode('utf_16_le') + "\t\t" + policy.value.decode('utf_16_le') + "\t\t" + str(binascii.b2a_hex(policy.data).decode())))
	elif(isinstance(policy.data, int) or isinstance(policy.data, str)):
		print(str(policy.key.decode('utf_16_le') + "\t\t" + policy.value.decode('utf_16_le') + "\t\t" + str(policy.data)))
	elif(policy.data is None or isinstance(policy.data,list)):
		print(str(policy.key.decode('utf_16_le') + "\t\t" + policy.value.decode('utf_16_le') + "\t\t" + str(policy.data)))
	else:
		print("ERR: " + str(type(policy.data)))
	pass

def read_data(path):
	# Check the 'data' sub module under 'rp' to understand the policy data structure.
	RPData = rp.data.RPData()
	RPReader = rp.reader.Reader(path,RPData)
	#print("\n\n" + path + "\n")
	for policy in RPData.body.policies:
		print_data(policy)

def read_ini_inf(policiesDir):
	#gpttmpl.inf
	if policiesDir.endswith('.inf'):
		print(" -- Printing: " + policiesDir)
		with open(policiesDir, 'rb') as f:
			contents = f.read()
		try:
			print(contents.decode("utf-8"))	
		except UnicodeDecodeError:
			print(contents.decode("utf-16-le"))	
		
	# Look for all policy files (.pol) in SYSVOL structure
	else:
		for root,directories,files in os.walk(policiesDir):
			for name in files:
				if name.endswith('.inf') or name.endswith('.ini'):
					path = os.path.join(root,name)
					print(" -- Printing: " + path)
					# Read in Config File
					with open(path, 'rb') as f:
						contents = f.read()
					try:
						print(contents.decode("utf-8"))	
					except UnicodeDecodeError:
						print(contents.decode("utf-16-le"))	

if __name__ == "__main__":

	parser = argparse.ArgumentParser()
	parser.add_argument("-s","--sysvol",required=False, action='store_true', help="Specifies that SYSVOL files are going to be read.")
	parser.add_argument("-c","--config",required=False, action='store_true', help="Specifies that the '.ini' and '.inf' config files are going to be read.")
	args = parser.parse_args()
  
	if args.sysvol:
		policiesDir = input("Please enter a directory or single policy (.pol) file:\n")
		#policiesDir = r"C:\Users\Kyhle\Downloads\sysvol\domain\policies"
	
		# Look for a single policy file (.pol) in SYSVOL structure
		if policiesDir.endswith('.pol'):
			print("\n\nReading Group Policy Information for: " + policiesDir + "\n")
			read_data(policiesDir)
		# Look for all policy files (.pol) in SYSVOL structure
		else:
			for root,directories,files in os.walk(policiesDir):
				for name in files:
					if name.endswith('.pol'):
						path = os.path.join(root,name)
						read_data(path)

	elif args.config:    
		policiesDir = input("Please enter a directory or single config (.ini or .inf) file:\n")
		#policiesDir = r"C:\Users\Kyhle\Downloads\sysvol\domain\policies"
		
		# Read gpttmpl.inf files
		read_ini_inf(policiesDir)
	else:
		print("No arguements specified, use --help to determine which arguements are available.")
		sys.exit(0)