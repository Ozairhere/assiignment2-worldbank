import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def read_worldbank_data(filename):
    
    # ----- Read the World Bank dataframe from the file ----- #
    df = pd.read_csv(filename, skiprows=4)
    df = df.drop(columns=['Country Code', 'Indicator Code'])
    
    # ----- Transpose the dataframe to have years as columns ----- #
    df_by_years = df.set_index('Country Name').T

    # ----- Reset the index and clean the transposed dataframes ----- #
    df_year = df_by_years.rename(columns={'index': 'Year'})
    df_years = df_year.transpose()
    
    # ----- Transpose the dataframe to have countries as columns ----- #
    years = df.columns[2:-1]
    data_by_country = df.pivot(index='Country Name', columns='Indicator Name', values=years)
    df_countries = data_by_country.transpose()

    # ----- Created csv files for dataframes ----- #
    # df_years.to_csv('years_dataframe.csv')
    # df_countries.to_csv('countries_dataframe.csv')

    return df_years, df_countries


def analyze_data(df):
    # ----- group by statistics ----- #
    group_by = df.groupby(['Country Name', 'Indicator Name'])['1960'].sum()
    group_by_data = group_by.reset_index()

    # Selected Countires & Indicator Name ----- #
    countries_name = ['China', 'Pakistan', 'United Kingdom']
    indicators_name =   ['Electricity production from hydroelectric sources (% of total)', 
                        'Urban population (% of total population)', 
                        'CO2 emissions from liquid fuel consumption (% of total)']
    
    
    data = group_by_data[group_by_data['Country Name'].isin(countries_name)]
    data = group_by_data[group_by_data['Indicator Name'].isin(indicators_name)]
    # group_by_data.to_csv('group_by_data_filters.csv', index=False)
    
    # ----- summary statistics ----- #
    describe_data = data.describe()
    # # describe_data.to_csv('describe_data.csv')

    
    data_df = data.pivot(index='Country Name', columns='Indicator Name', values='1960')
    correlation_matrix = data_df.corr()
    
    # ----- Calculate correlation matrix for the selected countries and indicators ----- #
    # correlation_matrix.to_csv('indicators_correlation.csv')

    
    # ----- Graph ----- #
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm',
                    xticklabels=correlation_matrix.columns.str.wrap(22),
                    yticklabels=correlation_matrix.columns.str.wrap(22))
    plt.xticks(rotation='horizontal')
    plt.title('Correlation Matrix of Indicators (Year 1960)')
    plt.show()
    
    
    for indicator in indicators_name:
        print(indicator)
        plt.figure()
        for country in countries_name:
            df_country = data[data['Country Name'] == country]
            plt.plot(df_country['Country Name'], df_country['1960'], label=country)
        plt.xlabel('Year')
        plt.ylabel(indicator)
        plt.title(f'{indicator} over Time')
        plt.legend()
        plt.show()

# ----- Main Function ----- #
def main():
    # ----- World_bank_filename ----- #
    file_name = 'world_bank_data.csv'
    
    # ----- Call read_worldbank_data function to get dataframes ----- #
    df_years, df_countries = read_worldbank_data(filename=file_name)
    
    # ----- Call analyze_data function and pass the dataframes as arguments ----- #
    analyze_data(df=df_years)
    
# ----- Call main function to run the program ----- #
if __name__ == '__main__':
    main()