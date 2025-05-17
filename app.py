import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


st.set_page_config(layout='wide' , page_title='Startup Analysis')
#import dataset
df = pd.read_csv('startup_cleaned.csv')
df['date'] = pd.to_datetime(df['date'] , errors='coerce')

df['year'] = df['date'].dt.year


#sets sidebar title
st.sidebar.title('Startup Funding Analysis')

def load_overall_analysis():
    st.title('Overall Analysis')
    col1 , col2 , col3 , col4 = st.columns(4)


    with col1:
        total = round(df['amount'].sum())
        st.metric('Total Funding:' , str(total) + ' Cr')

    with col2:
        max_funding = round(df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0])
        st.metric('Max Funding:' , str(max_funding) + ' Cr')

    with col3:
        avg = round(df.groupby('startup')['amount'].sum().mean())
        st.metric('Avg Funding:' , str(avg)  + ' Cr')

    with col4:
        all = df['startup'].nunique()
        st.metric('Total Funded Startups:' , str(all) )

def load_startup_detail(startup):
    st.title(startup)

    col1 , col2 = st.columns(2)

    with col1:
        st.subheader('Founders:')
        founder = df[df['startup'].str.contains(startup)]['investor']
        st.dataframe(founder)

    col3 , col4 = st.columns(2)

    with col3:

        st.subheader('Industry:')
        industry = df[df['startup'].str.contains(startup)]['vertical']
        st.dataframe(industry)

    with col4:
        st.subheader('Sub-Industry:')
        sub_industry = df[df['startup'].str.contains(startup)]['Subvertical']
        st.dataframe(sub_industry)

    col5 , col6 = st.columns(2)

    with col5:
        st.subheader('Locations:')
        location = df[df['startup'].str.contains(startup)]['city']
        st.dataframe(location)

def load_investor_detail(investor):
    st.title(investor)
    #recent investments
    recent_df = df[df['investor'].str.contains(investor)].head()[['date' , 'startup' , 'vertical' , 'city' , 'round' , 'amount']]

    st.subheader('Recent Investments:')
    st.dataframe(recent_df)

    #biggest investments

    big_df = df[df['investor'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(ascending=False)
    st.subheader('Biggest Investment Data:')
    st.dataframe(big_df)


    col1 , col2 = st.columns(2)
    with col1:
        big_df = df[df['investor'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(ascending=False)
        st.subheader('Biggest Investments Graph:')
        fig , ax = plt.subplots()
        ax.bar(big_df.index , big_df.values)
        st.pyplot(fig)

    with col2:
        vertical_plot = df[df['investor'].str.contains(investor)].groupby('vertical')['amount'].sum()
        st.subheader('Sectors Invested In : ')
        fig1 , ax1 = plt.subplots()
        ax1.pie(vertical_plot , labels=vertical_plot.index , autopct="%0.01f%%")
        st.pyplot(fig1)

    col3 , col4 = st.columns(2)

    with col3:
        stage_df = df[df['investor'].str.contains(investor)].groupby('round')['amount'].sum()
        st.subheader('Round Invested In:')
        fig2 , ax2 = plt.subplots()
        ax2.pie(stage_df , labels=stage_df.index , autopct="%0.01f%%")
        st.pyplot(fig2)

    with col4:
        city_invested_in = df[df['investor'].str.contains(investor)].groupby('city')['amount'].sum()
        st.subheader('City Invested In:')
        fig3 , ax3 = plt.subplots()
        ax3.pie(city_invested_in , labels=city_invested_in.index , autopct="%0.01f%%")
        st.pyplot(fig3)

    col5 , col6 = st.columns(2)

    with col5:
        year_data = df[df['investor'].str.contains(investor)].groupby('year')['amount'].sum()
        st.subheader('YoY Graph')
        fig4 , ax4 = plt.subplots()
        ax4.plot(year_data.index , year_data.values)
        st.pyplot(fig4)

#creates a dropdown menu in sidebar
option = st.sidebar.selectbox('Select One',['Overall Analysis','Startup','Investors'])

if option == 'Overall Analysis':
    btn0 = st.sidebar.button('Show Overall Analysis')
    if btn0:
        load_overall_analysis()
elif option == 'Startup':
    selected_startup = st.sidebar.selectbox('Select Startup ' , df['startup'].unique().tolist())
    btn1 = st.sidebar.button('Start Startup Analysis')
    st.title('Startup Analysis')
    if btn1:
        load_startup_detail(selected_startup)

else:
    selected_investor = st.sidebar.selectbox('select Investor' , sorted(set(df['investor'].str.split(',').sum())))
    st.title('Investor Analysis')
    btn2 = st.sidebar.button('Find Investor Details')
    if btn2:
        load_investor_detail(selected_investor)