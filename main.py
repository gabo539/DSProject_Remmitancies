from functions import *
from xml_parser import parse_xml  # Import the parse_xml function

# Load the data
wwrem_p_gdp = pd.read_csv('Dataframes/world_economic_indicators.csv')
gini_coeff = pd.read_csv('Dataframes/Gini_Coefficient_code.csv')
gdp_pcppp = pd.read_csv('Dataframes/GDP_percapita_PPP.csv')
relative_poverty = pd.read_csv('Dataframes/poverty-explorer.csv')

# Limiting to relevant data
wwrem_first_4_columns = wwrem_p_gdp.iloc[:, 0:4]

# Limitation to the interval from 1990 to 2019
wwrem_first_4_columns_90to20 = wwrem_first_4_columns[(wwrem_first_4_columns['Year'] >= 1990) & (wwrem_first_4_columns['Year'] <= 2019)]

# Summation of all remittances of all countries on each separate year
sum_per_year = wwrem_first_4_columns_90to20.groupby('Year')['Personal remittances, received (% of GDP)'].mean()

# Plot 1:  % remittances received of Worldwide GDP
plt.figure(figsize=(10, 6))
plt.plot(sum_per_year.index, sum_per_year.values, marker='o', linestyle='-')
plt.xlabel('Year')
plt.ylabel('Sum of Remittances, received (% of GDP)')
plt.title('Sum of Remittances, received (% of GDP) over years')
plt.grid(True)
plt.tight_layout()
plt.show()

### RELATIVE REMITTANCES ###

# Calculate the mean of "Personal remittances, received (% of GDP)" for each country in the period from 1990 till 2019
mean_remittances = wwrem_first_4_columns_90to20.groupby(['Country Name', 'Country Code'])[
    'Personal remittances, received (% of GDP)'].mean().reset_index()

# Rename the columns for clarity
mean_remittances.columns = ['Country Name', "Country Code", 'Mean Personal remittances, received (% of GDP)']

# Get Top 5 and Bottom 5 countries of relative remittances
top_5_rel_rem, bottom_5_rel_rem = top_5(mean_remittances, "Mean Personal remittances, received (% of GDP)")

### TOTAL REMITTANCES ###

# Ensure the relevant columns are numeric
wwrem_p_gdp['Personal remittances, received (% of GDP)'] = pd.to_numeric(
    wwrem_p_gdp['Personal remittances, received (% of GDP)'], errors='coerce')
wwrem_p_gdp['GDP (current US$)'] = pd.to_numeric(wwrem_p_gdp['GDP (current US$)_y'], errors='coerce')

# Calculate the Total Remittances
wwrem_p_gdp['Total Remittances'] = (
            (wwrem_p_gdp['Personal remittances, received (% of GDP)'] / 100) * wwrem_p_gdp['GDP (current US$)_y'])

wwrem_total_rem_90to19 = wwrem_p_gdp[(wwrem_p_gdp['Year'] >= 1990) & (wwrem_p_gdp['Year'] <= 2019)]

# Calculate the mean that each country received from 1990-2019
total_remittances_by_country = wwrem_total_rem_90to19.groupby(['Country Code'])[
    'Total Remittances'].mean().reset_index()

# Clean and Filter Dataframe
total_remittances_by_country = clean(total_remittances_by_country, 'Total Remittances')

total_remittances_by_country_clean = filter(total_remittances_by_country)

# Only keep the rows where the total remittances are greater than 0 (potentially no data)
total_remittances_by_country_clean = total_remittances_by_country_clean[
    (total_remittances_by_country_clean['Total Remittances'] >= 1)]

# Get Top 5 and Bottom 5 countries of total remittances
top_5_total_rem, bottom_5_total_rem = top_5(total_remittances_by_country_clean, 'Total Remittances')

gdp_for_top_5_total_rem = get_frame(top_5_total_rem, wwrem_total_rem_90to19)
gdp_for_top_5_rel_rem = get_frame(top_5_rel_rem, wwrem_total_rem_90to19)

