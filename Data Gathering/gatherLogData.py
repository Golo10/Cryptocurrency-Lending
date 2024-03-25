import requests
import constants
import utility

# Gather data from transaction log
def gather_log_data(block_number, method, account, asset):
    try:

        # Local variables
        page_number = 1

        # Fire API requests and aggregate data
        url_full = constants.REQUEST_API + constants.REQUEST_LOG + constants.COMPOUND_cETHv2 + constants.REQUEST_BLOCK_START + str(block_number) + constants.REQUEST_BLOCK_END + str(block_number) + constants.REQUEST_PAGES_START + str(page_number) + constants.REQUEST_DETAILS
        response = requests.get(url_full)

        if response.status_code == constants.REQUEST_OK:
            response_json = utility.create_json(response)
            response_json_transactions = utility.get_length_safely(response_json, constants.LOG_TOPICS)

            if response_json_transactions == 0:
                borrowIndex = get_borrow_index(response_json)
                if (borrowIndex > 0):
                    if method == "borrow":
                        return [0, borrowIndex]
                    elif method == "mint":
                        return [0, borrowIndex]
                    elif method == "redeem":
                        return [get_withdraw_amount(response_json, asset, account), borrowIndex]
                    elif method == "redeemUnderlying":
                        return [0, borrowIndex]
                    elif method == "repayBorrow":
                        return [get_repay_amount(response_json, asset, account), borrowIndex]
        return [-1, -1]
    
    except Exception as exception:
        print(exception)

# Get withdraw amount from log data
def get_withdraw_amount(response_json, asset_address, account_number):
    for log in response_json[constants.LOG_RESULT]:
        if (constants.TOPIC_WITHDRAW_COMPOUND_V2 in log[constants.LOG_TOPICS]):
            return utility.retrieve_withdraw_amount(log[constants.LOG_DATA], utility.transform_cryptocurrency(asset_address))
    return -1

# Get repay amount from log data
def get_repay_amount(response_json, asset_address, account_number):
    for log in response_json[constants.LOG_RESULT]:
        if (constants.TOPIC_REPAY_COMPOUND_V2 in log[constants.LOG_TOPICS]):
            return utility.retrieve_repay_amount(log[constants.LOG_DATA], utility.transform_cryptocurrency(asset_address))
    return -1

# Get borrow index
def get_borrow_index(response_json):
    for log in response_json[constants.LOG_RESULT]:
        if (constants.TOPIC_INTEREST_TWO_COMPOUND_V2 in log[constants.LOG_TOPICS]):
            return utility.retrieve_borrow_index(log[constants.LOG_DATA])
    return -1