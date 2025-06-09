from lets_plot import *
import pandas as pd 

genre_colors = {
        'Jazz': '#fee08b',
        'Pop': '#3288bd', 
        'EDM': '#fdae61',
        'Rap': '#d53e4f', 
        'Movies': '#ffffbf',
        'R&B': '#e6f598',
        'Indie': '#abdda4',
        'Rock': '#66c2a5',
        'Country': '#f46d43',
        'Latin': '#5e4fa2'}

genre_short_names = {
        'Jazz and Soul': 'Jazz',
        'Pop': 'Pop',
        'EDM, House, and Dance': 'EDM',
        'Rap and Hip Hop': 'Rap',
        'Movies, TV, and Theater': 'Movies',
        'R&B': 'R&B',
        'Indie': 'Indie',
        'Rock': 'Rock',
        'Country and Folk': 'Country',
        'Latin Inspired': 'Latin'
    }

def plot_unemployment(full_df):
        unemployment_df = full_df[['year', 'unemployment']].drop_duplicates().sort_values(by='year')
        plot = (ggplot(unemployment_df, aes(x='year', y='unemployment')) +
                geom_line(size=1.5, color='blue') +
                geom_point(size=3, color='blue') +
                geom_line(size=1.5, color='#3288bd') +
                geom_point(size=3, color='#3288bd') +
                xlab('Year') +
                ylab('Unemployment Rate (%)') +
                labs(title='UK Unemployment Rates 2000-2023') +
                theme_minimal())
        return plot

def categorize_economic_period(unemployment):
        if unemployment > 8:
            return 'Recession'
        elif unemployment > 5:
            return 'Moderate Unemployment'
        else:
            return 'Economic Stability'
        
def plot_single_genre_proportion(full_df, economic_period):
    """
    Takes a DataFrame with 'genre' and 'unemployment' columns and a specified economic period,
    calculates genre proportions for that period, and creates a single bar chart.
    """
    full_df = full_df.dropna(subset=['genre', 'unemployment'])
    full_df['economic_period'] = full_df['unemployment'].apply(categorize_economic_period)
    filtered_df = full_df[full_df['economic_period'] == economic_period]
    filtered_df = filtered_df[filtered_df['genre'] != "No Genre Found"]
    filtered_df['genre'] = filtered_df['genre'].map(genre_short_names)
    filtered_df['year'] = filtered_df['year'].astype(int)
    yearly_counts = filtered_df.groupby(['year', 'genre']).size().reset_index(name='count')
    total_per_year = yearly_counts.groupby('year')['count'].sum().reset_index(name='total_count')
    yearly_counts = yearly_counts.merge(total_per_year, on='year')
    yearly_counts['proportion'] = yearly_counts['count'] / yearly_counts['total_count']

    average_proportions = (
        yearly_counts.groupby('genre')['proportion']
        .mean()
        .reset_index(name='average_proportion')
        .sort_values(by='average_proportion', ascending=False)
    )

    average_proportions['genre'] = pd.Categorical(
        average_proportions['genre'],
        categories=average_proportions['genre'],
        ordered=True
    )
    
    if economic_period == 'Recession':
        unemployment_range = 'Unemployment Rate over 8%'
    elif economic_period == 'Moderate Unemployment':
        unemployment_range = 'Unemployment Rate between 5 and 7%'
    elif economic_period == 'Economic Stability':
        unemployment_range = 'Unemployment Rate below 5%'

    p = (
        ggplot(average_proportions, aes(x='genre', y='average_proportion', fill='genre')) +
        geom_bar(stat='identity') +
        ylab('Proportion') +
        theme(
            axis_text_x=element_text(angle=45, hjust=1),
            axis_title_x=element_blank()
        ) +
        scale_y_continuous(limits=[0, 0.5]) +
        ggtitle(f'Genre Appearence in UK top 40 Charts During years with \n {unemployment_range}') +
        scale_fill_manual(values=genre_colors))

    return p
        
def plot_genre_trends(data, plottype):
    ''' 
    cleans the data to calculate the proportions of each genre represented on the charts.
    can represent this as a barchart,  heatmap, or areachart
    '''
    data = data[data['genre'].notna() & (data['genre'] != 'No Genre Found')]
    genre_year_data = data.groupby(['year', 'genre']).size().reset_index(name='song_count')
    genre_year_data['proportion'] = genre_year_data.groupby('year')['song_count'].transform(lambda x: x / x.sum())
    genre_order = ['Pop', 'EDM, House, and Dance', 'Rap and Hip Hop', 'Rock']
    other_genres = genre_year_data[~genre_year_data['genre'].isin(genre_order)]['genre'].unique()
    genre_order += list(other_genres)
    genre_year_data['genre'] = pd.Categorical(genre_year_data['genre'], categories=genre_order, ordered=True)
    genre_year_data = genre_year_data.sort_values(by=['year', 'genre'])

    if plottype == 'barchart':
        plot = (ggplot(genre_year_data, aes(x='year', y='proportion', fill='genre')) +
                geom_bar(stat='identity', position='stack') +
                xlab('Year') +
                ylab('Proportion of Chart') +
                scale_fill_manual(values=genre_colors) +
                scale_fill_discrete(name='Genre', breaks=genre_order) +
                ggtitle('Figure 3: Pop is Consistently Popular, Rap and EDM Rise and Fall', 'Proportion of the UK top 40 Charts per Genre from 2000-2023'))
    elif plottype == 'heatmap':
         plot = (ggplot(genre_year_data, aes(x='year', y='genre', fill='proportion')) +
                geom_tile() +
                xlab('Year') +
                ylab('Genre') +
                scale_fill_gradient(low='white', high='blue', name='Proportion of Chart') +
                theme(axis_text_x=element_text(angle=45, hjust=1)) +
                scale_fill_manual(values=genre_colors) +
                ggsize(800, 1300))
    elif plottype == 'areachart':
        plot = (
            ggplot(genre_year_data, aes(x='year', y='proportion', fill='genre')) +
            geom_area() +
            xlab('Year') +
            ylab('Proportion of Chart') +
            scale_fill_discrete() +
            scale_fill_manual(values=genre_colors))
    return plot


