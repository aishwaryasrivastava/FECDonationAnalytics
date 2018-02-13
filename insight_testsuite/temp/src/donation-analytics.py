#----------------------------------------- IMPORTS ---------------------------------------
import math
import sys

#---------------------------------------- CONSTANTS --------------------------------------
# Filenames
INPUT_FILENAME = sys.argv[1]
PERCENTILE_FILENAME = sys.argv[2]
OUTPUT_FILENAME = sys.argv[3]

# Indices of the fields we need (based on the data dictionary described by the FEC)
INDICES = [0,7,10,13,14,15]

# Months with 30 and 31 days (used when checking date validity)
THIRTY_DAY_MONTHS = [4,6,9,11]
THIRTYONE_DAY_MONTHS = [m for m in range(1,13) if m not in THIRTY_DAY_MONTHS and m!=2]

#------------------------------------- CLASS DEFINITION ----------------------------------

# Class to store information about each contribution.
class Contribution:
	"""A simple representation of a contribution.
	:param info: A list of values for this contribution
	"""
	def __init__(self, info):
		self.CMTE_ID = info[0]								# Recipient ID
		self.NAME = info[1]									# Donor name
		self.ZIP_CODE = info[2][0:5]						# Contributor zip code (only the first 5 digits)
		self.TRANSACTION_DATE = info[3]						# Date of transaction
		self.TRANSACTION_MONTH = self.TRANSACTION_DATE[0:2]	# Month of transaction
		self.TRANSACTION_DAY = self.TRANSACTION_DATE[2:4]	# Day of transaction
		self.TRANSACTION_YEAR = self.TRANSACTION_DATE[4:]	# Year of transaction
		self.TRANSACTION_AMT = info[4]						# Amount of transaction
		self.OTHER_ID = info[5]								# Person donor or entity donor? (empty string if donor is a person!)
		self.UNIQUE_ID = self.NAME+self.ZIP_CODE			# The unique ID of the contribution

#--------------------------------------- METHOD DEFINITIONS --------------------------------
# Method to calculate the P-th percentile of the values in number_list using the nearest-rank method
def percentile(number_list, P):
	number_list.sort()
	n = math.ceil(P*len(number_list)/100)
	#return number_list[n-1]
	return number_list[n-1]

# Return true if year is a leap year, false otherwise.
def isLeapYear(year):
	if year % 4 != 0:
		return False
	elif year % 100 != 0:
		return True
	elif year % 400 != 0:
		return False
	else:
		return True

# Check the validity of the contribution record as stated in the "Input file considerations" section of the README
def isValidRecord(contribution):
	valid = True
	# Check if non-entity donor
	valid &= contribution.OTHER_ID == ""
	# Check if transaction date is valid
	day, month, year = int(contribution.TRANSACTION_DAY), int(contribution.TRANSACTION_MONTH), int(contribution.TRANSACTION_YEAR)
	valid &= contribution.TRANSACTION_DATE != ""
	valid &= (month in THIRTY_DAY_MONTHS and day <= 30) or (month in THIRTYONE_DAY_MONTHS and day <= 31) or (month == 2 and isLeapYear(year) and day == 29)
	# Check if valid zip code
	valid &= len(contribution.ZIP_CODE) >= 5
	# Check if valid name
	if(contribution.NAME.count(",") == 1):
		fname,lname = contribution.NAME.split(",")
		valid &= fname != "" and lname != ""
	# Check other information
	valid &= contribution.CMTE_ID != "" and contribution.TRANSACTION_AMT != ""
	return valid

# Returns a list of only relevant information according to INDICES
def isolateInformation(info):
	return [info[i] for i in INDICES]

# Return true if c1 and c2 are repeat donations, false otherwise.
def areRepeatDonations(c1, c2):
	return c1.CMTE_ID == c2.CMTE_ID and c1.TRANSACTION_YEAR == c2.TRANSACTION_YEAR and c1.ZIP_CODE == c2.ZIP_CODE

# Write information about cont with respect to all_conts in output_file (assume it is open and writeable)
def printRepeatDonors(output_file, cont, all_conts):
	output_file.write(cont.CMTE_ID+"|")
	output_file.write(cont.ZIP_CODE+"|")
	output_file.write(cont.TRANSACTION_YEAR+"|")
	output_file.write(str(percentile(all_conts,P))+"|")
	output_file.write(str(sum(all_conts))+"|")
	output_file.write(str(len(all_conts)))
	output_file.write("\n")

#--------------------------------------- MAIN --------------------------------------------

# Reading the percentile
percentile_file = open(PERCENTILE_FILENAME,"r")
for line in percentile_file:
	if line != "":
		P = int(line)
percentile_file.close()

# Opening the input file for reading
input_file = open(INPUT_FILENAME,"r")

# Opening output file for writing
output_file = open(OUTPUT_FILENAME,"w+")

# List of all processed contributions (instances of class Contribution)
processed_conts = []

# Read input file
for line in input_file:
	all_info = line.split("|")
	cont_info = isolateInformation(all_info)
	cont = Contribution(cont_info)
	# Throw away invalid records
	if (isValidRecord(cont)):
		# Find repeat donors
		if (cont.UNIQUE_ID in [x.UNIQUE_ID for x in processed_conts]):
			repeat_conts = [int(x.TRANSACTION_AMT) for x in processed_conts if areRepeatDonations(x, cont)]
			repeat_conts.append(int(cont.TRANSACTION_AMT))
			printRepeatDonors(output_file, cont, repeat_conts)
		processed_conts.append(cont)
		
input_file.close()
output_file.close()