from flask import Flask, url_for, redirect, request
import os
from searchSystem import VectorSearch
import json

app = Flask(__name__, static_folder='/Users/v.n.polyakov/PycharmProjects/info-search-engine/static')


@app.route("/")
def redirect_to_index_page():
    return redirect(url_for('static', filename='index.html'), 302)


def create_response(matches):
    res = []
    for doc_link, score in matches:
        res.append(
            {
                'name': doc_link,
                'score': score,
                'link': doc_link
            }
        )
    return json.dumps(res)


@app.route("/query", methods=["GET"])
def result_for_query():
    query = request.args.get('query')
    return create_response(VectorSearch().search(query))


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
