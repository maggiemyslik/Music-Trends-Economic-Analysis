def split_artists(artist_name):
    '''
    splits a string of artists into a list if there are multiple artists on one song
    '''
    artist_name = artist_name.lower()
    
    signs = ["featuring", " vs", " ft", "feat.", "feat", " and", "&", "/"]
    for item in signs:
        artist_name = artist_name.replace(item, ",")
    artist_list = [artist.strip() for artist in artist_name.split(",") if artist.strip()]
    
    return artist_list

def categorize_genre(genre):
    '''
    assignes a broad genre to each subgenre of music 
    '''
    genre = str(genre)
    genre = genre.lower()

    categories = {
        'Latin Inspired': ['soca', 'reggae', 'latin', 'moombahton'],
       
        'Jazz and Soul': ['jazz', 'soul', 'blues'],
    
        'Indie': ['indie', 'alt', 'madchester', 'neo', 'lilith', 'escape room'],
        
        'Country and Folk': ['country', 'folk', 'comic', 'stomp', 'oktoberfest'],
        
        'Rap and Hip Hop': ['rap', 'hip hop', 'hip-hop', 'drill', 'urban', 'afro', 'g funk'],
        
        'R&B': ['rnb', 'r&b', 'gold', 'relaxative'],
        
        'Rock': ['rock', 'wave', 'metal', 'grunge', 'emo', 'new romantic', 'beatlesque'],

        'EDM, House, and Dance': [
            'edm', 'elec', 'house', 'dance', 'ukg', 'grime', 'techno', 'dnb', 'bounce', 'rave',
            'garage', 'big beat', 'bass', 'tron', '2-step', 'big room', 'trance', 'hardcore',
            'complextro', 'charva', 'funky', 'brostep'],

        'Pop': ['pop', 'boy band', 'girl group', 'singer-songwriter', 'talent show', 'schlager'],

        
        'Movies, TV, and Theater': [
            'classic', 'broadway', 'tune', 'children', 'glee', 'filmi', 'hollywood', 'cartoon', 
            'backing', 'advocacy'],
        
        'No Genre Found': ['nan', 'fake', 'karaoke'],
    }

    for category, keywords in categories.items():
        if any(keyword in genre for keyword in keywords):
            return category

    return 'Other' 


def clean_year(date):
    '''
    gets the year as an integer from the date string
    '''
    date = str(date)
    year = date.split('-')[0]
    return year