### FDI ANALYSIS ###
xml_file = 'Dataframes/FDI.xml'

# XML-Daten in DataFrame laden
data = parse_xml(xml_file)
fdi_df = pd.DataFrame(data)
fdi_df_90to19 = fdi_df[(fdi_df['Year'] >= 1990) & (fdi_df['Year'] <= 2019)]

# Calculate the mean of "FDI" for each country in the period from 1990 till 2019
mean_fdi = fdi_df_90to19.groupby('Country Code')['Value'].mean().reset_index()

# Rename the columns for clarity
mean_fdi.columns = ['Country Code', 'Mean FDI']

# Filter & clean the data frame
mean_fdi = filter(mean_fdi)
mean_fdi = clean(mean_fdi, 'Mean FDI')

# Get Top 5 and Bottom 5 countries of relative remittances
top_5_rel_fdi, bottom_5_rel_fdi = top_5(mean_fdi, "Mean FDI")

total_gdp_mean_by_country = wwrem_total_rem_90to19.groupby(['Country Name', 'Country Code'])[
    'GDP (current US$)_x'].mean().reset_index()

# Filter and clean dataframe
total_gdp_mean_by_country = filter(total_gdp_mean_by_country)
total_gdp_mean_by_country = clean(total_gdp_mean_by_country, 'GDP (current US$)_x')
top_5_gdp, bottom_5_gdp = top_5(total_gdp_mean_by_country, 'GDP (current US$)_x')

x = comparable_country('IND', total_gdp_mean_by_country, mean_remittances, mean_fdi, 0.05)
y = comparable_country('MEX', total_gdp_mean_by_country, mean_remittances, mean_fdi, 0.05)
z = comparable_country('PHL', total_gdp_mean_by_country, mean_remittances, mean_fdi, 0.3)
v = comparable_country('NGA', total_gdp_mean_by_country, mean_remittances, mean_fdi, 0.05)

#analize fdi/rem over the years in comparable countries
gdp_by_country_per_year = wwrem_total_rem_90to19.groupby(['Country Name', 'Country Code'])['GDP (current US$)_x']

gdp_fdi_merge = pd.merge(wwrem_total_rem_90to19, fdi_df_90to19, on='Country Code')

# Group by relevant columns and aggregate using mean (or any other appropriate function)
gdp_fdi_merge = gdp_fdi_merge.groupby(['Country Name', 'Country Code', 'Year_x'], as_index=False).mean()

# Optional: Rename 'Year_x' to 'Year' for clarity
gdp_fdi_merge.rename(columns={'Year_x': 'Year'}, inplace=True)

gdp_fdi_clean = gdp_fdi_merge[[
    'Country Name', 'Country Code', 'Year',
    'Personal remittances, received (% of GDP)',
    'GDP (current US$)_x', 'Value'
]]

gdp_fdi_clean['Relative FDI (%)'] = (gdp_fdi_clean['Value'] / gdp_fdi_clean['GDP (current US$)_x']) * 100


### GDP ###

india_rem_df = get_row(wwrem_first_4_columns_90to20, 'IND')
x_fdi_df = get_row(gdp_fdi_clean, x)

mex_rem_df = get_row(wwrem_first_4_columns_90to20, 'MEX')
y_fdi_df = get_row(gdp_fdi_clean, y)

phil_rem_df = get_row(wwrem_first_4_columns_90to20, 'PHL')
z_fdi_df = get_row(gdp_fdi_clean, z)

nigeria_rem_df = get_row(wwrem_first_4_columns_90to20, 'NGA')
v_fdi_df = get_row(gdp_fdi_clean, v)

# Collect GDP growth rates for the countries
df_ind, df_x, gr_ind, _ = growth_rate_plots(gdp_fdi_clean, 'IND', x)
df_mex, df_y, gr_mex, _ = growth_rate_plots(gdp_fdi_clean, 'MEX', y)
df_phl, df_z, gr_phl, _ = growth_rate_plots(gdp_fdi_clean, 'PHL', z)
df_nga, df_v, gr_nga, _ = growth_rate_plots(gdp_fdi_clean, 'NGA', v)

