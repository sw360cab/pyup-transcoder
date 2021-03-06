import os
import shutil
import time
import parser
import file_pparser
import ftp_connector
import s3_connector
import gst_transcoder
import t_logger

# main
def main() :
  log = t_logger.setup('transcoder')

  ftp=0
  s3=0
  bucketName=0
  #
  # parse arguments
  #
  params = parser.parse()

  # parse file
  if (params.file and params.extpath):
    fileParams = file_pparser.readAndParseFile(params.extpath);
    if (len(fileParams.keys()) >0):
      params = parser.merge(fileParams,params)

  if os.path.exists(params.input ) is False:
    raise IOError (params.input,"does not exist")

  #
  # handle dest folder
  #
  if (params.inplace):
    dest = params.input
  else:
    dest = getOutputFolder ( params.input, params.output )
  
  try:
    os.mkdir(dest)
  except: 
    log.debug('%s folder already exists', dest)

  #
  # UPLOAD step configuration
  #
  if (params.upload):
    if (params.via == "ftp"):
      ftp = ftp_connector.connect(params)
    if (params.via == "s3"):
      bucketName = params.bucket if params.bucket else params.s3keyid.lower() + '_' +str(int(time.time()))
      s3 = s3_connector.connect(params)
    else:
      log.info("Only FTP and S3 supported")
  
  #
  # SOURCEDIR recursive exploration 
  # + TRANSCODING
  # + UPLOAD
  #
  for root, dirs, files in os.walk(params.input):
    if root != dest: # it may happen that dest is inside root folder
      log.info('current processed folders are %s and %s',root,dest)
      if (params.createtree):
        finalDest = generateIntermediateFolder(params.input, root, dest)

      for name in files:
        finalName = name
        finalPath = root + os.sep + name

        # deal with transcoding
        if (params.transcode):
          try :
            if (hasattr(params,'transcodingString')):
              finalName, finalPath = \
                gst_transcoder.transcodeFile(name,root,finalDest, \
                  preserveDate=(params.nopreserve) is None, \
                  transcodingString=params.transcodingString)
            else:
              finalName, finalPath = \
                gst_transcoder.transcodeFile(name,root,finalDest, \
                  preserveDate=(params.nopreserve) is None)
          except RuntimeError:
            log.info("File %s NOT transcoded", root+os.sep+name)
        # deal with ftp
        if ftp:
          ftp_connector.upload(ftp,finalName,finalPath)
        # deal with s3
        elif s3:
          s3_connector.upload(s3,bucketName,finalPath)

  #
  # Eventually remove local folder 
  #
  if params.remove:
    shutil.rmtree(dest, True)
    log.info("%s folder removed", dest) 
  
  log.info('Done!')

def getOutputFolder ( input, output ) :
  # check if input contains os.sep at the end 
  input = input if input[len(input)-1] == os.sep else input + os.sep

  if output:
    if ( os.path.isabs(output) ) is True:
      dest = output
    else:
      dest = input + output
  else:
    dest = input + 'transcoded'
  return dest

def generateIntermediateFolder (inputRoot, src, destRoot):
  if (inputRoot == src):
    return destRoot

  intermPath = src.replace(inputRoot,"")
  dest = destRoot + intermPath
  try:
    os.makedirs(dest)
  except: 
    log.debug('%s folder already exists', dest)
  return dest

if __name__ == '__main__': main()

