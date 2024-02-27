import time
import Utility
import gatherLogData as gather

def intermediate_file(file_name):

    # Create intermediate file and open file with raw data
    clean_file_name = "Intermediate_" + file_name
    clean_file = open(clean_file_name, "a")
    input_file = open(file_name, "r")

    # Read the first line in 
    line = input_file.readline()

    # Iterate over all lines of the input file
    while line:

        try:
            # Write transactions to clean file
            items = line.split("\t")
            if len(items) == 7:

                transaction_hash = items[0]
                transaction_block = items[1]
                transaction_date = items[2]
                transaction_from = items[3]
                transaction_currency = items[4]
                transaction_currency_clean = Utility.transform_cryptocurrency(transaction_currency)
                transaction_method = items[5]
                transaction_amount = items[6].rstrip()

                log_data = gather.gather_log_data(transaction_block, transaction_method, transaction_from, transaction_currency)
                if (log_data[1] != -1):
                    borrowIndex = str(log_data[1])
                    if (transaction_method == "borrow"):
                        clean_file.write(transaction_hash + "\t" + transaction_block + "\t" + transaction_date + "\t" + transaction_from + "\t" + transaction_currency_clean + "\t" + transaction_method + "\t" + transaction_amount + "\t" + borrowIndex + "\n")
                    elif (transaction_method == "mint"):
                        clean_file.write(transaction_hash + "\t" + transaction_block + "\t" + transaction_date + "\t" + transaction_from + "\t" + transaction_currency_clean + "\t" + "deposit" + "\t" + transaction_amount + "\t" + borrowIndex + "\n")
                    elif (transaction_method == "redeem"):
                        if (log_data[0] != -1):
                            transaction_amount = str(log_data[0])
                            clean_file.write(transaction_hash + "\t" + transaction_block + "\t" + transaction_date + "\t" + transaction_from + "\t" + transaction_currency_clean + "\t" + "withdraw" + "\t" + transaction_amount + "\t" + borrowIndex + "\n")
                    elif (transaction_method == "redeemUnderlying"):
                        clean_file.write(transaction_hash + "\t" + transaction_block + "\t" + transaction_date + "\t" + transaction_from + "\t" + transaction_currency_clean + "\t" + "withdraw" + "\t" + transaction_amount + "\t" + borrowIndex + "\n")
                    elif (transaction_method == "repayBorrow"):
                        if transaction_amount[0] == '-':
                            if (log_data[0] != -1):
                                transaction_amount = str(log_data[0])
                                clean_file.write(transaction_hash + "\t" + transaction_block + "\t" + transaction_date + "\t" + transaction_from + "\t" + transaction_currency_clean + "\t" + "repay" + "\t" + transaction_amount + "\t" + borrowIndex + "\n")
                        else:                            
                            clean_file.write(transaction_hash + "\t" + transaction_block + "\t" + transaction_date + "\t" + transaction_from + "\t" + transaction_currency_clean + "\t" + "repay" + "\t" + transaction_amount + "\t" + borrowIndex + "\n")

        except Exception as exception:
            print(exception)

       # Suspend execution because of limit of five calls per sec.      
        line = input_file.readline()
        time.sleep(0.3)

    # Close files again
    input_file.close()
    clean_file.close()

    return clean_file_name