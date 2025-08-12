import yfinance as yf
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime

st.title('Простое приложение для визуализации данных')
st.write("*На примере данных о котировках компании Apple с* ***2010/01/01***")


today = datetime.date.today()

col1, col2 = st.sidebar.columns(2)
with col1:
    start_date = st.date_input("Дата начала", value=datetime.date(2010, 1, 1), max_value=today)
with col2:
    end_date = st.date_input("Дата окончания", value=today, max_value=today)


@st.cache_data
def load_data(ticker, start, end):
    return yf.download(ticker, start=start, end=end)

df = load_data("AAPL", start_date, end_date)


if st.sidebar.checkbox("Показать таблицу с данными"):
    st.dataframe(df)



if isinstance(df.columns, pd.MultiIndex):
    df.columns = [' '.join(col) for col in df.columns.values]


close_col = 'Close AAPL'
volume_col = 'Volume AAPL'

close_series = df[close_col].squeeze()
volume_series = df[volume_col].squeeze()

st.subheader("Динамика цены закрытия Apple")

fig, ax1 = plt.subplots(figsize=(10, 5))

sns.lineplot(x=df.index, y=close_series, ax=ax1, color="blue", label="Цена закрытия")
ax1.set_xlabel("Дата")
ax1.set_ylabel("Цена $", color="blue")
ax1.tick_params(axis='y', labelcolor="blue")

ax2 = ax1.twinx()
ax2.bar(df.index, volume_series, alpha=0.3, color="black", label="Объём")
ax2.set_ylabel("Объём", color="black")
ax2.tick_params(axis='y', labelcolor="black")

fig.suptitle("Apple — Цена и объём торгов", fontsize=16)
ax1.grid(True)
fig.tight_layout()

st.pyplot(fig)