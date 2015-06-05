#!/usr/bin/env python

###	      	 	 ###
#	Run the server	   #
###	     	  	 ###

import socket
import Utilities
from threading import Thread
import netifaces as ni


HOST = ni.ifaddresses('eth0')[2][0]['addr']
PORT = 8080
MAX_CONNECT_REQUESTS = 5


import logging, logging.handlers
FORMAT = "%(asctime)s %(clientip)s %(levelname)s %(message)s"
logging.basicConfig(format=FORMAT,level=logging.INFO,datefmt='%Y-%m-%d %H:%M:%S', filename="../server.log")



############################################
# Create a socket and wait for connections #
############################################
def waitForConnections() : 

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((HOST, PORT))
	s.listen(MAX_CONNECT_REQUESTS)
	
	return s

#######################################
# Thread for handling client requests #
#######################################
def client_thread(p_clientSocket, p_clientip) :
	import re	
	import Classes
	import LocalDatabase
	import OnlineDatabase
	
	clientip = Utilities.convertTupleToList(p_clientip)
	extra = {"clientip": clientip[0]}
	extraServer = {"clientip": "SERVER"}

	message = p_clientSocket.recv(1024)

	logging.info("Received message " + message, extra=extra)
	components = message.split("/")
	
	# Message structure

	if (len(components) != 4 or len(message) > 64) : 
		logging.error("Invalid request : Message structure invalid", extra=extra)
		p_clientSocket.send("100")
		return -1


	# Barcode pattern
	barcode = components[0]
	UPCAPattern = r"^[0-9]{12}"
	UPCEPattern = r"^[0-9]{8}"
	EAN8Pattern = r"^[0-9]{8}"
	EAN13Pattern = r"^[0-9]{13}"


	if (re.match(UPCAPattern, barcode) == None and
	    re.match(UPCEPattern, barcode) == None and 
	    re.match(EAN8Pattern, barcode) == None and
	    re.match(EAN13Pattern, barcode) == None) : 
		logging.error("Invalid request : Invalid barcode", extra=extra)
		p_clientSocket.send("101")
		return -1
	

	# ScannerID pattern
	scannerID = components[1]
	scannerPattern = r"^[0-9]{1,15}"

	if (re.match(scannerPattern, scannerID) == None) : 
		logging.error("Invalid request : Invalid scanner ID", extra=extra)
		p_clientSocket.send("102")
		return -1


	# Input
	inputType = components[2]
	if (inputType != "0" and inputType != "1") : 
		logging.error("Invalid request : Invalid input type", extra=extra)
		p_clientSocket.send("103")
		return -1

	# Transaction number
	transactionNumber = components[3]
	transactionPattern = r"^[0-9]+"

	if (re.match(transactionPattern, transactionNumber) == None) : 
		logging.error("Invalid request : Invalid transaction number", extra=extra)
		p_clientSocket.send("104")
		return -1


	# Get product information
	try :
		localDB = LocalDatabase.LocalDatabase()
	except : 
		logging.critical("Can't connect to the local database.", extra=extraServer)
		p_clientSocket.send("107")
		return -1

	onlineDB = OnlineDatabase.OnlineDatabase()
	
	#print "Getting product " + barcode + " from local database"
	product = localDB.getProductForBarcode(barcode)

	#print "Getting user info from local database"
	user = localDB.getUserForScannerID(scannerID)
	
	# End the thread if the scanner isn't registered
	if (user == None) : 
		logging.error("Invalid request : The scanner " + scannerID + "has not been registered yet", extra=extra)
		p_clientSocket.send("106")
		return -1

	# Check if the transaction already exists
	if (not localDB.addTransaction(scannerID, transactionNumber, barcode, inputType)) :
		logging.warning("Invalid request : Transaction already exists", extra=extra)
		p_clientSocket.send("105")
		return -1
	

	# Check online databases for product information
	if (product == None) : 
		logging.info("Product " + barcode + " doesn't exist in local database", extra=extra)
		#print "Getting product " + barcode + " from online database"
		try : 
			product = onlineDB.getProductForBarcode(barcode)
		except : 
			logging.exception("Online database unavailable", extra=extra)

		# Add product to the database with only the barcode
		if (product == None) : 
			logging.info("Product " + barcode + " doesn't exist in online database", extra=extra)
			product = localDB.addProductToDatabase(barcode, None, None, None, None, None)
			p_clientSocket.send("999")
	
	# IN
	if (inputType == "1") : 
		logging.info("Adding product " + barcode + " to user #" + user.Index + "(" + user.Email + ") inventory.", extra=extra)
		localDB.addProductForUser(user, product)

	# OUT
	if (inputType == "0") :
		logging.info("Removing product " + barcode + " from user #" + user.Index + "(" + user.Email + ") inventory.", extra=extra)
		if (not localDB.removeProductForUser(user, product)) : 
			logging.info("User #" + user.Index + " does not have " + barcode + " in his inventory.", extra=extra)
			p_clientSocket.send("109")
			return -1
	
	p_clientSocket.send("OK")
	return 0
	
	

####################################
# Dispatch threads for each client #
####################################
def main() : 
		
	

	print "Waiting for connections at " + HOST + ":" + str(PORT)
	serverSocket = waitForConnections()
	
	while True : 
		
		(clientSocket, address) = serverSocket.accept()
		#print "Connection accepted for " + str(address)

		#print "Creating new thread"
		clientThread = Thread(target = client_thread, args = (clientSocket, address))

		#print "Starting thread"
		clientThread.start()
		
		

main()


		
	
