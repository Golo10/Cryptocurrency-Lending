import numpy as np
import solver as sv
import regression as rg

#Local constants
path = "/Golo10/Cryptocurrency-Lending/Empirical Analysis/"
input_file_name = path + "Aave2 DAI.csv"

#Open file
file = open(input_file_name, "r")

#Local arrays
y_gls = np.array([])  
y_gls_eth = np.array([])
x_btc_ewer = np.array([])
x_eth_ewer = np.array([])
x_btc_tsmom = np.array([])
x_eth_tsmom = np.array([])

#Skip headline of input file
line = file.readline()

#Iterate over all lines of the file
count_btc = 0
count_eth = 0
line = file.readline()
while line:
    items = line.split(";")
    if len(items) == 29:
        output_array = sv.transform_input_array(items)
        if (isinstance(output_array[0], float) and isinstance(output_array[2], float) and isinstance(output_array[4], float)):
            if (count_btc == 0):
                y_gls = np.append(y_gls, np.array([output_array[0]]))
                x_btc_ewer = np.append(x_btc_ewer, np.array([output_array[4]]))
                x_btc_tsmom = np.append(x_btc_tsmom, np.array([output_array[2]]))
                count_btc = count_btc + 1
            elif (count_btc >= 29):
                count_btc = 0
            else:
                count_btc = count_btc + 1
        if (isinstance(output_array[0], float) and isinstance(output_array[5], float) and isinstance(output_array[3], float)):
            if (count_eth == 0):
                y_gls_eth = np.append(y_gls_eth, np.array([output_array[0]]))
                x_eth_ewer = np.append(x_eth_ewer, np.array([output_array[5]]))
                x_eth_tsmom = np.append(x_eth_tsmom, np.array([output_array[3]]))
                count_eth = count_eth + 1
            elif (count_eth >= 29):
                count_eth = 0
            else:
                count_eth = count_eth + 1    
    line = file.readline()

#Check for normal distribution
print("Y Flows:")
print(rg.kolmogorov_smirnov(y_gls))

#Run regressions
if (len(y_gls) == len(x_btc_ewer)):
    rg.gls_regression("GLS 1m WBTC EWER", y_gls, x_btc_ewer)
else:
    print(len(y_gls))
    print(len(x_btc_ewer))

if (len(y_gls) == len(x_btc_tsmom)):
    rg.gls_regression("GLS 1m WBTC TSMOM", y_gls, x_btc_tsmom)
else:
    print(len(y_gls))
    print(len(x_btc_tsmom))

if (len(y_gls_eth) == len(x_eth_ewer)):
    rg.gls_regression("GLS 1m WETH EWER", y_gls_eth, x_eth_ewer)
else:
    print(len(y_gls_eth))
    print(len(x_eth_ewer))

if (len(y_gls_eth) == len(x_eth_tsmom)):
    rg.gls_regression("GLS 1m WETH TSMOM", y_gls_eth, x_eth_tsmom)
else:
    print(len(y_gls_eth))
    print(len(x_eth_tsmom))

#Close file
file.close
