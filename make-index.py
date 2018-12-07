#! /usr/bin/python3
import hashlib
import math
import os
import os.path

SLICE = 1024

def md5file(src):
  with open(src, 'rb') as srcfile:
    content = srcfile.read()
    return hashlib.md5(content).hexdigest()

def main(src, baseurl, system, lock, version):
  global SLICE
  srcstat = os.stat(src)
  srcstat.st_size
  output = ""
  with open(src, 'rb') as srcfile:
    srcfile = open(src, 'rb')
    count = int(srcstat.st_size / SLICE) + 1 if srcstat.st_size % SLICE != 0 else 0
    buf = bytearray(SLICE)
    output += "%s/%s|%s|%d\n" % (baseurl, os.path.basename(src), md5file(src), srcstat.st_size)
    for i in range(count):
      readed = srcfile.readinto(buf)
      start = i * SLICE
      stop  = start + readed - 1
      output += "%d,%d|%s|%d\n" % (start, stop, hashlib.md5(buf[:readed]).hexdigest(), readed)
  digest = hashlib.md5(output.encode()).hexdigest()
  dstfile = open(os.path.dirname(src) + '/%s-%s-%s-%s.txt' % (system, lock, version, digest), 'w')
  dstfile.write(output)
  dstfile.close()

if __name__ == "__main__":
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument("srcfile", help="Source file to make index")
  parser.add_argument("baseurl", help="The base url of file")
  parser.add_argument("--system", help="The type of system board", dest="system", default="1")
  parser.add_argument("--lock", help="The type of lock board", dest="lock", default="1")
  parser.add_argument("--version", help="The version of upgraded file", dest="version", default="1")
  args = parser.parse_args()
  main(args.srcfile, args.baseurl, args.system, args.lock, args.version)
