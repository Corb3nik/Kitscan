###									      ###
#	This class takes care of the manipulation of the online database	#
###									      ###

import requests
import json
import Classes
import LocalDatabase
##############################################
# Class for manipulating the online database #
##############################################
class OnlineDatabase : 

	####################
	# Get product data #
	####################
	def getProductForBarcode(self, p_barcode) : 
		
		r = requests.get("http://www.outpan.com/api/get_product.php?barcode=" + p_barcode)
		data = json.loads(r.text)
				
		# There is an error
		try : 	
			if (data["error"] != None) : 
				return None

		# There is no error
		except : 
			# Get name
			name = data["name"]

			# Get barcode
			barcode = data["barcode"]
				
		localDB = LocalDatabase.LocalDatabase()
		
		return localDB.addProductToDatabase(barcode, name, None, None, None, None)
