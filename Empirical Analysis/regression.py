from scipy.stats import kstest
import statsmodels.api as sm
import statsmodels.stats.api as sms
from statsmodels.compat import lzip

def ols_regression(title, dependent, independent):
 
    # perform ols regression
    ols_result = ols_helper(dependent, independent)
 
    # printing the summary table
    print(title)
    print(ols_result.summary())

    # return ols results
    return ols_result

def kolmogorov_smirnov(y):
    return kstest(y, 'norm')

def gls_regression(title, dependent, independent):

    # adding the constant term
    x = sm.add_constant(independent)

    # performing the regression and fitting the model
    result = sm.GLS(dependent, x).fit()

    # printing the summary table
    print(title)
    print(result.summary())

def logit_regression(title, dependent, independent):

    # adding the constant term
    x = sm.add_constant(independent)

    # performing the regression and fitting the model
    result = sm.Logit(dependent, x).fit()

    # printing the summary table
    print(title)
    print(result.summary())

def durbin_watson(ols_result):

    # produce the test result
    durbin_watson_results = sms.durbin_watson(ols_result.resid)

    print("test statistic: " + str(durbin_watson_results))

def breusch_pagan(ols_result):

    # produce the test result
    breusch_pagan_result = sms.het_breuschpagan(ols_result.resid, ols_result.model.exog)

    print("p-value: " + str(breusch_pagan_result[1]))

def ols_helper(dependent, independent):

    # adding the constant term
    x = sm.add_constant(independent)

    # performing the regression and fitting the model
    ols_result = sm.OLS(dependent, x).fit()
 
    # return ols returns
    return ols_result