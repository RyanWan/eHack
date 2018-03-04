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
    copyfile("../AutoPhrase/models/AutoPhrase.txt","phrases/"+fileName)


    response = {}
    frequencies = []

    phrase_file = 'phrases/'+fileName
    with open(phrase_file) as fp:  
        lines = fp.readlines()
        for line in lines:
            lineContent = line.split()
            if len(lineContent) >= 2:
                score = float(lineContent[0])
                separator = " "
                phrase = separator.join(lineContent[1:])

                if score >= 0.75:
                    frequencies.append({"text": phrase,"size": int(score * 100)})
                elif score >= 0.5:
                    frequencies.append({"text": phrase,"size": int(score * 50)})
                elif score >= 0.1:
                    frequencies.append({"text": phrase,"size": int(score * 10)})

    response['frequency'] =  frequencies

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






