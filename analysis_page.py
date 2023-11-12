import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# import seaborn as sns
import plotly.express as px
import country_converter as coco
import plotly.figure_factory as ff
# import plotly.graph_objects as go
# from wordcloud import WordCloud
# import warnings
# warnings.filterwarnings('ignore')


def show_analysis_page():
    st.header("Data Science 2023 Dataset Overview")
    st.text(
        "The dataset is composed of annual salaries from various data science fields.")
    st.subheader("1. Dataset Overview")
    st.text("This is the overview of dataset")

    # Overview of dataset
    df = pd.read_csv("data_scientist.csv")
    df.drop(df[['salary', 'salary_currency']], axis=1, inplace=True)
    st.dataframe(df.head())

    # st.text("So, we have 9 columns with 3755 rows")
    # st.text("3 numeric columns : work_year, salary_in_usd,remote_ratio.")
    # st.text("6 categorical columns : experience_level,employment_type, job_title, employee_residense, company_location, company_size.")

    st.subheader("2. Univariate Analysis")
    top15_job_titles = df['job_title'].value_counts()[:15]
    fig = px.bar(y=top15_job_titles.values, x=top15_job_titles.index,
                 text=top15_job_titles.values, title='Top 15 Job Designations')
    fig.update_layout(xaxis_title="Job Designations", yaxis_title="Count")
    st.plotly_chart(fig)
    st.text("There are many job titles which does not make it convenient for the prediction\n"
            "This prediction categories all into 3 most dominant job:\n"
            "Data Engineer, Data Scientist, Data Analyst")

    group = df['employment_type'].value_counts()
    emp_type = ['Full-Time', 'Part-Time', 'Contract', 'Freelance']

    fig = px.bar(x=emp_type, y=group.values,
                 color=group.index, text=group.values,
                 title='Employment Type Distribution')

    fig.update_layout(xaxis_title="Employment Type", yaxis_title="count")
    st.plotly_chart(fig)

    country = coco.convert(names=df['employee_residence'], to="ISO3")
    df['employee_residence'] = country
    residence = df['employee_residence'].value_counts()
    fig = px.choropleth(locations=residence.index,
                        color=residence.values,
                        color_continuous_scale=px.colors.sequential.YlGn,
                        title='Employee Location On Map')
    st.plotly_chart(fig)

    top_15_emp_locations = residence[:15]
    fig = px.bar(y=top_15_emp_locations.values, x=top_15_emp_locations.index,
                 color=top_15_emp_locations.index, text=top_15_emp_locations.values,
                 title='Top 15 Locations of Employees')

    fig.update_layout(xaxis_title="Location of Employees", yaxis_title="count")
    st.plotly_chart(fig)

    group = df['company_size'].value_counts()
    fig = px.bar(y=group.values, x=group.index,
                 color=group.index, text=group.values,
                 title='Distribution of Company Size')

    fig.update_layout(xaxis_title="Company Size", yaxis_title="count")
    st.plotly_chart(fig)

    hist_data = [df['salary_in_usd']]
    group_labels = ['salary_in_usd']

    fig = ff.create_distplot(hist_data, group_labels, show_hist=False)
    fig.update_layout(title='Distribution Plot of Salary in USD')
    st.plotly_chart(fig)
    st.text("Salary in USD is mostly distributed between 95/100k - 175/180k.")

    remote_type = ['Fully Remote', 'Partially Remote', 'No Remote Work']

    fig = px.bar(x=remote_type, y=df['remote_ratio'].value_counts().values,
                 color=remote_type, text=df['remote_ratio'].value_counts(
    ).values,
        title='Remote Ratio Distribution')

    fig.update_layout(xaxis_title="Remote Type", yaxis_title="count")
    st.plotly_chart(fig)


if __name__ == "__main__":
    show_analysis_page()
