import numpy as np


## 无投资计划

# ---------------------------------------------------
# 输入贷款总额pv、贷款年化利率rate、还款期限period
# 输出每月还款额payment、缴纳利息总额interest
# ---------------------------------------------------
def get_payment(pv, rate, period):
    # 贷款月利率r
    r = rate/12
    if r == 0:
        payment = pv / period
    else:
        payment = (pv * r) / (1 - (1 / (1 + r))**period)
    interest = payment * period - pv
    
    return payment, interest

# ---------------------------------------------------
# 输入贷款总额pv、贷款年化利率rate、每月还款额payment
# 输出还款期限period、缴纳利息总额interest
# ---------------------------------------------------
def get_period(pv, rate, payment):
    # 贷款月利率r
    r = rate/12
    if r == 0:
        period = pv / payment
    else:
        period = - np.log(1 - pv * r / payment) / np.log(1 + r)
    interest = payment * period - pv
    
    return np.ceil(period), interest


## 有投资计划

# ---------------------------------------------------
# 输入贷款总额pv、贷款年化利率rate、购房基金初始资金init_fund、投资收益率ret、还款期限period
# 输出每月还款额payment、每月基金支出payment_fund_actual、每月额外支出payment_add、缴纳利息总额interest
# ---------------------------------------------------
def get_payment_w_invest(pv, rate, init_fund, ret, period):
    # 贷款月利率r
    r = rate/12
    if r == 0:
        payment = pv / period
    else:
        payment = (pv * r) / (1 - (1 / (1 + r))**period) # total payment
    interest = payment * period - pv
    
    # 投资月收益率g
    g = (1 + ret)**(20/260) - 1
    if g == 0:
        # 从购房基金中每月最大支出金额payment_fund
        payment_fund = init_fund / period
    else:
        payment_fund = init_fund * g / (1 - (1 / (1 + g))**period)
    payment_fund_actual = min(payment, payment_fund)
    payment_add = max(0, payment - payment_fund)
    
    return payment, payment_fund_actual, payment_add, interest

# ---------------------------------------------------
# 输入贷款总额pv、贷款年化利率rate、购房基金初始资金init_fund、投资收益率ret、每月还款额payment
# 输出还款期限period、每月基金支出payment_fund_actual，每月额外支出payment_add、缴纳利息总额interest
# 注：必须输入还款额总额，因为只输入payment_fund_actual或payment_add无法确定还款期限
# ---------------------------------------------------
def get_period_w_invest(pv, rate, init_fund, ret, payment):
    # 贷款月利率r
    r = rate/12
    if r == 0:
        period = pv / payment
    else:
        period = - np.log(1 - pv * r / payment) / np.log(1 + r)
    interest = payment * period - pv
    
    # 投资月收益率g
    g = (1 + ret)**(20/260) - 1
    if g == 0:
        # 从购房基金中每月最大支出金额payment_fund
        payment_fund = init_fund / period
    else:
        payment_fund = init_fund * g / (1 - (1 / (1 + g))**period)
    payment_fund_actual = min(payment, payment_fund)
    payment_add = max(0, payment - payment_fund)
    
    return period, payment_fund_actual, payment_add, interest

# ---------------------------------------------------
# 也可以先用无投资计划的方法计算出每月还款额payment、还款期限period
# 再直接根据购房基金初始资金init_fund、投资收益率ret、每月还款额payment、还款期限period
# 从而计算每月基金支出payment_fund_actual，每月额外支出payment_add
# ---------------------------------------------------
def separate_payment(init_fund, ret, payment, period):
    g = (1 + ret)**(20/260) - 1
    if g == 0:
        # 从购房基金中每月最大支出金额payment_fund
        payment_fund = init_fund / period
    else:
        payment_fund = init_fund * g / (1 - (1 / (1 + g))**period)
    payment_fund_actual = min(payment, payment_fund)
    payment_add = max(0, payment - payment_fund)
    
    return payment_fund_actual, payment_add