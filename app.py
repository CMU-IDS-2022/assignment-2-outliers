import streamlit as st
st.set_page_config(layout="wide")
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
    df_mobility = df_mobility.melt("date", var_name='Mobility Type', value_name='Percentage change')

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

def timestamp(t):
  return pd.to_datetime(t).timestamp() * 1000

def globe_vis(location_df, countries):

    st.write(
        " First, to give us some context, let us look at how the COVID-19 disease has spread in various countries across time.")
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
        "The map above gives us insight into how the number of covid cases has changed in the span of 2 years across the countries of the world."
        " We see from the graph that within the span of the first 3 months, the infection has spread to almost all countries of the world. "
        "This shows how quickly the COVID-19 disease can spreads from one location to another. "
        "There is an almost exponential increase in the number of cases as months progressed. "
        "Overall, we can see that countries that have reported the most number of cases include USA, India, Brazil, France, UK, Russia, Germany and Turkey. "
        "We can also see that it is of a fluctuating nature in which there are periods in which  cases sharply increase and then reduce. "
        "An interesting observation is to note how once a country gets infected with COVID-19, it does not go away! "
        "It is evident that the past couple of months of December 2021 and January 2022 has seen a huge increase in the number of cases especially in the United States. ")

    st.write("Now, since we have an idea of the overall trend, let's shift our focus to the United States and delve deeper into the trends of COVID-19 in the US.")

    return

def multiselect_vis(df):

    # TO DO -- MAYBE PUT SOME LINES IN ANOTHER CHART? FIX LEGEND
    # convert to date object

    st.header(
        'How have the number of daily covid cases/ deaths/ testing rate/ hospitalization rate and vaccintaion rate varied in the US?')

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
        x='date:T',
        y='count:Q',
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

    st.write("The trend in daily cases indicates that the US has been seeing a continuous presence of covid infection"
             "Additionally, it appears that there have been 3 major spikes in covid cases:"
             " October 2020 - February 2021, July 2021 - October 2021 and December 2021 - February 2022"
             "So how has the increase in number of cases affected the number of daily deaths in the US?"
             "While the scale of the deaths is much lower compared to daily cases, we can still "
             "see similar spike patterns in death as the daily cases. This indicates that the "
             "3 periods that are present could indicate periods of appearance of new variants that are more"
             "infectious and dangerous than the earlier ones. A point to note is that"
             "though there has been almost a three times increase in cases in the last wave, the number of deceased has not seen any"
             "singnificant increase. This further strengthens the point that vaccinations has helped in preventing serious"
             "illness and death due to COVID-19 Coronavirus. Now that we have seen how the trend has varied in time, "
             "we might now want to know whether there is any difference in number of cases across gender and age-group?")

    return


def pie_radix(df):

    st.header('How has COVID-19 affected across Genders and Age Groups?')

    source = pd.DataFrame({"Gender": ["Male", "Female"], "Cases": [max(df['cumulative_confirmed_male']),
                                                                   max(df['cumulative_confirmed_female'])]})

    base = alt.Chart(source).encode(
        theta=alt.Theta("Cases:Q", stack=True),
        color=alt.Color(field="Gender", type="nominal"),
        tooltip=["Gender", "Cases"]
    ).properties(
        width=500
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
        width=500
    )

    radix_chart = base.mark_arc(innerRadius=20, stroke="#fff")

    pie_slice, radix_slice = st.columns([1, 1])
    pie_slice.write(pie_chart)
    radix_slice.write(radix_chart)

    pie_slice.write(
        "The pie chart tells us that the Coronavirus has infected approximately an equal number of Males and Females. "
        "However, by hovering over the pie chart and looking at the numbers "
        "we can see that there are ~ 3M more Females that were infected as compared to Males. \n")

    radix_slice.write("The radix chart tells us that young adults of age 20-29 experienced the most number of cases, "
                      "alongside the middle aged adults of 30-60. "
        "The elderly and children have been comparitively less affected. However, it is worth noting that there have been"
        "cases of children under 10 years of age also testing positive.")
    radix_slice.write("\n")
    st.write("Now, it might be interesting to see whether through"
        " the course of the two years there have been certain periods during which there is a change in the distribution of cases"
             "across Age Groups. ")

    return

