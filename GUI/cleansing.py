import pandas as pd 
import re 
import string
from sklearn.feature_extraction import text 
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import linear_kernel
    

try:
   
    # Import all the files
    listingsDF = pd.read_csv(r'C:\Users\Candy\OneDrive - Nanyang Technological University\Year 1 Semester 2\CZ1015\Mini Project\Git\listings.csv')
    
    calendarDF = pd.read_csv(r'C:\Users\Candy\OneDrive - Nanyang Technological University\Year 1 Semester 2\CZ1015\Mini Project\Git\calendar.csv')
    
    reviewsDF = pd.read_csv(r'C:\Users\Candy\OneDrive - Nanyang Technological University\Year 1 Semester 2\CZ1015\Mini Project\Git\reviews.csv')

    # =============================================================================
    # Clean listings
    # =============================================================================
    #Clean listings

    listingsDF['location']= listingsDF[['latitude', 'longitude']].astype(str) .apply(lambda x: ','.join(x), axis=1) # combine latitute and longitude into one table
    
    listingsDF['location'] = ('(' + listingsDF['location']+')').astype(str) # add '(' to the front and ')' to the back
    
    listingsDF['location']= listingsDF['location'].map(lambda x: eval(x)) # convert string to tuple
    
    #Instead of dropping we select what we need
    listingsDF = listingsDF[['id', 'name','description', 
                             'host_id', 'host_name', 'property_type', 'price', 
                             'number_of_reviews', 'review_scores_rating','location']]
    
    #We drop all rows with empty cells
    listingsDF = listingsDF.dropna(axis=0, how='any')
    
    #Remove the '$' from price
    listingsDF.price = listingsDF.price.str.replace('[$]', '')
    
    #Remove the ',' from price
    listingsDF.price = listingsDF.price.str.replace(',', '')
    
    #Convert price from object to float
    listingsDF['price'] = listingsDF['price'].astype(float)
    
    
    # =============================================================================
    # EDA + Description aDF cleansing    
    # =============================================================================
    aDF = listingsDF[['id','name', 'description','location']]
    
    
    # =============================================================================
    # Functions to clean text
    # =============================================================================
    
    pd.set_option('display.max_colwidth', -1)
    
    def clean(text):
        text = text.lower()
        text = re.sub('[^\w\s]', '', text) #This removes all the punctuations
        text = re.sub(r'\n',' ', text) #This relaces the \n with space
        text = re.sub(r'\r','', text) #\r
        text = re.sub('[^0-9a-z #+_]', '', text) #Special chars
        
        return text
    
    aDF['description'] = aDF['description'].apply(clean)
    
    # =============================================================================
    # Stop words
    # =============================================================================
    
    #Manually adding words
    stop_words = text.ENGLISH_STOP_WORDS.union(["will"])
    
    
    from sklearn.feature_extraction.text import CountVectorizer
    from collections import Counter
    
    #Must vectorize before fitting...
    vec = CountVectorizer(stop_words=stop_words)
    doc = vec.fit_transform(aDF['description'])
    
    aDF['words'] = aDF['description'].apply(lambda x: len(str(x).split())) #length of each description
    
    # =============================================================================
    # Cosine similarity
    # =============================================================================
    cos_simi = cosine_similarity(doc) #?? Ignores magnitude | s = cos(angle) = d1.d2 / ||d1|| * || d2|| where (d1.d2 = d1x*d2x + d1y*d2y)
    
    aDF['index'] = aDF.index

    
    
    
except IOError:
    print("File not found or file is opened. Please make sure your that file name is correct and it is placed in the correct directory. Remember to close it.")
except KeyError:
    print("Wrong file format. Please change!")
except Exception:
    print("Other issues. Please check your file")