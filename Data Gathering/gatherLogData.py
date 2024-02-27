import requests
import Constants
import Utility

# Gather data from transaction log
def gather_log_data(block_number, method, account, asset):
    try:

        # Local variables
        page_number = 1

        # Fire API requests and aggregate data
        url_full = Constants.REQUEST_API + Constants.REQUEST_LOG + Constants.COMPOUND_cETHv2 + Constants.REQUEST_BLOCK_START + str(block_number) + Constants.REQUEST_BLOCK_END + str(block_number) + Constants.REQUEST_PAGES_START + str(page_number) + Constants.REQUEST_DETAILS
        response = requests.get(url_full)

        if response.status_code == Constants.REQUEST_OK:
            response_json = Utility.create_json(response)
            response_json_transactions = Utility.get_length_safely(response_json, Constants.LOG_TOPICS)

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
    for log in response_json[Constants.LOG_RESULT]:
        if (Constants.TOPIC_WITHDRAW_COMPOUND_V2 in log[Constants.LOG_TOPICS]):
            return Utility.retrieve_withdraw_amount(log[Constants.LOG_DATA], Utility.transform_cryptocurrency(asset_address))
    return -1

# Get repay amount from log data
def get_repay_amount(response_json, asset_address, account_number):
    for log in response_json[Constants.LOG_RESULT]:
        if (Constants.TOPIC_REPAY_COMPOUND_V2 in log[Constants.LOG_TOPICS]):
            return Utility.retrieve_repay_amount(log[Constants.LOG_DATA], Utility.transform_cryptocurrency(asset_address))
    return -1

# Get borrow index
def get_borrow_index(response_json):
    for log in response_json[Constants.LOG_RESULT]:
        if (Constants.TOPIC_INTEREST_TWO_COMPOUND_V2 in log[Constants.LOG_TOPICS]):
            return Utility.retrieve_borrow_index(log[Constants.LOG_DATA])
    return -1