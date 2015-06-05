###									      ###
#	This class takes care of the manipulation of the local database		#
###									      ###

import Utilities
import Classes
import MySQLdb

#############################################
# Class for manipulating the local database #
#############################################
class LocalDatabase : 

	###########################
	# Connect to the database #
	###########################
	def __init__(self) :

		HOST = "localhost"
		PASSWD = "toor"
		USER = "root"
		DBName = "shopping"

		self.DB = MySQLdb.connect(host=HOST, passwd=PASSWD, user=USER, db=DBName)
		#print ("Connected to database")


	#####################################
	# Create User object from scannerID #
	#####################################
	def getUserForScannerID(self, p_scannerID) : 
		
		cursor = self.DB.cursor()
		
		cursor.execute("""
				SELECT *
				FROM TB_Users
				WHERE TB_Users.Index = (SELECT TB_Scanners.Index
							FROM TB_Scanners
							WHERE ScannerID = %s)
				""", (p_scannerID,))
		
		results = cursor.fetchone()

		if (results == None) : 
			return None

		results = list(results)
		
		cursor.close()

		return Classes.User(str(results[0]), str(results[1]), str(results[2]), 
					str(results[3]), str(results[4]), str(results[5]), 
					str(results[6]), str(results[7]))

	######################################
	# Create Product object from barcode #
	######################################
	def getProductForBarcode(self, p_barcode) : 

		cursor = self.DB.cursor()
		
		cursor.execute("""
				SELECT *
				FROM TB_Products
				WHERE Barcode = %s 
				""", (p_barcode, ))

		results = cursor.fetchone()

		if (results == None) : 
			return None
		
		results = Utilities.convertTupleToList(results)		

		cursor.close()

		return Classes.Product(str(results[0]), str(results[1]), str(results[2]), 
					str(results[3]), str(results[4]), str(results[5]), 
					str(results[6]))
	
	#########################################################
	# Check if the user has an entry for a specific product #
	#########################################################
	def userHasProduct(self, p_user, p_product) : 
		
		cursor = self.DB.cursor()
		
		cursor.execute("""
				SELECT Quantity
				FROM TB_UserInventoryContent
				WHERE IDX_User = %s AND IDX_Product = %s
				""", (p_user.Index, p_product.Index))

		results = cursor.fetchone()

		cursor.close()
		if (results == None) : 
			return None

		
		else : 
			return Utilities.convertTupleToList(results)[0]


	###############################################
	# Add a product entry to the user's inventory #
	###############################################
	def addProductForUser(self, p_user, p_product) : 
		

		cursor = self.DB.cursor()
		productQty = self.userHasProduct(p_user, p_product)

		# User already has that product
		if (productQty != None) : 

			cursor.execute("""
					UPDATE TB_UserInventoryContent
					SET Quantity = %s
					WHERE IDX_User = %s AND IDX_Product = %s
					""", (str(int(productQty) + 1), 
						p_user.Index, 
						p_product.Index))
			
			self.DB.commit()
		
		# User does not have that product
		else : 
			cursor.execute("""
					INSERT INTO TB_UserInventoryContent (IDX_User, IDX_Product, Quantity)
					VALUES (%s, %s, 1)
					""", (p_user.Index, p_product.Index))
	
			self.DB.commit()

		cursor.close()

	###################################################
	# Remove a product entry in the user's inventory #
	###################################################
	def removeProductForUser(self, p_user, p_product) : 
		
		cursor = self.DB.cursor()
		productQty = self.userHasProduct(p_user, p_product)
		

		# User already has that product
		if (int(productQty) > 0) : 
			
			cursor.execute("""
					UPDATE TB_UserInventoryContent
					SET Quantity = %s
					WHERE IDX_User = %s AND IDX_Product = %s
					""", (str(int(productQty) - 1), 
						p_user.Index, 
						p_product.Index))
			
			self.DB.commit()
			cursor.close()
			return True


		return False

	

	###############################################################
	# Add a transaction --- Returns a boolean for success/failure #
	###############################################################
	def addTransaction(self, p_scannerID, p_transactionNumber, p_barcode, p_inputType) : 

		cursor = self.DB.cursor()
		
		cursor.execute("""
				SELECT *
				FROM TB_TransactionHistory
				WHERE ScannerID = %s AND TransactionNumber = %s
				""", (p_scannerID, p_transactionNumber))

		results = cursor.fetchone()

		# The transaction doesn't exists.
		if (results == None) : 
			cursor.execute("""
					INSERT INTO TB_TransactionHistory (ScannerID, TransactionNumber, Barcode, InputType)
					VALUES (%s, %s, %s, %s)
					""", (p_scannerID, p_transactionNumber, p_barcode, p_inputType))

			self.DB.commit()
			cursor.close()
			return True
		
		# The transaction already exists.
		else : 
			cursor.close()
			return False
	
	#################################
	# Add a product to the database #
	#################################
	def addProductToDatabase(self, p_barcode, p_name, p_company, p_category1, p_category2, p_category3) : 

		

		cursor = self.DB.cursor()
			
		cursor.execute("""
				INSERT INTO TB_Products (Barcode, Name, IDX_Company, IDX_Category1, IDX_Category2, IDX_Category3)
				VALUES (%s, %s, %s, %s, %s, %s)
				""",(p_barcode, p_name, p_company, p_category1, p_category2, p_category3))

		self.DB.commit()

		cursor.close()

		return self.getProductForBarcode(p_barcode)
		
