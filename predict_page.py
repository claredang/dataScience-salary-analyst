import streamlit as st
import pickle
import numpy as np
import pycountry


def load_model():
    with open('saved_steps.pkl', 'rb') as file:
        data = pickle.load(file)
    return data


# Declare model variables
data = load_model()
regressor = data["model"]
le_company_location = data["le_company_location"]
le_experience_level = data["le_experience_level"]
le_job_category = data["le_job_category"]


def country_to_country_code(country_name):
    try:
        country = pycountry.countries.get(name=country_name)
        return country.alpha_2
    except AttributeError:
        return None


def show_predict_page():
    countries = [country.name for country in pycountry.countries]
    experience_level = (
        "Entry",
        "Middle",
        "Senior",
        "Expert"
    )
    job_category = ("Data Scientist", "Data Analyst", "Data Engineer")
    country_valid = ('ES', 'CA', 'US', 'DE', 'GB',
                     'IN', 'FR', 'AU', 'BR', 'PT', 'GR')

    # UI
    st.title("Salary Prediction :moneybag:")
    job_category = st.selectbox("Job Title", job_category)
    country = st.selectbox("Company Location", countries)
    country_code = country_to_country_code(country)
    # if country_code:
    #     print(f"The country code for {country} is {country_code}.")
    if country_code not in country_valid:
        country_code = 'GR'
    # else:
    #     print(f"The country code for {country} is not valid")
    experience_level = st.selectbox("Experience Level", experience_level)

    ok = st.button("Calculate Salary", type="primary")
    # company_location, experience_level, job_category
    if ok:
        X = np.array([[country_code, experience_level, job_category]])
        X[:, 0] = le_company_location.transform(X[:, 0])
        X[:, 1] = le_experience_level.transform(X[:, 1])
        X[:, 2] = le_job_category.transform(X[:, 2])
        X = X.astype(float)

        salary = regressor.predict(X)
        st.subheader(f"The estimated salary is ${salary[0]:.2f}")


if __name__ == "__main__":
    show_predict_page()
