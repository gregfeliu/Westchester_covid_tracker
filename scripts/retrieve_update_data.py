#!/usr/bin/env python
# coding: utf-8


# Imports
import git
import pandas as pd
import seaborn as sns
sns.set_style("dark")
sns.set(font_scale=1.25)
import numpy as np
import warnings
warnings.filterwarnings('ignore')



# Update the data from the source https://github.com/nytimes/covid-19-data 
repo = git.Repo('../covid-19-data')
repo.remotes.origin.pull()

# Engineer the data
us_counties = pd.read_csv("../covid-19-data/us-counties.csv", infer_datetime_format=True)
westchester_data = us_counties[us_counties['county'] == 'Westchester']
westchester_data.drop(columns = 'fips', inplace=True)
westchester_data.reset_index(inplace=True)

## Scaling Cases Data
### pop of westchester is 967506
westchester_pop = 967506
scale_to_100k = westchester_pop / 100000
westchester_data['total_cases_per_100k'] = westchester_data['cases'] / scale_to_100k


## New cases per capita over past week
new_cases = [westchester_data['total_cases_per_100k'][idx+1] - 
                              westchester_data['total_cases_per_100k'][idx] for idx in range(len(westchester_data)-1)]
new_cases.append(np.nan)
westchester_data['new_cases_per_cap'] = new_cases
westchester_data['new_cases_per_cap_past_7_days'] = westchester_data['new_cases_per_cap'].rolling(window=7, min_periods=0).sum()

## Saving Data
westchester_cases = westchester_data.to_csv("../westchester_coronavirus.csv")


# Plotting the data 
## adding new date columns
westchester_data['dates_datetime'] = pd.to_datetime(westchester_data['date'], infer_datetime_format=True)
latest_date = westchester_data.iloc[-1]['date']
print(f"The latest date in this dataset is: {latest_date}")

## functions to help plot data
def make_lineplot(x_col, y_col, x_col_name, y_col_name, title):
    ax = sns.lineplot(data=westchester_data, x=x_col, y=y_col)
    ax.tick_params(axis='x', labelrotation = 315, size = 12)
    ax.set_xlabel(x_col_name)
    ax.set_ylabel(y_col_name)
    ax.set_title(title)
    return ax

def make_save_lineplot(x_col, y_col, x_col_name, y_col_name, title, new_title):
    ax = make_lineplot(x_col, y_col, x_col_name, y_col_name, title)
    fig = ax.get_figure()
    fig.savefig("../images/" + new_title, bbox_inches ='tight')


## Plot and save new cases over past 7 days per 100k people plot
make_save_lineplot("dates_datetime", "new_cases_per_cap_past_7_days",
                   'Date', 
                    'New Cases Per Cap Past 7 Days',
                    "Number of New Cases in Westchester,NY Over Past 7 Days (Per 100,000 People)", 
                   'Plot_of_New_Cases_Per_Past_7_Days.png')
