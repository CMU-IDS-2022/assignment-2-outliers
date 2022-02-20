import streamlit as st
import pandas as pd
import altair as alt
from vega_datasets import data

def globe_vis(location_df):
    countries = alt.topo_feature(data.world_110m.url, 'countries')

    rotation_degree_x = st.slider('X axis', -180, 180, 0, help="Slide over to rotate left to right")
    rotation_degree_z = st.slider('Y axis', -180, 180, 0, help="Slide over to rotate top to bottom")

    return alt.Chart(countries).mark_geoshape(stroke='black', strokeWidth=1.5)\
        .encode(color='cumulative_confirmed:Q', tooltip=['country_name:N', 'cumulative_confirmed:Q'])\
        .transform_lookup(
            lookup='id',
            from_=alt.LookupData(location_df, key='id', fields=['cumulative_confirmed', "country_name"])
        )\
        .project(type='orthographic')\
        .properties(
            width=700,
            height=700,
            title='Cumulative covid cases in the world'
        ).configure_projection(
        rotate=[rotation_degree_x, rotation_degree_z, 0]
        )

if __name__ =="__main__":

    st.title("COVID-19 Coronavirus Data Dashboard")

    # Worldwide heat map based on number of cases in the recent past
    df_index = pd.read_csv("data/index.csv")
    df_index = df_index[["location_key", "country_name"]]

    df_geography = pd.read_csv("data/geography.csv")
    df_geography = df_geography[["location_key", "latitude", "longitude"]]

    df_cases = pd.read_csv("data/epidemiology.csv")
    df_cases = df_cases[["date", "location_key", "cumulative_confirmed", "cumulative_deceased"]]

    country_info = pd.read_json('data/all_countries.json')
    countries = list(country_info.name)
    # country_info.set_index("name", inplace=True)

    # Set index so that join can be done easily
    df_geography.set_index("location_key", inplace=True)
    df_index.set_index("location_key", inplace=True)
    df_cases.set_index("location_key", inplace=True)
    # Perform inner join to get latitude and longitude details for country
    location_df = df_index.join(df_geography, how="inner")
    location_df = location_df.join(df_cases, how="left")

    # Reset index
    location_df.reset_index(inplace=True)

    # Getting rid of subregion fields
    location_df = location_df[location_df['location_key'].str.len() == 2]
    location_df = location_df.astype({'country_name': 'string'})

    location_df = location_df[location_df['country_name'].isin(countries)]
    location_df["id"] = location_df["country_name"].map(
        lambda x: country_info[country_info["name"] == x]["numericCode"].values[0])

    globe = globe_vis(location_df)
    st.write(globe)

