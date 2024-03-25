import requests
import constants
import datetime

# Get request to receive transactions form Etherscan
def make_request(protocol, page, block_start, block_end):
    url_full = constants.REQUEST_API + constants.REQUEST_ACCOUNT + protocol + "&startblock=" + str(block_start) + "&endblock="+ str(block_end) + constants.REQUEST_PAGES_START + str(page) + constants.REQUEST_DETAILS      
    response = requests.get(url_full)
    if response.status_code == constants.REQUEST_OK:
        return response
    else:
        raise ValueError("Web request was unsuccessful")

# Transform response into json
def create_json(response):
    response_json = response.json()
    if response_json is None:
        raise TypeError("Cannot create json with valid value")
    else:
        return response_json
    
# Return length of json and avoid Nonetype error    
def get_length_safely(response_json, keyword):
    try:
        return (len(response_json[keyword]))
    except:
        return 0   
    
# Retrieve relevant transactional data
def retrieve_transactions(response_json, file):
    function_dictionary = {}
    cryptocurrency_dictionary = {}

    try:
        for transaction in response_json[constants.TRANSACTION_RESULT]:
            if transaction[constants.TRANSACTION_ERROR] == "0":

                # Retrieve relevant transactional data
                transaction_hash = transaction[constants.TRANSACTION_HASH]
                transaction_date = transaction[constants.TRANSACTION_DATE]
                transaction_from = transaction[constants.TRANSACTION_FROM]
                transaction_block = transaction[constants.TRANSACTION_BLOCK]
                transaction_function = retrieve_functions(transaction[constants.TRANSACTION_FUNCTION])
                transaction_method = transaction[constants.TRANSACTION_METHOD]
                transaction_input = transaction[constants.TRANSACTION_INPUT]
                transaction_currency = transaction[constants.TRANSACTION_TO]
                transaction_currency_clean = transform_cryptocurrency(transaction_currency)
                transaction_amount = retrieve_amount(transaction_method, transaction[constants.TRANSACTION_VALUE], transaction_input, transaction_currency_clean)
                
                # Aggregate cryptocurrency data
                if transaction_currency_clean not in cryptocurrency_dictionary:
                    cryptocurrency_dictionary[transaction_currency_clean] = 1
                else:
                    cryptocurrency_dictionary[transaction_currency_clean] += 1

                # Aggregate function data
                if transaction_function not in function_dictionary:
                    function_dictionary[transaction_function] = 1
                else:
                    function_dictionary[transaction_function] += 1

                # Write data to file
                if transaction_method in constants.COMPOUND_V2_RELEVANT_METHODS:
                    file.write(transaction_hash + "\t" + transaction_block + "\t" + transaction_date + "\t" + transaction_from + "\t" + transaction_currency_clean + "\t" + transaction_function + "\t" + str(transaction_amount) + "\n")

        return [cryptocurrency_dictionary, function_dictionary]
    except:
        return [cryptocurrency_dictionary, transaction_function]

# Estimate withdrawals and repayments
def estimate_amount(file, account, type, time, currency):
    amount: float = 0
    for line in file:
        items = line.split("\t")
        if (account == items[2]) and (currency == items[4]) and (int(time) > int(items[1])):
            if (type == "withdraw") and (items[3] == "supply"):
                amount = amount + float(items[5][:(len(items[5])- 2)])
            elif (type == "withdraw") and (items[3] == "withdraw") and (items[5][0] != '-'):
                amount = amount - float(items[5][:(len(items[5])- 2)])
            elif (type == "withdraw") and (items[3] == "withdraw") and (items[5][0] == '-'):
                return amount
            elif (type == "repay") and (items[3] == "borrow"):
                amount = amount + float(items[5][:(len(items[5])- 2)])
            elif (type == "repay") and (items[3] == "repay") and (items[5][0] != '-'):
                amount = amount - float(items[5][:(len(items[5])- 2)])
            elif (type == "repay") and (items[3] == "repay") and (items[5][0] == '-'):
                return amount
    return amount