def plot_genre_with_unemployment(data, genre):
    genre_data = data[data['genre'] == genre]
    year_totals = data.groupby('year').size().rename("year_total").reset_index()
    genre_counts = genre_data.groupby('year').size().rename("genre_count").reset_index()
    proportions = pd.merge(genre_counts, year_totals, on='year', how='left')
    proportions['proportion'] = proportions['genre_count'] / proportions['year_total']
    unemployment_data = data[['year', 'unemployment']].drop_duplicates()
    combined_data = pd.merge(proportions, unemployment_data, on='year', how='left')
    combined_data.rename(columns={"unemployment": "unemployment_rate"}, inplace=True)
    max_proportion = combined_data['proportion'].max()
    combined_data['scaled_unemployment'] = combined_data['unemployment_rate'] / combined_data['unemployment_rate'].max() * max_proportion
        
    plot = ggplot(combined_data, aes(x='year')) + \
            geom_bar(aes(y='proportion'), stat='identity', fill='blue', alpha=0.7) + \
            geom_line(aes(y='scaled_unemployment'), color='red', size=1.5) + \
            geom_point(aes(y='scaled_unemployment'), color='red', size=2.5) + \
            xlab('Year') + \
            ylab('Proportion (Genre and Scaled Unemployment)') + \
            scale_y_continuous(format=".0%") 
    return plot

def plot_genre_proportion(data, genre):
    genre_data = data
    plot = ggplot(genre_data, aes(x='trending_year', y='proportion')) + \
        geom_bar(stat='identity', fill='blue') + \
        ggtitle(f'Proportion of the Chart for {genre} (2000-2023)') + \
        xlab('Year') + \
        ylab('Proportion') + \
        scale_y_continuous(format=".0%") 
    
    return plot

def plot_minor_genres(full_df):
    excluded_genres = ['Pop', 'EDM, House, and Dance', 'Rap and Hip Hop', 'No Genre Found']
    filtered_data = full_df[~full_df['genre'].isin(excluded_genres) & full_df['genre'].notna()]
    minor_genre_data = filtered_data.groupby(['year', 'genre']).size().reset_index(name='minor_genre_count')
    total_genre_data = full_df.groupby('year').size().reset_index(name='total_count')
    genre_year_data = pd.merge(minor_genre_data, total_genre_data, on='year')
    genre_year_data['proportion'] = genre_year_data['minor_genre_count'] / genre_year_data['total_count']
    other_genres = genre_year_data['genre'].unique()
    genre_year_data['genre'] = pd.Categorical(genre_year_data['genre'], categories=other_genres, ordered=True)
    genre_year_data = genre_year_data.sort_values(by=['year', 'genre'])

    plot = (ggplot(genre_year_data, aes(x='year', y='proportion', fill='genre')) +
            geom_bar(stat='identity', position='stack') +
            xlab('Year') +
            ylab('Proportion of Chart (Relative to All Genres)') +
            scale_fill_manual(values=genre_colors) +
            labs(title='Minor Genres Have Declined in Popularity Since 2000',
                subtitle = 'Proportion of the UK top 40 Chart held by Genres other than \n Pop, EDM, and Rap',
                fill='Genre') +
            theme_minimal())
    return plot

def get_top_artist_table(data):
    artist_year_counts = data.groupby(['year', 'artist_name']).size().reset_index(name='appearances')    
    top_artists = (
        artist_year_counts
        .sort_values(['year', 'appearances'], ascending=[True, False])
        .groupby('year', as_index=False)
        .head(1)
    )
    formatted_df = top_artists.to_markdown(index=False)
    return formatted_df

    
def get_top_genre_table(data):
    filtered_df = data[
        data['genre'].notna() & 
        (data['genre'].str.strip() != '') & 
        (data['genre'] != 'No Genre Found')
    ].copy()
    genre_year_counts = filtered_df.groupby(['year', 'genre']).size().reset_index(name='appearances')
    top_genres = (
        genre_year_counts
        .sort_values(['year', 'appearances'], ascending=[True, False])
        .groupby('year', as_index=False)
        .head(1)
    )    
    formatted_df = top_genres.to_markdown(index=False)
    return formatted_df


def get_mean_genre_appearance_table(data):
    filtered_df = data[
        data['genre'].notna() & 
        (data['genre'].str.strip() != '') & 
        (data['genre'] != 'No Genre Found')
    ].copy()
    genre_year_counts = filtered_df.groupby(['year', 'genre']).size().reset_index(name='count')    
    mean_genre_appearances = genre_year_counts.groupby('genre')['count'].mean().reset_index()    
    mean_genre_appearances['count'] = mean_genre_appearances['count'].round(2)    
    mean_genre_appearances.rename(columns={'count': 'mean_appearances'}, inplace=True)    
    sorted_df = mean_genre_appearances.sort_values('mean_appearances', ascending=False)    
    formatted = sorted_df.to_markdown(index=False)
    return formatted



