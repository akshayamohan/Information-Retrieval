# Save a dictionary into a pickle file.

import pickle


details = {
    
            "ip": "3.137.198.3",
            "port": "9999",
            "name": "execute_query"
            }

pickle.dump( details, open( "project2_index_details.pickle", "wb" ) )

favorite_color = pickle.load( open( "project2_index_details.pickle", "rb" ) )
print(favorite_color)