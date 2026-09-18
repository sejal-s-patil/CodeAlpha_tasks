import streamlit as st
import pandas as pd
import numpy as np

st.title("Student Performance Dataset")

# Create dataset
np.random.seed(42)

n = 100

df = pd.DataFrame({
    "Student_ID": [f"S{i:03d}" for i in range(1, n + 1)],
    "Gender": np.random.choice(["Male", "Female"], n),
    "Study_Hours": np.round(np.random.uniform(1, 7, n), 1),
    "Attendance": np.round(np.random.uniform(50, 100, n), 1),
    "Assignments_Score": np.round(np.random.uniform(30, 100, n), 1),
    "Midterm_Score": np.round(np.random.uniform(25, 100, n), 1),
    "Final_Score": np.round(np.random.uniform(25, 100, n), 1),
    "Sleep_Hours": np.round(np.random.uniform(4.5, 9.5, n), 1),
    "Internet_Hours": np.round(np.random.uniform(1, 9, n), 1)
})

# Save CSV
df.to_csv("student_performance.csv", index=False)

# Display on Streamlit
st.success("Dataset created successfully!")

st.write("### Student Performance Data")
st.dataframe(df)

st.write("### Dataset Shape")
st.write(f"Rows: {df.shape[0]}")
st.write(f"Columns: {df.shape[1]}")