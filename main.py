from flask import Flask, request, jsonify
from google.cloud import language_v1

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return 'route : OK'

@app.route('/senti', methods=['GET', 'POST'])
def senti():
    if request.method == 'POST':
        sentence = request.json["sentence"]
        res_senti, res_magni = analyze_sentiment(sentence)
        result_dict = {'original_sentence':sentence, 'senti_score':res_senti, 'magnitude':res_magni}

        return jsonify(result_dict)

def analyze_sentiment(text_content):
    client = language_v1.LanguageServiceClient()
    type_ = language_v1.Document.Type.PLAIN_TEXT
    language = "ja"
    document = {"content": text_content, "type_": type_, "language": language}
    encoding_type = language_v1.EncodingType.UTF8
    response = client.analyze_sentiment(request = {'document': document, 'encoding_type': encoding_type})
    res_senti = round(response.document_sentiment.score, 4)
    res_magnitude = round(response.document_sentiment.magnitude, 4)
    return res_senti, res_magnitude

if __name__ == "__main__":
    app.run()