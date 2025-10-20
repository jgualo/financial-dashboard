import pandas as pd
import streamlit as st
import plotly.express as px
from datetime import datetime, timedelta

st.set_page_config(
    layout="wide",
    page_title="DFP",
    page_icon="📊" 
)

### Variables
non_expenses_categories = ['Interés Cuenta Remunerada', 'Rentabilidad Indexa Capital', 'Nómina']
fixed_salary_categories = ['Nómina']
currency = '€'
STEP_MONTH = timedelta(days=30.2)

### Fetch the data from 
excel_file = pd.ExcelFile('C:/Users/josec/OneDrive/Escritorio/codigos/finanzas_streamlit/Finanzas.xlsx')
all_sheets = excel_file.parse(None)

movements = all_sheets['Movimientos']
account = all_sheets['Cuentas']

### Functions to calculate KPIs
def get_current_total_balance(account):
    current_total_balance = sum(account['Saldo_Actual'])
    return current_total_balance

def get_fixed_salary(movements):
    import_by_category = movements.groupby('Tipo de Gasto')['Importe'].sum().reset_index()
    import_by_category_filtered = import_by_category[import_by_category['Tipo de Gasto'].isin(fixed_salary_categories)]
    return abs(sum(import_by_category_filtered['Importe']))

def get_income(movements):
    import_by_category = movements.groupby('Tipo de Gasto')['Importe'].sum().reset_index()
    import_by_category_filtered = import_by_category[import_by_category['Tipo de Gasto'].isin(non_expenses_categories)]
    return abs(sum(import_by_category_filtered['Importe']))

def get_expenses(movements):
    import_by_category = movements.groupby('Tipo de Gasto')['Importe'].sum().reset_index()
    import_by_category_filtered = import_by_category[~import_by_category['Tipo de Gasto'].isin(non_expenses_categories)]
    return abs(sum(import_by_category_filtered['Importe']))

def get_saving(movements):
    saving = get_fixed_salary(movements) - get_expenses(movements)
    if get_fixed_salary(movements) == 0:
        saving_rate = 0
    else:
        saving_rate = ((get_fixed_salary(movements) - get_expenses(movements)) / get_fixed_salary(movements)) * 100

    return saving, saving_rate

def get_df_income_vs_expenses(movements):
    import_by_category_month = movements.groupby(['Tipo de Gasto', 'Mes'])['Importe'].sum().reset_index()
    income_by_category_month = import_by_category_month[import_by_category_month['Tipo de Gasto'].isin(non_expenses_categories)]
    expenses_by_category_month = import_by_category_month[~import_by_category_month['Tipo de Gasto'].isin(non_expenses_categories)]

    income_by_month = income_by_category_month.groupby('Mes')['Importe'].sum().reset_index()
    income_by_month = income_by_month.rename(columns={'Importe': 'Ingresos'})
    expenses_by_month = expenses_by_category_month.groupby('Mes')['Importe'].sum().reset_index()
    expenses_by_month = expenses_by_month.rename(columns={'Importe': 'Gastos'})
    expenses_by_month['Gastos'] = abs(expenses_by_month['Gastos'])

    income_expenses_by_month = pd.merge(expenses_by_month, income_by_month, on='Mes', how='outer')
    income_expenses_by_month = income_expenses_by_month.fillna(0)

    return income_expenses_by_month

def get_df_expenses_by_category_by_month(movements):
    import_by_category_month = movements.groupby(['Tipo de Gasto', 'Mes'])['Importe'].sum().reset_index()
    expenses_by_category_month = import_by_category_month[~import_by_category_month['Tipo de Gasto'].isin(non_expenses_categories)]

    expenses_by_category_month = expenses_by_category_month.rename(columns={'Importe': 'Gastos'})
    expenses_by_category_month['Gastos'] = abs(expenses_by_category_month['Gastos'])

    return expenses_by_category_month

def get_expenses_by_category(movements):
    bar_chart_data = movements.groupby('Tipo de Gasto')['Importe'].sum().reset_index()
    bar_chart_data = bar_chart_data[~bar_chart_data['Tipo de Gasto'].isin(non_expenses_categories)]
    bar_chart_data['Importe'] = bar_chart_data['Importe'].abs()

    return bar_chart_data

def get_balance_by_account(account):
    balance_by_account = account[['Nombre_Cuenta', 'Saldo_Actual']]
    balance_by_account = balance_by_account.rename(columns={'Nombre_Cuenta': 'Nombre Cuenta', 'Saldo_Actual': 'Saldo Actual'})

    return balance_by_account

