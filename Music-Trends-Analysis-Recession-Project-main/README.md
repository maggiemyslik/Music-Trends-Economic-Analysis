# UK Music Trends and Economic Conditions Analysis
**AUTHOR:** Maggie Myslik - BSc Politics and Data Science, LSE

*LSE, DS105 Autumn Term 2024, Spotify API Assignment*

![Recession Pop Art](recession-pop-art.jpg)

## PROJECT SUMMARY 
This repository explores trends in the UK Top 40 music charts from 2000 to 2023 and their relationship with economic conditions, such as recessions and periods of stability. The analysis investigates genre dominance, shifts in minor genres, and how external economic factors may influence musical preferences. The key findings reveal the increasing dominance of Pop, EDM, and Rap, alongside notable changes in genre representation during economic downturns.

## SOURCES
- [The Office for National Statistics](https://www.ons.gov.uk/employmentandlabourmarket/peoplenotinwork/unemployment/timeseries/mgsx/lms)
- [Official Charts top 40 Biggest Songs in the UK per Year](https://www.officialcharts.com/chart-news/the-official-top-40-biggest-songs-of-2022__38203/)
- [Wikipedia Page for each Year in British Music Charts](https://en.wikipedia.org/wiki/2010_in_British_music_charts)
- [Recession Pop Article and Cover Image](https://www.berklee.edu/berklee-now/news/recession-pop-playlist)

## CREATING VIRTUAL ENVIRONMENT
1. you can create a new environment with the following command:
`conda create -n .venv`

2. Then, activate the environment:
`conda activate .venv`
You should see a (.venv) in your terminal prompt now.

3. Install the required packages:
`pip install -r requirements.txt`

## ACCESSING THE SPOTIFY API
1. [Visit the Spotify Developer Dashboard](https://developer.spotify.com/documentation/web-api)
2. Create a new application to obtain your Client ID and Client Secret.
3. Add your credentials to an .env file in the project directory:
        SPOTIFY_CLIENT_ID=your_client_id
        SPOTIFY_CLIENT_SECRET=your_client_secret
In Notebook 1, you will use these credentials to get a token to access the API data. 

## RUNNING THE CODE

1. Activate the virtual environment (see instructions above).
2. Run NB01_data_collection.ipynb to collect the raw data.
3. Run NB02_database_creation.ipynb to process the data and generate the topcharts.db SQLite database.
4. Open NB03 - Data Visualisation.ipynb and run the cells to reproduce the analysis and visualizations.

*Notes:*
The custom Python functions used in the notebooks are defined in the visualizations.py, spotify_auth.py, data_cleaning.py, and data_collection.py scripts.
