from flask import Flask, render_template
import pymongo


import config


app = Flask(__name__)
client = pymongo.MongoClient(config.mongodb_connection)
db = client['account_data']
col = db['account_data']

@app.route("/")
def main():
    # query = { "Timestamp": { "$lt": datetime.datetime.now() } }
    result = col.find().sort("Timestamp", -1).limit(1)
    balance_data = result[0]['Balance Data']
    print(balance_data)

    # for item in result:
    #     print(item)
    # print('hotdog')
    return render_template(
        'index.html',
        title='Stonks!',
        net_liq=balance_data['net-liquidating-value']
        )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5001')
