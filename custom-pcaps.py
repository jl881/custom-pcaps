import binascii
import struct
from math import floor
import sys
import getopt
from ast import literal_eval

def writeByteStringToFile(bytestring, filename):
    bytelist = bytestring.split()  
    bytes = binascii.a2b_hex(''.join(bytelist))
    bitout = open(filename, 'wb')
    bitout.write(bytes)

def writeByteStringToFile(bytestring, filename):
    bytelist = bytestring.split()  
    bytes = binascii.a2b_hex(''.join(bytelist))
    bitout = open(filename, 'wb')
    bitout.write(bytes)

def ip_checksum(iph):
    words = splitN(''.join(iph.split()),4)
    csum = 0;
    for word in words:
        csum += int(word, base=16)
    csum += (csum >> 16)
    csum = csum & 0xFFFF ^ 0xFFFF
    return csum

def splitN(str1,n):
    return [str1[start:start+n] for start in range(0, len(str1), n)]

def main(argv):

  usecs = []
  ofname = ''

  if (len(argv) <5):
    print('custom-pcaps.py <list of timestamps (us)> <packet length> <src mac> <outputfile>')
    sys.exit()
  if (type(literal_eval(argv[1])) == list):
    usecs = literal_eval(argv[1])
  else:
    with open(argv[1]) as f:
      usecs = literal_eval(f.read())
  paylen = int(argv[2])-42
  src = argv[3]
  ofname = argv[4]

  payload = 'AA'
  for i in range(paylen-1):
    payload = payload + ' AA'

  ulen = struct.pack('>H', int(argv[2])-34).encode('hex')
  phlen = struct.pack('<L', int(argv[2])).encode('hex')

  bstring = 'D4 C3 B2 A1 02 00 04 00 00 00 00 00 00 00 00 00 FF 7F 00 00 01 00 00 00 '
  ethh= 'FF FF FF FF FF FF '+src+' 08 00 '
  iph='45 00 '+struct.pack('>H', int(argv[2])-14).encode('hex')+' 00 01 00 00 40 11 XX XX C0 A8 00 01 C0 A8 01 01 '
  udph='00 78 00 79 '+ulen+' 00 00 '

  check = ip_checksum(iph.replace('XX XX','00 00'))
  check = struct.pack('>H', check).encode('hex')
  iph = iph.replace('XX XX',check)

  utime = '00 00 00 00'
  for i in range(len(usecs)):
    if (usecs[i] > 1000000):
      utime = struct.pack('<L', int(floor(usecs[i]/1000000))).encode('hex')
      us_since_utime = struct.pack('<L', usecs[i]%1000000).encode('hex') 
    else:
      us_since_utime = struct.pack('<L', usecs[i]).encode('hex')
    pkt_hdr = ' '+utime+' '+us_since_utime+' '+phlen+' ' + phlen + ' '
    bstring = bstring +pkt_hdr + ethh + iph + udph + payload

  writeByteStringToFile(bstring, ofname)

main(sys.argv)