# Combine all DataFrames into one
combined_df = pd.concat([df_ind, df_mex, df_phl, df_nga, df_x, df_y, df_z, df_v])

# Reset index for the combined DataFrame
combined_df.reset_index(drop=True, inplace=True)

# Save the combined DataFrame to a CSV file (optional)
combined_df.to_csv('combined_gdp_growth_rates.csv', index=False)

### GDP PPP ###

# Adjust the column names based on inspection
gdp_pcppp.columns = ['Country', 'Country Code'] + [str(year) for year in range(1990, 2020)]

# Melt the dataframe to long format
gdp_pcppp = pd.melt(gdp_pcppp, id_vars=['Country', 'Country Code'], var_name='Year', value_name='GDP_PPP')

# Convert 'Year' column to integer
gdp_pcppp['Year'] = gdp_pcppp['Year'].astype(int)

gdp_pc_ppp_plot(gdp_pcppp, "IND", "TTO")
gdp_pc_ppp_plot(gdp_pcppp, "MEX", "GNB")
gdp_pc_ppp_plot(gdp_pcppp, "NGA", "ROU")
gdp_pc_ppp_plot(gdp_pcppp, "PHL", "LCA")

negative_gdp_growth = combined_df[combined_df['GDP Growth Rate (%)'] < 0]
negative_gdp_sums = negative_gdp_growth.groupby('Country Name')['GDP Growth Rate (%)'].sum().reset_index()
negative_gdp_sums = negative_gdp_sums.rename(columns={'GDP Growth Rate (%)': 'Summed Up Decrease Rate (%)'})
print(negative_gdp_sums)

countries_to_include = ['India', 'Nigeria', 'Mexico', 'Philippines']
filtered_df = negative_gdp_sums[negative_gdp_sums['Country Name'].isin(countries_to_include)]
total_negative_growth = filtered_df["Summed Up Decrease Rate (%)"].sum()
rem_counties_neg_fluc = total_negative_growth / 4
print('avg rem countries fluc: ', rem_counties_neg_fluc)

countries_to_include = ['Guinea-Bissau', 'Romania', 'St. Lucia', 'Trinidad and Tobago']
filtered_df = negative_gdp_sums[negative_gdp_sums['Country Name'].isin(countries_to_include)]
total_negative_growth = filtered_df["Summed Up Decrease Rate (%)"].sum()
fdi_counties_neg_fluc = total_negative_growth / 4
print('avg fdi countries fluc: ', fdi_counties_neg_fluc)

### POVERTY LINE PLOTS ###

countries = [
    'India', 'Trinidad and Tobago', 'Nigeria', 'Romania',
    'Mexico', 'Guinea-Bissau', 'Philippines', 'Saint Lucia', 'France', 'South Korea'
]
filtered_poverty = relative_poverty[
    (relative_poverty['Country'].isin(countries)) & (relative_poverty['Year'] >= 1990) & (
                relative_poverty['Year'] <= 2019)]

# Create plots for each pair of countries
fig, axs = plt.subplots(2, 2, figsize=(14, 15))
fig.suptitle('40% of median - share of population below poverty line')

# Common axis limits
y_limits = [0, 20]
x_limits = [1990, 2019]


poverty_line_plots("India", "Trinidad and Tobago", filtered_poverty, 0, 0, axs, y_limits, x_limits)
poverty_line_plots("Nigeria", "Romania", filtered_poverty, 0, 1, axs, y_limits, x_limits)
poverty_line_plots("Mexico", "Guinea-Bissau", filtered_poverty, 1, 0, axs, y_limits, x_limits)
poverty_line_plots("Philippines", "Saint Lucia", filtered_poverty, 1, 1, axs, y_limits, x_limits)

plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.show()