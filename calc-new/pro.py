from itertools import count
from operator import is_
import streamlit as st
import pandas as pd
from latepayment import *
import numpy
import sys

#左侧输入框
is_house = False
st.sidebar.subheader('第一步--选择方案')
type = st.sidebar.selectbox(
    '选择房车',
    ('车','房')
)
if type == '房':
    is_house = True
car = st.sidebar.selectbox(
    '选择车型和还款期限(月)',
    ('',
'兰博基尼Aventador-12', 
'兰博基尼Aventador-24',
'兰博基尼Aventador-36',
'兰博基尼Aventador-60',
'法拉利812GT S-12', 
'法拉利812GT S-24', 
'法拉利812GT S-36', 
'法拉利812GT S-60', 
'保时捷911-12', 
'保时捷911-24', 
'保时捷911-36', 
'特斯拉Model S-36', 
'特斯拉Model S-60',
'新BMW iX3-48', 
'新BMW iX3-24', 
'新BMW iX3-36', 
'新BMW iX3-48', 
'新BMW iX3-60'),
    disabled = is_house
)    
house = st.sidebar.selectbox(
    '选择城市(均价)',
    ('',
'北京市', 
'上海市', 
'深圳市',
'三亚市', 
'苏州市',
'嘉兴市'),
    help = '请在第三步中自定义还款期限',
    disabled = not is_house
)
aera = st.sidebar.number_input(
    "房屋面积(平方米)",
    value = 100,
    disabled = not is_house,
    step = 1 
)


ft = open('./ch.txt', 'r', encoding='utf-8')
pro_list = [120, 0.05, 200]
flag = 0
temp = ''
for line in ft:
    if (house in line and house != '') or (car in line and car != ''):
        for i in line:
            if i != '-' and flag == 0:
                continue
            if i == '-' and flag == 0:
                flag += 1
                continue
            if i != '-' and flag > 0:
                temp += i
                continue
            if i == '-' and flag > 0:
                pro_list[flag-1] = float(temp)
                temp = ''
                flag += 1
ft.close()


if is_house:
    pro_list[2] = pro_list[2] * aera
st.sidebar.subheader('第二步--输入贷款金额')
total_price = st.sidebar.number_input(
    "房/车总价(万元)",
    value = float(pro_list[2]),
    step = 1.0
)
down_payment = st.sidebar.number_input(
    "首付(万元)",
    value = 40
)

st.sidebar.subheader('第三步--输入贷款细节')
rate = st.sidebar.number_input(
    "贷款利率(%)",
    help = '贷款利率请输入贷款的年化利率',
    value = float(pro_list[1] * 100),
    step = 0.1
)
period = st.sidebar.number_input(
    "还款期限(月)",
    value = int(pro_list[0]),
    help = '还款期限/每月还款额 二选一输入'
)
payment = st.sidebar.number_input(
    "每月还款额(元)",
    value = 0,
    help = '还款期限/每月还款额 二选一输入'
)

st.sidebar.subheader('第四步--输入投资计划')
init_fund = st.sidebar.number_input(
    "投资初始资金(万元)",
    help = '当不希望将所有存款用于首付，但有计划分出一部分资金用于投资，并专门用于偿付房/车贷款时，请在下方输入投资计划细节。\n投资初始资金指计划分出的这部分资金，投资收益率指您期望这部分资金的年化收益率。',
    value = 0
)
ret = st.sidebar.number_input(
    "投资收益率(%)",
    help ='投资收益率请输入年化收益率',
    value = .0,
    step = 0.1
)


#计算
pv = (total_price - down_payment) * 10000
rate /= 100

if init_fund == 0:     #无投资计划
    if payment == 0 and period != 0:
        payment, interest = get_payment(pv, rate, period)
    elif period == 0 and payment != 0:
        period, interest = get_period(pv, rate, payment)
    elif period == 0 and payment == 0:
        st.subheader('还款期限和每月还款额至少有一个大于0')
        sys.exit()
    else:
        st.subheader('请将还款期限置为0以进行计算')
        sys.exit()        
    payment_fund_actual, payment_add = 0, 0
else:   #有投资计划
    init_fund *= 10000
    ret /= 100
    if payment == 0 and period != 0:
        payment, payment_fund_actual, payment_add, interest = get_payment_w_invest(pv, rate, init_fund, ret, period)
    elif period == 0 and payment != 0:
        period, payment_fund_actual, payment_add, interest = get_period_w_invest(pv, rate, init_fund, ret, payment)
    elif period == 0 and payment == 0:
        st.subheader('还款期限和每月还款额至少有一个大于0')
        sys.exit()
    else:
        st.subheader('请将还款期限置为0以进行计算')
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
st.write('全国城市房价,中国各地房价e.cn)')

st.subheader('房贷利率来源')
st.write('2022年9月首套房贷款利率,取各银行最低报价')