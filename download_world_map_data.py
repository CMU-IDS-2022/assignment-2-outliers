import pandas as pd

countries = ['CR', 'TM', 'NC', 'RO', 'TO', 'HK', 'SS', 'IM', 'MX', 'UA', 'SA', 'TN', 'BG', 'LB',
             'HU', 'DE', 'LT', 'US', 'TG', 'FI', 'MQ', 'IQ', 'NP', 'NR', 'TH', 'TC', 'EH', 'FR', 'AS', 'IS',
             'UG', 'VU', 'NZ', 'TV', 'ZM', 'ES', 'IN', 'MV', 'TK', 'GM', 'SR', 'KG', 'PE', 'IL', 'YE', 'AU',
             'ML', 'TW', 'BT', 'BB', 'CN', 'EE', 'HT', 'GH', 'GQ', 'KE', 'MM', 'BF', 'NL', 'TJ', 'NU', 'AR',
             'PK', 'PR', 'KI', 'MY', 'FO', 'AG', 'SV', 'LU', 'NI', 'DK', 'LC', 'BZ', 'TF', 'CK', 'SD', 'LR',
             'BE', 'GY', 'HR', 'CF', 'BR', 'GW', 'CA', 'AO', 'CU', 'MS', 'GL', 'CO', 'KM', 'MC', 'PW', 'KZ',
             'ZA', 'KH', 'SB', 'CL', 'DJ', 'AD', 'SM', 'WS', 'BH', 'GE', 'EC', 'GS', 'NG', 'MW', 'ET', 'KN',
             'CH', 'DO', 'ME', 'TD', 'GU', 'AT', 'GF', 'AI', 'IT', 'JE', 'UM', 'PF', 'YT', 'AZ', 'BY', 'PL',
             'JO', 'PY', 'JP', 'MA', 'SE', 'UZ', 'SL', 'BD', 'AF', 'CW', 'GT', 'SG', 'EG', 'ZW', 'CY', 'PT',
             'JM', 'CZ', 'ID', 'KW', 'MT', 'PG', 'NE', 'SK', 'TT', 'GR', 'OM', 'GG', 'DM', 'MG', 'MU', 'RE',
             'ER', 'IO', 'LK', 'GD', 'LY', 'LV', 'SN', 'LS', 'BS', 'BI', 'MZ', 'AW', 'QA', 'SO', 'PA', 'BM',
             'AE', 'BA', 'GA', 'MP', 'HM', 'WF', 'LI', 'HN', 'GI', 'DZ', 'MN', 'VC', 'NF', 'SI', 'BJ', 'MR',
             'TR', 'KY', 'AL', 'IE', 'SJ', 'CX', 'MH', 'SZ', 'NO', 'RS', 'AQ', 'SC', 'AM', 'CM', 'FJ', 'BV',
             'UY', 'RW', 'BW', 'GN', 'PH']

df_new_cases = pd.DataFrame()
for country in countries:
    file_name = "https://storage.googleapis.com/covid19-open-data/v3/location/" + country + ".csv"
    df = pd.read_csv(file_name)
    df_new_cases = pd.concat([df_new_cases, df])

df_new_cases = df_new_cases[['location_key', 'date', 'country_code', 'country_name', 'new_confirmed', 'latitude', 'longitude']]
df_new_cases.to_csv('new_confirmed_countrywise.csv', index=False)