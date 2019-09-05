from flask import Flask, render_template, redirect 
from flask_pymongo import PyMongo
import scrape_mars
import os

# Create an instance of Flask app
app = Flask(__name__)

#Use flask_pymongo to set up connection through mLab
app.config["MONGO_URI"] = os.environ.get('authentication')
mongo = PyMongo(app)

# Use flask_pymongo to set up mongo connection locally 
app.config["MONGO_URI"] = "mongodb://127.0.0.1:27017/mars_app"
mongo = PyMongo(app)

# Create route
@app.route("/")
def home(): 

    # Find data
    mars_dict = mongo.db.mars_dict.find_one()

    # Return template and data
    return render_template("index.html", mars_dict=mars_dict)

# Route for scrape function
@app.route("/scrape")
def scrape(): 

    # Run scrapped functions
    mars_dict = mongo.db.mars_dict
    mars_data = scrape_mars.scrape_mars_news()
    mars_data = scrape_mars.scrape_mars_featured_image()
    mars_data = scrape_mars.scrape_mars_weather()
    mars_data = scrape_mars.scrape_mars_facts()
    mars_data = scrape_mars.scrape_mars_hemispheres()
    mars_dict.update({}, mars_data, upsert=True)

    return redirect("/", code=302)

if __name__ == "__main__": 
    app.run(debug= True) # Use "debug = False" in real life
