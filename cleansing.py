# =============================================================================
# Import necessary libraries
# =============================================================================
import pandas as pd 
import re 
import string
from sklearn.feature_extraction import text 
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import linear_kernel
from sklearn.feature_extraction.text import CountVectorizer
from collections import Counter 

try:
   
    # Import all the files
    listingsDF = pd.read_csv(r'C:\Users\Candy\OneDrive - Nanyang Technological University\Year 1 Semester 2\CZ1015\Mini Project\Git\listings.csv')
    
    calendarDF = pd.read_csv(r'C:\Users\Candy\OneDrive - Nanyang Technological University\Year 1 Semester 2\CZ1015\Mini Project\Git\calendar.csv')
    
    reviewsDF = pd.read_csv(r'C:\Users\Candy\OneDrive - Nanyang Technological University\Year 1 Semester 2\CZ1015\Mini Project\Git\reviews.csv')

    # =============================================================================
    # Clean the data, doing pre-processing for usage
    # =============================================================================
    #Clean listings

    listingsDF['location']= listingsDF[['latitude', 'longitude']].astype(str) .apply(lambda x: ','.join(x), axis=1) # combine latitute and longitude into one table
    
    listingsDF['location'] = ('(' + listingsDF['location']+')').astype(str) # add '(' to the front and ')' to the back
    
    listingsDF['location']= listingsDF['location'].map(lambda x: eval(x)) # convert string to tuple
    
    #Instead of dropping we select what we need
    listingsDF = listingsDF[['id', 'name','description', 
                             'host_id', 'host_name', 'property_type', 'price', 
                             'number_of_reviews', 'review_scores_rating','location']]
    
    #We drop all rows with empty cells - don't do that, it will affect the calendar
#    listingsDF = listingsDF.dropna(axis=0, how='any')
    
    #Remove the '$' from price
    listingsDF.price = listingsDF.price.str.replace('[$]', '')
    
    #Remove the ',' from price
    listingsDF.price = listingsDF.price.str.replace(',', '')
    
    #Convert price from object to float
    listingsDF['price'] = listingsDF['price'].astype(float)
    
    
    # =============================================================================
    # Extract the necessary columns to be used, into a dataframe
    # =============================================================================
    aDF = listingsDF[['id','name', 'description','location']]
    aDF['full_description'] = aDF['description']
    
    # =============================================================================
    # Clean the description column
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
    # Remove Stop words
    # =============================================================================
    
    #Manually adding words
    stop_words = text.ENGLISH_STOP_WORDS.union(["will"])
    
    #Use CountVectorizer to count the frequency of words in the descriptions
    vec = CountVectorizer(stop_words=stop_words)
    doc = vec.fit_transform(aDF['description'])
    
    aDF['words'] = aDF['description'].apply(lambda x: len(str(x).split())) #length of each description
    
    # =============================================================================
    # Include availability of each listings, to be displayed alongside the recommended listings
    # =============================================================================
    calendarDF.available = calendarDF.available.str.replace('t', '1')
    calendarDF.available = calendarDF.available.str.replace('f', '0')
    calendarDF.available = calendarDF.available.astype(int)
    
    sortingDF = calendarDF.groupby(['listing_id'], as_index=False).mean()
    sortedDF = pd.DataFrame(sortingDF)
    sortedDF.rename(columns={'listing_id': 'id'}, inplace=True)
    sortedDF.available = sortedDF.available.apply(lambda x: x*100)
    sortedDF.available = sortedDF.available.round(2)
    aDF = pd.merge(aDF, sortedDF, on="id")
    
    # =============================================================================
    # Cosine similarity
    # =============================================================================
    cos_simi = cosine_similarity(doc) #?? Ignores magnitude | s = cos(angle) = d1.d2 / ||d1|| * || d2|| where (d1.d2 = d1x*d2x + d1y*d2y)
    
    aDF['index'] = aDF.index

    # =============================================================================
    # Keep listing_id that are found in both calendarDF and aDF - dont need to uncommment as both produce the same results
    # =============================================================================
    
#    aDF=  aDF.loc[((aDF.id.isin(calendarDF['listing_id']))),:]    
#    calendarDF= calendarDF.loc[((calendarDF.listing_id.isin(aDF['id']))),:]    
    
    
    
except IOError:
    print("File not found or file is opened. Please make sure your that file name is correct and it is placed in the correct directory. Remember to close it.")
except KeyError:
    print("Wrong file format. Please change!")
except Exception:
    print("Other issues. Please check your file")