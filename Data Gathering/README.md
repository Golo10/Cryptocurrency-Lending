

* createTransactionFile  :   Pull raw transaction data and save data locally
* createIntermediateFile :   Add borrow index from logs to transaction data (Compound V2) 
* createCompleteFile     :   Create complete file by replacing the borrow index with interest rates (Compound V2) 
* computeRatesCompound   :   Compute interest rates based on borrow index (Compound V2)  
* gatherLogData          :   Pull borrow index from transaction log (Compound V2)  
* constants              :   Collection of constants such as addresses on the Ethereum blockchain or method ids
* utility                :   Collection of helper functions

Mass-API calls do not seem to be working reliably with the free plan. 
