from boto.s3.connection import S3Connection
from boto.s3.key import Key
import t_logger
import os

def connect(s3params):
  log = t_logger.setup(__name__)
  conn = S3Connection(s3params.s3keyid, s3params.s3secretkey)
  return conn

def upload(s3,bucketName,path):
  bucket = s3.create_bucket(bucketName)
  log.info('Bucket %s is OK',bucketName)

  log.debug('Starting trasfer of %s',path)
  pathName = os.path.basename(path)
  log.debug('S3 key will be %s', pathName)

  storedData = Key(bucket)
  storedData.key = pathName
  storedData.set_contents_from_filename(path)

  log.debug('S3 trasfer of %s completed',path)

