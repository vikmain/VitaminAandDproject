# Declare the required library files 
import streamlit as st
import pandas as pd
import altair as alt

# Load data and print the name as you want
st.title("Vitamin A & D Screening Dashboard")
st.write("Summary of persons screened across CHC/PHC facilities")

summary = pd.read_csv("outputs/summary.csv")

# Show the summary table 
st.subheader("Summary Table")
st.dataframe(summary)

# Create a bar chart to show the persons Screened 
st.subheader("Persons Screened per Facility")
bar_chart = alt.Chart(summary[summary["Facility_Clean"] != "Total"]).mark_bar().encode(
    x=alt.X("Facility_Clean", sort="-y"),
    y="Persons Screened",
    tooltip=["Facility_Clean", "Persons Screened", "% Total Screened"]
).properties(width=700, height=400)
st.altair_chart(bar_chart)

# Implement the pie chart to show the percentage
st.subheader("Percentage of Total Screened")
pie_chart = alt.Chart(summary[summary["Facility_Clean"] != "Total"]).mark_arc().encode(
    theta=alt.Theta("% Total Screened", type="quantitative"),
    color=alt.Color("Facility_Clean", legend=alt.Legend(title="Facility")),
    tooltip=["Facility_Clean", "% Total Screened"]
).properties(width=700, height=400)
st.altair_chart(pie_chart)

# Filters  extension the use of optional extension. It is create for individual data 
st.subheader("Filter Options")
facility_filter = st.multiselect("Select facilities to view:", summary["Facility_Clean"].unique())
if facility_filter:
    filtered_summary = summary[summary["Facility_Clean"].isin(facility_filter)]
    st.dataframe(filtered_summary)
    st.altair_chart(
        alt.Chart(filtered_summary).mark_bar().encode(
            x="Facility_Clean", y="Persons Screened"
        )
    )
