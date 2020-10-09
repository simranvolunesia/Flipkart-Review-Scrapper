from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/review",methods=["POST"])
def review():
    try:
        query = str(request.form["query"])
        d = {"q": query}
        r = requests.get("https://www.flipkart.com/search", params=d).text
        obj = BeautifulSoup(r, "lxml")
        i = obj.find("div", class_="_1UoZlX")
        link = i.a["href"]
        link = "https://www.flipkart.com" + link
        r = requests.get(link).text
        obj = BeautifulSoup(r, "lxml")
        try:
            prod_name = obj.find("span", class_="_35KyD6").text
        except:
            prod_name = None
        try:
            overall_rating = obj.find("div", class_="hGSR34").text
        except:
            overall_rating = None
        try:
            price = obj.find("div", class_="_1vC4OE _3qQ9m1").text
        except:
            price = None
        reviews = []
        for i in obj.find_all("div", class_="col _390CkK"):
            try:
                rating = str(i.find_all("div", class_="hGSR34 E_uFuv")[0]).split("<img")[0].split(">")[1]
            except:
                rating = None
            try:
                review_heading = i.p.text
            except:
                review_heading = None
            try:
                overall_review = str(i.find_all("div", class_="")[0]).split("</div>")[0].split('class="">')[1].replace("<br/>"," ")
            except:
                overall_review = None
            mydict = {"rating":rating, "review_heading":review_heading, "overall_review":overall_review}
            reviews.append(mydict)

        return render_template("result.html",prod_name = prod_name, overall_rating = overall_rating, price = price, reviews = reviews)
    except:
        return render_template("exception.html")

if __name__=="__main__":
    app.run(debug=True)