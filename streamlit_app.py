import streamlit as st
st.set_page_config(layout="wide", page_icon=":shark:")
import pandas as pd
import altair as alt
from vega_datasets import data
from datetime import datetime, timedelta


@st.cache
def read_files_globe():

    country_info = pd.read_json('data/all_countries.json')
    countries = list(country_info.name)

    # Perform inner join to get latitude and longitude details for country
    df_new_cases_country = pd.read_csv("data/new_confirmed_countrywise.csv")

    location_df = df_new_cases_country
    # Getting rid of subregion fields
    location_df = location_df[location_df['location_key'].str.len() == 2]
    location_df = location_df.astype({'country_name': 'string'})

    # Filter countries
    # location_df = location_df[location_df['country_name'].isin(countries)]

    # Get recognized countries for plotting
    countries = alt.topo_feature(data.world_110m.url, 'countries')


    # Clean and transform to get year and month from date
    location_df = location_df.dropna(subset=['date'])
    location_df['date'] = location_df['date'].map(lambda row: datetime.strptime(row, '%Y-%m-%d').date())
    location_df['month'] = location_df['date'].map(lambda row: row.month)
    location_df['year'] = location_df['date'].map(lambda row: row.year)

    # Groupby year,month and country name
    location_df = location_df.groupby(['year', 'month', 'country_name', 'latitude', 'longitude']).sum().reset_index()

    # Convert date  to Year- month format
    location_df['date'] = location_df.apply(lambda row: datetime.strptime(str(row['year'])+'-'+str(row['month']), '%Y-%m').date(), axis=1)

    # Fill NA with 0
    location_df['new_confirmed'] = location_df['new_confirmed'].fillna(0)

    # Clean the data to get rid of wrong latitudes and longitudes
    location_df = location_df.dropna(subset=['latitude', 'longitude'])
    location_df = location_df[location_df["latitude"] >= -89]
    location_df = location_df[location_df["latitude"] <= 89]
    location_df = location_df[location_df["longitude"] >= -179]
    location_df = location_df[location_df["longitude"] <= 179]
    location_df = location_df[location_df["new_confirmed"] != 0]

    return location_df, countries

@st.cache
def read_gender_age_files(df):
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

    return scatter_plot_data, bar_char_data

@st.cache
def read_files_economy(df):
    df_economy = df[["date", "gdp_per_capita_usd", "new_confirmed"]]
    df_economy.rename(
        columns={"date": "Date", "new_confirmed": "Covid Cases", "gdp_per_capita_usd": "GDP Per Capita USD"},
        inplace=True)
    df_economy = df_economy.melt("Date", var_name='parameter', value_name='Value')

    return df_economy

@st.cache
def read_files_mobility(df):

    df_mobility = df[["date", "mobility_retail_and_recreation", "mobility_grocery_and_pharmacy", "mobility_parks",
                      "mobility_transit_stations", "mobility_workplaces", "mobility_residential"]]
    df_mobility = df_mobility.rename(columns={"date": "Date", "mobility_retail_and_recreation": "Retail",
                                              "mobility_grocery_and_pharmacy": "Grocery",
                                              "mobility_parks": "Parks",
                                              "mobility_transit_stations": "Stations",
                                              "mobility_workplaces": "Workplaces",
                                              "mobility_residential": "Residential"})

    df_mobility = df_mobility.melt("Date", var_name='Mobility Type', value_name='Percentage change')


    return df_mobility

@st.cache
def read_cases_file():
    df = pd.read_csv("data/US_epidemiology.csv")
    df["date"] = df["date"].map(lambda date: datetime.strptime(date, '%Y-%m-%d'))
    df = df.fillna(0)

    return df

@st.cache
def read_files_multiselect(df):
    reverse_parameter_map = {"new_confirmed": "Daily confirmed",
                             "new_deceased": "Daily deceased",
                             "new_tested": "Daily tested",
                             "new_hospitalized_patients": "Daily hospitalized",
                             "new_persons_vaccinated": "Daily vaccinated"}
    df = df.rename(columns=reverse_parameter_map)
    return df

