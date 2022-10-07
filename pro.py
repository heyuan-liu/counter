from matplotlib.cbook import ls_mapper
import streamlit as st
import pandas as pd

#左侧输入框
st.sidebar.subheader('输入贷款金额')
total_price = st.sidebar.number_input(
    "房/车总价(万元)",
    value=100
)
down_payment = st.sidebar.number_input(
    "首付(万元)",
    value=40
)

st.sidebar.subheader('输入贷款细节')
loan_rate = st.sidebar.number_input(
    "贷款利率(%)",
    help='???',
    value=3
)
term_repayment = st.sidebar.number_input(
    "还款期限(月)",
    value=48
)
monthly_repayment = st.sidebar.number_input(
    "每月还款(元)",
    value=6000
)

st.sidebar.subheader('输入投资计划')
investment_initial_capital = st.sidebar.number_input(
    "投资初始资金(万元)",
    help="???",
    value=12
)
ROL = st.sidebar.number_input(
    "投资收益率(%)",
    help='年化',
    value=8
)


#右侧方案栏
total_loan = total_price - down_payment
total_interest = 0
monthly_initial_capital = 0
indexlist = ['房/车总价','首付','贷款总额','贷款利率','还款期限','每月还款','缴纳利息总额','投资初始资金','投资收益率（年化）','每月投入资金']
datalist = [total_price,down_payment,total_loan,loan_rate,term_repayment,monthly_repayment,total_interest,investment_initial_capital,ROL,monthly_initial_capital]
cur_pd = pd.DataFrame(
    {
        '详细数据': datalist,
    }
    , index=[i for i in indexlist]
)
st.title('贷款计算器')
st.header('方案详情')
programe_name = st.text_input(
    "方案名称",
    value='方案一'
)
st.table(cur_pd)

temp_pd = cur_pd
if st.button('保存方案'):
    last_pd = cur_pd
else:
    last_pd = temp_pd
st.header('上个方案')
last_programe_name = st.text_input(
    "方案名称",
    key='方案0',
    value=programe_name,
    disabled=True
)
st.table(last_pd)