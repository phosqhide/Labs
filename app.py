import pandas as pd
import os
import re
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Data processing
def clean_html_tags(df):
    for column in df.columns:
        df[column] = df[column].astype(str).str.replace(r'<.*?>', '', regex=True)
    return df

def read_files_to_dataframe(directory_path):
    headers = ['Year', 'Week', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI', 'Empty']

    all_data = []

    for filename in os.listdir(directory_path):
        if filename.endswith(".csv"):
            filepath = os.path.join(directory_path, filename)
            print(filepath)
            
            df = pd.read_csv(filepath, header=1, names=headers, index_col=False)
            df = clean_html_tags(df)
            df = df.drop(df.loc[df['VHI'] == -1].index)
            df = df.drop("Empty", axis=1)
            df = df.drop(df.index[-1]) 
            
            region_id = filename.split('_')[2]  
            df['area'] = region_id
            
            all_data.append(df)

    main_df = pd.concat(all_data, ignore_index=True)
    main_df['Week'] = main_df['Week'].astype(float).astype(int)
    main_df['area'] = main_df['area'].astype(int)
    main_df['Year'] = main_df['Year'].astype(int)
    main_df = main_df.sort_values(by=['area', 'Year', 'Week']).reset_index(drop=True)
    return main_df

directory = '../data'    
df = read_files_to_dataframe(directory)


def refresh_state():
    st.session_state.option = 'VCI'
    st.session_state.area = df['area'].unique()[0]
    st.session_state.weeks = (1, 52)
    st.session_state.years = (1982, 2024)


## Streamlit
if 'option' not in st.session_state:
    st.session_state.option = 'VCI'

if 'area' not in st.session_state:
    st.session_state.area = df['area'].unique()[0]

if 'weeks' not in st.session_state:
    st.session_state.weeks = (1, 52)

if 'years' not in st.session_state:
    st.session_state.years = (1982, 2024)

# col1, col2 = st.columns(2)

# with col1:
st.write("Створіть dropdown список, який дозволить обрати часовий ряд VCI, TCI, VHI для набору даних із лабораторної роботи 2;")
def get_time():
    options = ['VCI', 'TCI', 'VHI']
    option = st.selectbox("Оберіть часовий ряд", options, key='option')

    st.write(df[['Year', option]].head())

get_time()

st.write("Створіть dropdown список, який дозволить вибрати область, для якої буде виконуватись аналіз;")
def get_area():
    option = st.selectbox("Оберіть область", df['area'].unique(), key='area')
    st.write(df.loc[df['area'] == option].head())
    return option
get_area()

st.write("Створіть slider, який дозволить зазначити інтервал тижнів, за які відбираються дані;")

def get_weeks():
    values = st.slider("Виберіть інтервал тижнів", 1, 52, (1, 52), key='weeks')
    st.write(df.loc[(df['Week'] >= values[0]) & (df['Week'] <= values[1])])
    return values
get_weeks()

st.write("Створіть slider, який дозволить зазначити інтервал років, за які відбираються дані;")

def get_years():
    values = st.slider("Виберіть інтервал років", 1982, 2024, (1982, 2024), key='years')
    st.write(df.loc[(df['Year'] >= values[0]) & (df['Year'] <= values[1])])
    return values
get_years()

st.write("Створіть button для скидання всіх фільтрів і повернення до початкового стану дани (відповідно інтерактивні елементи повинні мати початкові значення);")
st.button('Скинути всі фільтри', on_click=refresh_state, key='reset_button')

st.write("Створіть три вкладки для відображення таблиці з відфільтрованими даними, відповідного до неї графіка та графіка порівняння даних по областях.Перший графік повинен відображати відфільтровані дані (часові ряди за діапазон років, що обмежені інтервалом тижнів). Другий графік має відображати порівняннязначень VCI, TCI або VHI (залежно від обраної опції у списку dropdown) для обраної області з усіма іншими областями за вказаний часовий інтервал. Продумайте вигляд цих графіків. ")

# with col2:
def tab():
    tab1, tab2, tab3 = st.tabs(["Таблиця", "Графік", "Порівняння"])

    with tab1:
        st.write("Таблиця з відфільтрованими даними")
        filtered_data = df[(df['Year'] >= st.session_state.years[0]) & 
                        (df['Year'] <= st.session_state.years[1]) & 
                        (df['Week'] >= st.session_state.weeks[0]) & 
                        (df['Week'] <= st.session_state.weeks[1]) & 
                        (df['area'] == st.session_state.area)]
        st.write(filtered_data)

    with tab2:
        st.write("Графік відповідного до таблиці")
        plt.figure(figsize=(10, 6))
        sns.lineplot(x='Week', y=st.session_state.option, data=filtered_data, hue='Year')
        plt.title(f"Графік {st.session_state.option} по тижнях для вибраних років і області")
        plt.xlabel("Тиждень")
        plt.ylabel(st.session_state.option)
        st.pyplot()

    with tab3:
        st.write("Графік порівняння даних по областях")
        
        areas = df['area'].unique()
        selected_areas = st.multiselect("Оберіть області для порівняння", areas, default=areas[:2])
        
        filtered_data_2 = df[(df['Year'] >= st.session_state.years[0]) & 
                                    (df['Year'] <= st.session_state.years[1]) & 
                                    (df['Week'] >= st.session_state.weeks[0]) & 
                                    (df['Week'] <= st.session_state.weeks[1]) & 
                                    df['area'].isin(selected_areas)]

        plt.figure(figsize=(10, 6))
        sns.lineplot(x='Week', y=st.session_state.option, data=filtered_data_2, hue='area')
        plt.title(f"Порівняння {st.session_state.option} по областях")
        plt.xlabel("Тиждень")
        plt.ylabel(st.session_state.option)
        st.pyplot()
tab()


st.write("Створіть два checkbox для сортування даних за зростанням та спаданням значень VCI, TCI або VHI (залежно від обраної опції у списку dropdown). Продумайте реакцію програми, якщо увімкнені обидва чекбокси.")



grown = st.checkbox("Сортувати за зростанням")
decline = st.checkbox("Сортувати за спаданням")

if grown and decline:
    st.write("Оберіть тільки один чекбокс")
    st.write(df)
elif grown:
    sorted_data = df.sort_values(by=st.session_state.option, ascending=True)
    st.write(sorted_data)
elif decline:
    sorted_data = df.sort_values(by=st.session_state.option, ascending=False)
    st.write(sorted_data)
else:
    st.write(df)  