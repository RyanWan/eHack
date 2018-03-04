from flask import Flask, jsonify,render_template,url_for
from amazon_comments_scraper import scrapper
from sentiment import getSentiment
import os.path
import os
from shutil import copyfile

from subprocess import call


app = Flask(__name__)


@app.route("/")
def main():
    return render_template("index.html",name=None)



@app.route('/product/<id>', methods=['GET'])
def product(id):

    fileName = id + ".txt"
    srcComment = "comments/" + fileName
    # if this already been search, load the cache
    if os.path.exists(srcComment)  == True:
        print("loading cache")
    else:
        f = open('id.txt','w')
        f.write(id)
        f.close()

        scrapper('id.txt')
        print('********** scrapping finished *************')

    # move the review to the autophrase directory
    desComment = "../AutoPhrase/data/"
    copyfile(srcComment, desComment+'review.txt')
    #subprocess.call(['../AutoPhrase/auto_phrase.sh'])
    call("./auto_phrase.sh",cwd="../AutoPhrase",shell=True)







    response = {}







    return jsonify(response)


@app.route('/sentiment', methods=['GET'])
def sentiment():
    senti = getSentiment()
    return senti




if __name__ == '__main__':
    app.run(debug=True, host='localhost')
    url_for('static', filename='d3.layout.cloud.js')
    # url_for('static', filename='json/stl_waterareas.geojson"')
    # url_for('static', filename='json/map.geojson"')
    # url_for('static', filename='crimedata/input.csv"')






