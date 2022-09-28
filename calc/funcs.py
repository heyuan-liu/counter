import sys

def get_cardinal_number(salary, low, high):
    """
    根据月薪获取社保缴费基数
    :param salary: 月薪
    :param low: 下限基数
    :param high: 上限基数
    :return: 实际缴费基数
    """
    if salary <= low:
        return low
    elif low < salary <= high:
        return salary
    else:
        return high


def get_tax_rate(tax_rate_tb, salary):
    """
    根据月薪（年终奖）获取税率
    :param tax_rate_tb: 税率表，格式 [(分段下限, 分段上限, 税率, 速算扣除), (...), ...]
    :param salary: 月薪或年终奖
    :return: salary所在分段的税率和速算扣除金额
    """
    for tax_rate in tax_rate_tb:
        if tax_rate[0] < salary <= tax_rate[1]:
            return tax_rate[2], tax_rate[3]


salary_tax_rate_tb = [
    (0, 36000, 0.03, 0),
    (36000, 144000, 0.1, 2520),
    (144000, 300000, 0.2, 16920),
    (300000, 420000, 0.25, 31920),
    (420000, 660000, 0.3, 52920),
    (660000, 960000, 0.35, 85920),
    (960000, sys.maxsize, 0.45, 181920),
]

bonus_tax_rate_tb = [
    (0, 3000, 0.03, 0),
    (3000, 12000, 0.1, 210),
    (12000, 25000, 0.2, 1410),
    (25000, 35000, 0.25, 2660),
    (35000, 55000, 0.3, 4410),
    (55000, 80000, 0.35, 7160),
    (80000, sys.maxsize, 0.45, 15160),
]


def get_five_insurances(salary, yi_liao_rate=0.02, yang_lao_rate=0.08, gong_ji_jin_rate=0.12):
    """
    计算个人五险一金的缴纳金额
    :param salary: 月薪
    :param yi_liao_rate: 医疗保险缴纳比例
    :param yang_lao_rate: 养老保险缴纳比例
    :param gong_ji_jin_rate: 公积金缴纳比例
    :return: 缴纳金额
    """
    yi_liao_cn = get_cardinal_number(salary, 5360, 29732)
    yang_lao_cn = get_cardinal_number(salary, 3613, 26541)
    gong_ji_jin_cn = get_cardinal_number(salary, 2320, 27786)

    five_insurances = yi_liao_cn * yi_liao_rate + yang_lao_cn * yang_lao_rate + round(gong_ji_jin_cn * gong_ji_jin_rate)

    return five_insurances


def calc_salary_tax(salary, deduct_salary):
    """
    计算月薪（或年终奖v2）个税
    :param salary: 累计月薪
    :param deduct_salary: 累计缴纳五险一金 + 累计6项附加扣除 + 累计个税起征点
    :return:
    """
    # 应纳税额 = 累计月薪 - 累计缴纳五险一金 - 累计6项附加扣除 - 累计个税起征点
    taxable_amount = salary - deduct_salary
    # 查表获取税率和速算扣除
    tax_rate = get_tax_rate(salary_tax_rate_tb, taxable_amount)
    # 累计个税 = 应税金额 * 税率- 速算扣除
    return taxable_amount * tax_rate[0] - tax_rate[1]


def calc_bonus_tax(salary):
    """
    计算年终奖v1个税，需要把年终奖总额除以12，再查税率表，相当于平均每月的个税
    :param salary:
    :return:
    """
    tax_rate = get_tax_rate(bonus_tax_rate_tb, salary / 12)
    return salary * tax_rate[0] - tax_rate[1]


def calc_salary(monthly_salary=20000, yi_liao_rate=0.02, yang_lao_rate=0.08, gong_ji_jin_rate=0.12,
                six_special=1000, bonus_months=4):
    total_salary = 0  # 累计月薪
    total_five_insurances = 0  # 累计五险一金
    total_tax_threshold = 0  # 累计个税起征点
    total_six_special = 0  # 累计6项附加扣除
    pre_tax_amount = 0  # 前几月累计个税

    money_every_month = []  # 返回每个月到手工资
    tax_every_month = []  # 返回每个月缴纳个税

    for i in range(1, 13):
        total_salary += monthly_salary

        five_insurances = get_five_insurances(monthly_salary, yi_liao_rate, yang_lao_rate, gong_ji_jin_rate)
        total_five_insurances += five_insurances
        total_tax_threshold += 5000
        total_six_special += six_special

        # 不需要纳税的部分
        to_deduct = total_five_insurances + total_tax_threshold + total_six_special

        # 当月个税 = 当年所得累计个税 - 前几月累计个税
        taxed_amount = round(calc_salary_tax(total_salary, to_deduct) - pre_tax_amount, 2)
        tax_every_month.append(taxed_amount)
        # pre_tax_amount 累计当月个税，为下个月做准备
        pre_tax_amount += taxed_amount

        # 到手工资 = 月薪 - 当月个税 - 当月缴纳五险一金
        money = round(monthly_salary - taxed_amount - five_insurances, 2)
        money_every_month.append(money)

        # 默认按照12月份发年终奖计算
        if i == 12:
            # 年终奖 = bonus_months * 月薪
            bonus = bonus_months * monthly_salary
            # v1版本  调整前
            bonus_taxed_amount_v1 = calc_bonus_tax(bonus)
            tax_every_month.append(bonus_taxed_amount_v1)
            bonus_money_v1 = bonus - bonus_taxed_amount_v1
            money_every_month.append(round(bonus_money_v1, 2))

            # v2 版本 调整后
            bonus_taxed_amount_v2 = round(calc_salary_tax(total_salary + bonus, to_deduct) - pre_tax_amount, 2)
            tax_every_month.append(bonus_taxed_amount_v2)
            bonus_money_v2 = bonus - bonus_taxed_amount_v2
            money_every_month.append(round(bonus_money_v2, 2))

    return money_every_month, tax_every_month


# [25346.73, 25074.41, 23950.58, 23950.57, 23950.57, 23950.57, 23950.57, 22394.51, 21956.07, 21956.06, 21956.06, 21956.07, 115410.0, 99032.95]
