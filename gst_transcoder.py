import os
import subprocess
import string
import mimetypes
import t_logger

def transcodeFile (originalFilename,sourcePath,destPath,
  transcodingString='''gst-launch filesrc location=$src ! decodebin2 name=d d. ! queue ! ffmpegcolorspace ! videoscale ! deinterlace !   
  x264enc profile=1 ! mp4mux name=mux ! filesink location=$dest d. ! queue ! audioconvert ! audioresample ! faac ! mux.'''):
  print transcodingString
  # transcode using GStreamer
  log = t_logger.setup(__name__)
  log.debug('current file is: %s', originalFilename)
  sourceFile = sourcePath + os.sep + originalFilename

  videoType = mimetypes.guess_type(sourceFile)
  if ( videoType[0] is None or string.find( videoType[0],"video" ) < 0):
    log.debug('Not a video file')
    return originalFilename, sourceFile

  fileName, fileExtension = os.path.splitext(originalFilename)
  # Start transcoding
  newFilePath = destPath + os.sep + fileName + ".mp4"
  log.debug('new file will be: %s', newFilePath)

  transcodingTemplate = string.Template(transcodingString)
  pipeline = transcodingTemplate.substitute(src=sourceFile,dest=newFilePath)
  log.warn('template %s', pipeline )

  # calling a shell GST process
  result = subprocess.call( pipeline.split(" ") )

  log.info( ('OK' if result == 0 else 'NO')+' transcoding %s',newFilePath)
  if result != 0:
    raise RuntimeError('Unable to transcode file')

  return fileName + '.mp4', newFilePath

if __name__ == "__main__":
  import sys
  transcodeFile (sys.argv[1],sys.argv[2],sys.argv[3])