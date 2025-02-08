# Documentation Data Science Project SS2024 Group E

---

# About the Project

This project performs an economic analysis using various data sources such as world economic indicators, Gini coefficients, GDP per capita (PPP), poverty data, and Foreign Direct Investment (FDI) data. The analysis includes calculating remittances, FDI, and GDP growth rates, and visualizing the data through various plots.

## Table of Contents

1. [Requirements](#requirements)
2. [Data Sources](#data-sources)
3. [Project Structure](#project-structure)
4. [Functions Overview](#functions-overview)
5. [Running the Project](#running-the-project)
6. [Detailed Steps](#detailed-steps)

## Requirements

- Python 3.7 or higher
- pandas
- matplotlib
- xml.etree.ElementTree

## Data Sources

The project uses the following data sources, which should be placed in the `Dataframes` directory:

1. `world_economic_indicators.csv`: Contains world economic indicators including personal remittances and GDP data.
2. `Gini_Coefficient_code.csv`: Contains Gini coefficient data.
3. `GDP_percapita_PPP.csv`: Contains GDP per capita (PPP) data.
4. `poverty-explorer.csv`: Contains poverty data.
5. `FDI.xml`: Contains FDI data in XML format.

## Project Structure

```
.
├── Dataframes
│   ├── world_economic_indicators.csv
│   ├── Gini_Coefficient_code.csv
│   ├── GDP_percapita_PPP.csv
│   ├── poverty-explorer.csv
│   └── FDI.xml
├── functions.py
├── xml_parser.py
├── main.py
└── README.md
```

## Functions Overview

### functions.py

- `top_5(df, column_name)`: Returns the top 5 and bottom 5 rows based on the specified column.
- `clean(df, column_name)`: Cleans the specified column in the DataFrame.
- `filter(df)`: Filters the DataFrame.
- `get_frame(top_5_df, full_df)`: Gets the relevant frame from the full DataFrame based on the top 5 DataFrame.
- `comparable_country(base_country, gdp_df, rem_df, fdi_df, threshold)`: Finds a comparable country based on GDP, remittances, and FDI data.
- `get_row(df, country_code)`: Gets the row for the specified country code.
- `growth_rate_plots(df, country1, country2)`: Generates growth rate plots for the specified countries.
- `gdp_pc_ppp_plot(df, country1, country2)`: Generates GDP per capita (PPP) plots for the specified countries.
- `poverty_line_plots(country1, country2, df, row, col, axs, y_limits, x_limits)`: Generates poverty line plots for the specified countries.

### xml_parser.py

- `parse_xml(xml_file)`: Parses the XML file and returns a list of dictionaries containing the data.

## Running the Project

1. Place the required data files in the `Dataframes` directory.

2. Ensure you have the necessary Python packages installed. You can install them using pip:
   
   ```sh
   pip install pandas matplotlibunktion zur Extraktion der Daten aus XML
   ```

3. Run the `main.py` script:
   
   ```sh
   python main.py
   ```

## Detailed Steps

1. **Load Data**: The script starts by loading data from CSV files and an XML file.
2. **Filter Relevant Data**: It then filters the data to focus on the years 1990 to 2019.
3. **Calculate and Plot Remittances**: The script calculates the sum of remittances as a percentage of GDP for each year and plots this data.
4. **Calculate Mean Remittances**: It calculates the mean remittances received by each country from 1990 to 2019 and identifies the top 5 and bottom 5 countries.
5. **Calculate Total Remittances**: The script calculates total remittances by converting percentages to absolute values based on GDP.
6. **FDI Analysis**: It loads and processes FDI data, calculating the mean FDI for each country and identifying the top 5 and bottom 5 countries.
7. **Comparable Country Analysis**: The script identifies countries comparable to India, Mexico, Philippines, and Nigeria based on GDP, remittances, and FDI data.
8. **GDP Growth Analysis**: It analyzes GDP growth rates for the identified countries and generates growth rate plots.
9. **GDP PPP Analysis**: The script processes GDP per capita (PPP) data and generates plots comparing selected countries.
10. **Poverty Line Analysis**: It analyzes poverty data and generates plots showing the share of the population below the poverty line for selected countries.

## Output

- The project generates various plots visualizing the economic data and saves the combined GDP growth rates to a CSV file (`combined_gdp_growth_rates.csv`).

---

This README file provides a comprehensive overview of the project, including setup instructions, data sources, and a detailed description of the analysis steps.

## Data Sources

This project utilized several datasets, each of which provided essential information for the analysis. The data sources, along with their descriptions and any preprocessing steps taken, are listed below:

1. **World Economic Indicators**
   
   - **Source**: [World Economic Indicators 1960-2022 Dataset on Kaggle](https://www.kaggle.com/datasets/mittvin/world-economic-indicators-1960-2022-dataset)
   - **Description**: This dataset contains various economic indicators, including personal remittances received as a percentage of GDP for countries worldwide.
   - **Preprocessing Steps**:
     - The dataset was loaded and filtered to include only the first four columns.
     - Data was limited to the interval from 1990 to 2019.
     - Aggregate remittances received (% of GDP) were calculated for each year.
     - Further filtering was done for the years 1995 and 2015 for specific analyses.

2. **Gini Coefficient Data**
   
   - **Source**: [Gini Coefficient of Countries on Kaggle](https://www.kaggle.com/datasets/therockk/gini-coefficient-of-countries)
   - **Description**: This dataset provides the Gini coefficient, which measures income inequality, for various countries.
   - **Preprocessing Steps**:
     - The dataset was merged with the World Economic Indicators dataset for the years 1995 and 2015 based on the country code.

3. **GDP per Capita (PPP)**
   
   - **Source**: [GDP per Capita All Countries on Kaggle](https://www.kaggle.com/datasets/nitishabharathi/gdp-per-capita-all-countries)
   - **Description**: This dataset contains the GDP per capita in Purchasing Power Parity (PPP) terms for countries worldwide.
   - **Preprocessing Steps**:
     - Relevant columns for the years 1995 and 2015 were extracted.
     - The data was merged with the World Economic Indicators dataset for the respective years based on the country code.

4. **Foreign Direct Investment (FDI) Data**
   
   - **Source**: [Foreign Direct Investment, Net Inflows (BoP, Current US$) on World Bank](https://data.worldbank.org/indicator/BX.KLT.DINV.CD.WD)
   - **Description**: This dataset contains information on net inflows of Foreign Direct Investment (FDI) as recorded in the balance of payments, in current US dollars.
   - **Preprocessing Steps**:
     - The XML data was parsed using a custom `parse_xml` function.
     - Data was filtered to include only the years from 1990 to 2019.
     - The mean FDI for each country was calculated over this period.

5. **Poverty Data Explorer**
   
   - **Source**: [Poverty Data Explorer - Our World in Data](https://ourworldindata.org/explorers/poverty-explorer) 
   - **Description**: This dataset provides key poverty indicators from World Bank data.
   - 
   
   **<u>Additional Preprocessing Steps:</u>**
   
   - **Filtering Out Aggregate Codes**:
     
     - A list of aggregate country codes (e.g., 'ABW', 'AFE', 'AFW', etc.) was used to exclude non-country entries from the analysis. This was applied consistently across different datasets.
   
   - **Handling Missing Values**:
     
     - Missing values in numeric columns were converted to zeros where appropriate.
     - NaN values in specific columns were dropped to ensure accurate calculations.
   
   - **Data Integration**:
     
     - Datasets were merged based on the country code to create unified datasets for analysis.
     - Columns were renamed and restructured for clarity and consistency.