@st.cache
def get_df_usa(df_cases):

    df_vaccination_usa = df_cases[["date", "new_persons_vaccinated"]]
    df_vaccination_usa.rename(columns={"date": "Date", "new_persons_vaccinated": "Number of vaccinated individuals"},
                              inplace=True)
    df_cases_usa = df_cases[["date", "new_confirmed"]]
    df_cases_usa.rename(columns={"date": "Date", "new_confirmed": "Number of cases"},
                        inplace=True)
    df_death_hospitalized_usa = df_cases[["date", "new_deceased", "new_hospitalized_patients"]]
    df_death_hospitalized_usa.rename(columns={"date": "Date", "new_deceased": "Number of deaths",
                                              "new_hospitalized_patients": "Number of hospitalizations"},
                                     inplace=True)
    df_death_hospitalized_usa = df_death_hospitalized_usa.melt("Date", var_name='Parameter', value_name='Count')

    return df_vaccination_usa, df_cases_usa, df_death_hospitalized_usa

@st.cache
def read_nz_cases():
    df_cases_newzealand = pd.read_csv("data/NZ.csv")
    df_cases_newzealand['date'] = df_cases_newzealand['date'].map(lambda row: datetime.strptime(row, '%Y-%m-%d').date())

    df_cases_newzealand_daily = df_cases_newzealand[["date", "new_confirmed"]]
    df_cases_newzealand_daily.rename(columns={"date": "Date", "new_confirmed": "Number of cases"},
                                     inplace=True)

    return df_cases_newzealand, df_cases_newzealand_daily

@st.cache
def get_cor_data(df_cases):
    df_correlation = df_cases[["new_confirmed", "average_temperature_celsius", "rainfall_mm", "relative_humidity"]]
    df_correlation.rename(columns={"date": "Date", "new_confirmed": "Cases",
                                   "average_temperature_celsius": "Temperature",
                                   "rainfall_mm": "Rainfall", "relative_humidity": "Humidity"}, inplace=True)
    cor_data = (df_correlation
                .corr().stack()
                .reset_index()  # The stacking results in an index on the correlation values, we need the index as normal columns for Altair
                .rename(columns={0: 'correlation', 'level_0': 'Parameter 1', 'level_1': 'Parameter 2'}))
    cor_data['correlation_label'] = cor_data['correlation'].map('{:.2f}'.format)  # Round to 2 decimal

    return cor_data

def timestamp(t):
  return pd.to_datetime(t).timestamp() * 1000

