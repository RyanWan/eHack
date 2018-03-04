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
    srcPhrase  = "phrases/" + fileName
    # if this already been search, load the cache
    if os.path.exists(srcPhrase) == True:
        print("loading cache of phrase")
    else:
        if os.path.exists(srcComment)  == True:
            print("loading cache of text")
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

        count = 0

        for line in lines:
            if count > 100:
                break
            lineContent = line.split()
            if len(lineContent) >= 2:
                score = float(lineContent[0])
                separator = " "
                phrase = separator.join(lineContent[1:])

                if score == 1:
                    continue

                if count <= 8:
                    frequencies.append({"text": phrase,"size": int(score * 80)})
                elif count <=  40:
                    frequencies.append({"text": phrase,"size": int(score * 50)})
                elif count <=  70:
                    frequencies.append({"text": phrase,"size": int(score * 40)})
                elif count <= 100 and score > 0.3:
                    frequencies.append({"text": phrase,"size": max(20, int(score * 20))})
            count += 1


    senti = getSentiment(id)

    response['frequency'] =  frequencies
    response['sentiment'] = senti


    return jsonify(response)




if __name__ == '__main__':
    app.run(debug=True, host='localhost')
    url_for('static', filename='d3.layout.cloud.js')
    # url_for('static', filename='json/stl_waterareas.geojson"')
    # url_for('static', filename='json/map.geojson"')
    # url_for('static', filename='crimedata/input.csv"')
