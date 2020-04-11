from cleansing import *
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import linear_kernel
import gmaps # use google maps
from ipywidgets.embed import embed_minimal_html #export google maps into html
import calmap # plot the calendar
import matplotlib.pyplot as plt, mpld3 #export calendar into img

def filterCalendar(user_startDate, user_endDate):
    filtercalDF =calendarDF[(calendarDF['date'] <= user_endDate) & (calendarDF['date'] >= user_startDate)]
    return filtercalDF

def topListings(preference_textinput, algorithm_type,calendarDF):
    from cleansing import aDF
    aDF=  aDF.loc[((aDF.id.isin(calendarDF['listing_id']))),:]
    user_inputDF = pd.DataFrame(columns=['description'])
    user_inputDF['description'] = [preference_textinput]
    
     # Collate the name, score, and other columns into on edataframe
    def rec(index, aDF, scores):
        count=0
        recdf = pd.DataFrame(columns=['name', 'description','score','id','location'])
        for x in index:
            recdf.at[count,'name']=aDF['name'][x]
            recdf.at[count,'description']=aDF['description'][x]
            recdf.at[count,'score']=scores[count]
            recdf.at[count,'id'] = aDF['id'][x]
            recdf.at[count,'location'] = aDF['location'][x]
            count+=1
        return recdf
    
    tfv = TfidfVectorizer()
    desc = tfv.fit_transform((aDF['description'])) #fitting and transforming the vector 
    user = tfv.transform(user_inputDF['description'])
    aDF = aDF.reset_index(drop=True)
    
    if (algorithm_type == "Cosine-Similarity"):
        cosScores = map(lambda x: cosine_similarity(user, x),desc)
        wrap = list(cosScores)        
        index = sorted(range(len(wrap)), key=lambda i: wrap[i], reverse=True)[:5] #Sort the index for top n recommendations

        coslist=[]
        for x in index:
            coslist.append(wrap[x][0][0]) #Create a list of similarity scores
        
        results =rec(index,aDF,coslist)
        return results
                
    else: # k nearest neighbour
        n_neighbors = 5
        
        nei = NearestNeighbors(n_neighbors, p=2)
        nei.fit(desc)
        nn = nei.kneighbors(user, return_distance=True) 
        
        index = nn[1][0][0:] #//Change to start from index 0 to include the point itself
        dist = nn[0][0][0:]
        
        results =rec(index,aDF,dist)
        return results
    
def googleMaps(dataset):
    gmaps.configure(api_key='AIzaSyBqISZOJygJfOxnrnfRs8XlSTxZmmk94do') #please don't spread the api_key because it is my credentials, only use for this project purpose, thanks.
    
    # create the info box template
    info_box_template = """
    <dl>
    <dt>Name</dt><dd>{name}</dd>
    <dt>id</dt><dd>{id}</dd>
    <dt>score</dt><dd>{score}</dd>
    <dt>location</dt><dd>{location}</dd>
    </dl>
    """
    dataset.drop(columns=['description'], inplace=True) # drop description as it is too long
    
    gmap_dict= dataset.to_dict('records') # convert each row into a dictionary of the list
    
    gmap_locations =dataset['location'].to_list() # to show the markers on the map
    
    gmap_info = [info_box_template.format(**id) for id in gmap_dict] #map the gmap_dict with the info box template
    
    marker_layer = gmaps.marker_layer(gmap_locations, info_box_content=gmap_info) # create the markers to be shown on google map
    
    fig = gmaps.figure()
    fig.add_layer(marker_layer) # combine with the current map
    embed_minimal_html('map.html', views=[fig])

def calendarImg(dataset):
    for i, id_input in enumerate(dataset.id):
        df = calendarDF[calendarDF.listing_id.isin([id_input])]
        df['available_num'] =[3 if x ==1 else -1 for x in df['available']] # instead of t and f, it will be 3 and -1
        df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d').dt.strftime('%Y-%m-%d %H:%M:%S') # convert date format with h:m:s
        events=pd.Series(df['available_num']) # convert the dataset into series
        events.index= pd.DatetimeIndex(df['date']) # set date as the index 
        calmap.calendarplot(events, monthticks=1, daylabels='MTWTFSS',cmap='YlGn', fillcolor='grey', linewidth=1, fig_kws=dict(figsize=(16, 4)))
        name = "img"+str(i)+".png"
        plt.savefig(name)
        
