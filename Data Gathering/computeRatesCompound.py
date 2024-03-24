import math

# return deposit and borrow APY
def compoundInterface(indexCurrent, indexPrior, blockCurrent, blockPrior, currency):
    daysPerYear = 365
    borrowRatePerDay = getBorrowRatePerDay(int(indexCurrent), int(indexPrior), int(blockCurrent), int(blockPrior))
    if borrowRatePerDay >= 0:
        borrowRateAPY = (math.pow(borrowRatePerDay + 1, daysPerYear) - 1) * 100
        borrowRateAPR = (borrowRatePerDay * daysPerYear * 100)
        depositRateAPR = getDepositRateAPR(borrowRateAPR, currency)
        depositRateAPY = getDepositRateAPY(depositRateAPR, daysPerYear)
        return [depositRateAPY, borrowRateAPY]
    return [-1, -1]

# convert depositRateAPR into depositeRateAPY
def getDepositRateAPY(depositRateAPR, daysPerYear):
    depositRatePerDay = (depositRateAPR / daysPerYear) / 100
    return (math.pow(depositRatePerDay + 1, daysPerYear) - 1) * 100

# calculate borrow rate per day based on information in transaction logs
def getBorrowRatePerDay(indexCurrent, indexPrior, blockCurrent, blockPrior):
    blocksPerDay = 7200
    deltaBlocks = 1 if (blockCurrent == blockPrior) else (blockCurrent - blockPrior)
    if ((deltaBlocks < 0) or (indexCurrent <= 0) or (indexPrior <= 0) or (indexCurrent < indexPrior)):
        return -1
    else:
        deltaIndex = indexCurrent / indexPrior - 1
        ratePerBlock = (deltaIndex / deltaBlocks)
        return ratePerBlock * blocksPerDay

# estimate deposite rate based on borrow rate and parameters of the currency
# Calculation is based on the following assumptions:
# DAI: reserve factor of 15%, base of 0%, slope of 0.0625, kink of 80%, and jumpslope of 1.2995
# ETH: reserve factor of 20%, base of 2%, slope of 0.225, kink of 80%, and jumpslope of 1.475
# USDC: reserve factor of 15%, base of 0%, slope of 0.0625, kink of 80%, and jumpslope of 1.2995
# USDT: reserve factor of 7.5%, base of 0%, slope of 0.0625, kink of 80%, and jumpslope of 1.2995
# WBTC: reserve factor of 20%, base of 2%, slope of 0.28125, kink of 80%, and jumpslope of 48.26875
def getDepositRateAPR(borrowRate, currency):
    defaultKink = 0.8
    defaultBase = 0.00
    defaultSlope = 0.0625
    defaultJumpSlope = 1.2995
    defaultReserveFactor = 0.15
    # estimate deposite rate depending on currency
    if (currency == "ETH"):
        return estimateDepositRate(borrowRate, 0.02, 0.225, 1.475, 0.2, defaultKink)
    elif (currency == "WBTC"):
        return estimateDepositRate(borrowRate, 0.02, 0.28125, 48.26875, 0.2, defaultKink)
    elif (currency == "USDT"):
        return estimateDepositRate(borrowRate, defaultBase, defaultSlope, defaultJumpSlope, 0.075, defaultKink)
    else:
        return estimateDepositRate(borrowRate, defaultBase, defaultSlope, defaultJumpSlope, defaultReserveFactor, defaultKink)

# estimate deposite rate based on borrow rate and parameters
def estimateDepositRate(borrowRate, baseRate, slope, jumpSlope, reserveFactor, kink):
    if borrowRate == 0:
        return 0
    else:
        borrowRatePercent = borrowRate / 100
        utilization = (borrowRatePercent - baseRate) / slope
        normalRatePercent = (utilization * borrowRatePercent * (1 - reserveFactor))
        if (utilization > kink):
            return ((normalRatePercent + (jumpSlope * (utilization - kink))) * 100)
        else:
            return (normalRatePercent * 100)
