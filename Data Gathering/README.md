# Data Gathering

This is a simple application for the extraction of Ethereum on-chain transactions with the Etherscan.io APIs. The source code is designed for the free API plan (limited to five calls per second). Some parts of this application are DeFi system-specific (Compound V2), and this application is broken down into the following parts:

* createTransactionFile  :   Pull raw transaction data and save data locally
* createIntermediateFile :   Add borrow index from logs to transaction data (Compound V2) 
* createCompleteFile     :   Create complete file by replacing the borrow index with interest rates (Compound V2) 
* computeRatesCompound   :   Compute interest rates based on borrow index (Compound V2)  
* gatherLogData          :   Pull borrow index from transaction log (Compound V2)  
* constants              :   Collection of constants such as addresses on the Ethereum blockchain or method ids
* utility                :   Collection of helper functions

Please note that mass-API calls do not seem to be working reliably with the free plan. Please consult the Compound documation for information about the calculation of interest rates (https://docs.compound.finance/v2/#protocol-math).
