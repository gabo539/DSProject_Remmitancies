import matplotlib.pyplot as plt
import pandas as pd
def top_5(frame, column_name):
    # Drop rows with NaN values in the "Mean Personal remittances, received (% of GDP)" column
    frame = frame.dropna()
    # Sort the DataFrame in descending order by selected column
    sorted_frame= frame.sort_values(by = column_name, ascending= False)
    # Get Top 5 countries
    top_5_countries = sorted_frame.head(5)
    # Get Bottom 5 Countries
    bottom_5_countries = sorted_frame.tail(5)
    return top_5_countries, bottom_5_countries

# Function to get a specific country
def get_row(frame, country_code):
    country_name_data = frame[frame['Country Code'] == country_code]
    return country_name_data

def filter(frame):
    # List of aggregate country codes to exclude
    aggregate_codes = [
        'ABW', 'AFE', 'AFW', 'ARB', 'CEB', 'CHI', 'CSS', 'EMU', 'EUU',
        'FCS', 'HIC', 'IBD', 'IBT', 'IDX', 'INX', 'LAC', 'LCN', 'LDC',
        'LIC', 'LMY', 'LTE', 'MEA', 'MIC', 'MNA', 'NAC', 'OED', 'OSS',
        'PRE', 'PSS', 'SAS', 'SSA', 'SSF', 'SST', 'TLA', 'TMN', 'TSA',
        'TSS', 'UMC', 'WLD', 'PST', 'ECS', 'EAS', 'EAP', 'TEA', 'EAR',
        'TEC', 'LMC', 'ECA', 'IDA', "IDB", "HPC"
    ]

    # Filter the DataFrame to exclude aggregate country codes
    filter_frame = frame[~frame['Country Code'].isin(aggregate_codes)]
    return filter_frame

def clean(frame, column_name):
    # Convert NaN values to 0
    frame[column_name]= frame[column_name].fillna(0)
    # Convert column to integer format
    frame[column_name] = frame[column_name].apply(lambda x: int(x))
    return frame

def get_frame(frame, wwrem_total_rem_90to19):
    # Filter the GDP data to include only the countries in top_5_total_rem
    countries_codes = frame['Country Code'].unique()
    gdp_only = wwrem_total_rem_90to19[wwrem_total_rem_90to19['Country Code'].isin(countries_codes)]

    # Calculate the mean GDP for these countries from 1990 to 2019
    top_5_gdp_mean = gdp_only.groupby(['Country Name', 'Country Code'])[
        'GDP (current US$)_x'].mean().reset_index()

    # Rename the columns for clarity
    top_5_gdp_mean.columns = ['Country Name', 'Country Code', 'Mean GDP (current US$)']

    # Convert the GDP values to integers
    top_5_gdp_mean['Mean GDP (current US$)'] = top_5_gdp_mean['Mean GDP (current US$)'].astype(int)

    return top_5_gdp_mean

def comparable_country(ccode, total_gdp_mean_by_country, mean_remittances, mean_fdi, tolerance):
    # relative rem. country and comparable fdi countries from 1990 till 2019
    row = get_row(mean_remittances,ccode)

    frame_merged_1 = pd.merge(total_gdp_mean_by_country,mean_fdi, on='Country Code')
    #new column for calculated relativ mean fdi per country
    frame_merged_1['Relative Mean FDI (%)'] = (frame_merged_1['Mean FDI'] / frame_merged_1['GDP (current US$)_x']) * 100
    # get reference country's rem
    target_value = row['Mean Personal remittances, received (% of GDP)'].iloc[0]
    #subtract reference countries rem to calculated reltive mean fdi for every country and just take the countries below the tolerance
    filtered_df = frame_merged_1[abs(frame_merged_1['Relative Mean FDI (%)'] - target_value) < tolerance]
    frame_merged_2 = pd.merge(filtered_df,mean_remittances, on='Country Code')
    #get reference country's fdi
    df = get_row(frame_merged_1, ccode)
    target_value_2 = df['Relative Mean FDI (%)'].iloc[0]
    #potential countries copy
    frame_dif = frame_merged_2.copy()
    #get differences
    frame_dif['Relative Mean FDI (%)'] = (frame_dif['Relative Mean FDI (%)'] - target_value).abs()
    frame_dif['Mean Personal remittances, received (% of GDP)'] = (frame_dif ['Mean Personal remittances, received (% of GDP)'] - target_value_2).abs()
    frame_dif['Sum of Differences'] = frame_dif['Relative Mean FDI (%)'] + frame_dif['Mean Personal remittances, received (% of GDP)']
    # figure out country with the smallest difference
    min_index = frame_dif['Sum of Differences'].idxmin()

    return frame_dif.loc[min_index, 'Country Code']

