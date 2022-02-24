import streamlit as st
import pandas as pd
from datetime import datetime
import altair as alt
import numpy as np
from vega_datasets import data

if __name__ == "__main__":
    st.title("COVID-19 Coronavirus Data Dashboard")

    # convert to date object
    df = pd.read_csv("data/US_epidemiology.csv")
    df["date"] = df["date"].map(lambda date: datetime.strptime(date, '%Y-%m-%d'))
    df = df.fillna(0)

    parameter_map = {"Daily confirmed": "new_confirmed",
                     "Daily deceased": "new_deceased",
                     "Daily tested": "new_tested",
                     "Daily hospitalized": "new_hospitalized_patients",
                     "Daily vaccinated": "new_persons_vaccinated"}

    reverse_parameter_map = {"new_confirmed": "Daily confirmed",
                             "new_deceased": "Daily deceased",
                             "new_tested": "Daily tested",
                             "new_hospitalized_patients": "Daily hospitalized",
                             "new_persons_vaccinated": "Daily vaccinated"}

    parameters = st.multiselect("What parameters would you like to view?",
                                ["Daily confirmed", "Daily deceased", "Daily tested",
                                 "Daily hospitalized", "Daily vaccinated"], default="Daily confirmed")

    selected_fields = [parameter_map[parameter] for parameter in parameters]
    selected_fields.append("date")
    plot_data = df[selected_fields]
    selected_fields.remove("date")
    plot_data = plot_data.melt("date", var_name='parameter', value_name='count')
    plot_data["Name"] = plot_data["parameter"].map(lambda x: reverse_parameter_map[x])

    range_ = ['red', 'steelblue', 'chartreuse', '#F4D03F', '#D35400']
    plot = alt.Chart(plot_data).mark_line().encode(
        x='date:T',
        y='count:Q',
        color=alt.Color('parameter:N', scale=alt.Scale(scheme='goldorange')),
        tooltip=["parameter", "count"]
    ).interactive().properties(
        width=1000,
        height=400
    )
    st.altair_chart(plot)

    # Pie chart
    #
    # pts = alt.selection(type="multi")
    # source = pd.DataFrame({"category": ["Male", "Female"], "value": [21804507, 24557094]})
    #
    #
    # pie = alt.Chart(source).mark_arc().encode(
    #     theta=alt.Theta(field="value", type="quantitative"),
    #     color=alt.Color(field="category", type="nominal"),
    #     tooltip=["category", "value"]
    # ).add_selection(pts)
    #
    # st.altair_chart(pie)

    # plot_2 = alt.Chart(df[["date"], ["new_confirmed"], [""]]).mark_line().encode(
    #     x='date:T',
    #     y='new_confirmed:Q'
    # ).transform_filter(
    #     pts
    # ).interactive().properties(
    #     width=1000,
    #     height=400
    # )
    #
    # st.altair_chart(plot_2)

    source = pd.DataFrame({"Gender": ["Male", "Female"], "Cases": [21804507, 24557094]})


    base = alt.Chart(source).encode(
        theta=alt.Theta("Cases:Q", stack=True),
        color=alt.Color(field="Gender", type="nominal"),
        tooltip=["Gender", "Cases"]
    ).properties(
        width=500
    )
    pie = base.mark_arc(outerRadius=120)
    text = base.mark_text(radius=150, size=15).encode(text="Gender:N")

    pie_chart = pie+text

    source_age = pd.DataFrame({"Age group": ["0-9", "10-19", "20-29","30-39","40-49","50-59","60-69","70-79"],
                                "Cases": [3193461, 5859563, 8489652, 7820802, 6711128, 6205893, 4365465, 2341249]})
    # Age group
    base = alt.Chart(source_age).encode(
        theta=alt.Theta("Cases:Q", stack=True),
        radius=alt.Radius("Cases", scale=alt.Scale(type="sqrt", zero=True, rangeMin=20)),
        color="Age group:N",
        tooltip=["Age group:N", "Cases:Q"]
    )

    radix_chart = base.mark_arc(innerRadius=20, stroke="#fff")

    pie_slice, radix_slice = st.columns([3, 1])
    pie_slice.write(pie_chart)
    radix_slice.write(radix_chart)

    df_male_female_date = df[["date", "new_confirmed_male", "new_confirmed_female"]]
    df_male_female_date.rename(columns={"date": "Date", "new_confirmed_male": "Male", "new_confirmed_female": "Female"},
                               inplace=True)
    scatter_plot_data = df_male_female_date.melt("Date", var_name='Gender', value_name='New Cases')

    df_age_date = df[["date", "new_confirmed_age_0", "new_confirmed_age_1",
                      "new_confirmed_age_2", "new_confirmed_age_3", "new_confirmed_age_4",
                      "new_confirmed_age_5", "new_confirmed_age_6", "new_confirmed_age_7"]]
    df_age_date.rename(columns={"date": "Date",
                                "new_confirmed_age_0": "0-9",
                                "new_confirmed_age_1": "10-19",
                                "new_confirmed_age_2": "20-29",
                                "new_confirmed_age_3": "30-39",
                                "new_confirmed_age_4": "40-49",
                                "new_confirmed_age_5": "50-59",
                                "new_confirmed_age_6": "60-69",
                                "new_confirmed_age_7": "70-79"},
                               inplace=True)

    bar_char_data = df_age_date.melt("Date", var_name='Age Group', value_name='New Cases')

    brush = alt.selection(type="interval", encodings=["x"])

    scale_1 = alt.Scale(domain=['Male', 'Female'],
                      range=['red', 'green'])

    color = alt.Color('Gender:N', scale=scale_1)

    points = (
        alt.Chart(scatter_plot_data)
            .mark_point()  # Create scatter plot
            .encode(
            x="Date:T",
            y="New Cases:Q",
            tooltip=["Gender", "Date", "New Cases"],
            color=alt.condition(brush, "Gender:N", alt.value("lightgray")),
        ).add_selection(brush)
    ).properties(title="Click and drag to create a selection region",
                 height=400,
                 width=1000
                 )


    bars = (
        alt.Chart(bar_char_data)
            .mark_bar()  # Create bar plot
            .encode(
            x="New Cases:Q",
            color=alt.Color("Age Group:N"),
            y="Age Group:N",
        ).transform_filter(brush).interactive(

        ).properties(
            height=200,
            width=1000
        )
    )

    # Concatenate bar plot and scatter plot vertically
    chart = alt.vconcat(points, bars).properties(
    ).configure_range(
        category={"scheme": "category10"}
).configure_point(
        opacity=1.0
    )

    st.write(chart)

    df_economy = df[["date", "gdp_per_capita_usd", "new_confirmed"]]
    df_economy.rename(columns={"date": "Date", "new_confirmed": "Covid Cases", "gdp_per_capita_usd": "GDP Per Capita USD"},
                               inplace=True)
    df_economy = df_economy.melt("Date", var_name='parameter', value_name='Value')
    economy_chart = alt.Chart(df_economy).mark_line().encode(
        x='Date',
        y='Value',
        color='parameter',
        strokeDash='parameter',
    ).properties(
        width=1000
    )
    st.write(economy_chart)

    df_mobility = df[["date", "mobility_retail_and_recreation", "mobility_grocery_and_pharmacy", "mobility_parks", "mobility_transit_stations", "mobility_workplaces", "mobility_residential"]]
    df_mobility = df_mobility.melt("date", var_name='Mobility Type', value_name='Percentage change')
    mobility_chart = alt.Chart(df_mobility).mark_area().encode(
        alt.X('date:T',
              axis=alt.Axis(format='%m-%Y', domain=False, tickSize=0)
              ),
        alt.Y('sum(Percentage change):Q', stack='center', axis=None),
        alt.Color('Mobility Type:N',
                  scale=alt.Scale(scheme='category10')
                  )
    ).properties(
        width=1000
    ).interactive()
    st.write(mobility_chart)
