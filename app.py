import streamlit as st
import pandas as pd
import altair as alt
from vega_datasets import data
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import math

def globe_vis(location_df, countries, country_names, country_info):

    '''
    # TO DO:
    1) Slider for time
    2) Fix empty areas
    3) Fix color scheme
    4) Reduce size of slider and place on the side of the visualization
    5) Fix boundary of earth
    '''

    #rotation_degree_x = st.slider('X axis', -180, 180, 0, help="Slide over to rotate left to right")
    #rotation_degree_z = st.slider('Y axis', -180, 180, 0, help="Slide over to rotate top to bottom")
    date_slider = st.slider('Date', min(location_df['date']), max(location_df['date']), max(location_df['date']), step=timedelta(days=30), help="Slide over to see different dates")
    temp_df = location_df[location_df['year'] == date_slider.year]
    temp_df = temp_df[temp_df['month'] == date_slider.month]
    temp_df = temp_df[["country_name", "new_confirmed"]]
    countries_with_val = set(temp_df['country_name'])
    new_countries = []
    flag = 0
    for i in country_names:
        if i not in countries_with_val:
            flag = 1
            new_countries.append(i)
    if flag:
        new_confirmed = [0] * len(new_countries)
        new_df = pd.DataFrame({'country_name':new_countries, 'new_confirmed': new_confirmed})
        temp_df = pd.concat([temp_df, new_df], ignore_index = True, axis = 0)


    temp_df["id"] = temp_df["country_name"].map(
        lambda x: country_info[country_info["name"] == x]["numericCode"].values[0])

    globe = alt.Chart(countries).mark_geoshape(stroke='black', strokeWidth=1.5)\
        .encode(size=alt.Size('new_confirmed:Q'), tooltip=['country_name:N', 'new_confirmed:Q'])\
        .transform_lookup(
            lookup='id',
            from_=alt.LookupData(temp_df, key='id', fields=["country_name", "new_confirmed"])
        )\
        .project(type='equirectangular')\
        .properties(
            width=1000,
            height=500,
            title='Monthly covid cases in the world'
        )\
        # .configure_projection(
        # rotate=[rotation_degree_x, rotation_degree_z, 0]
        # )
    st.write(globe)
    return

@st.cache
def read_initial():

    country_info = pd.read_json('data/all_countries.json')
    countries = list(country_info.name)

    # Perform inner join to get latitude and longitude details for country
    df_new_cases_country = pd.read_csv("data/new_confirmed_countrywise.csv")

    location_df = df_new_cases_country
    # Getting rid of subregion fields
    location_df = location_df[location_df['location_key'].str.len() == 2]
    location_df = location_df.astype({'country_name': 'string'})

    location_df = location_df[location_df['country_name'].isin(countries)]
    country_names = countries
    countries = alt.topo_feature(data.world_110m.url, 'countries')
    location_df = location_df.dropna(subset=['date'])
    location_df['date'] = location_df['date'].map(lambda row: datetime.strptime(row, '%Y-%m-%d').date())
    location_df['month'] = location_df['date'].map(lambda row: row.month)
    location_df['year'] = location_df['date'].map(lambda row: row.year)
    location_df = location_df.groupby(['year', 'month', 'country_name']).sum().reset_index()
    location_df['date'] = location_df.apply(lambda row: datetime.strptime(str(row['year'])+'-'+str(row['month']), '%Y-%m').date(), axis=1)
    location_df['new_confirmed'] = location_df['new_confirmed'].fillna(0)
    # location_df['new_confirmed'] = location_df.apply(lambda row: 0 if row['new_confirmed'] <= 0 else math.log(row['new_confirmed'], 1.5), axis=1)
    return location_df, countries, country_names, country_info

if __name__ =="__main__":

    st.title("COVID-19 Coronavirus Data Dashboard")

    location_df, countries, country_names, country_info = read_initial()

    globe_vis(location_df, countries, country_names, country_info)


