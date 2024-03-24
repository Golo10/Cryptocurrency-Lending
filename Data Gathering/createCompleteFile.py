import computeRatesCompound as utliity

def complete_file(file_name):

    # Create complete file and open file with raw data
    clean_file_name = "Complete_" + file_name
    clean_file = open(clean_file_name, "a")
    input_file = open(file_name, "r")

    # Read the first line in 
    line = input_file.readline()
    items = line.split("\t")
    if len(items) == 8:
        transaction_hash = items[0]
        transaction_block = items[1]
        transaction_date = items[2]
        transaction_from = items[3]
        transaction_currency = items[4]
        transaction_method = items[5]
        transaction_amount = items[6]
        transaction_borrow_index = items[7].rstrip()

        # Iterate over all lines of the input file
        line = input_file.readline()
        while line:

            # Read the next line in 
            items = line.split("\t")
            if len(items) == 8:
                transaction_hash_t1 = items[0]
                transaction_block_t1 = items[1]
                transaction_date_t1 = items[2]
                transaction_from_t1 = items[3]
                transaction_currency_t1 = items[4]
                transaction_method_t1 = items[5]
                transaction_amount_t1 = items[6]
                transaction_borrow_index_t1 = items[7].rstrip()

                # Get rates for Compound
                rates = utliity.compoundInterface(transaction_borrow_index, transaction_borrow_index_t1, transaction_block, transaction_block_t1, transaction_currency)
                transaction_rate = str(rates[0])
                if ((transaction_method == "borrow") or (transaction_method == "repay")):
                    transaction_rate = str(rates[1])

                # Write transactions to clean file
                clean_file.write(transaction_hash + "\t" + transaction_block + "\t" + transaction_date + "\t" + transaction_from + "\t" + transaction_currency + "\t" + transaction_method + "\t" + transaction_amount + "\t" + transaction_rate + "\n")

                # Copy current values from t+1
                transaction_hash = transaction_hash_t1
                transaction_block = transaction_block_t1
                transaction_date = transaction_date_t1
                transaction_from = transaction_from_t1
                transaction_currency = transaction_currency_t1
                transaction_method = transaction_method_t1
                transaction_amount = transaction_amount_t1
                transaction_borrow_index = transaction_borrow_index_t1

            # Increment line and wait        
            line = input_file.readline()

        # Close files again
        input_file.close()
        clean_file.close()

    return clean_file_name