def globe_vis(location_df, countries):

    st.write("")
    st.write(
        "<p style='font-size:18px'> First, to give us some context, let us look at how the COVID-19 disease has spread in various <b style='color:#900C3F'>countries across time</b>!<p>",
    unsafe_allow_html=True)
    st.header('How has the number of covid cases varied across the world in the past two years?')


    world = countries
    # Slider for date
    date_slider = st.slider('Silde the Date to see how the number of COVID cases vary with time', min(location_df['date']), max(location_df['date']), min(location_df['date']),
                            step=timedelta(days=30), help="Slide over to see different dates")

    # Get subset of dataframe based on selection
    temp_df = location_df[location_df['year'] == date_slider.year]
    temp_df = temp_df[temp_df['month'] == date_slider.month]
    temp_df = temp_df[["date", "country_name", "new_confirmed", "latitude", "longitude"]]

    # Background chart
    background = alt.Chart(world, title="Variation of Covid cases across years on a monthly basis across countries").mark_geoshape(
        fill='#C4D0AF',
        stroke='black',
    ).project('equirectangular').properties(
        width=1200,
        height=600
    )

    # Points chart

    # First aggregate latitutde longitude points based on country, then plot them, where the count = number of new cases
    points = alt.Chart(temp_df).transform_aggregate(
        latitude='mean(latitude)',
        longitude='mean(longitude)',
        count='sum(new_confirmed)',
        groupby=['country_name']
    ).mark_circle().encode(
        latitude='latitude:Q',
        longitude='longitude:Q',
        color=alt.value("#B62B24"),
        size=alt.Size('count:Q', scale=alt.Scale(domain=[1, 20000000], range= [25, 7500]), legend=None),
        tooltip=[alt.Tooltip("country_name", title="Country Name"), alt.Tooltip('count:Q', title= "New Cases")]
    )

    # Plot both
    glob_plot = background + points
    st.altair_chart(glob_plot, use_container_width=True)

    st.write(
        "<p style='font-size:18px'>The map above gives us insight into how the number of covid cases has changed in the span of 2 years across the countries of the world.</p>",
    unsafe_allow_html=True)

    st.write("<p style='font-size:18px'><ul >"
             "<li style='font-size:18px'> We see from the graph that within the span of the first <b style='color:#900C3F'>3 months</b>, the infection "
             "has spread to almost <b style='color:#900C3F'>all countries</b> of the world. This shows how quickly the COVID-19 disease can "
             "spread from one location to another</li>"
             "<li style='font-size:18px'> There is an almost <b style='color:#900C3F'>exponential</b> increase in the number of cases as months progressed</li>"
             "<li style='font-size:18px'>Overall, we can see that the countries that have reported the most number of cases include <b style='color:#900C3F'>USA, India, Brazil, "
             "France, UK, Russia, Germany and Turkey </b></li>"
             "<li style='font-size:18px'> We can also see that it is of a <b style='color:#900C3F'>fluctuating </b> nature in which there are periods in which  cases sharply increase and then decreases</li>"
             "<li style='font-size:18px'> An interesting observation is to note how once a country gets infected with COVID-19, it does not go away!</li>"
             "<li style='font-size:18px'>It is evident that the past couple of months of December 2021 and January 2022 has seen a huge increase in the number of cases  </li>"
             " </ul>"
             "</p>", unsafe_allow_html=True)

    st.write("")
    st.write("<p style='font-size:18px'>Now, since we have an idea of the overall trend, let's shift our focus "
             "to the <b style='color:#900C3F'>United States (US) </b> and delve deeper into the trends of COVID-19 in the US.</p>", unsafe_allow_html=True)

    return

def multiselect_vis(df):


    st.header(
        'How have the number of daily covid cases/ deaths/ testing rate/ hospitalization rate/ vaccintaion rate varied in the US?')

    parameters = st.multiselect("Select the parameters  you would like to view!",
                                ["Daily confirmed", "Daily deceased", "Daily tested",
                                 "Daily hospitalized", "Daily vaccinated"], default="Daily confirmed")

    selected_fields = [parameter for parameter in parameters]
    selected_fields.append("date")
    plot_data = df[selected_fields]
    selected_fields.remove("date")
    plot_data = plot_data.melt("date", var_name='parameter', value_name='count')
    plot_data["Name"] = plot_data["parameter"].map(lambda x: x)

    plot = alt.Chart(plot_data).mark_line().encode(
        x=alt.X('date:T', title="Date"),
        y=alt.Y('count:Q', title="Count"),
        color=alt.Color('parameter:N', scale=alt.Scale(
            domain=["Daily confirmed", "Daily deceased", "Daily tested", "Daily hospitalized",
                    "Daily vaccinated"],
            range=['brown', 'red', 'yellow', 'blue', 'green'])),
        tooltip=["parameter", "count"]
    ).interactive().properties(
        width=1000,
        height=400
    )
    st.altair_chart(plot)

    st.write("<p style='font-size:18px'>You can play around with the above chart and compare the trends of different parameters! You can zoom in and out of the chart as required!</p>", unsafe_allow_html=True)
    st.write(
        "<p style='font-size:18px'>Individual bar charts have also been plotted below to remove the scale imbalance between the features "
        "to get a clearer comparison between them!</p>", unsafe_allow_html=True)
    st.write("")
    st.write("")
    st.write("<p style='font-size:18px'>"
             "The trend in daily cases indicates that the US has been seeing a <b style='color:#900C3F'>continuous presence </b> of covid infection. "
             "Additionally, it can be seen that there have been <b style='color:#900C3F'>3 major spikes </b> in covid cases: "
             "<ul><li style='font-size:18px'>October 2020 - February 2021 </li> <li style='font-size:18px'>July 2021 - October 2021</li> <li style='font-size:18px'>December 2021 - February 2022</li> </ul></p>", unsafe_allow_html=True)
    st.write("<p style='font-size:18px'>So how has the increase in number of cases affected the number of daily deaths in the US? "
             "While the scale of <b style='color:#900C3F'>deaths is much lower</b> compared to daily cases, we can still "
             "see similar spike patterns in death as the daily cases. This indicates that these "
             "3 periods that are present could represent  periods of appearance of new variants namely the <b style='color:#900C3F'>Alpha, Delta and "
             "Omicron.</b></p>", unsafe_allow_html=True)
    st.write("<p style='font-size:18px'>It can be seen that <b style='color:#900C3F'>Omicron (3rd wave) is highly infectious</b> as the number of cases soared. A point to note is that "
             "though there has been almost a three times increase in cases in the last wave, <b style='color:#900C3F'>the number of deceased has not seen any "
             "singnificant increase</b>. The number of Hospitalizations has increased, however not in proportion to the increase in cases. "
             "At the same time, from the vaccination graph we see that a large number of individuals were <b style='color:#900C3F'>vaccinated</b> before this period. "
             "Therefore the fact that the death rate has not increased and in fact has gone down if you consider the ratio: number_of_deaths/number_of_cases, "
             "can be attributed to the argument that <b style='color:#900C3F'>vaccinations have helped </b>in preventing serious "
             "illness and therefore prevented hospitalizations and death due to COVID-19.</p>", unsafe_allow_html=True)
    st.write("")


    return


