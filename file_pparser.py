import re

def readAndParseFile(filename):
  """
    Read line by line a file and parse it
  """
  params={}

  with open(filename, 'r') as f:
    for line in f:
      elem = parse(line)
      if (elem):
        params[ elem[0] ]=elem[1]
  return params

def parse(completeLine,separator=r'='):
  """
    Strip and split a key/value string 
    "=" is default separator
  """
  uncommentedStr = re.sub ( r'((#.*)?$)', '',  completeLine )
  if (len(uncommentedStr) > 0):
    key,value=re.split(separator,uncommentedStr,1)
    #do stri strings
    return key.strip(),value.strip()

if __name__ == "__main__":
  import sys
  d = readAndParseFile(sys.argv[1])
  for key, value in d.iteritems():
    print (key,value)
