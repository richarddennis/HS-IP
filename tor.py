from StringIO import StringIO
import cStringIO
import binascii
from collections import namedtuple
import pprint
import os
import time
import ssl,socket,struct
from binascii import hexlify
import sys
import itertools
import consensus
import sys
import base64
import urllib2
import zlib
from Crypto.Hash import SHA
import unittest
import threading
import struct
import string
from time import sleep
import threading
import errno
import re
from datetime import datetime, timedelta

from rendFuncs import *

import mysql.connector


##Connects to mysql db
db=mysql.connector.connect(user='root', password ='edge#540', database='hsip')
cursor=db.cursor()

#Onion name
onion_Add = "silkroad6ownowfk" #Hidden service address , can be with or without the .onion at the end

#Creates a new table for each onion address
cursor.execute("CREATE TABLE IF NOT EXISTS " + onion_Add + 
	"(consensus  CHAR(40) NOT NULL," 
	+ "identityb32  CHAR(40) NOT NULL,"
	+ "pubdate  CHAR(40) NOT NULL,"
	+ "dirport  CHAR(6) NOT NULL,"
	+ "ip  CHAR(40) NOT NULL,"
	+ "orport  CHAR(40) NOT NULL,"
	+ "identityhash  CHAR(40) NOT NULL,"
	+ "nick  CHAR(40) NOT NULL,"
	+ "version  CHAR(40) NOT NULL,"
	+ "flags  VARCHAR(500) NOT NULL,"
	+ "identity  VARCHAR(256) NOT NULL,"
	+ "digest  CHAR(40) NOT NULL,"
	+ "pubtime  CHAR(40) NOT NULL)"
	)


def calculate_and_write_hsdir(h,d,m,y):
	while True:
		if h < 24:

			if d < 10:
				d = "0"+str(d)
			if h < 10:
				h = "0"+str(h)
			if m < 10:
				m = "0"+str(m)
			
			consensus_file_name = str(y) + "-" + str(m) + "-" + str(d) + "-" + str(h) + "-00-00-consensus"
			print consensus_file_name 

			consensus.fetchConsensus(consensus_file_name) #Retrieves the consensus 

			responsible_HSDir_list = [] #Setting up variables to take an array list to be used later on
			descriptor_id_list = [] #Setting up variables to take an array list to be used later on

			for i in range(0, 2):
			    descriptor_id = get_descriptor_Id(onion_Add, i) #Passes the onion address and i to the get_descriptor_id function in rendFunccs ("descriptor-id" is a identifier that is calculated by the hidden service and its clients)
			    descriptor_id_list.append(descriptor_id) # Makes sure all 3 desciptor ids are stored
			    responsible_HSDir = find_responsible_HSDir(descriptor_id)# Passes the descriptor to the find_responsible_HSDir function in rendFunccs (returns the responsible hidden service directories for the selected hidden service)
			    responsible_HSDir_list.append(responsible_HSDir) # Saves all responsible HSDir information in a list to use later (3 responsible hidden service directories)

			identityb32, pubdate, dirport, ip, orport, identityhash, nick, version, flags, identity, digest, pubtime = extract_HSDir_data(responsible_HSDir_list) # Extracts the data from the reponsible Hidden service directories and assigns these to several variables for use later on
			# web_addresses = connect_to_web_lookup(ip_addresses, dirport, descriptor_id_list) # Creates the IP address with Port numbers for all the responsible hidden service directories

			c = 0

			while c < len(nick):
				format = """','"""

				flags[c] = str(flags[c]).replace("'", "")
				identity[c] = str(identity[c]).replace("'", "")

				sql = """INSERT INTO """ + onion_Add +"""(consensus, identityb32, pubdate, dirport, ip, orport, identityhash, nick, version, flags, identity, digest, pubtime)
				         VALUES ('""" +consensus_file_name + format + identityb32[c] + format + pubdate[c] + format + dirport[c] + format + ip[c] + format + orport[c] + format + identityhash[c] + format + nick[c] + format + version[c] + format + flags[c] + format + binascii.hexlify(identity[c]) + format + digest[c] + format + pubtime[c] + """')"""

				try:
				   cursor.execute(sql)
				   db.commit()
				except:
				   db.rollback()
				   print "adding to db error"

				c = c + 1
				
			h = int(h) + 1 
		else:
			h = 00
			d = int(d) + 1
			return d
				# 	d = d + 1

def run_calculate(h,d,m,y):
	if m in [1,3,5,7,8,10,12]:
		while True:
			d = calculate_and_write_hsdir(h,d,m,y)
	   		if d == 31:
	      			calculate_and_write_hsdir(h,d,m,y)
	       			d = 1
	       			m = m + 1
	       			break

	if m == 2:
		while True:
			d = calculate_and_write_hsdir(h,d,m,y)
	   		if d == 28:
	      			calculate_and_write_hsdir(h,d,m,y)
	       			d = 1
	       			m = m + 1
	       			break


	if m in[4,6,9,11]:
		while True:
			d = calculate_and_write_hsdir(h,d,m,y)
	   		if d == 30:
	      			calculate_and_write_hsdir(h,d,m,y)
	       			d = 1
	       			m = m + 1
	       			break

h = 00 #Hour
d = 07 #Day
m = 10 #Month
y = 2013 #Year

run_calculate(h,d,m,y)
run_calculate(00,1,1,2014)
run_calculate(00,1,1,2015)