def pie_radix(df):

    st.header('How has COVID-19 affected people across Gender and Age Groups?')

    source = pd.DataFrame({"Gender": ["Male", "Female"], "Cases": [max(df['cumulative_confirmed_male']),
                                                                   max(df['cumulative_confirmed_female'])]})

    base = alt.Chart(source).encode(
        theta=alt.Theta("Cases:Q", stack=True),
        color=alt.Color(field="Gender", type="nominal"),
        tooltip=["Gender", "Cases"]
    ).properties(
        width=500,
        title="COVID cases across Gender"
    )
    pie = base.mark_arc(outerRadius=120)
    text = base.mark_text(radius=150, size=15).encode(text="Gender:N")

    pie_chart = pie + text

    source_age = pd.DataFrame({"Age group": ["0-9", "10-19", "20-29", "30-39", "40-49", "50-59", "60-69", "70-79"],
                               "Cases": [max(df['cumulative_confirmed_age_0']),
                                         max(df['cumulative_confirmed_age_1']),
                                         max(df['cumulative_confirmed_age_2']),
                                         max(df['cumulative_confirmed_age_3']),
                                         max(df['cumulative_confirmed_age_4']),
                                         max(df['cumulative_confirmed_age_5']),
                                         max(df['cumulative_confirmed_age_6']),
                                         max(df['cumulative_confirmed_age_7'])]})
    # Age group
    base = alt.Chart(source_age).encode(
        theta=alt.Theta("Cases:Q", stack=True),
        radius=alt.Radius("Cases", scale=alt.Scale(type="sqrt", zero=True, rangeMin=20)),
        color="Age group:N",
        tooltip=["Age group:N", "Cases:Q"]
    ).properties(
        width=500,
        title="COVID cases across Age Group"
    )

    radix_chart = base.mark_arc(innerRadius=20, stroke="#fff")

    pie_slice, radix_slice = st.columns([1, 1])
    pie_slice.write(pie_chart)
    radix_slice.write(radix_chart)

    pie_slice.write(
        "<p style='font-size:18px'>The pie chart tells us that the Coronavirus has infected approximately an  <b style='color:#900C3F'>equal number of Males and Females</b>. "
        "However, by hovering over the pie chart and looking at the numbers "
        "we can see that there are ~ 3M more Females that were infected as compared to Males.</p>", unsafe_allow_html=True)

    radix_slice.write("<p style='font-size:18px'>The radix chart tells us that young adults of age  <b style='color:#900C3F'>20-29</b> experienced the most number of cases, "
                      "alongside the middle aged adults of 30-60. "
                      "The elderly and children have been comparitively less affected. However, it is worth noting that there have been "
                      "cases of children under 10 years of age also testing positive.</p>", unsafe_allow_html=True)
    radix_slice.write("\n")
    st.write("<p style='font-size:18px'>Now, it might be interesting to see whether through"
             " the course of the two years there have been certain periods during which there is a change in the distribution of cases "
             "across Age Group and Gender </p>", unsafe_allow_html=True)
    return