def get_max_date_in_movements(movements):
    max_date = movements['Mes'].max()
    return max_date

def get_min_date_in_movements(movements):
    min_date = movements['Mes'].min()
    return min_date

def filter_movements_by_time_range(movements, min, max):
    movements['Formatted Date'] = movements['Mes'].apply(lambda x: datetime.strptime(x, '%Y-%m'))
    movements_filtered = movements[movements['Formatted Date'].between(min, max)]
    movements_filtered = movements_filtered.fillna(0)
    return movements_filtered

### Dashboard Title
st.title('Dashboard Finanzas Personales')

### Filter panels
st.subheader('Filtros')

min_value_date = datetime.strptime(get_min_date_in_movements(movements), '%Y-%m')
max_value_date = datetime.strptime(get_max_date_in_movements(movements), '%Y-%m')

available_months = pd.date_range(
    start=min_value_date, 
    end=max_value_date, 
    freq='MS'
).tolist()

time_range_precise = st.select_slider(
    "Selecciona un rango de meses",
    options=available_months,
    value=(available_months[0], available_months[-1]),
    format_func=lambda x: x.strftime('%Y-%m') 
)

start_date = time_range_precise[0]
end_date = time_range_precise[1]

movements_filtered = filter_movements_by_time_range(movements, start_date, end_date)

current_total_balance = get_current_total_balance(account)
income = get_income(movements_filtered)
expenses = get_expenses(movements_filtered)
fixed_salary = get_fixed_salary(movements_filtered)
saving, saving_rate = get_saving(movements_filtered)



st.subheader('KPIs')

col_current_total_balance, col_income, col_expenses, col_saving = st.columns(4)

with col_current_total_balance:
    current_total_balance_formatted = f'{current_total_balance:,.2f} {currency}'
    st.metric('Saldo Total Actual', current_total_balance_formatted)

with col_income:
    income_formatted = f'{income:,.2f} {currency}'
    fixed_salary_formatted = f'{fixed_salary:,.2f} {currency}'
    st.metric('Ingresos', income_formatted, delta=fixed_salary_formatted)

with col_expenses:
    expenses_formatted = f'{expenses:,.2f} {currency}'
    st.metric('Gastos', expenses_formatted)

with col_saving:
    saving_formatted = f'{saving:,.2f} {currency}'
    saving_rate_formatted = f'{saving_rate:,.2f} %'
    st.metric('Ahorro', saving_formatted, delta=saving_rate_formatted)

st.write('## Visión Temporal')
st.write('### Evolución Ingresos vs. Gastos (Mensual)')

df_income_vs_expenses = get_df_income_vs_expenses(movements_filtered)

if start_date == end_date:
    st.bar_chart(
        df_income_vs_expenses,
        x='Mes',
        y=['Gastos', 'Ingresos'],
        color=["#FF000080", "#2ECC71"]
    )
else:
    st.area_chart(
        df_income_vs_expenses,
        x='Mes',
        y=['Gastos', 'Ingresos'],
        color=["#FF000080", "#2ECC71"]
    )

st.write('### Evolución de Gastos por Categoría (Mensual)')

df_expenses_by_category_by_month = get_df_expenses_by_category_by_month(movements_filtered)

if start_date == end_date:
    st.bar_chart(
        df_expenses_by_category_by_month, 
        x='Mes', 
        y='Gastos', 
        color='Tipo de Gasto', 
        stack='normalize'
    )
else:
    st.area_chart(
        df_expenses_by_category_by_month, 
        x='Mes', 
        y='Gastos', 
        color='Tipo de Gasto', 
        stack='normalize'
    )

st.write('## Detalles Analíticos')

expenses_by_category, balance_by_account = st.columns(2)

with expenses_by_category:
    df_expenses_by_category = get_expenses_by_category(movements_filtered)

    st.write('### Distribución de Gastos por Categoría')

    piechart_expenses_by_category = px.pie(
        df_expenses_by_category,
        names='Tipo de Gasto',
        values='Importe'
    )

    st.plotly_chart(piechart_expenses_by_category, use_container_width=True)


with balance_by_account:
    df_balance_by_account = get_balance_by_account(account)

    st.write('### Distribución de Saldos por Cuentas')

    piechar_balance_by_account = px.pie(
        df_balance_by_account,
        names='Nombre Cuenta',
        values='Saldo Actual'
    )

    st.plotly_chart(piechar_balance_by_account, use_container_width=True)