# =============================================================================
# Import necessary libraries
# =============================================================================
from cleansing import *
import pandas as pd

#TF-IDF
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import linear_kernel

#Doc2Vec
import nltk
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from gensim.models import Word2Vec
from nltk.tokenize import word_tokenize
from gensim.parsing.preprocessing import STOPWORDS
from gensim.parsing.preprocessing import remove_stopwords
from gensim.models.callbacks import CallbackAny2Vec

#Visuals
import gmaps # use google maps
from ipywidgets.embed import embed_minimal_html #export google maps into html
import calmap # plot the calendar
import matplotlib.pyplot as plt, mpld3 #export calendar into img

def filterCalendar(user_startDate, user_endDate):
    filtercalDF =calendarDF[(calendarDF['date'] <= user_endDate) & (calendarDF['date'] >= user_startDate)] 
    removeCalDF =pd.DataFrame((filtercalDF[filtercalDF['available']==0]).listing_id.unique()) #get those listingsID that are booked during the date range
    removeCalDF = removeCalDF.rename(columns={0:'listing_id'})
    keepCalDF = filtercalDF[~filtercalDF.listing_id.isin(removeCalDF.listing_id)].dropna() #remove those listingsID that are booked during the date range
    return keepCalDF

def topListings(preference_textinput, algorithm_type,calDF,user_beds):
    from cleansing import aDF #if never import this, aDF cannot work..
    
    # keep those available IDs based on calendar
    aDF=  aDF.loc[((aDF.id.isin(calDF['listing_id']))),:] 
    
    #  remove those listings that have insufficient beds
    aDF = aDF[ aDF.beds >= user_beds ]
    
    user_inputDF = pd.DataFrame(columns=['description'])
    user_inputDF['description'] = [preference_textinput]
    
    if(("TF-IDF" in algorithm_type) ==True):
        
        def rec(index, aDF, scores):
            count=0
            recdf = pd.DataFrame(columns=['name', 'description','score','id','location','listing_url','available'])
            for x in index:
                recdf.at[count,'name']=aDF['name'][x]
                recdf.at[count,'description']=aDF['description'][x]
                recdf.at[count,'score']=scores[count]
                recdf.at[count,'id'] = aDF['id'][x]
                recdf.at[count,'location'] = aDF['location'][x]
                recdf.at[count,'listing_url'] = aDF['listing_url'][x]
                recdf.at[count,'available'] = aDF['available'][x]
                recdf.at[count,'reviews'] = aDF['reviews'][x]
                count+=1
            return recdf
        
        tfv = TfidfVectorizer()
        desc = tfv.fit_transform((aDF['description'])) #fitting and transforming the vector 
        user = tfv.transform(user_inputDF['description'])
        aDF = aDF.reset_index(drop=True)
        
        if (algorithm_type == "Cosine-Similarity (TF-IDF)"):
            cosScores = map(lambda x: cosine_similarity(user, x),desc)
            wrap = list(cosScores)        
            index = sorted(range(len(wrap)), key=lambda i: wrap[i], reverse=True)[:5] #Sort the index for top n recommendations
    
            coslist=[]
            for x in index:
                coslist.append(wrap[x][0][0]) #Create a list of similarity scores
            
            results =rec(index,aDF,coslist)
            return results
                    
        else: #K-Nearest Neighbour (TF-IDF)
            n_neighbors = 5
            
            nei = NearestNeighbors(n_neighbors, p=2)
            nei.fit(desc)
            nn = nei.kneighbors(user, return_distance=True) 
            
            index = nn[1][0][0:] #//Change to start from index 0 to include the point itself
            dist = nn[0][0][0:]
            
            results =rec(index,aDF,dist)
            return results
    else: # Cosine-Similarity (Doc2Vec)
        
        desclist = list(aDF['description']) #Convert the description into a list
        
        for x in range(len(desclist)):
            desclist[x] = remove_stopwords(desclist[x]) #Remove stop words in description
    
        u_input = ' '.join(preference_textinput)
        user_input_label = 'user_input'
        
        #Clean
        cleaned_input = clean(u_input)
        #Remove stop words
        cleaned_removed_input = ' '.join([word for word in u_input.split() if word not in STOPWORDS])
        #Tokenize
        inputtoken = word_tokenize(cleaned_removed_input)
        
        desclist.append(cleaned_removed_input)
        
        #Create a copy of dataframe, Update the dataframe with the user input
        bDF = aDF
        bDF = bDF.append({'id':0, 'name':user_input_label, 'description':cleaned_removed_input, 'full_description':u_input}, ignore_index=True)

        #Convert the listing id into string first, then into a list
        bDF['id'] = bDF['id'].astype(str)
        id_label = list(bDF['id'])
        id_label.append('0')
        
        #Tag each document
        train_corpus = [TaggedDocument(words=word_tokenize(_d.lower()), tags=[id_label[i]]) for i, _d in enumerate(desclist)]
        
        #Model training
        epoch_logger = EpochLogger()
        
        model = Doc2Vec(vector_size=80, min_count=2, epochs=20, dm=1, hs=1, window=2, compute_loss=True, callbacks=[epoch_logger])

        #Build the vocab then train the model
        model.build_vocab(train_corpus)

        model.train(train_corpus, total_examples=model.corpus_count, epochs=model.epochs)
        
        model.save("d2v.model")
        print("Model Saved") #For visualization later
        
        model.docvecs['953595'] #This is where our vectors are stored in | Search by the unique tag
        
        #User input vector will be used to calculate similarity
        vector = model.infer_vector(inputtoken)
        
        #Put the similarity in a list
        for doc_id in range(len(train_corpus)):
            inferred_vector = vector
            print(doc_id)
            sims = model.docvecs.most_similar([inferred_vector], topn=len(model.docvecs))
        
        simsL = [list(e) for e in sims] #Convert to List of List
        
        #Put in dataframe
        descDF = bDF[['name', 'description','id','location','listing_url','available','reviews']]
        simsDF = pd.DataFrame(simsL, columns=['id','scores'])
        results = pd.merge(descDF, simsDF, on='id')
        results = results.sort_values(by=['scores'], ascending=False)
        results = results.head(6) # get the top 5 IDs
        results= results.iloc[1:] # remove first row
        results = results.rename(columns={"scores": "score"})
        return results
    
def googleMaps(dataset):
    gmaps.configure(api_key='AIzaSyBqISZOJygJfOxnrnfRs8XlSTxZmmk94do') #please don't spread the api_key because it is my credentials, only use for this project purpose, thanks.
    
    # create the info box template
    info_box_template = """
    <dl>
    <dt>Name</dt><dd>{name}</dd>
    <dt>ID</dt><dd>{id}</dd>
    <dt>Score</dt><dd>{score}</dd>
    <dt>Location</dt><dd>{location}</dd>
    <dt>Availability (%)</dt><dd>{available}</dd>
    <dt>URL</dt><dd>{listing_url}</dd>
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

# Display start and end of epoch
class EpochLogger(CallbackAny2Vec):
     '''Callback to log information about training'''

     def __init__(self):
         self.epoch = 0

     def on_epoch_begin(self, model):
         print("Epoch #{} start".format(self.epoch))

     def on_epoch_end(self, model):
         print("Epoch #{} end".format(self.epoch))
         self.epoch += 1
