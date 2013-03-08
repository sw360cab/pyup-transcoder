import logging

def setup (appName):
  fmt = '%(asctime)s %(name)-10s %(levelname)-6s %(message)s'
  logging.basicConfig(level=logging.DEBUG,
                      format=fmt,
                      datefmt='%m/%d/%y %H:%M',
                      filename='transcoder.log',
                      filemode='w')
  # define a Handler which writes INFO messages or higher to the sys.stderr
  console = logging.StreamHandler()
  console.setLevel(logging.INFO)
  formatter = logging.Formatter(fmt)
  console.setFormatter(formatter)
  # add the handler to the root logger
  logging.getLogger('').addHandler(console)
  logging.debug('Logger setup completed')
  return logging.getLogger(appName)

