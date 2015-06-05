###			      ###
#	Useful methods		#
###			      ###


###############################
# Convert a tuple into a list #
###############################
def convertTupleToList(p_tuple) : 

	string = str(p_tuple)
	string = string.replace("L,", "")
	string = string.replace("(", "")
	string = string.replace(")", "")

	return string.split(" ")
