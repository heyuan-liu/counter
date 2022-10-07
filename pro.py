import streamlit as st
import pandas as pd
from latepayment import *
import numpy

#左侧输入框
st.sidebar.subheader('输入贷款金额')
total_price = st.sidebar.number_input(
    "房/车总价(万元)",
    value = 100
)
down_payment = st.sidebar.number_input(
    "首付(万元)",
    value = 40
)

st.sidebar.subheader('输入贷款细节')
st.sidebar.info('还款期限/每月还款额 二选一输入')
rate = st.sidebar.number_input(
    "贷款利率(%)",
    help = '???',
    value = 3
)
period = st.sidebar.number_input(
    "还款期限(月)",
    value = 48
)
payment = st.sidebar.number_input(
    "每月还款额(元)",
    value = 0
)

st.sidebar.subheader('输入投资计划')
init_fund = st.sidebar.number_input(
    "投资初始资金(万元)",
    help = "???",
    value = 0
)
ret = st.sidebar.number_input(
    "投资收益率(%)",
    help ='年化',
    value = 0
)



#计算
pv = (total_price - down_payment) * 10000
rate /= 100
if init_fund == 0 and ret == 0:
    if payment == 0 and period != 0:
        payment, interest = get_payment(pv, rate, period)
    if period == 0 and payment != 0:
        period, interest = get_period(pv, rate, payment)
    payment_fund_actual, payment_add = 0, 0
if init_fund != 0 and ret != 0:
    init_fund *= 10000
    ret /= 100
    if payment == 0 and period != 0:
        payment_fund_actual, payment_add, interest = get_payment_w_invest(pv, rate, init_fund, ret, period)
    if period == 0 and payment != 0:
        payment_fund_actual, payment_add, interest = get_period_w_invest(pv, rate, init_fund, ret, payment)


#右侧方案栏
indexlist = ['房/车总价','首付','贷款总额','贷款利率','还款期限','每月还款额','缴纳利息总额','投资初始资金','投资收益率（年化）','每月投入资金','每月额外支出']
datalist = [total_price*10000,down_payment*10000,pv,rate,period,payment,interest,init_fund,ret,payment_fund_actual,payment_add]
cur_pd = pd.DataFrame(
    {
        '详细数据': datalist,
    }
    , index = indexlist
)
st.title('贷款计算器')
st.header('方案详情')
programe_name = st.text_input(
    "方案名称",
    value='方案一'
)
st.table(cur_pd)

if st.button('保存方案'):
    f = open("./data.txt","w")
    f.write(str(programe_name) + '\n')
    for line in datalist:
        f.write(str(line) + '\n')
    f.close()

fp = open('./data.txt','r')
last_data=[]
flag = 0
for line in fp:
    line=line.strip('\n') 
    if flag == 0:
        programe_name = line
    else:
        last_data.append(line)
    flag += 1   

fp.close()
last_data = numpy.array(last_data,dtype=float)   
last_pd = pd.DataFrame(
    {
        '详细数据': last_data,
    }
    , index = indexlist
)
st.header('上个方案')
last_programe_name = st.text_input(
    "方案名称",
    key='方案0',
    value=programe_name,
    disabled=True
)
st.table(last_pd)