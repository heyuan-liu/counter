import streamlit as st
import pandas as pd
from latepayment import *
import numpy
import sys

#左侧输入框
pro_data = st.sidebar.selectbox(
    '选择方案(名称/价格/期限/年化利率)',
    ('',
'兰博基尼Aventador 808 12 0.0670 ', 
'兰博基尼Aventador 808 24 0.0680 ',
'兰博基尼Aventador 808 36 0.0690 ',
'兰博基尼Aventador 808 60 0.0700 ',
'法拉利812GTS 540 12 0.0700 ', 
'法拉利812GTS 540 24 0.0700 ', 
'法拉利812GTS 540 36 0.0700 ', 
'法拉利812GTS 540 60 0.0720 ', 
'保时捷911 140 12 0.0399 ', 
'保时捷911 140 24 0.0499 ', 
'保时捷911 140 36 0.0599 ', 
'特斯拉ModelS 89 36 0.0660 ', 
'特斯拉ModelS 89 60 0.0600 ',
'新BMWiX3 40 48 0.0588 ', 
'新BMWiX3 40 24 0.0388 ', 
'新BMWiX3 40 36 0.0488 ', 
'新BMWiX3 40 48 0.0588 ', 
'新BMWiX3 40 60 0.0688 ', 
'北京市均价 7.0367 自选 0.0485 ', 
'上海市均价 6.9206 自选 0.0465 ', 
'深圳市均价 6.8708 自选 0.0460 ',
'三亚市均价 3.5840 自选 0.0480 ', 
'苏州市均价 2.3775 自选 0.0410 ',
'嘉兴市均价 1.8912 自选 0.0440 ')
)

#将方案数据转换为输入数据
pro_list = [0, 0, 0]
flag = 0
temp = ''
is_house = False
if pro_data != '':
    for i in pro_data:
        if i != ' ' and flag == 0:
            continue
        if i == ' ' and flag == 0:
            flag += 1
            continue
        if i != ' ' and flag > 0:
            temp += i
            continue
        if i == ' ' and flag > 0:
            if temp == '自选':
                pro_list[flag-1] = 0
                is_house = True
            else:
                pro_list[flag-1] = float(temp)
            temp = ''
            flag += 1

aera = st.sidebar.number_input(
    "房屋面积",
    value = 100,
    disabled = not is_house
)
if is_house:
    pro_list[0] = pro_list[0] * aera
st.sidebar.subheader('输入贷款金额')
total_price = st.sidebar.number_input(
    "房/车总价(万元)",
    value = pro_list[0]
)
down_payment = st.sidebar.number_input(
    "首付(万元)",
    value = 40
)

st.sidebar.subheader('输入贷款细节')
rate = st.sidebar.number_input(
    "贷款利率(%)",
    help = '贷款利率请输入贷款的年化利率',
    value = pro_list[2] * 100
)
period = st.sidebar.number_input(
    "还款期限(月)",
    value = int(pro_list[1]),
    help = '还款期限/每月还款额 二选一输入'
)
payment = st.sidebar.number_input(
    "每月还款额(元)",
    value = 0,
    help = '还款期限/每月还款额 二选一输入'
)

st.sidebar.subheader('输入投资计划')
init_fund = st.sidebar.number_input(
    "投资初始资金(万元)",
    help = '当不希望将所有存款用于首付，但有计划分出一部分资金用于投资，并专门用于偿付房/车贷款时，请在下方输入投资计划细节。\n投资初始资金指计划分出的这部分资金，投资收益率指您期望这部分资金的年化收益率。',
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

if init_fund == 0 and ret == 0:     #无投资计划
    if payment == 0 and period != 0:
        payment, interest = get_payment(pv, rate, period)
    elif period == 0 and payment != 0:
        period, interest = get_period(pv, rate, payment)
    elif period == 0 and payment == 0:
        st.subheader('还款期限和每月还款额至少有一个大于0')
        sys.exit()
    else:
        st.subheader('还款期限和每月还款额至少有一个等于0')
        sys.exit()        
    payment_fund_actual, payment_add = 0, 0
elif init_fund != 0 and ret != 0:   #有投资计划
    init_fund *= 10000
    ret /= 100
    if payment == 0 and period != 0:
        payment_fund_actual, payment_add, interest = get_payment_w_invest(pv, rate, init_fund, ret, period)
    elif period == 0 and payment != 0:
        payment_fund_actual, payment_add, interest = get_period_w_invest(pv, rate, init_fund, ret, payment)
    elif period == 0 and payment == 0:
        st.subheader('还款期限和每月还款额至少有一个大于0')
        sys.exit()
    else:
        st.subheader('还款期限和每月还款额至少有一个等于0')
        sys.exit() 
elif init_fund == 0 and ret != 0:
    st.subheader('请填写投资初始资金')
    sys.exit()    
else:
    st.subheader('请填写投资收益率')
    sys.exit()



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

#按钮保存方案数据
if st.button('保存方案'):
    f = open("./data.txt","w")
    f.write(str(programe_name) + '\n')
    for line in datalist:
        f.write(str(line) + '\n')
    f.close()

#读取上一次保存的数据
fp = open('./data.txt','r')
last_data = []
flag = 0
for line in fp:
    line = line.strip('\n') 
    if flag == 0:
        programe_name = line
    else:
        last_data.append(line)
    flag += 1   
fp.close()

last_data = numpy.array(last_data,dtype = float)   
last_pd = pd.DataFrame(
    {
        '详细数据': last_data,
    }
    , index = indexlist
)

st.header('上个方案')
last_programe_name = st.text_input(
    "方案名称",
    key = '方案0',
    value = programe_name,
    disabled = True
)
st.table(last_pd)
st.subheader('房价来源')
st.write('全国城市住宅房价排行榜(2022年09月)')
st.write('全国城市房价,中国各地房价均价查询-城市房产网 (cityhouse.cn)')

st.subheader('房贷利率来源')
st.write('2022年9月首套房贷款利率,取各银行最低报价')