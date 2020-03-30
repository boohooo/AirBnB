from cleansing import *
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
import gmaps # use google maps
from ipywidgets.embed import embed_minimal_html

# =============================================================================
# User input
# =============================================================================
def EDA_description(preference_textinput):
    from cleansing import aDF
    #prefrence_textinput = "i want somewhere quiet and also close to the space needle if not some other tourist spot is ok or shopping malls"
    
    testcorp = [preference_textinput]
    
    tfv = TfidfVectorizer()
    
    desc = tfv.fit_transform((aDF['description'])) #fitting and transforming the vector    desc
    
    qq = tfv.transform(testcorp)
    
    testcos = map(lambda x: cosine_similarity(qq, x),desc)

    wrap = list(testcos)
    
    aDF = aDF.reset_index(drop=True)
    
    recdf = pd.DataFrame(columns=['name', 'description','score','id','location']) 
    
    def rec(index, aDF, scores):
        count=0
        for x in index:
            recdf.at[count,'name']=aDF['name'][x]
            recdf.at[count,'description']=aDF['description'][x]
            recdf.at[count,'score']=scores[count]
            recdf.at[count,'id'] = aDF['id'][x]
            recdf.at[count,'location'] = aDF['location'][x]
            count+=1
        return recdf
    
    # =============================================================================
    # Use nearest neighbours      
    # =============================================================================

    n_neighbors = 6
    
    nei = NearestNeighbors(n_neighbors, p=2)
    
    nei.fit(desc)
    
    nn = nei.kneighbors(qq, return_distance=True) 
    
    index = nn[1][0][1:]
    dist = nn[0][0][1:]
    
    gmap_df =rec(index,aDF,dist)

    # =============================================================================
    # Use Google maps
    # =============================================================================


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
    gmap_df.drop(columns=['description'], inplace=True) # drop description as it is too long
    
    gmap_dict= gmap_df.to_dict('records') # convert each row into a dictionary of the list
    
    gmap_locations =gmap_df['location'].to_list() # to show the markers on the map
    
    gmap_info = [info_box_template.format(**id) for id in gmap_dict] #map the gmap_dict with the info box template
    
    marker_layer = gmaps.marker_layer(gmap_locations, info_box_content=gmap_info) # create the markers to be shown on google map
    
    fig = gmaps.figure()
    fig.add_layer(marker_layer) # combine with the current map
    embed_minimal_html('map.html', views=[fig])
    return gmap_df


test =EDA_description("i want somewhere quiet and also close to the space needle if not some other tourist spot is ok or shopping malls")