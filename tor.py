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

from torfuncs import *
from rendFuncs import *

import mysql.connector


##Connects to mysql db
db=mysql.connector.connect(user='root', password ='edge#540', database='hsip')
cursor=db.cursor()

name = "silkroad6ownowfk"

cursor.execute("CREATE TABLE IF NOT EXISTS " + name + 
	"(identityb32  CHAR(40) NOT NULL,"
	+ "pubdate  CHAR(40) NOT NULL,"
	+ "dirport  CHAR(6) NOT NULL,"
	+ "ip  CHAR(40) NOT NULL,"
	+ "orport  CHAR(40) NOT NULL,"
	+ "identityhash  CHAR(40) NOT NULL,"
	+ "nick  CHAR(40) NOT NULL,"
	+ "version  CHAR(40) NOT NULL,"
	+ "flags  CHAR(90) NOT NULL,"
	+ "identity  CHAR(40) NOT NULL,"
	+ "digest  CHAR(40) NOT NULL,"
	+ "pubtime  CHAR(40) NOT NULL)"
	)


# #Will soon remove, want to put all data in a db rather than txt files
# extension =".txt"
# x = 0
# fileName = name + extension
# while(os.path.exists(fileName)):
#     x = x + 1
#     fileName = name + str(x) + extension

# file = open(fileName, 'w+')


i = 0
consensus.fetchConsensus(i) #Retrieves the consensus 


print "Retriving hidden service descriptor" #Keeping the user informed
#"kpvz7ki2v5agwt35"#Hidden Wiki   #"3g2upl4pq6kufc4m"#duck duck go     #"idnxcnkne4qt76tg" #homepage of the Tor project   #All various hidden service addresses, some dont work as temporarily gone down etc
onion_Add = "silkroad6ownowfk" #Hidden service address , can be with or without the .onion at the end

responsible_HSDir_list = [] #Setting up variables to take an array list to be used later on
descriptor_id_list = [] #Setting up variables to take an array list to be used later on

for i in range(0, 2):
    descriptor_id = get_descriptor_Id(onion_Add, i) #Passes the onion address and i to the get_descriptor_id function in rendFunccs ("descriptor-id" is a identifier that is calculated by the hidden service and its clients)
    descriptor_id_list.append(descriptor_id) # Makes sure all 3 desciptor ids are stored
    responsible_HSDir = find_responsible_HSDir(descriptor_id)# Passes the descriptor to the find_responsible_HSDir function in rendFunccs (returns the responsible hidden service directories for the selected hidden service)
    responsible_HSDir_list.append(responsible_HSDir) # Saves all responsible HSDir information in a list to use later (3 responsible hidden service directories)

ip_addresses, dirport, port, nickname, identity = extract_HSDir_data(responsible_HSDir_list) # Extracts the data from the reponsible Hidden service directories and assigns these to several variables for use later on
# web_addresses = connect_to_web_lookup(ip_addresses, dirport, descriptor_id_list) # Creates the IP address with Port numbers for all the responsible hidden service directories

print responsible_HSDir_list


sys.exit(0)




