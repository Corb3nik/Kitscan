###									      ###
#	Reprensentations of the different elements in the local database	#
###									      ###


#####################################
# Represents a User in the database #
#####################################
class User : 
	def __init__(self, p_index, p_email, p_firstName, p_lastName, p_streetAddress,  p_zipCode, p_IDX_city, p_phoneNumber) :
		self.Index = p_index
		self.Email = p_email
		self.FirstName = p_firstName
		self.LastName = p_lastName
		self.StreetAddress = p_streetAddress
		self.ZipCode = p_zipCode
		self.IDX_City = p_IDX_city
		self.PhoneNumber = p_phoneNumber

########################################
# Represents a Product in the database #
########################################
class Product : 
	def __init__(self, p_index, p_barcode, p_name, p_company, p_category1, p_category2, p_category3) : 
		self.Index = p_index
		self.Barcode = p_barcode
		self.Name = p_name
		self.Company = p_company
		self.Category1 = p_category1
		self.Category2 = p_category2
		self.Category3 = p_category3

