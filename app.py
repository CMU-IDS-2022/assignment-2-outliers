import streamlit as st
st.set_page_config(layout="wide")
import pandas as pd
import altair as alt
from vega_datasets import data
from datetime import datetime, timedelta
from PIL import Image

corona_virus = Image.open('data/coronavirus.jpeg')

data_url = "https://goo.gle/covid-19-open-data"
wikipedia_url = "https://en.wikipedia.org/wiki/COVID-19_pandemic"
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
    return df

def timestamp(t):
  return pd.to_datetime(t).timestamp() * 1000

def globe_vis(location_df, countries):
    # TO DO --- LEGEND FIX IT
    world = countries
    # Slider for date
    date_slider = st.slider('Date', min(location_df['date']), max(location_df['date']), min(location_df['date']),
                            step=timedelta(days=30), help="Slide over to see different dates")

    # Get subset of dataframe based on selection
    temp_df = location_df[location_df['year'] == date_slider.year]
    temp_df = temp_df[temp_df['month'] == date_slider.month]
    temp_df = temp_df[["date", "country_name", "new_confirmed", "latitude", "longitude"]]

    # Background chart
    background = alt.Chart(world).mark_geoshape(
        fill='lightgray',
        stroke='black'
    ).properties(
        width=1300,
        height=900
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
        size=alt.Size('count:Q', scale=alt.Scale(domain=[1, 20000000], range= [25, 7500])),
        tooltip=['count:Q', "country_name"]
    )

    # Plot both
    st.altair_chart(background + points, use_container_width=True)

    return

def multiselect_vis(df):

    # TO DO -- MAYBE PUT SOME LINES IN ANOTHER CHART? FIX LEGEND
    # convert to date object

    parameter_map = {"Daily confirmed": "new_confirmed",
                     "Daily deceased": "new_deceased",
                     "Daily tested": "new_tested",
                     "Daily hospitalized": "new_hospitalized_patients",
                     "Daily vaccinated": "new_persons_vaccinated",
                     "Daily ICU patients": "new_intensive_care_patients"}

    reverse_parameter_map = {"new_confirmed": "Daily confirmed",
                             "new_deceased": "Daily deceased",
                             "new_tested": "Daily tested",
                             "new_hospitalized_patients": "Daily hospitalized",
                             "new_persons_vaccinated": "Daily vaccinated",
                             "new_intensive_care_patients": "Daily ICU patients"}

    parameters = st.multiselect("What parameters would you like to view?",
                                ["Daily confirmed", "Daily deceased", "Daily tested",
                                 "Daily hospitalized", "Daily vaccinated", "Daily ICU patients"], default="Daily confirmed")

    selected_fields = [parameter_map[parameter] for parameter in parameters]
    selected_fields.append("date")
    plot_data = df[selected_fields]
    selected_fields.remove("date")
    plot_data = plot_data.melt("date", var_name='parameter', value_name='count')
    plot_data["Name"] = plot_data["parameter"].map(lambda x: reverse_parameter_map[x])

    plot = alt.Chart(plot_data).mark_line().encode(
        x='date:T',
        y='count:Q',
        color=alt.Color('parameter:N', scale=alt.Scale(
            domain=["new_confirmed", "new_deceased", "new_tested", "new_hospitalized_patients", "new_persons_vaccinated",
                    "new_intensive_care_patients"],
            range=['brown', 'red', 'yellow', 'blue', 'green', 'orange'])),
        tooltip=["parameter", "count"]
    ).interactive().properties(
        width=1000,
        height=400
    )
    st.altair_chart(plot)

    return


def pie_radix(df):

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
    )

    radix_chart = base.mark_arc(innerRadius=20, stroke="#fff")

    pie_slice, radix_slice = st.columns([3, 1])
    pie_slice.write(pie_chart)
    radix_slice.write(radix_chart)

    return