def gender_age_connected_vis(scatter_plot_data, bar_char_data):

    # TO DO --- FIX XTICK AND YTICK AS THE BAR X AXIS KEEPS CHANGING

    st.header("How has the number of cases varied across Age Groups through the pandemic?")
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

    st.write("The first visualization here reiterates the fact that Males and Females have been infected"
             "equally through the course of the pandemic. Hence, from this observation we can conclude that the Coronavirus has affected people"
             "equally irrespective of their gender. ")
    st.write("By sliding a small window through time and observing the chart at the bottom, "
             "we can see that initially the elderly have a higher number of cases and with time, we see that the younger 20-29 age groups"
             "are starting to contract the infection more. This could be attributed to the fact that the elderly were more likely to"
             "contract the virus initially, but they were the first ones"
             "to get vaccinated and hence they gained improved protection prior to the rest of the population. "
             "So this could be a reason why the number of cases for the elderly starts to drop and the younger population started to"
             "fall sick at later times")

    st.write("We now have some idea about how the number of cases varied with time and how Coronavirus affected across genders"
             "and age groups. So how does the US compare to another country in the world? Have they also seen similar trends "
             "as the US? Let's find out!")

    return

def economy_vis(df_economy):

    # TO DO --- FIND ANOTHER ECONOMY PARAMETER; FIX LEGEND
    economy_chart = alt.Chart(df_economy).mark_line().encode(
        x='Date',
        y='Value',
        color='parameter',
        strokeDash='parameter',
    ).properties(
        width=1000
    )
    st.write(economy_chart)

    return

def mobility_vis(df_mobility):


    # TO DO -- WHAT DOES IT IMPLY? FIX LEGEND
    mobility_chart = alt.Chart(df_mobility).mark_area().encode(
        alt.X('date:T',
              axis=alt.Axis(format='%m-%Y', domain=False, tickSize=0)
              ),
        alt.Y('sum(Percentage change):Q', stack='center', axis=None),
        alt.Color('Mobility Type:N',
                  scale=alt.Scale(scheme='category10')
                  )
    ).properties(
        width=600
    ).interactive()
    st.write(mobility_chart)

    return

def plot_usa_line(df_vaccination_usa, df_cases_usa, df_death_hospitalized_usa):

    vaccination_usa_chart = alt.Chart(df_vaccination_usa).mark_line().encode(
        x='Date',
        y='Number of vaccinated individuals'
    ).interactive().properties(
        width=1000,
        height=400
    )
    st.write(vaccination_usa_chart)

    cases_usa_chart = alt.Chart(df_cases_usa).mark_line().encode(
        x='Date',
        y='Number of cases'
    ).interactive().properties(
        width=1000,
        height=400
    )
    st.write(cases_usa_chart)

    deaths_hospitalization_chart = alt.Chart(df_death_hospitalized_usa).mark_line().encode(
        x='Date',
        y='Count',
        color='Parameter',
        strokeDash='Parameter',
    ).interactive().properties(
        width=1000,
        height=400
    )
    st.write(deaths_hospitalization_chart)
    return cases_usa_chart

def init_text():
    data_url = "https://goo.gle/covid-19-open-data"
    wikipedia_url = "https://en.wikipedia.org/wiki/COVID-19_pandemic"

    st.markdown(
        "Through this dashboard we explore [The Google Health COVID-19 Open Data](%s) regarding the onset and the spread of the COVID-19 Coronavirus" % data_url)

    st.header("About the Coronavirus disease (COVID-19)")
    st.markdown("The [COVID-19 pandemic](%s), also known as the coronavirus pandemic,\
                 is an ongoing global pandemic of coronavirus disease 2019 (COVID-19) \
                 caused by severe acute respiratory syndrome coronavirus 2 (SARS-CoV-2). \
                 The novel virus was first identified  in the Chinese city of\
                 Wuhan in December 2019 and further spread to almost all parts of the globe.\
                 The World Health Organization (WHO) declared it a Public Health \
                 Emergency of International Concern on 30 January 2020 and labelled it a pandemic on 11 March 2020. \
                 As of 20 February 2022, the COVID-19 pandemic had caused more than 423 million cases and 5.88 million deaths,\
                 making it one of the deadliest in history. The disease is highly transmissible , mainly transmitted via the respiratory route when \
                 people inhale droplets and small airborne particles (that form an aerosol) that infected people exhale as \
                 they breathe, talk, cough, sneeze, or sing. Over the past two years, mutations of the virus have produced many strains (variants) \
                 with varying degrees of infectivity and virulence. The pandemic led to unprecedented lockdowns and movement \
                 restrictions imposed by many countries. Educational institutions and public areas were partially \
                  or fully closed in many jurisdictions, and many events were cancelled or postponed. \
                  Misinformation circulated through social media and mass media, and political tensions intensified. \
                  The pandemic raised issues of racial and geographic discrimination, health equity, and the balance between \
                  public health imperatives and individual rights." % wikipedia_url)

