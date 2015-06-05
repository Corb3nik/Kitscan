#! /usr/bin/env python

###			      ###	
#	Runs the scanner	#	  
###			      ###

import re

###################################
# Get the next transaction number #
###################################
def getTransactionNumber() :
	
	try :
		f = open("transactionNumber", "r+") 
		transactionNumber = int(f.read())
		f.close()

	except : 
		transactionNumber = 1

	f = open("transactionNumber", "w")
	f.write(str(transactionNumber + 1))
	f.close()

	print ("Transaction number : " + str(transactionNumber))

	transactionPattern = r"^[0-9]+"

	if (re.match(transactionPattern, str(transactionNumber)) == None) : 
		return -1

	return str(transactionNumber)
	

#################################
# Get the barcode from the user #
#################################
def getBarcode() : 
	
	barcode = raw_input("Barcode :  ")

	# Validate barcode pattern
	barcodePattern = r"^[0-9]{8,14}"

	if (re.match(barcodePattern, barcode) == None) : 
		return -1

	return barcode


###############################################
# Get the input type (1 = Input | 0 = Output) #
###############################################
def getInputType() : 
	

	inputType = raw_input("Input Type (0 | 1) : ")
	if (inputType != "0" and inputType != "1") : 
		return -1

	return inputType


######################
# Get the scanner ID #
######################
def getScannerID() : 
	from uuid import getnode as get_mac

	# ScannerID pattern
	scannerPattern = r"^[0-9]{1,15}"

	if (re.match(scannerPattern, str(get_mac())) == None) : 
		return -1

	print ("Scanner Id : " + str(get_mac()))
	return str(get_mac())


##############################
# Send information to server #
##############################
HOST = "10.10.10.105"
PORT = 8080
def sendToServer(p_barcode, p_scannerID, p_inputType, p_transactionNumber) : 
	import socket
	
	print ("Sending information to server")

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	try : 
		s.connect((HOST, PORT))
		s.send(p_barcode + "/" + p_scannerID + "/" + p_inputType + "/" + p_transactionNumber)
		msg =  s.recv(1024)

	except Exception,e: 
		print ("Aborting : The server is currently offline")
		return "108"

	print ("Receiving response : " + msg)

	return msg

########################
# Translate error code #
########################
def translateErrorCode(p_errorCode) : 

	if (p_errorCode == "100") : 
		print "Message sent invalid : Please try again."
		return 

	if (p_errorCode == "101") : 
		print "The barcode you have entered isn't supported."
		return

	if (p_errorCode == "102") :
		print "Scanner ID invalid : Please try again." 
		return

	if (p_errorCode == "103") :
		print "Input type invalid : Please try again." 
		return

	if (p_errorCode == "104") :		
		print "Transaction number invalid : Please try again" 
		return

	if (p_errorCode == "105") :
		print "This transaction already exists : Please try again." 
		return
		
	if (p_errorCode == "106") : 
		print "This scanner has not been registered yet : Please register it."
		return

	if (p_errorCode == "107") : 
		print "The server is currently experiencing some problems : Please try again later."
		return

	if (p_errorCode == "108") : 
		print "Can't connect to the server : Please verify your internet connection and try again."
		return
	
	if (p_errorCode == "109") : 
		print "You are trying to remove an item that doesn't exist in your inventory."
		return

	if (p_errorCode == "999") : 
		print "Your item is missing some info, please put your item aside and complete the missing info online."
		return	
	else : 
		print "An unknown error has occurred. Please try again."
		return




########
# Main #
########
def main() : 
	
	while (True) : 
		# Check barcode
		barcode = getBarcode()

		if (barcode == -1) : 
			print ("Invalid barcode...")
			continue
		
		# Check Scanner ID
		scannerID = getScannerID()
		
		if (scannerID == -1) : 
			print ("Invalid Scanner ID...")
			continue 		
			
		# Check input type
		inputType = getInputType()

		if (inputType == -1) : 
			print ("Invalid input type...")
			continue

		# Check transaction number
		transactionNumber = getTransactionNumber()

		if (transactionNumber == -1) : 
			print ("Invalid transaction number")
			continue

		# Send to server and analyze response
		response = sendToServer(barcode, scannerID, inputType, transactionNumber)

		if (response == "OK") : 
			print ("Transaction completed successfully")
	
		else : 
			translateErrorCode(response)
	
		print "###########"


main()


	

	
	
		
