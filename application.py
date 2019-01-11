from flask import Flask,render_template, request, flash
import sys
import json
import urllib.request
import logging
import re
import nltk
import operator
from nltk.corpus import stopwords


#init flask app

application = Flask(__name__)
KEYSTRING = "cfbti040rmqm52z9bpxs5qar" 
URL_BASE = "https://openapi.etsy.com/v2/"
#shop = pd.DataFrame(columns =['shop_id','listings','term_counts'])

"""Create a list of common words to remove"""
stop_words=["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", 
            "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", 
            "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", 
            "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", 
            "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", 
            "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", 
            "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", 
            "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", 
            "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than",
            "too", "very", "s", "t", "can", "will", "just", "don", "should", "now","the","a","mm","x"]

def get_data_from_api(url):

    # Input: a url
    # Output: the .json objects found at that url
    
    try:
        with urllib.request.urlopen(url) as url:
            objects = json.loads(url.read().decode())
    except:
        e = sys.exc_info()[0]
        logging.error("We had an error (" + str(e) + ") with url " + url + ".")
        objects = None
    return objects

def get_listings(shop_id):

    # Input: a shop_id
    # Output: A list of listings from that shop, from the Etsy API
    
    url = (
        URL_BASE 
        + "shops/" 
        + str(shop_id)
        + "/listings/active?"
        + "&api_key=" + KEYSTRING
    )
    object = get_data_from_api(url)
    if object and object['results']:
        return object['results']
    else:
        return [] 

def get_listing_terms(listings):

    # Input: a list of Etsy Listing objects
    # Output: a list of terms found in various fields in these listings
    
    terms = []
    for listing in listings:

        if listing['title']:
            terms += listing['title'].split()
        if listing['description']:
            terms += listing['description'].split()    
            
    return terms

nltk.download('stopwords')  


def clean_terms(terms):

    # Input: a list of terms
    # Output: a list of these terms with non-alphabetic characters and stopwords removed, 
    #         converted to lowercase, and tokenized
    
    cleaned = []
    stops = set(stopwords.words("english"))
    for term in terms:
        stems = re.sub('[^a-zA-Z]+', ' ', term).lower().strip().split()
        text = [w for w in stems if not w in stops]
    
        for stem in text:
            cleaned.append(stem)
    return cleaned

def get_term_counts(terms):

    # Input: a list of terms
    # Output: a hash from term to term count
    
    term_counts = {}
    if not terms:
        return term_counts
    for term in terms:
        if term not in term_counts:
            term_counts[term] = 0
        term_counts[term] += 1
    return term_counts 

def get_listing_terms(listings):

    # Input: a list of Etsy Listing objects
    # Output: a list of terms found in various fields in these listings
    
    terms = []
    for listing in listings:

        if listing['title']:
            terms += listing['title'].split()
        if listing['description']:
            terms += listing['description'].split()    
            
    return terms



def get_term_counts(terms):

    # Input: a list of terms
    # Output: a hash from term to term count
    
    term_counts = {}
    if not terms:
        return term_counts
    for term in terms:
        if term not in term_counts:
            term_counts[term] = 0
        term_counts[term] += 1
    return term_counts               

@application.route('/')
def index():
	#initModel()
	#render out pre-built HTML file right on the index page
		return render_template("index.html")

@application.route('/',methods=['POST'])
def predict():
	if request.method == 'POST':
		data = []
		data.append(request.form['comment'])
		


	logging.info("Getting listings.")
	#shop_id = ["6004422"]
	total_listings = []
	new_shop = []
	for id in data:
		new_shop = get_listings(id)
	#df = pd.DataFrame(columns = ['listings','term_counts'])
	#df['listings'] = new_shop			

	terms = []
	all_terms = []
	terms += get_listing_terms(new_shop)
	# Store the term-count hash in the shop object
	term_counts = get_term_counts(clean_terms(terms))
	all_terms += term_counts.keys()

	out = [i[0] for i in sorted(term_counts.items(), key=operator.itemgetter(1), reverse=True)[:5]]
	return render_template('index.html',prediction = out,comment = data)

    
	


if __name__ == '__main__':
	application.run(debug=True)    


