
#pyup-transcoder
> a Python-based software to transcode videos and upload files to a remote server or S3-bucket

##Usage
	~$ python transcoder.py -h
	usage: transcoder.py [-h] -in INPUT [-out OUTPUT] [-r] [-t] [-up]
                     [-via {ftp,s3}] [-ftphost HOST] [-ftpport PORT]
                     [-ftpusername USERNAME] [-ftppassword PASSWORD]
                     [-ftpbasedir BASEDIR] [-ftppath PATH] [-s3keyid S3KEYID]
                     [-s3secretkey S3SECRETKEY] [-s3bucket BUCKET]
	
	A simple transcoder and uploader software
	
	optional arguments:
	  -h, --help            show this help message and exit
	  -in INPUT, --input INPUT
                        input folder
	  -out OUTPUT, --output OUTPUT
                        optional output folder
	-r, --removelocal     remove created files after execution
  	-t, --transcode       whether to transcode or not
  	-up, --upload         whether to upload or not
  	-via {ftp,s3}         upload with [ftp] or [s3]
  	-ftphost HOST         FTP host
  	-ftpport PORT         FTP port
  	-ftpusername USERNAME
                          FTP username
  	-ftppassword PASSWORD
  	                      FTP password
  	-ftpbasedir BASEDIR   FTP base directory to connect to
  	-ftppath PATH         FTP destination path to be created
  	-s3keyid S3KEYID      Your AWS Access Key ID
  	-s3secretkey S3SECRETKEY
                          Your AWS Secret Access Key
  	-s3bucket BUCKET      S3 bucket name
  	-f, --externalfile    whether parameters should be taken from an external
                        file
  	-extpath EXTPATH, --externalfilepath EXTPATH
                        path of external file contining parameters

_Note_ configuration parameters from command line take precedence over file ones.

## Trasconde

Trascoding is performed using GStreamer framework. 
Videos are encoded using a pipeline with the following features:

* H.264/AVC as video codec
* AAC as audio codec
* MP4 as container

A custom GStreamer pipeline can be provided via file (A basic knowledge of GStreamer is required)

## Upload

Upload is allowed via:

* FTP (authenticated/anonymous)
* Amazon Web Services S3 (exinsting/new Bucket)

Credentials and several options can be provided via file

## TODO
* OO version
* GStreamer via gst-python lib
* GUI
* FTP TLS
 