# Transform account number to log format
def transform_to_64(account):
    short_number = account[2:len(account)]
    long_number = "0x000000000000000000000000" + short_number
    return long_number

# Transforms cryptocurrency address into code
def transform_cryptocurrency(cryptocurrency_address):
    if cryptocurrency_address in constants.POPULAR_CRYPTOCURRENCIES:
        return constants.POPULAR_CRYPTOCURRENCIES[cryptocurrency_address]
    else:
        return cryptocurrency_address

# Adjust amount for USDC, USDT, and WBTC
def clean_amount(amount_hex, currency):
    if (currency == "USDC"):
        return (int(amount_hex, 16) / 1000000)
    elif (currency == "USDT"):
        return (int(amount_hex, 16) / 1000000)
    elif (currency == "WBTC"):
        return (int(amount_hex, 16) / 100000000)
    else:
        return (int(amount_hex, 16) / 1000000000000000000)

# Retrieve cryptocurrency from input
def retrieve_cryptocurrency(method, input):
    if method in constants.COMPOUND_V2_RELEVANT_METHODS:
        cryptocurrency_address = "0x" + input[34:74]
        return cryptocurrency_address
    else:
        return "none"

# Retrieve borrow rate from log data
def retrieve_borrow_rate(data):
    length = len(data)
    rate_hex = data[(length - 64):length]
    return (int(rate_hex, 16) / 10000000000000000000000000)

# Retrieve supply rate from log data
def retrieve_supply_rate(data):
    rate_hex = data[2:66]
    return (int(rate_hex, 16) / 10000000000000000000000000)

# Retrieve variable borrow rate from log data
def retrieve_variable_borrow_rate(data):
    rate_hex = data[130:194]
    return (int(rate_hex, 16) / 10000000000000000000000000)

# Retrieve borrow index
def retrieve_borrow_index(data):
    rate_hex = data[66:130]
    return int(rate_hex, 16)

# Retrieve withdraw amount from log data
def retrieve_withdraw_amount(data, currency):
    amount_hex = data[66:130]
    return clean_amount(amount_hex, currency)

# Retrieve repay amount from log data
def retrieve_repay_amount(data, currency):
    amount_hex = data[130:194]
    return clean_amount(amount_hex, currency)

# Retrieve interest mode from log data
def retrieve_mode(data):
    length = len(data)
    rate_hex = data[(length - 128):(length - 64)]
    return int(rate_hex, 16)

# Retrieve amount from input
def retrieve_amount(method, value, input, currency):
    if method in constants.COMPOUND_V2_RELEVANT_METHODS:
        if constants.COMPOUND_V2_RELEVANT_METHODS.get(method) == "mint":
            return (int(value) / 1000000000000000000)
        else:
            length = len(input)
            amount_hexadecimal = input[(length - 64):length]
            if amount_hexadecimal == "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff":
                return -999999999999
            else:
                return clean_amount(amount_hexadecimal, currency)
        
# Retrieve function from functionName
def retrieve_functions(function_name):
    SEPARATOR = '('
    return function_name.split(SEPARATOR, 1)[0]

# Convert timeStamp into date
def format_date(time_stamp):
    return datetime.datetime.fromtimestamp(int(time_stamp)).strftime('%Y-%m-%d %H:%M:%S')

# Aggregate dictionaries
def aggregate_functions(dictionary_one, dictionary_two):
    for element in dictionary_one:
        if element not in dictionary_two:
            dictionary_two[element] = dictionary_one[element]
        else:
            dictionary_two[element] += dictionary_one[element]
    return (dictionary_two)

# Create new file
def create_file(protocol_name):
    current_time = datetime.datetime.now()
    file_name = protocol_name + current_time.strftime('%Y%m%d%H%M%S') + ".txt"
    return file_name
