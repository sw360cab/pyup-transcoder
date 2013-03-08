import ftplib
import t_logger

def connect(ftpparams):
  ftp = ftplib.FTP()
  
  global log
  
  log= t_logger.setup(__name__)

  ftp.connect(ftpparams.host, ftpparams.port)
  if (hasattr(ftpparams,'username')):
    ftp.login(ftpparams.username, ftpparams.password)
  if (hasattr(ftpparams,'basedir')):
    ftp.cwd(ftpparams.basedir)
  
  if (hasattr(ftpparams,'path')):
    path = ftpparams.path
    try:
      ftp.mkd(path)
    except ftplib.error_perm, resp:
      if str(resp) == '550 ' + path + ': File exists':
        log.debug('Directory already exists')
      else:
        raise
    ftp.cwd(ftpparams.basedir+path)

  return ftp

def upload(ftp,fileName,filePath):
  log.info('FTP upload of %s started @ %s:%s',fileName,ftp.host,ftp.port)
  ftp.storbinary("STOR " + fileName, open(filePath, "rb"),1024)
  log.info('FTP trasfer of %s completed',fileName)

