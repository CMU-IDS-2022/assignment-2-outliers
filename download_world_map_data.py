import pandas as pd


countries = ['TH', 'CI', 'FR', 'GS', 'GY', 'LK', 'CG', 'CO', 'SG', 'ZM', 'VN', 'CM', 'AU',
             'ML', 'VC', 'QA', 'LB', 'BM', 'SI', 'CR', 'BV', 'BT', 'FK', 'BY', 'KY', 'RU',
             'SZ', 'MY', 'PL', 'WF', 'EC', 'IM', 'JE', 'WS', 'BD', 'TF', 'MS', 'FI', 'AL',
             'NI', 'UG', 'MX', 'AS', 'CW', 'IL', 'GW', 'ME', 'JP', 'BF', 'ER', 'LS', 'AR',
             'LT', 'MK', 'SM', 'AQ', 'KE', 'TO', 'BN', 'SD', 'RE', 'HT', 'FJ', 'PN', 'SJ',
             'SL', 'TL', 'MW', 'BE', 'BZ', 'LC', 'SS', 'SY', 'MQ', 'CZ', 'UA', 'GH', 'SX',
             'TW', 'AE', 'BW', 'VU', 'DO', 'AG', 'KP', 'YT', 'NL', 'SB', 'CU', 'JM', 'BQ',
             'MN', 'EH', 'GI', 'KZ', 'AM', 'RS', 'CF', 'AF', 'PY', 'GB', 'BI', 'ST', 'EG',
             'CX', 'GT', 'CV', 'AD', 'IE', 'XK', 'MD', 'MU', 'VE', 'KM', 'DZ', 'RW', 'US',
             'ET', 'NP', 'YE', 'UY', 'MA', 'MG', 'BR', 'SH', 'MT', 'DM', 'HN', 'LY', 'ID',
             'LA', 'IR', 'MM', 'HU', 'NC', 'PK', 'VG', 'GF', 'GE', 'GN', 'ES', 'HM', 'SC',
             'SN', 'FM', 'IQ', 'NF', 'RO', 'ZA', 'KW', 'BA', 'AN', 'BJ', 'MZ', 'TK', 'MP',
             'MO', 'IT', 'DE', 'NE', 'NU', 'LU', 'IO', 'TN', 'TT', 'AI', 'SV', 'BG', 'PE',
             'SK', 'PG', 'NR', 'PW', 'AW', 'TD', 'AT', 'KI', 'IN', 'TG', 'UZ', 'VA', 'GR',
             'KH', 'TV', 'TZ', 'FO', 'GL', 'AZ', 'KG', 'CN', 'PH', 'JO', 'KN', 'CC', 'TJ',
             'PR', 'TC', 'ZW', 'LV', 'SO', 'DJ', 'CH', 'GG', 'PA', 'TR', 'MC', 'MV', 'AO',
             'CY', 'SE', 'NG', 'OM', 'CL', 'BS', 'BH', 'HR', 'PS', 'DK', 'LI', 'BB', 'MR',
             'PF', 'GM', 'HK', 'SA', 'GD', 'CA', 'CD', 'GA', 'LR', 'CK', 'MH', 'SR', 'GQ',
             'TM', 'VI', 'KR', 'BO', 'EE', 'NO', 'IS', 'NZ', 'UM', 'PT', 'GU']

df_new_cases = pd.DataFrame()
for country in countries:
    file_name = "https://storage.googleapis.com/covid19-open-data/v3/location/" + country + ".csv"
    df = pd.read_csv(file_name)
    df_new_cases = pd.concat([df_new_cases, df])

df_new_cases = df_new_cases[['location_key', 'date', 'country_code', 'country_name', 'new_confirmed', 'latitude', 'longitude']]
df_new_cases.to_csv('new_confirmed_countrywise.csv', index=False)