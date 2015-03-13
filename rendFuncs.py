from StringIO import StringIO
import binascii
from collections import namedtuple
import pprint
import os
import time
import ssl,socket,struct
from Crypto.Hash import SHA
from Crypto.Cipher import *
from Crypto.PublicKey import *
import sys
from Crypto.Util import *
import consensus
import base64
import re
from urlparse import urlparse,urljoin,urlunsplit
import urllib
import urllib2
import csv
import sha
import struct
import itertools
import re

from hashlib import sha1
from base64 import b32encode, b32decode, b64decode
from random import randint
from bisect import bisect_left




### Follows the Tor Rendezvous Specification   -- https://gitweb.torproject.org/torspec.git/blob/HEAD:/rend-spec.txt


#Descriptor ID can only be created by the hidden service and its clients. 
#Modified version of Donncha O' Cearbhaill code
#Input is the onion address as well the replica - How many times these descriptors have been published (3) Although some HS can have up to 10
# descriptor-id  = H(permanent-id | H(time-period | descriptor-cookie | replica))
def get_descriptor_Id(onion_Add, replica):
  service_id = b32decode(onion_Add, 1) 
  time_period = int((((time.time()) + ((struct.unpack('B', service_id[0])[0] * 86400) ) / 256) ) / 86400 + 0)
  s = sha1()
  s.update(struct.pack('>I', time_period)[:4]);
  s.update('{0:02X}'.format(replica).decode('hex'))
  s = s.digest()
  d = sha1()
  d.update(service_id)
  d.update(s)
  d = d.digest()
  return b32encode(d).lower()

#Modified version of Donncha O' Cearbhaill code, as explained in the report, had a lot of difficulty finiding the responsible HSdirectors 
#Takes an input of a descriptor id
def find_responsible_HSDir(descriptor_id):
   responsible_HSDirs = []
   HSDir_List = consensus.get_HSDir_Flag()  # Allows us to only get the data containing the HSDir flags
   orHashList = sorted(map(lambda x: x['identity'], HSDir_List))
   descriptor_position = bisect_left(orHashList, b32decode(descriptor_id,1)) #should be identiy list not HSDir_List #TODO - Add the other part of the list to it so it makes a circle
   for i in range(0,3): #This is becuase of the 3 replicas, it is important to get all 3
      responsible_HSDirs.append(orHashList[descriptor_position+i])
   return (map(lambda x: consensus.get_router_by_hash(x) ,responsible_HSDirs))

#No input required, this function just creates a random 20 byte value and returns this 
def create_rendezvous_cookie():
   rendezvous_cookie = os.urandom(20) #Random 20 byte value
   return rendezvous_cookie

#Creates the IP address with Port numbers for all the responsible hidden service directories
# For each descriptor it will be containted three ip addresses and ports,
#Takes an input of ip_addresses, dirport, descriptor_id_list which where calculated from the function above.
def connect_to_web_lookup(ip_addresses, dirport, descriptor_id_list):
  web_addresses =[]
# creates a list of all possible web addresses to connect to using the data retrieved from above
  for i in range(0,len(descriptor_id_list)):
    for j in range(0,3):
      a_elem = i*3 + j
      web_addresses.append(ip_addresses[a_elem]+':'+str(dirport[a_elem]))
  return web_addresses

#Takes the rendezvous point nickname, and searches the concensus for all the data such as IP address for the rendv. point
# Returned will be the ip address, onion port, identity and onion key for the rendv. point 
def calc_rendezvous_point_data(rendezvous_point):
  # print rendezvous_point #testing,currently not being passed, no item error
  rp_ip = consensus.getRouter(rendezvous_point)['ip']
  rp_or_port = consensus.getRouter(rendezvous_point)['orport']
  rp_id = consensus.getRouter(rendezvous_point)['identity']
  router_descriptor = consensus.getRouterDescriptor((consensus.getRouter(rendezvous_point))['identityhash'])
  onion_key = consensus.getRouterOnionKey(router_descriptor)
  return rp_id, rp_ip, rp_or_port, onion_key

def getIndex(str,arr):
     for i in range(len(arr)):
             if str in arr[i]:
                     return i
     return -1

#Takes an input of the responsible HSdirs, and then calculate the data such as IP address, port etc. for each of the reponsible HSdir
#Output is the ip_addresses, dirport, port, nickname, identity for all three responsble HSdirs (although there can be more or less than 3 although this is rare)
def extract_HSDir_data(responsible_HSDir_list):
  # Extracts the data here from the list generated above to connect to the web url to get the rendezvous2 data
  ip_addresses = [i.get('ip') for j in responsible_HSDir_list for i in j]
  dirport =  [i.get('dirport') for j in responsible_HSDir_list for i in j]
  port =  [i.get('port') for j in responsible_HSDir_list for i in j]
  nickname = [i.get('nick') for j in responsible_HSDir_list for i in j]
  identity = [i.get('identity') for j in responsible_HSDir_list for i in j]
  return ip_addresses, dirport, port, nickname, identity


