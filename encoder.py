import sys
import getpass
import os.path
from Crypto.Cipher import AES
from Crypto.Hash import SHA512
from subprocess import call

def getFileNameFromInput (argv, maxSize):
	if len(argv) < 3:
		print "No input file specified."
		return None

	filename = argv[2]

	if not os.path.isfile(filename):
		print "This is not a file."
		return None
	
	if os.stat(filename).st_size > maxSize*1024*1024:
		print "The file is too big. Max size is:", maxSize, "mega bytes."
		return None
	
	return filename
	
def getPasswordFromStdIn(text):
	password = getpass.getpass(text)
	
	#if len(password) < 1:
	#	print "Password is too short, please input at least 1 character."
	#	return None
	return password

def isHelpMode(argv):
	for i in xrange(1, len(argv)):
		if argv[i] == "-h" or argv[i] == "--help":
			return True
	return False	

def helpMode():
	print """Usage:
	Syntax: 
		python encoder OPERATION FILE 
	Valid value for OPERATION: 
		-h 
			prints this usage and exits 
		-e | --encrypt
			encrypts the specified FILE
		-d | --decrypt
			decrypts the specified FILE
		-r | --read
			shows the content of the specified FILE after
			a decryption and encrypts the file automatically with the 
			same specified password after reading.
		-w | --write
			opens the specified FILE for reading/writing after
			a decryption and encrypts the file automatically with the 
			same specified password after editing.
	Valid value for FILE: 
		the local path to an existing file. """
	
def enum(**enums):
    return type('Enum', (), enums)
	
def getMode(argv, mode):
	if isHelpMode(argv):
		return mode.HELP
	for i in xrange(1, len(argv)):
		if argv[i] == "-e" or argv[i] == "--encrypt":
			return mode.ENCRYPT
		if argv[i] == "-d" or argv[i] == "--decrypt":
			return mode.DECRYPT
		if argv[i] == "-r" or argv[i] == "--read":
			return mode.READ
		if argv[i] == "-w" or argv[i] == "--write":
			return mode.WRITE
			
	print "No valid mode could be recognized. Please read the help section again."
	return None

def pad(s, blocksize, padding):
	return s + (blocksize - len(s) % blocksize) * padding

def unpad(s, padding):
	while s[len(s)-1] == padding:
		s = s[:len(s)-2]
	return s
	
def createNewFileName(cryptMode, mode, filename, encryptExt, decryptExt, readWriteExt):
	if mode == cryptMode.ENCRYPT and filename[-3:] == decryptExt:
		return filename[:-3] + encryptExt
	if mode == cryptMode.ENCRYPT:
		return filename + encryptExt
	if mode == cryptMode.DECRYPT and filename[-3:] == encryptExt:
		return filename[:-3] + decryptExt
	if mode == cryptMode.READ or mode == cryptMode.WRITE:
		return filename + readWriteExt
	return None

def calcHash(pw):
	h = SHA512.new()
	h.update(pw)
	return h.hexdigest()
	
def encryptFile(fileContent, password, newFileName, blocksize, padding):
	cipher = pad(fileContent, blocksize, padding)
	for i in xrange(4):
		encrypter = AES.new(password[i*32:i*32+32], AES.MODE_CBC, password[i*32:i*32+16])
		cipher = encrypter.encrypt(cipher)

	open(newFileName, 'w').close()
	newFile = open(newFileName, 'w')
	newFile.write(cipher)
	newFile.close()
	
def decryptFile(plaintext, password, newFileName, padding):
	for i in xrange(3, -1, -1):
		decrypter = AES.new(password[i*32:i*32+32], AES.MODE_CBC, password[i*32:i*32+16])
		plaintext = decrypter.decrypt(plaintext)	
	
	plaintext = unpad(plaintext, padding)
	open(newFileName, 'w').close()
	newFile = open(newFileName, 'w')
	newFile.write(plaintext)
	newFile.close()

#
# ======================================================================
#

cryptMode = enum(ENCRYPT=1, DECRYPT=2, READ=3, WRITE=4, HELP=5)
	
# Maximale Groesse der Datei in mb, die verschluesselt werden kann.
maxFileSize = 100
# was an das File angehaengt wird beim Verschluesseln.
fileExtensionEncrypt = "_en"
# was an das File angehaengt wird beim Verschluesseln.
fileExtensionDecrypt = "_de"
fileExtensionTmp	 = "_tmp_DELETE_THIS_FILE"
padding = '{'
blocksize = 32

# Zu verschluesselnde Datei.
filename = getFileNameFromInput(sys.argv, maxFileSize)
if filename == None:
	helpMode()
	exit(0)

fileContent = open(filename).read()
	
# Passwort fuer die eigentliche Verschluesselung.
password = getPasswordFromStdIn("Please enter the password for the en/decryption: ")
if password == None:
	exit(0)
	
password = calcHash(password)

mode = getMode(sys.argv, cryptMode)
if mode == cryptMode.HELP or mode == None:
	helpMode()
	exit(0)

newFileName = createNewFileName(cryptMode, mode, filename, fileExtensionEncrypt, fileExtensionDecrypt, fileExtensionTmp)
if newFileName == None:
	print "The specified file doesn't seem to be a file encrypted with this tool. Try a file with the ending 'en'."
	exit(0)

if mode == cryptMode.ENCRYPT:
	encryptFile(fileContent, password, newFileName, blocksize, padding)
	exit(0)
	
if mode == cryptMode.DECRYPT:
	decryptFile(fileContent, password, newFileName, padding)
	exit(0)

if mode == cryptMode.READ:
	decryptFile(fileContent, password, newFileName, padding)
	call(["less", newFileName])
	call(["rm", "-rf", newFileName])
	exit(0)
	
if mode == cryptMode.WRITE:
	decryptFile(fileContent, password, newFileName, padding)
	call(["nano", newFileName])	
	newEncryptFileName = createNewFileName(cryptMode, cryptMode.ENCRYPT, filename, fileExtensionEncrypt, fileExtensionDecrypt, fileExtensionTmp)
	newFileContent = open(newFileName).read()
	call(["rm", "-rf", newFileName])
	encryptFile(newFileContent, password, newEncryptFileName, blocksize, padding)	
	exit(0)






