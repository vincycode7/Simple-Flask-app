from flask import Flask, jsonify, request, render_template
import copy
#initialize Flask app
app = Flask(__name__)

#Item class
class Item:
    def __init__(self):
        self.items = {}

    def create_item(self, name, price):
        self.items[name] = {'name' : name, 'price':price}

    def update_item_price(self, item, new_price):
        self.items[item]['price'] = new_price
    def show_item(self):
        return self.items
    
#store class
class Stores:
    def __init__(self):
        self.store = {}

    def create_astore(self,store_name):
        self.store[store_name]  = {'name' : store_name, 'items': Item() }

    def add_item_tostore(self, store, item, price):
        self.store[store]['items'].create_item(item, price)
    
    def _stores(self):
        return copy.deepcopy(self.store)

    def get_stores(self,name):
        if name != None:
            print('abeg na')
            store = self._stores()[name]
            print(f'sssttt --> {store}')
            store['items'] = store['items'].show_item()
            return store
        else:
            print('enteredd here')
            stores = self._stores()
            print(f'stores --> {stores}')
            for key in  stores.keys():
                stores[key]['items']  = stores[key]['items'].show_item()
                print(f'later ---> {stores}')
            return stores

    def get_item_instore(self, store, item):
        return self.get_stores(name=store)['items'] if item == None else self.get_stores(name=store)['items'][item]


#Initialize store
stores = Stores()

@app.route('/', methods=['GET'])
def homepage():
    return render_template('index.html')

#Tell app which request to understand
@app.route('/store', methods=['POST']) #e.g https://www.facedget.com/ (homepage)
def create_store():
    request_data = request.get_json()
    print(f'checking request --> {request_data} {type(request_data)}')
    
    try:
        stores.create_astore(request_data.get('name'))
        reply = stores.get_stores(name=request_data.get('name'))
        print(f'pretty print --> {reply}')
        return jsonify(reply)
    except Exception as e:
        return jsonify({"message":e})

@app.route('/store/<string:name>', methods=['GET'])
def get_specific_store(name):
    try:
        return jsonify(stores.get_stores(name=name))
    except Exception as e:
        return jsonify({"message" : e})

@app.route('/store', methods=['GET'])
def get_all_store():
    return jsonify(stores.get_stores(name=None))

@app.route('/store/<string:name>/item', methods=['POST'])
def put_item_in_store(name):
    request_data = request.get_json()
    print(f'down --> {request_data}')
    try:
        stores.add_item_tostore(name, item=request_data['item'], price=request_data['price'])
        return jsonify(stores.get_item_instore(store=name, item=request_data['item']))
    except Exception as e:
        return jsonify({"message" : e})

@app.route('/store/<string:name>/item', methods=['GET'])
def get_allitem_in_store(name):
    print(f'pretty print --> {name}')
    return stores.get_item_instore(store=name, item=None)

@app.route('/store/<string:name>/item/<string:item>', methods=['GET'])
def get_item_in_store(name):
    print(f'pretty print --> {name}')
    return stores.get_item_instore(store=name, item=item)

app.run(port=5000)