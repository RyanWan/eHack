from flask import Flask, jsonify,render_template,url_for



app = Flask(__name__)


@app.route("/")
def main():
    return render_template("index.html",name=None)



@app.route('/product/<id>', methods=['GET'])
def click(id):
    ret = eng.predict(int(id))


    response = {}
    particles = []
    types = [0] * 8

    piSum = 0.0


    for p in ret:
        tmp = {}
        tmp['x'] = p[0]
        tmp['y'] = p[1]
        tmpType = int(p[2])
        types[tmpType-1] += 1
        tmp['type'] = tmpType;
        tmp['pi'] = float(p[3])
        piSum += float(p[3])
        particles.append(tmp)

    response['typeCount'] = types
    response['maxPercent'] = max(types) * 1.0 / sum(types)
    response['pi'] = piSum/sum(types)
    response['maxType'] = types.index(max(types)) + 1
    response['particles'] = particles


    return jsonify(response)

@app.route('/clear', methods=['GET'])
def clear():
    eng.clearParticle(nargout=0)
    return jsonify({"success":True})


if __name__ == '__main__':
    app.run(debug=True, host='localhost')
    url_for('static', filename='d3.layout.cloud.js')
    # url_for('static', filename='json/stl_waterareas.geojson"')
    # url_for('static', filename='json/map.geojson"')
    # url_for('static', filename='crimedata/input.csv"')






