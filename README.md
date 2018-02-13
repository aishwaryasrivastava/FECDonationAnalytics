# Insight Data Engineering Fellowship Coding Challenge
#### Submission Details
Aishwarya Srivastava on Feb 13, 2018.

EMAIL: aishwaryasrivastava@mail.com

PHONE: (614) 815-0930

# Introduction
`src\donation-analytics.py` is a program written in Python3 that processes the list of contributions in `input\itcont.txt` and writes the number of repeat donations made to a recipient in the same year and area on the provided output file. The program reads value P from `input\percentile.txt` to calculate and write the Pth percentile of each repeat donation. The format of the output file is the same as provided in the coding challenge description.

# Usage
The following command can be used to run the program:

`python3 ./src/donation-analytics.py ./input/itcont.txt ./input/percentile.txt ./output/repeat_donors.txt`

where `./src/donation-analytics.py` is the program,
`./input/itcont.txt` is the list of contributions, `./input/percentile.txt` holds the value P for calculating the P-th percentile, and `./output/repeat_donors.txt` is the file on which the output will be written. 
Alternatively, the shell script `run.sh` can also be run from the root folder.

#### A note about the Python version and libraries: 
This program is written in Python3, which has a few extra functionalities than the older versions. Therefore, running the program in any other version may cause issues. Also, the program makes use of 2 python libraries, namely `math.py` and `sys.py`, so making sure that these libraries are installed and functional is encouraged.

# Approach
The program makes use of object oriented encapsulation to hold each contribution's information in an instance of the `Contribution` class. There are also many functions that help in calculation and checking the input validity, such as `percentile(number_list, P)` that calculates the nearest-rank method to calculate the `P`th percentile of `number_list`, `isValidRecord(contribution)` that checks whether the information held by the `contribution` object (an instance of the `Contribution` class) is valid i.e. doesn't have empty values for fields and has a legal value for the date of transaction (read more in the `Checking input validity` section). The main program reads each record line by line, and processes it during run-time. This means that the program checks the validity of the records, determines if it is a repeat contribution, and writes the relevant information on the output file, all at run-time.

#### Checking input validity
The program makes sure that all input processed is valid and not malformed. For example, when reading the transaction date, the program makes sure that dates like "29 Feb 2015" are not accepted, as such a date would not exist in real life. The program also checks the form of the donor name - it checks for the existance of a ",", and makes sure the first and last name that it separates are not empty strings. Other than that, the program also checks for other non-empty fields, as specified in the project description.
