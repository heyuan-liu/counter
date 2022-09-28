import streamlit as st
import pandas as pd
from funcs import calc_salary

st.title('工资计算器')

city_selectbox = st.sidebar.selectbox(
    "选择城市",
    ('北京市', '萨克就够了')
)

monthly_salary = st.sidebar.text_input(
    '月薪',
    value=20000
)

yi_liao_rate = st.sidebar.text_input(
    '医疗保险缴纳比例(%)',
    value=2
)

yang_lao_rate = st.sidebar.text_input(
    '养老保险缴纳比例(%)',
    value=8
)

gong_ji_jin_rate = st.sidebar.text_input(
    '公积金缴纳比例(%)',
    value=12
)

six_special = st.sidebar.text_input(
    '六项附加扣除',
    value=1000
)

bonus_months = st.sidebar.text_input(
    '年终奖几个月',
    value=4
)

money, tax = calc_salary(float(monthly_salary), float(yi_liao_rate) / 100, float(yang_lao_rate) / 100,
                         float(gong_ji_jin_rate) / 100, int(six_special), int(bonus_months))

money_pd = pd.DataFrame(
    {'到手工资': money[:12]},
    index=[i for i in range(1, 13)]  # 调整index从1开始
)

st.bar_chart(money_pd)

bonus_v1 = money[12]
bonus_v2 = money[13]
st.write('改版前的年终奖：', bonus_v1, '元，改版后：', bonus_v2, '元')
bonus_delta, tax_delta = st.columns(2)
with bonus_delta:
    st.metric('年终奖到手变化', value=bonus_v2, delta=round(bonus_v2-bonus_v1, 2), delta_color='inverse')
with tax_delta:
    bonus_tax_v1 = tax[12]
    bonus_tax_v2 = tax[13]
    st.metric('年终奖纳税变化', value=bonus_tax_v2, delta=round(bonus_tax_v2-bonus_tax_v1, 2), delta_color='inverse')


all_pd = pd.DataFrame(
    {
        '缴纳个税': tax[:12],
        '到手工资': money[:12],
     }
    , index=[f'{i}月' for i in range(1, 13)]
)

st.table(all_pd)

