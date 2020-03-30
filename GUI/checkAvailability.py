from cleansing import *

def checkAvailability(test_id):

    g = calendarDF.groupby('listing_id') #group by listing_id, now data frame is grouped into different group corresponding to listing_id

    # =============================================================================
    # Put it in series?
    # =============================================================================
    
    #default conditions before checking through dataframes and ids.
    listing_inputExists = False #check if user input of listing id exists in listing id.
    
    for listing_id, listing_id_df in g: #for each listing id in g, each dataframe inside the listing id,
        if (listing_id ==test_id ): #check through all listing id for input
            df = listing_id_df #store the found dataframe into df
    
    ser = pd.Series(df['available']) #store the series (one-dimensional labeled array) of 'available' inside the listing_id_df. 
    data = ser.ne('f') #ne returns True for every element which is Not Equal to the element in passed series.


    # =============================================================================
    # Calculate no. of days
    # =============================================================================

    # (index number) , (number of available slots)
    
    num = 0 #store number of available 
    
    for a in data: #for each element in data
        if (a == True): #if data is true, print data
            num = num +1
            
    # =============================================================================
    # Show percentage        
    # =============================================================================
    pct = (100*num)/365 #calculate percentage of availability

    pct = '{0:.2f}%'.format(pct) #convert into 2dp and put % behind the number
    
    return pct

    # =============================================================================
# put it into a list

test['pct']= test['id'].apply(checkAvailability)
