import numpy as np
from scipy.optimize import Bounds
from scipy.optimize import minimize
from scipy.optimize import LinearConstraint

#Inverted utility function for borrowing in the alternative case
def inverted_alternative_utility_function(parameters, a_b, r_f, cs, r_coll, r_loan, var_coll, var_loan, cov_coll_loan):
    y_c, y_cb, y_f = parameters
    return (-r_f - cs - y_c*r_coll + y_cb*r_loan + 0.5*a_b*y_c*y_c*var_coll + 0.5*a_b*y_cb*y_cb*var_loan + a_b*y_c*y_cb*cov_coll_loan)

#Inverted utility function for borrowing in the general case
def inverted_utility_function(parameters, a_b, r_f, cs, r_invest, r_coll, r_loan, var_coll, var_loan, var_invest, cov_coll_loan, cov_coll_invest, cov_loan_invest):
    y_c, y_i, y_cb, y_f = parameters
    return (-r_f - cs - y_i*r_invest - y_c*r_coll + y_cb*r_loan + 0.5*a_b*y_i*y_i*var_invest + 0.5*a_b*y_c*y_c*var_coll + 0.5*a_b*y_cb*y_cb*var_loan + a_b*y_c*y_cb*cov_coll_loan + a_b*y_c*y_i*cov_coll_invest + a_b*y_cb*y_i*cov_loan_invest)

#Formalization of the constrained minimization problem
def constrained_minimization(r_f, cs, a_b, m_f, m_c, r_coll, r_loan, r_invest, var_coll, var_loan, var_invest, cov_coll_loan, cov_coll_invest, cov_loan_invest):

    initial_guess = [0.5, 0.5, 0.0, 0.0]
    y_f_upper_bound = 1.0 / m_f
    y_cb_upper_bound = 1.0 / m_c
    y_c_upper_bound = 1.0 + (1.0 / m_f)
    y_i_upper_bound = 1.0 + (1.0 / m_f)

    bounds = Bounds([0.0, 0.0, 0.0, 0.0], [y_c_upper_bound, y_i_upper_bound, y_cb_upper_bound, y_f_upper_bound])
    linear_constraint = LinearConstraint([[1, 1, -1, -1], [0, 0, m_c, m_f], [-1, 0, m_c, 0]], [1, 0, -1], [1, 1, 0])

    res = minimize(inverted_utility_function, initial_guess, method='trust-constr', args=(a_b, r_f, cs, r_invest, r_coll, r_loan, var_coll, var_loan, var_invest, cov_coll_loan, cov_coll_invest, cov_loan_invest), 
                   constraints=[linear_constraint], options={'verbose': 1}, bounds=bounds)

    if res.success:
        print(res.x)
        return res.x
    else:
        return [1.0, 0.0, 0.0, 0.0]    

#Clean output
def clean_floating_numbers(number, maximum):
    if (number < 0.0):
        return 0.0
    elif (number > maximum):
        return maximum
    else:
        return number

#Start calculation
def perform_calculation(r_f, r_b, cs, r_coll, r_loan, r_invest, var_coll, var_loan, var_invest, cov_coll_loan, cov_coll_invest, cov_loan_invest):

    #Local constants
    a_b = 2.4
    k_f = 0.5
    k_c = 0.4

    #Calculate m_f and m_c
    m_f = (1 + r_f + cs)/k_f
    m_c = (1 + r_b)/k_c

    #Find optimal weights
    optimal_weights = constrained_minimization(r_f, cs, a_b, m_f, m_c, r_coll, r_loan, r_invest, var_coll, var_loan, var_invest, cov_coll_loan, cov_coll_invest, cov_loan_invest)
    clean_optimal_weight = clean_floating_numbers(optimal_weights[2], (1.0 / m_c))
    return clean_optimal_weight

#Read imput file in
def transform_input_array(input_array):

    if len(input_array) == 29:

        #Read input values
        r_cb = float(input_array[1].replace(',', '.'))/100
        r_f = float(input_array[2].replace(',', '.'))/100
        cs = float(input_array[3].replace(',', '.'))/100
        r_loan = float(input_array[4].replace(',', '.'))/100
        r_invest = float(input_array[5].replace(',', '.'))/100
        r_coll_BTC_TSMOM = float(input_array[6].replace(',', '.'))/100
        r_coll_ETH_TSMOM = float(input_array[7].replace(',', '.'))/100
        r_coll_BTC_EWER = float(input_array[8].replace(',', '.'))/100
        r_coll_ETH_EWER = float(input_array[9].replace(',', '.'))/100
        var_invest = float(input_array[10].replace(',', '.'))/10000
        var_loan = float(input_array[11].replace(',', '.'))/10000
        var_coll_BTC_TSMOM = float(input_array[12].replace(',', '.'))/10000
        var_coll_ETH_TSMOM = float(input_array[13].replace(',', '.'))/10000
        var_coll_BTC_EWER = float(input_array[14].replace(',', '.'))/10000
        var_coll_ETH_EWER = float(input_array[15].replace(',', '.'))/10000
        cov_loan_coll_BTC_TSMOM = float(input_array[16].replace(',', '.'))/10000
        cov_loan_coll_ETH_TSMOM = float(input_array[17].replace(',', '.'))/10000
        cov_loan_coll_BTC_EWER = float(input_array[18].replace(',', '.'))/10000
        cov_loan_coll_ETH_EWER = float(input_array[19].replace(',', '.'))/10000
        cov_loan_invest = float(input_array[20].replace(',', '.'))/10000
        cov_invest_coll_BTC_TSMOM = float(input_array[21].replace(',', '.'))/10000
        cov_invest_coll_ETH_TSMOM = float(input_array[22].replace(',', '.'))/10000
        cov_invest_coll_BTC_EWER = float(input_array[23].replace(',', '.'))/10000
        cov_invest_coll_ETH_EWER = float(input_array[24].replace(',', '.'))/10000
        loan_value = float(input_array[25].replace(',', '.'))
        
        #Calculate loan shares
        ycb_BTC_TSMOM = perform_calculation(r_f, r_cb, cs, r_coll_BTC_TSMOM, r_loan, r_invest, var_coll_BTC_TSMOM, var_loan, var_invest, cov_loan_coll_BTC_TSMOM, cov_invest_coll_BTC_TSMOM, cov_loan_invest)
        ycb_ETH_TSMOM = perform_calculation(r_f, r_cb, cs, r_coll_ETH_TSMOM, r_loan, r_invest, var_coll_ETH_TSMOM, var_loan, var_invest, cov_loan_coll_ETH_TSMOM, cov_invest_coll_ETH_TSMOM, cov_loan_invest)
        ycb_BTC_EWER = perform_calculation(r_f, r_cb, cs, r_coll_BTC_EWER, r_loan, r_invest, var_coll_BTC_EWER, var_loan, var_invest, cov_loan_coll_BTC_EWER, cov_invest_coll_BTC_EWER, cov_loan_invest)
        ycb_ETH_EWER = perform_calculation(r_f, r_cb, cs, r_coll_ETH_EWER, r_loan, r_invest, var_coll_ETH_EWER, var_loan, var_invest, cov_loan_coll_ETH_EWER, cov_invest_coll_ETH_EWER, cov_loan_invest)

        #Return final values
        return [loan_value, loan_value, ycb_BTC_TSMOM, ycb_ETH_TSMOM, ycb_BTC_EWER, ycb_ETH_EWER]
  