# Define the function to calculate GDP growth rate
def calculate_gdp_growth_rate(df, country_code):
    country_df = df[df['Country Code'] == country_code][['Country Name', 'Country Code', 'Year', 'GDP (current US$)_x']]
    country_df = country_df.sort_values(by='Year')
    country_df['GDP Growth Rate (%)'] = country_df['GDP (current US$)_x'].pct_change() * 100
    country_df['GDP Growth Rate (%)'] = country_df['GDP Growth Rate (%)'].round(2)
    return country_df


def growth_rate_plots(df, ccode_rem, ccode_fdi):
    plt.figure(figsize=(10, 6))

    df_rem_gdp = calculate_gdp_growth_rate(df, ccode_rem)
    df_fdi_gdp = calculate_gdp_growth_rate(df, ccode_fdi)

    avg_growth_rate_rem = df_rem_gdp['GDP Growth Rate (%)'].mean()
    avg_growth_rate_fdi = df_fdi_gdp['GDP Growth Rate (%)'].mean()


    # Plot for GDP (Gross Domestic Product)
    plt.plot(df_rem_gdp['Year'], df_rem_gdp['GDP Growth Rate (%)'], label=f'{ccode_rem} GDP Growth Rate', color='red')
    plt.plot(df_fdi_gdp['Year'], df_fdi_gdp['GDP Growth Rate (%)'], label=f'{ccode_fdi} GDP Growth Rate', color='blue')

    # Axes labels and title
    plt.xlabel('Year')
    plt.ylabel('GDP Growth Rate (%)')
    plt.title(f'{ccode_rem} and {ccode_fdi} GDP Growth Rate (1990-2019)')
    plt.legend()

    plt.axhline(y=0, color='black', linestyle='--', linewidth=1.8)

    # Show plot
    plt.grid(True)
    plt.show()

    return df_rem_gdp, df_fdi_gdp, avg_growth_rate_rem, avg_growth_rate_fdi

def gdp_pc_ppp_plot(frame, ccode_rem, ccode_fdi):
    # Filter data for ccode_rem and ccode_fdi
    rem_gdp_pcppp = frame[frame['Country Code'] == ccode_rem]
    fdi_gdp_pcppp = frame[frame['Country Code'] == ccode_fdi]

    # Plotting the data
    plt.figure(figsize=(10, 6))
    plt.plot(rem_gdp_pcppp['Year'], rem_gdp_pcppp['GDP_PPP'], label= ccode_rem, marker='o',  color='red')
    plt.plot(fdi_gdp_pcppp['Year'], fdi_gdp_pcppp['GDP_PPP'], label= ccode_fdi, marker='o',  color='blue')

    # Adding titles and labels
    plt.title("GDP per Capita PPP of "+ ccode_rem + " and " + ccode_fdi + " (1990-2019)")
    plt.xlabel('Year')
    plt.ylabel('GDP per Capita PPP (current international $)')
    plt.legend()
    plt.grid(True)
    plt.show()

def poverty_line_plots(country_rem, country_fdi, frame, x, y, axs, y_limits, x_limits):
    # Plot for India (urban and rural) vs Trinidad and Tobago
    rem_data = frame[frame['Country'] == country_rem]
    fdi_data = frame[frame['Country'] == country_fdi]
    axs[x, y].plot(rem_data['Year'], rem_data['40% of median - share of population below poverty line'],
                   label= country_rem, color='red')
    axs[x, y].scatter(rem_data['Year'], rem_data['40% of median - share of population below poverty line'],
                      color='red')
    axs[x, y].plot(fdi_data['Year'], fdi_data['40% of median - share of population below poverty line'],
                   label= country_fdi, color='blue')
    axs[x, y].scatter(fdi_data['Year'], fdi_data['40% of median - share of population below poverty line'],
                      color='blue')
    axs[x, y].set_title(country_rem + ' vs ' + country_fdi)
    axs[x, y].set_xlabel('Year')
    axs[x, y].set_ylabel('40% of median - share of population below poverty line')
    axs[x, y].set_xlim(x_limits)
    axs[x, y].set_ylim(y_limits)
    axs[x, y].legend()



