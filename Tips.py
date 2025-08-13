import yfinance as yf
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import io

st.title('Простое приложение для визуализации данных: работа с файлом tips.csv')
st.write("С загрузкой файла и возможностью выгрузить графики")


uploaded_file = st.sidebar.file_uploader('Загрузи файл tips.csv(находится в том же репозитории, что и данный streamlit)', type='csv')
if uploaded_file is not None:
    if uploaded_file.name == 'tips.csv':
        tips = pd.read_csv(uploaded_file, sep=',')
        # if st.sidebar.checkbox("В подтверждение загрузки показать первые 5 записей"):
        #     st.dataframe(tips.head(5))

        if st.sidebar.checkbox('Динамика чаевых в **январе 2023**'):
            st.write('***Для этого графика была сформирована новая колонка time_order, заполненная рандомными числами января 2023 года***')
            st.write('Скачивание графика в PNG')
 
            n = len(tips)
            tips['time_order'] = pd.to_datetime('2023-01-01') + pd.to_timedelta(np.random.randint(0, 31, size = n), unit='D')

            plt.figure(figsize=(10, 6))
            sns.lineplot(data=tips, x='time_order', y='tip')
            plt.xlabel('Дата заказа')
            plt.ylabel('Чаевые в $')
            plt.title('Динамика чаевых в январе 2023')
            plt.xticks(rotation=45)
            plt.grid(axis='x')

            st.pyplot(plt)

            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)

            st.download_button(
                label='Скачать график в PNG',
                data=buf,
                file_name='tips_lineplot.png',
                mime='image/png'
            )

            plt.close()

        if st.sidebar.checkbox('Гистограмма **счетов**'):
            st.write('Гистограмма счетов')
            st.write('Скачивание графика в PNG')

            fig = px.histogram(tips,
                   x='total_bill',
                   title='Гистограмма суммы счета',
                   nbins=20,
                   color_discrete_sequence=['green']
            )

            fig.update_layout(
                xaxis_title = 'Сумма счета',
                yaxis_title = 'Количество заказов'
            )

            st.plotly_chart(fig)  

            html_bytes = fig.to_html().encode('utf-8')

            st.download_button(
                label="Скачать график в HTML",
                data=html_bytes,
                file_name="tips_bars_html.html",
                mime="text/html"
            )
        
        if st.sidebar.checkbox('Cвязь между **счетом, чаевыми и размером группы**, с разделением по **полу**'):
            st.write('Cвязь между счетом, чаевыми и размером группы, с разделением по полу')
            st.write('Скачивание графика в HTML')

            fig = px.scatter(tips,
                x='total_bill',
                y='tip', 
                title='Связь между счетом, чаевыми, размером группы и полом',
                labels={'total_bill': 'Счет', 'tip': 'Чаевые'},
                color='sex',
                size='size',
                color_discrete_map={
                    'Male': 'blue',
                    'Female': 'red'
                }
            )

            st.plotly_chart(fig)  

            html_bytes = fig.to_html().encode('utf-8')

            st.download_button(
                label="Скачать график в HTML",
                data=html_bytes,
                file_name="tips_chart_html.html",
                mime="text/html"
            )
        
        if st.sidebar.checkbox('Cвязь между **счетом и чаевыми**, по **полу и курению**'):
                st.write('Cвязь между счетом и чаевыми, по полу и курению')
                st.write('Скачивание графика в PNG')

                fig, axes = plt.subplots(1, 2, figsize=(10, 6)) 

                sns.scatterplot(
                    data=tips[tips['sex'] == 'Male'],
                    x='total_bill',
                    y='tip',
                    hue='smoker',
                    ax=axes[0]
                )
                axes[0].set_title('Мужчины')
                axes[0].set_xlabel('Размер счета')
                axes[0].set_ylabel('Чаевые')

                sns.scatterplot(
                    data=tips[tips['sex'] == 'Female'],
                    x='total_bill',
                    y='tip',
                    hue='smoker',
                    ax=axes[1]
                )
                axes[1].set_title('Женщины')
                axes[1].set_xlabel('Размер счета')
                axes[1].set_ylabel('Чаевые')


                handles, labels = axes[0].get_legend_handles_labels()
                # fig.legend(handles, labels, title="Курящий?", loc="upper center", ncol=2)

                st.pyplot(fig)


                buf = io.BytesIO()
                fig.savefig(buf, format='png')
                buf.seek(0)

                st.download_button(
                    label='Скачать график в PNG',
                    data=buf,
                    file_name='scatter_sex_smoker.png',
                    mime='image/png'
                )

                plt.close(fig)

    else:
        st.error('Пожалуйста, загрузите файл с именем tips.csv из репозитория')
        st.stop()
else:
    st.stop()


