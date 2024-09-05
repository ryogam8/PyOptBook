from problem import CarGroupProblem
import streamlit as st
import pandas as pd

def preprocess(students, cars):
    students_df = pd.read_csv(students)
    cars_df = pd.read_csv(cars)
    return students_df, cars_df

def convert_to_csv(df: pd.DataFrame) -> None:
    return df.to_csv().encode('utf-8')

col1, col2 = st.columns(2, gap="medium")

with col1:
    students = st.file_uploader("Student Data", type="csv")
    cars = st.file_uploader("Cars Data", type="csv")
    if students is not None and cars is not None:
        if st.button("Run Optimization"):
            students_df, cars_df = preprocess(students, cars)
            solution_df = CarGroupProblem(students_df, cars_df).solve()
            with col2:
                st.write("##### Optimization Result")
                csv = convert_to_csv(solution_df)
                st.download_button("Press to download", csv, 'solution.csv', 'text/csv', key="download-csv")
                st.write(solution_df)
