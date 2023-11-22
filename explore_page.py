import pandas as pd
import plotly_express as px
from plotly import graph_objects as go
import streamlit as st

data = pd.read_csv("data_scientist.csv")

# Divide all title into only 3 categories: Data Scientist, Data Analyst, Data Engineer
job_dict = {
    'Data Scientist': [
        'Data Scientist', 'Principal Data Scientist', 'Applied Scientist', 'AI Developer',
        'Research Scientist', 'Head of Data', 'Data Science Manager', 'AI Programmer',
        'Director of Data Science', 'Machine Learning Scientist', 'Applied Machine Learning Scientist',
        'Lead Data Scientist', 'Deep Learning Researcher', 'Data Science Consultant',
        'Machine Learning Developer', '3D Computer Vision Researcher', 'Machine Learning Researcher',
        'Data Science Tech Lead', 'Data Scientist Lead', 'Product Data Scientist', 'Data Science Lead',
        'Machine Learning Manager', 'AI Scientist', 'Head of Data Science', 'Applied Data Scientist',
        'Head of Machine Learning'
    ],
    'Data Analyst': [
        'Data Analyst', 'Data Quality Analyst', 'Compliance Data Analyst', 'Business Data Analyst',
        'Lead Data Analyst', 'Marketing Data Analyst', 'Data Analytics Specialist', 'Insight Analyst',
        'Product Data Analyst', 'BI Data Analyst', 'Data Operations Analyst', 'Data Analytics Lead',
        'Principal Data Analyst', 'Financial Data Analyst', 'BI Analyst', 'Data Analytics Manager',
        'Data Analytics Consultant', 'Data Manager', 'Manager Data Management'
    ],
    'Data Engineer': [
        'Data Engineer', 'Data Modeler', 'Analytics Engineer', 'Business Intelligence Engineer',
        'Data Strategist', 'Data DevOps Engineer', 'Big Data Engineer', 'Data Specialist',
        'BI Data Engineer', 'Data Infrastructure Engineer', 'Cloud Database Engineer', 'ETL Engineer',
        'Data Operations Engineer', 'BI Developer', 'Azure Data Engineer', 'Computer Vision Engineer',
        'Machine Learning Infrastructure Engineer', 'Cloud Data Engineer', 'ETL Developer',
        'Data Architect', 'Big Data Architect', 'Autonomous Vehicle Technician', 'ML Engineer',
        'Machine Learning Software Engineer', 'Data Analytics Engineer', 'Research Engineer',
        'Computer Vision Software Engineer', 'Data Lead', 'Data Management Specialist',
        'Applied Machine Learning Engineer', 'MLOps Engineer', 'Machine Learning Research Engineer',
        'Deep Learning Engineer', 'Machine Learning Engineer', 'Data Science Engineer',
        'Lead Machine Learning Engineer', 'NLP Engineer', 'Principal Machine Learning Engineer',
        'Software Data Engineer', 'Principal Data Architect', 'Lead Data Engineer'
    ]
}


def map_job(job):
    for k, v_list in job_dict.items():
        if job in v_list:
            return k
    return job


def process(df):
    # Filter year and employment type
    df = df[df.work_year.isin([2022, 2023])]
    df = df[df.employment_type == 'FT']

    # Map job title to job category
    df['job_category'] = df.job_title.map(map_job)

    # Filter company location
    country_counts = df.company_location.value_counts()
    idx = (country_counts > 10).values
    countries = country_counts[idx].index
    df = df[df.company_location.isin(countries)]
    df = df.reset_index(drop=True)

    # Rename experience levels
    entry_lvl_map = {'EN': 'Entry', 'MI': 'Middle',
                     'SE': 'Senior', 'EX': 'Expert'}
    df.experience_level.replace(entry_lvl_map, inplace=True)
    return df


def show_explore_page():
    df = process(data)
    job_cats = list(job_dict.keys())
    salary_meds = {}
    for job_cat in job_cats:
        salary_meds[job_cat] = df[df.job_category ==
                                  job_cat].salary_in_usd.median()

    # Color map for job categories
    job_cat_cmap = {'Data Scientist': '#9cd3f7',
                    'Data Analyst': '#fc88a7', 'Data Engineer': '#80c779'}

    # Create the histograms
    fig = px.histogram(df, x='salary_in_usd', nbins=50, color='job_category', marginal='rug',
                       color_discrete_map=job_cat_cmap,
                       labels={'salary_in_usd': 'Yearly salary in USD', 'job_category': 'Job category'}, opacity=0.5)
    fig.update_layout(
        bargap=0.1, title="Yearly salary distribution in US dollars<br><sup>2022/2023</sup>")

    # Plot the median vertical bars
    for k, v in salary_meds.items():
        fig.add_vline(x=v, line_width=6, line_color='black')
        fig.add_vline(x=v, line_width=3, line_color=job_cat_cmap[k])

    # ============ Salary Distribution Dashboard # ============
    st.header("Yearly Salary Distribution")
    st.plotly_chart(fig)

    fig = go.Figure()
    # Get the df for a single job category each time
    for job in job_cats:
        # Prepare the temporary dataframe (filter and sort)
        temp_df = df[df.job_category == job]
        dfs = []
        sort_order = ['Entry', 'Middle', 'Senior', 'Expert']
        for x in sort_order:
            dfs.append(temp_df[temp_df.experience_level == x])
        temp_df = pd.concat(dfs)
        # Add box plots
        fig.add_trace(go.Box(
            y=temp_df.salary_in_usd,
            x=temp_df.experience_level,
            name=job, marker_color=job_cat_cmap[job]))
        fig.update_layout(
            title="Annual salary distribution in US dollars by experience level and job category<br><sup>2022/2023</sup>",
            xaxis_title="Experience level",
            yaxis_title="Annual salary (USD)",
            boxmode='group')
    st.header("Salaries by Experience Level and Job Category")
    st.plotly_chart(fig)

    st.header("Salary Evolution of Median")
    levels = ['Entry', 'Middle', 'Senior', 'Expert']
    job_cats = ['Data Scientist', 'Data Analyst', 'Data Engineer']

    # Calculate the medians
    medians = {}
    for job in job_cats:
        job_medians = []
        for level in levels:
            temp_df = df[df.experience_level == level]
            temp_df = temp_df[temp_df.job_category == job]
            job_medians.append(temp_df.salary_in_usd.median())
        medians[job] = job_medians

    # Plot the calculations
    traces = []
    for job in job_cats:
        traces.append(go.Scatter(x=levels, y=medians[job], mode='lines+markers',
                                 name=job, marker=dict(color=job_cat_cmap[job])))
    fig = go.Figure(data=traces)
    fig.update_layout(
        title="Evolution of the median annual salary<br><sup>2022/2023</sup>",
        xaxis_title="Experience level",
        yaxis_title="Annual salary (USD)")
    st.plotly_chart(fig)


if __name__ == "__main__":
    show_explore_page()
