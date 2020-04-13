# =============================================================================
# Import necessary libraries
# =============================================================================
import pandas as pd 
import re 
import string
from textblob import TextBlob

try:
    # =============================================================================
    # Import the excel files
    # =============================================================================
    listingsDF = pd.read_csv(r'C:\Users\Candy\OneDrive - Nanyang Technological University\Year 1 Semester 2\CZ1015\Mini Project\Git\listings.csv')
    
    calendarDF = pd.read_csv(r'C:\Users\Candy\OneDrive - Nanyang Technological University\Year 1 Semester 2\CZ1015\Mini Project\Git\calendar.csv')
    
    reviewsDF = pd.read_csv(r'C:\Users\Candy\OneDrive - Nanyang Technological University\Year 1 Semester 2\CZ1015\Mini Project\Git\reviews.csv')

    # =============================================================================
    # Clean the data, doing pre-processing for usage
    # =============================================================================
    listingsDF['location']= listingsDF[['latitude', 'longitude']].astype(str) .apply(lambda x: ','.join(x), axis=1) # combine latitute and longitude into one table
    
    listingsDF['location'] = ('(' + listingsDF['location']+')').astype(str) # add '(' to the front and ')' to the back
    
    listingsDF['location']= listingsDF['location'].map(lambda x: eval(x)) # convert string to tuple 
    
    # =============================================================================
    # Extract the necessary columns to be used, into a dataframe
    # =============================================================================
    aDF = listingsDF[['id','name', 'description','location','listing_url','beds']]
    aDF['full_description'] = aDF['description']
    
    # =============================================================================
    # Clean any text column
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
    # Get the polarity of the listingID 
    # =============================================================================
    revDF = reviewsDF[['listing_id', 'comments']] 
    revDF['comments'] = revDF['comments'].astype(str) #change to str so that can clean !!!
    revDF['comments'] = revDF['comments'].apply(clean)

    p = lambda x: TextBlob(x).sentiment.polarity
    revDF['polarity'] = revDF['comments'].apply(p) 

    revDF = revDF[['listing_id', 'polarity']]
    revDF = revDF.groupby('listing_id').mean() #group by id and get the mean of polarity and subjectivity
    revDF['id'] = revDF.index #id column became index so need to set it back as column
    
    # Get the reviews' sentiment
    for index, row in revDF.iterrows():
        if(revDF['polarity'][index]>0.5):
            revDF.at[index, 'reviews'] = 'Mostly positive'
        elif(revDF['polarity'][index]>0):
            revDF.at[index, 'reviews'] = 'Positive'
        elif(revDF['polarity'][index]<-0.5):
            revDF.at[index, 'reviews'] = 'Mostly Negative'
        elif(revDF['polarity'][index]<-0):
            revDF.at[index, 'reviews'] = 'Negative'
        else:
            revDF.at[index, 'reviews'] = 'Neutral'
    
    aDF = pd.merge(aDF, revDF, on="id")
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
