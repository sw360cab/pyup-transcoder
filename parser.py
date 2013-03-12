import argparse
import t_logger

def parse ():
  parser = argparse.ArgumentParser(description='A simple transcoder and uploader software')
  parser.add_argument('-in', '--input', help='input folder',required=True)
  parser.add_argument('-out', '--output', help='optional output folder')
  parser.add_argument('-r', '--removelocal', help='remove created files after execution', dest='remove', action='store_const', const=True)

  parser.add_argument('-t','--transcode',help='whether to transcode or not', action='store_const', const=True)
  parser.add_argument('-up','--upload',help='whether to upload or not', action='store_const', const=True)
  parser.add_argument('-via', help='upload with [ftp] or [s3]', choices=['ftp', 's3'], default='ftp')
  
  # FTP params
  parser.add_argument('-ftphost', help='FTP host', dest='host')
  parser.add_argument('-ftpport', help='FTP port', default=21, type=int, dest='port')
  parser.add_argument('-ftpusername', help='FTP username', dest='username')
  parser.add_argument('-ftppassword', help='FTP password', dest='password')
  parser.add_argument('-ftpbasedir', help='FTP base directory to connect to', dest='basedir', default='/')
  parser.add_argument('-ftppath', help='FTP destination path to be created', dest='path')
 
  # S3 params
  parser.add_argument('-s3keyid', help='Your AWS Access Key ID')
  parser.add_argument('-s3secretkey', help='Your AWS Secret Access Key')
  parser.add_argument('-s3bucket', help='S3 bucket name', dest='bucket')
  
  # external file paramters
  parser.add_argument('-f','--externalfile', help='whether parameters should be taken from an external file', dest='file', action='store_const', const=True)
  parser.add_argument('-extpath','--externalfilepath', help='path of external file contining parameters', dest='extpath')

  log = t_logger.getLogger(__name__)
  log.debug('Args parsed succesfully')
  
  return parser.parse_args()

def merge (source,dest):
  """
    Merge parameters Source in Dest

    Source is Dictionary at the moment
  """
  for key, value in source.iteritems():
    if (key not in dest.__dict__):
      dest.__dict__[key] = value
  return dest

def validate ():
  return

if __name__ == "__main__":
  d = {'a':2,'b':3}
  merged = merge(d, parse())
  print merged