def gender_age_connected_vis(scatter_plot_data, bar_char_data):

    # TO DO --- FIX XTICK AND YTICK AS THE BAR X AXIS KEEPS CHANGING
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
        width=1000
    ).interactive()
    st.write(mobility_chart)

    return

if __name__ =="__main__":

    # st.title("COVID-19 Coronavirus Data Dashboard")
    col1, mid, col2 = st.columns([20, 1, 10])
    with col1:
        st.title('COVID-19 Coronavirus Data Dashboard')
    # with col2:
        # st.image(corona_virus, caption='Coronavirus')

    st.markdown("Through this dashboard we explore [The Google Health COVID-19 Open Data](%s) regarding the onset and the spread of the COVID-19 Coronavirus"  % data_url)

    st.header("About the Coronavirus disease (COVID-19)")
    st.markdown("The [COVID-19 pandemic] (%s), also known as the coronavirus pandemic,\
             is an ongoing global pandemic of coronavirus disease 2019 (COVID-19) \
             caused by severe acute respiratory syndrome coronavirus 2 (SARS-CoV-2). \
             The novel virus was first identified from an outbreak in the Chinese city of\
             Wuhan in December 2019, and attempts to contain it there failed, allowing it to \
             spread across the globe. The World Health Organization (WHO) declared a Public Health \
             Emergency of International Concern on 30 January 2020 and a pandemic on 11 March 2020. \
             As of 20 February 2022, the pandemic had caused more than 423 million cases and 5.88 million deaths,\
             making it one of the deadliest in history." % wikipedia_url)
    st.write("Let us now dive in to see what the data can tell us about the spread of this disease." )
    st.header('How has the number of covid cases varied across the world?')
    # Plot the world covid cases
    location_df, countries = read_files_globe()
    globe_vis(location_df, countries)

    st.write("The map above gives us insight into how the number of covid cases has changed in the span of 2 years across the countries of the world."
             "We see from the graph that within the span of the first two moths, the infection has spread to almost all countries of the world. There is a "
             "steady increase in the number of cases as months progressed. Overall, "
             "we can see that countries that have reported the most number of cases include USA, India, Brazil, France, UK, Russia, Germany, Turkey"
             "Data from the [] also indicate that the United States of America has experienced the highest number of covid cases and we will now "
             "attempt to delve deeper into the trends of COVID-19 in the US.")

    st.header('How have the number of daily covid cases/ deaths/ testing/ hospitalization and testing varied in the US?')

    df_cases = read_cases_file()

    # Plot the multiselect timeseries data for cases
    df_multiselect = read_files_multiselect(df_cases)
    multiselect_vis(df_multiselect)

    st.write("The trend in daily cases indicates that the US has been seeing a continuous presence of covid infection"
             "Additionally, it appears that there have been 3 major spikes in covid cases:"
             " October 2020 - February 2021, July 2021 - October 2021 and December 2021 - February 2022"
             "So how has the increase in number of cases affected the number of daily deaths in the US?"
             "While the scale of the deaths is much lower compared to daily cases, we can still "
             "see similar spike patterns in death as the daily cases. This indicates that the "
             "3 periods that are present could indicate periods of appearance of new variants that are more"
             "infectious and dangerous than the earlier ones. On observing the vaccination graph and ICU admitted patients graph, "
             "we see that the number of ICU admitted patients has dropped a lot. This could be attributed to the effect of "
             "vaccinations in preventing the infection from causing serious conditions. This evidence supports the widely "
             "acknowledged claim that vaccines are effective and can  help prevent serious illness")
    # Plot the pie chart and radix chart
    pie_radix(df_cases)

    # Plot the gender-age connected charts
    scatter_plot_data, bar_chart_data = read_gender_age_files(df_cases)
    gender_age_connected_vis(scatter_plot_data, bar_chart_data)

    # Plot economy
    df_economy = read_files_economy(df_cases)
    economy_vis(df_economy)

    # Plot mobility data
    df_mobility = read_files_mobility(df_cases)
    mobility_vis(df_mobility)










