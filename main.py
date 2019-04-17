from flask import make_response, render_template, request
import os, json
from shop import app, auth, ADMIN, PASSWORD, APPHOST, APPPORT, DEBUG
from shop.service import *

LOGIN = "admin"
PSW = "admin"


@app.route("/", methods=["POST", "GET"])
def main():
    if request.method == 'POST':
        data = json.loads(request.data.decode('utf-8').replace('\0', ''))

        if data["action"] == "sendProducts":
            products = get_products(data["category"])
            return make_response(json.dumps({"action": "setProducts", "products": products}), 200, {"content_type": "application/json"})
        elif data["action"] == "sendBrands":
            pass
        elif data["action"] == "sendPath":
            path = get_category_path(data["category"])
            return make_response(json.dumps({"action": "setPath", "path": path}), 200, {"content_type": "application/json"})
        elif data["action"] == "sendFilterValues":
            values = get_filter_values(data["category"])
            return make_response(json.dumps({"action": "setFilterValues", "values": values}), 200, {"content_type": "application/json"})
        elif data["action"] == "sendFilteredProducts":
            products = get_filtered_products(data)
            return make_response(json.dumps({"action": "setFilteredProducts", "products": products}), 200, {"content_type": "application/json"})
        elif data["action"] == "sendLowPricedProducts":
            products = get_low_priced_products(data)
            return make_response(json.dumps({"action": "setLowPricedProducts", "products": products}), 200, {"content_type": "application/json"})
        elif data["action"] == "sendHighPricedProducts":
            products = get_high_priced_products(data)
            return make_response(json.dumps({"action": "setHighPricedProducts", "products": products}), 200, {"content_type": "application/json"})
        elif data["action"] == "authorize":
            if data["login"] == LOGIN and data["password"] == PSW:
                categories = json.dumps(
                    {"Category1": {"Category11": {}, "Category12": {}}, "Category2": {}, "Category3": {}})
                render_template('MainPage.html', categories=categories)
        return make_response("ok")
    else:
        shop_info = get_shop_info()
        categories = get_categories()
        return render_template('MainPage.html', categories=json.dumps(categories), shop_info=json.dumps(shop_info))


@auth.get_password
def get_pw(username):
    if username == ADMIN:
        return PASSWORD
    return None


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000)) # For Heroku, in another way can be used APPPORT
    app.run(debug=bool(DEBUG), port=port, host=APPHOST)