if __name__ =="__main__":

    st.title("COVID-19 Coronavirus Data Dashboard")

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

    # Plot mobility data streamgraph usa
    df_mobility_usa = read_files_mobility(df_cases)

    # Plot mobility data streamgraph NZ
    df_cases_newzealand = pd.read_csv("data/NZ.csv")
    df_cases_newzealand['date'] = df_cases_newzealand['date'].map(lambda row: datetime.strptime(row, '%Y-%m-%d').date())
    df_mobility_newzealand = read_files_mobility(df_cases_newzealand)



    df_cases_newzealand_daily = df_cases_newzealand[["date", "new_confirmed"]]
    df_cases_newzealand_daily.rename(columns={"date": "Date", "new_confirmed": "Number of cases"},
                        inplace=True)
    cases_nz_chart = alt.Chart(df_cases_newzealand_daily).mark_line().encode(
        x='Date',
        y='Number of cases'
    )

    st.header("How does the US compare to New Zealand?")
    st.write("Shown below is an interesting visualization called the streamgraph that is telling us how the percentage of "
             "mobility of the population for day-to-day activities varied with respect to a baseline which was pre-covid. This "
             "will give us an idea of the patterns of movement of the citizens of the US and New Zealand. NZ was in the "
             "news for containing the virus very well and had strict restrictions in place. Let us see if the data"
             " has the same story to tell!")
    col1_1, col1_2 = st.columns(2)
    with col1_1:
        st.header("US mobility")
        mobility_vis(df_mobility_usa)

    with col1_2:
        st.header("NZ mobility")
        mobility_vis(df_mobility_newzealand)

    st.write("The mobility changes are very different for each of the countries! It is evident that the citizens of the US "
             "have not changed any of their movement patterns through the pandemic. However, the New Zealanders appears to have"
             " sharply reduced their activity during a few months which could point to those months when they had strict lockdowns")
    st.write("So was the NZ then under severe impact of Covid that they required strict measures? How did their cases compare to "
             "that of the US?")
    col2_1, col2_2 = st.columns(2)

    with col2_1:
        st.header("US cases")
        st.write(cases_usa_chart)

    with col2_2:
        st.header("NZ cases")
        st.write(cases_nz_chart)

    st.write("Well, it is clear from these graphs that the NZ had very few cases but they must have adopted very strict "
             "measures because of which we see a significant change in movements of it's citizens. This shows us how "
             "two countries approach a situation they face in very different ways!")

    # Correlation plot
    df_correlation = df_cases[["new_confirmed", "average_temperature_celsius", "rainfall_mm", "relative_humidity"]]
    df_correlation.rename(columns={"date": "Date", "new_confirmed": "Cases",
                                              "average_temperature_celsius": "Temperature",
                                   "rainfall_mm": "Rainfall", "relative_humidity": "Humidity"}, inplace=True)
    cor_data = (df_correlation
                .corr().stack()
                .reset_index()  # The stacking results in an index on the correlation values, we need the index as normal columns for Altair
                .rename(columns={0: 'correlation', 'level_0': 'Parameter 1', 'level_1': 'Parameter 2'}))
    cor_data['correlation_label'] = cor_data['correlation'].map('{:.2f}'.format)  # Round to 2 decimal
    base = alt.Chart(cor_data).encode(
        x='Parameter 1:O',
        y='Parameter 2:O'
    ).properties(
        width=500,
        height=500
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

    st.write(cor_plot + text)  # The '+' means overlaying the text and rect layer








