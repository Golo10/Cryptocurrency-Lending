# Import packages
import time

# Import additional files
import Utility
import Constants

# Request Constants
REQUEST_MAX_BLOCKS = 17588468 
REQUEST_MIN_BLOCKS = 12000000
REQUEST_LIMIT_BLOCKS = 10000
REQUEST_MIN_PAGES = 1

# Global variables to gather data
page_number = 1
transactions_number = 0
block_number_end = REQUEST_MAX_BLOCKS
block_number_start = block_number_end - REQUEST_LIMIT_BLOCKS
transactions_array = []
function_dictionary = {}
cryptocurrency_dictionary = {}

# Create and open file
file_name = Utility.create_file("Compound_cETHv2_")
file = open(file_name, "a")

# Fire API requests and aggregate data
try:
    while ((page_number < Constants.REQUEST_MAX_PAGES) and (block_number_start > REQUEST_MIN_BLOCKS)):

        # Fire API request, read data in, and increment variables
        response = Utility.make_request(Constants.COMPOUND_cETHv2, page_number, block_number_start, block_number_end)
        response_json = Utility.create_json(response)
        response_json_transactions = Utility.get_length_safely(response_json, "result")

        if response_json_transactions == 0:
            page_number = 1
            block_number_end = block_number_start - 1
            block_number_start = block_number_start - REQUEST_LIMIT_BLOCKS
        else:
            transactions_number = transactions_number + response_json_transactions
            page_number = page_number + 1
            transactions_array = Utility.retrieve_transactions(response_json, file)
            function_dictionary = Utility.aggregate_functions(function_dictionary, transactions_array[1])
            cryptocurrency_dictionary = Utility.aggregate_functions(cryptocurrency_dictionary, transactions_array[0])
 
        # Suspend execution because of limit of five calls per sec.
        time.sleep(0.5)
except ValueError:  
    print("Parsed through all pages")
except Exception as exception:
    print(exception)

file.close()

print("Total number of transactions: " + str(transactions_number))
print(function_dictionary)
print(cryptocurrency_dictionary)
