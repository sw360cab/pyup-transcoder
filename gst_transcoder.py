import os
import subprocess
import shlex
import string
import mimetypes
import t_logger
import file_timestamp

def transcodeFile (originalFilename,sourcePath,destPath, preserveDate=True,
  transcodingString='''gst-launch filesrc location=$src ! decodebin2 name=d d. ! queue ! \
  ffmpegcolorspace ! videoscale ! video/x-raw-rgb ! deinterlace ! ffmpegcolorspace ! \
  x264enc profile=1 ! mp4mux name=mux ! filesink location=$dest d. ! queue ! audioconvert ! audioresample ! faac ! mux.'''):
  #transcodingString='''gst-launch-1.0 filesrc location=$src ! decodebin name=d \
  #d. ! queue ! videoconvert ! videoscale ! video/x-raw ! \
  #videoconvert ! deinterlace ! x264enc ! video/x-h264,profile=main ! h264parse \
  #! mp4mux name=mux ! filesink location=$dest d. ! queue ! audioconvert ! \
  #audioresample ! faac ! mux.''') // lamemp3enc
  
  # transcode using GStreamer
  log = t_logger.getLogger(__name__)
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
  pipeline = transcodingTemplate.substitute(src='"'+sourceFile+'"',dest='"'+newFilePath+'"')
  log.warn('template %s', pipeline )

  # calling a shell GST process
  result = subprocess.call( shlex.split(pipeline) )

  log.info( ('OK' if result == 0 else 'NO')+' transcoding %s',newFilePath)
  if result != 0:
    raise RuntimeError('Unable to transcode file')
  
  # fixing file timestamp
  if (preserveDate) is True:
    log.info("Fixing timestamp for %s ", newFilePath)
    file_timestamp.copyFileTimestamp(sourceFile,newFilePath)
  
  return fileName + '.mp4', newFilePath

if __name__ == "__main__":
  import sys
  transcodeFile (sys.argv[1],sys.argv[2],sys.argv[3])
