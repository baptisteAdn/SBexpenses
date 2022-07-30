import streamlit as st
import calendar
from datetime import datetime
import plotly.express as exp
import pandas as pd

import database as db #Local import

#-------Settings--------
page_title ='Incomes and expenses tracker, Sahana et Baptiste'
page_icon = ':money_with_wings:'
layout = 'wide'
currency ='CAD'

#Setting the categories of income and expenses
incomes_category = ['Salary','Health Insurance','Dividend','Other Income']
expenses_category = ['Rent','Groceries','Car','Eat out','Saving','Bills','Vacations'
    ,'Other expenses']
who_category = ['Sahana', 'Baptiste']
for_category = ['Split','Not Split']
#-------------------------------------

st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
st.title(page_title + ' ' + page_icon)

#-------------Get year and Month--------
years = [datetime.today().year, datetime.today().year+1]
months = list(calendar.month_name[1:])
days = [x for x in range(1,32)]


#------------DataBase Interface-------
def get_all_periods():
    items = db.fetch_all_periods()
    periods = [item['key'] for item in items]
    return periods


#-------Splitting my app into tabs------
tab_titles = ['Expenses and Incomes register', 'Data visualization']
tabs = st.tabs(tab_titles)
#---------------------------------------

#---------Tab 1: Expenses and Incomes register--------
with tabs[0]:
    st.header(f'Data Entry in {currency}')
    with st.form('entry_form', clear_on_submit=True):
        col1, col2, col3 = st.columns(3)
        col1.selectbox('Select Day', days, key='day')
        col2.selectbox('Select Month', months, key='month')
        col3.selectbox('Select Year', years, key='year')

        '---'
        with st.expander('Income'):
            for income in incomes_category:
                st.number_input(f'{income}', min_value=0., format='%2f', step=10., key=income)
        with st.expander('Expenses'):
            for expense in expenses_category:
                st.number_input(f'{expense}',min_value=0., format='%2f', step=10., key=expense)

        '---'
        submitted = st.form_submit_button('Save Data')
        if submitted:
            period = str(st.session_state['year']) + '_' + str(st.session_state['month']) + '_' + str(st.session_state['day'])
            incomes = {income: st.session_state[income] for income in incomes_category}
            expenses = {expense: st.session_state[expense] for expense in expenses_category}
            db.insert_period(period, incomes, expenses)
            st.success('Data Saved')

#---------Tab 2: Data visualization--------
with tabs[1]:
    st.header(f'Data Visualization')
    with st.form('saved_periods'):
        col1,col2,col3 = st.columns(3)
        col1.selectbox('Select start Day', days,key='start_day')
        col2.selectbox('Select start Month', months, key='start_month')
        col3.selectbox('Select start Year', years, key='start_year')

        col1, col2, col3 = st.columns(3)
        col1.selectbox('Select end Day', days, key='end_day')
        col2.selectbox('Select end Month', months, key='end_month')
        col3.selectbox('Select end Year', years, key='end_year')

        period = st.selectbox('Select Period', get_all_periods(), key='period')
        submitted = st.form_submit_button('Plot Period')
        if submitted:
            period_data = db.get_period(period)
            expenses = period_data.get('expenses')
            incomes = period_data.get('incomes')

            #Display total income and expenses
            # total_income = sum(incomes.values())
            # total_expense = sum(expenses.values())
            # col1,col2 = st.columns(2)
            # col1.metric('Total Income', f'{total_income} {currency}')
            # col2.metric('Total Expense', f'{total_expense} {currency}')

            df_expenses = pd.DataFrame.from_dict(expenses)
            df_incomes = pd.DataFrame.from_dict(incomes)

            #Get the period from the text box
            period = str(st.session_state['period'])


            st.subheader('Expenses')
            col1,col2 = st.columns(2)
            col1.write(df_expenses)
            fig_exp = exp.pie(names=['Rent','Groceries','Bills','Savings'], values=df_expenses.iloc[0],
                              title=f'Expenses Pie chart of {period}')
            col2.plotly_chart(fig_exp, use_container_width=True)

            '---'
            st.subheader('Incomes')
            col1, col2 = st.columns(2)
            col1.write(df_incomes)
            fig_inc = exp.pie(names=['Salary', 'Health', 'Other incomes'], values=df_incomes.iloc[0],
                              title=f'Expenses Pie chart of {period}')
            col2.plotly_chart(fig_inc, use_container_width=True)