def gender_age_connected_vis(scatter_plot_data, bar_char_data):

    st.header("How has the number of COVID cases varied across time for different Age Groups and Gender ?")
    brush = alt.selection(type="interval", encodings=["x"])

    points = (
        alt.Chart(scatter_plot_data)
            .mark_point()  # Create scatter plot
            .encode(
            x="Date:T",
            y="New Cases:Q",
            tooltip=["Gender", "Date", "New Cases"],
            color=alt.condition(brush, "Gender:N", alt.value("lightgray")),
        ).add_selection(brush)
    ).properties(title="Click and drag to create a selection region and move the region across left to right",
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
            tooltip=alt.Tooltip(["New Cases", "Age Group"])
        ).transform_filter(brush).interactive().properties(
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

    st.write("<p style='font-size:18px'>The first visualization here reiterates the fact that Males and Females have been infected "
             "equally through the course of the pandemic. Hence, from this observation we can conclude that the  <b style='color:#900C3F'>Coronavirus has affected people "
             "almost equally irrespective of their gender</b>. </p>", unsafe_allow_html=True)
    st.write("<p style='font-size:18px'>By sliding a small window through time and observing the chart at the bottom, "
             "we can see that  <b style='color:#900C3F'>initially the elderly</b> have a higher number of cases and with time, we see that the younger 20-29 age groups"
             "  start to contract the infection more. This could be attributed to the fact that the elderly "
             "were the  <b style='color:#900C3F'>first ones "
             "to get vaccinated </b>and hence they gained improved protection prior to the rest of the population. "
             "So this could be a reason why the number of cases for the elderly starts to drop and the younger population started to "
             "fall sick at later times.</p>", unsafe_allow_html=True)

    st.write(
        "<p style='font-size:18px'>We now have some idea about how the number of cases varied with time and how Coronavirus affected across genders "
        "and age groups.</p>", unsafe_allow_html=True)

    st.write("")
    st.write("")
    st.write("<p style='font-size:18px'>We know that in order to contain the spread of the COVID19 virus, different countries imposed varying levels of containment measures such as <b style='color:#900C3F'>lockdowns</b> and <b style='color:#900C3F'>movement restrictions</b>. "
             "Let us now see how the US government approached this and compare it with another country - how the New Zealand government approached it! </p>", unsafe_allow_html=True)

    return


def mobility_vis(df_mobility):

    # TO DO -- WHAT DOES IT IMPLY? FIX LEGEND
    mobility_chart = alt.Chart(df_mobility).mark_area().encode(
        alt.X('Date:T',
              axis=alt.Axis(format='%m-%Y', domain=False, tickSize=0)
              ),
        alt.Y('sum(Percentage change):Q', stack='center', axis=None),
        alt.Color('Mobility Type:N',
                  scale=alt.Scale(scheme='category10')
                  ),
        alt.Tooltip(["Mobility Type", "Date"])
    ).properties(
        width=600
    ).interactive()
    st.write(mobility_chart)

    return

def plot_usa_line(df_vaccination_usa, df_cases_usa, df_death_hospitalized_usa):

    vaccination_usa_chart = alt.Chart(df_vaccination_usa).mark_line(color='green').encode(
        x='Date',
        y='Number of vaccinated individuals',
        tooltip=alt.Tooltip(["Number of vaccinated individuals", "Date"])
    ).interactive().properties(
        width=600,
        title="COVID Vaccination in the US"
    )

    cases_usa_chart = alt.Chart(df_cases_usa).mark_line(color='brown').encode(
        x='Date',
        y='Number of cases',
        tooltip=alt.Tooltip(["Number of cases", "Date"])
    ).interactive().properties(
        width=600,
        title="COVID Cases in the US"
    )

    deaths_hospitalization_chart = alt.Chart(df_death_hospitalized_usa).mark_line().encode(
        x='Date',
        y='Count',
        tooltip=alt.Tooltip(["Parameter", "Count", "Date"]),
        color='Parameter',
        strokeDash='Parameter'
    ).interactive().properties(
        width=800,
        title="Deaths and Hospitalizations due to COVID in the US"
    )

    col1_1, col1_2 = st.columns(2)
    with col1_1:
        st.header("Vaccinations")
        st.write(vaccination_usa_chart)

    with col1_2:
        st.header("Cases")
        st.write(cases_usa_chart)

    _, col_head, _ = st.columns([1, 2, 1])
    with col_head:
        st.header("Deaths & Hospitalizations")

    _, col, _ = st.columns([1,2,1])
    with col:
        st.write(deaths_hospitalization_chart)

    st.write("<p style='font-size:18px'> Now that we have seen how the trend has varied in time, "
             "we might now want to know whether COVID affects a particular category of people more than others? "
             "Is there any difference in number of cases across <b style='color:#900C3F'>gender </b> and  <b style='color:#900C3F'>age-groups </b>? Let's see what the total numbers uptill Feb 2022 are!</p>", unsafe_allow_html=True)

    return cases_usa_chart

def nz_cases_vis(df_cases_newzealand_daily):
    cases_nz_chart = alt.Chart(df_cases_newzealand_daily).mark_line().encode(
        x='Date',
        y='Number of cases',
        tooltip=alt.Tooltip(["Number of cases", "Date"])
    ).interactive().properties(
        width=600,
        title="COVID cases in New Zealand"
    )

    return cases_nz_chart

def nz_usa_vis(cases_usa_chart, cases_nz_chart, df_mobility_usa, df_mobility_newzealand):

    st.header("How does the US compare to New Zealand in terms of COVID cases and containment measures taken?")
    st.write(
        "<p style='font-size:18px'>Shown below is an interesting visualization called the  <b style='color:#900C3F'>streamgraph </b>that is telling us how the percentage of "
        "mobility of the population for day-to-day activities varied with time. This "
        "will give us an idea of the  <b style='color:#900C3F'>patterns of movement of the citizens </b>of the US and New Zealand."
        " Feel free to zoom in and out of the visualizations!</p>", unsafe_allow_html=True)

    st.write("<p style='font-size:18px'>New Zealand was recently in the news for containing the virus very well and had strict restrictions in place. Let us see if the data"
        " has the same story to tell!</p>", unsafe_allow_html=True)

    col1_1, col1_2 = st.columns(2)
    with col1_1:
        st.header("Change in Mobility in the US")
        mobility_vis(df_mobility_usa)

    with col1_2:
        st.header("Change in Mobility in New Zealand")
        mobility_vis(df_mobility_newzealand)

    st.write(
        "<p style='font-size:18px'>The mobility changes are very different for each of the countries! It is evident that the citizens of the  <b style='color:#900C3F'>US "
        "have not significantly changed </b> their movement patterns through the pandemic. However, the New Zealanders appears to have"
        "  <b style='color:#900C3F'> sharply reduced</b> their outdoor activity during most of the months which could point to those months when they had strict lockdowns imposed by the government. "
        "<b>This decrease in movement is shown after May 22nd on which the New Zealand government imposed it's first lockdown.</b> </p>",
    unsafe_allow_html=True)
    st.write(
        "<p style='font-size:18px'>So was New Zealand severely impacted by Covid that they required strict measures? How did their cases compare to "
        "that of the US?</p>", unsafe_allow_html=True)


    col2_1, col2_2 = st.columns(2)

    with col2_1:
        st.header("Cases in the US")
        st.write(cases_usa_chart)

    with col2_2:
        st.header("Cases in New Zealand")
        st.write(cases_nz_chart)

    st.write(
        "<p style='font-size:18px'>Well, it is clear from these graphs (Note the change in scale of the y-axis!) that New Zealand had very few cases but they still <b style='color:#900C3F'>adopted very strict</b> "
        "measures because of which we see a significant decrease in movements of it's citizens and correspondingly low COVID-19 cases. This shows us how "
        "two countries approach a similar situation in very different ways! There May(not)be a <a href = 'https://www.theregreview.org/2020/06/09/parker-lessons-new-zealand-covid-19-success/'> few lessons for all "
        "countries to learn</a> "
        "to deal with a future pandemic?</p>", unsafe_allow_html=True)

    st.write("")
    st.write("<p style='font-size:18px'>Now, let's get back to the US!</p>", unsafe_allow_html=True)
    st.write("<p style='font-size:18px'> Did you notice that it looks like covid cases sharply increase in the months of October-Janunary for both 2021 and 2022? "
             "This begs the question - Does COVID spread more in the winter? Is it somehow affected by the cooler temperature? Let's check the correlation between some weather parameters and COVID cases to find out!</p>", unsafe_allow_html=True)

    return

def cor_vis(cor_data):

    st.header("Is there any correlation between Weather and COVID? ")

    st.write(
        "<p style='font-size:18px'>Seen below is a correlation plot to investigate the <b style='color:#900C3F'>dependence </b> between multiple variables at the same time. "
        "We are mainly interested in seeing whether the number of covid cases has any dependence on any of the weather "
        "parameters such as <b style='color:#900C3F'>temperature</b>, <b style='color:#900C3F'>rainfall</b>, <b style='color:#900C3F'>humidity</b>?</p>", unsafe_allow_html=True)

    base = alt.Chart(cor_data).encode(
        x='Parameter 1:O',
        y='Parameter 2:O'
    ).properties(
        width=500,
        height=500,
        title="Correlation plot of COVID cases with Weather attributes"
    )

    # Text layer with correlation labels
    # Colors are for easier readability
    text = base.mark_text().encode(
        text='correlation_label',
        color=alt.condition(
            alt.datum.correlation > 0.5,
            alt.value('white'),
            alt.value('black')
        )
    )

    # The correlation heatmap itself
    cor_plot = base.mark_rect().encode(
        color='correlation:Q'
    )

    col1_1, col1_2 = st.columns(2)
    with col1_1:
        st.write(cor_plot + text)  # The '+' means overlaying the text and rect layer

    with col1_2:
        st.write(
            "<p style='font-size:18px'>We can see from the matrix that there appears to be <b style='color:#900C3F'>no significant correlation </b>between the number of cases"
            " and any of the weather parameters. There is a 0.3 correlation (pearsons correaltion coefficient) between temperature and covid cases, however 0.3 is too small a magnitude to conclude a significant correlation between them."
            " It is at best a shaky relationship. </p>", unsafe_allow_html=True)
        st.write("<p style='font-size:18px'> But what about the trend from the daily cases graph that "
            "tells us that during the months of <b style='color:#900C3F'>November - February</b>, there seems to be a spike in cases? Having ruled out weather as a probable cause, this can now probably be attributed to the <b style='color:#900C3F'>holiday "
            "season (Christmas)</b> because of which people tend to get together, celebrate and take part in festivities which could result in more infections. </p>", unsafe_allow_html=True)

    return

def init_text():
    data_url = "https://goo.gle/covid-19-open-data"
    wikipedia_url = "https://en.wikipedia.org/wiki/COVID-19_pandemic"

    st.markdown(
        "<p style='font-size:18px'>Through this dashboard we explore <a href='https://goo.gle/covid-19-open-data'>"
        "The Google Health COVID-19 Open Data</a> and try to study the onset and spread of the COVID-19 Coronavirus in the United States "
        "through interesting visualizations!</p>", unsafe_allow_html=True)

    st.header("About the Coronavirus disease (COVID-19)")
    st.markdown("<p style='font-size:18px'>The <a href = 'https://en.wikipedia.org/wiki/COVID-19_pandemic'>COVID-19 pandemic</a>, also known as the coronavirus pandemic,\
                 is an ongoing <b style='color:#900C3F'>global pandemic </b>of coronavirus disease 2019 (COVID-19) \
                 caused by severe acute respiratory syndrome coronavirus 2 (SARS-CoV-2). \
                 The novel virus was first identified  in the Chinese city of\
                 Wuhan in December 2019 and further spread to almost all parts of the globe.\
                 The World Health Organization (WHO) declared it a <b style='color:#900C3F'>Public Health \
                 Emergency</b> of International Concern on 30 January 2020 and labelled it a pandemic on 11 March 2020. \
                 As of 20 February 2022, the COVID-19 pandemic had caused more than <b style='color:#900C3F'>423 million</b> cases and <b style='color:#900C3F'>5.88</b> million deaths,\
                 making it one of the deadliest in history. The disease is highly transmissible , mainly transmitted via the respiratory route when \
                 people inhale droplets and small airborne particles (that form an aerosol) that infected people exhale as \
                 they breathe, talk, cough, sneeze, or sing. Over the past two years, mutations of the virus have produced many strains (variants) \
                 with varying degrees of infectivity and virulence leading to unprecedented lockdowns and movement \
                 restrictions imposed by many countries.</p>", unsafe_allow_html=True)

if __name__ =="__main__":

    st.markdown("<h1><span style='color:#900C3F'>COVID-19</span> Coronavirus Data Dashboard</h1>", unsafe_allow_html=True)

    init_text()

    # Plot the world covid cases
    location_df, countries = read_files_globe()
    globe_vis(location_df, countries)

    df_cases = read_cases_file()
    # Plot the multiselect timeseries data for cases
    df_multiselect = read_files_multiselect(df_cases)
    multiselect_vis(df_multiselect)

    # Plotting the line graphs, continuing Viz 2
    df_vaccination_usa, df_cases_usa, df_death_hospitalized_usa = get_df_usa(df_cases)
    cases_usa_chart = plot_usa_line(df_vaccination_usa, df_cases_usa, df_death_hospitalized_usa)

    # Plot the pie chart and radix chart
    pie_radix(df_cases)

    # Plot the gender-age connected charts
    scatter_plot_data, bar_chart_data = read_gender_age_files(df_cases)
    gender_age_connected_vis(scatter_plot_data, bar_chart_data)

    df_cases_newzealand, df_cases_newzealand_daily = read_nz_cases()

    # Plot mobility data streamgraph usa and NZ
    df_mobility_usa = read_files_mobility(df_cases)
    df_mobility_newzealand = read_files_mobility(df_cases_newzealand)

    cases_nz_chart = nz_cases_vis(df_cases_newzealand_daily)
    nz_usa_vis(cases_usa_chart, cases_nz_chart, df_mobility_usa, df_mobility_newzealand)

    # Correlation plot
    cor_data = get_cor_data(df_cases)
    cor_vis(cor_data)

    st.write("")
    st.write("")

    st.write("<p style='font-size:18px'>Through this dashboard we were able to get an idea of how the COVID-19 Coronavirus has spread in the US"
             ". We hope we were able to convey some interesting insights about COVID-19! There is still a lot of other parameters that can be explored "
             "with this data, so we encourage you to put on your thinking hat and try it out! <br><br><b style='color:#900C3F'>Happy Visualizing!</b></p> <br><br>", unsafe_allow_html=True)

    st.markdown(
        "This project was created by [Bharani Ujjaini Kempaiah](buk@andrew.cmu.edu) and [Ruben John Mampilli](rmampill@andrew.cmu.edu)\
         for the [Interactive Data Science](https://dig.cmu.edu/ids2022) course at\
          [Carnegie Mellon University](https://www.cmu.edu)")




