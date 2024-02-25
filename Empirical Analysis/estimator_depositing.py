import numpy as np
import solver as sv
import regression as rg

#Local constants
input_file = "Compound2 USDC Daily"
path = "/Golo10/Cryptocurrency-Lending/Empirical Analysis/"
input_file_name = path + input_file + ".csv"

#Open file
file = open(input_file_name, "r")

#Local arrays
y_gls = np.array([])
y_logit = np.array([])  
x = np.array([])

#Skip headline of input file
line = file.readline()

count = 0
line = file.readline()
while line:
    items = line.split(";")
    if len(items) == 3:
        if ((count == 0) or (count == 1)):
            y_gls_input = float(items[0].replace('.',''))
            y_logit_input = float(items[1])
            x_input = float(items[2].replace(',','.'))
            y_gls = np.append(y_gls, np.array(y_gls_input))
            y_logit = np.append(y_logit, np.array(y_logit_input))
            x = np.append(x, np.array(x_input))
            count = 1
        elif (count >= 29):
            count = 0
        else:
            count = count + 1
    line = file.readline()

#Run regressions
if (len(y_gls) == len(x)):
    title = input_file + ": GLS 1d"
    rg.gls_regression(title, y_gls, x)
else:
    print(len(y_gls))
    print(len(x))

#Run Breusch-Pagan and Durbin-Watson Tests
if (len(y_gls) == len(x)):
    title = input_file + ": OLS 1d"
    ols_result = rg.ols_regression(title, y_gls, x)
    print("Breusch-Pagan:")
    rg.breusch_pagan(ols_result)
    print("Durbin-Watson:")
    rg.durbin_watson(ols_result)

#Close file
file.close
