from flask import make_response, render_template, request, send_from_directory
import os
import json
from shop import app, auth, ADMIN, PASSWORD, APPHOST, APPPORT, DEBUG
from shop.service import *


@app.route("/", methods=["POST", "GET"])
def main():
    if request.method == 'POST':
        data = json.loads(request.data.decode('utf-8').replace('\0', ''))

        if data["action"] == "sendProducts":
            products = get_products(data["category"])
            return make_response(json.dumps({"action": "setProducts", "products": products}), 200,
                                 {"content_type": "application/json"})
        elif data["action"] == "sendBrands":
            brands = get_brands()
            return make_response(json.dumps({"action": "setBrands", "brands": brands}), 200,
                                 {"content_type": "application/json"})
        elif data["action"] == "sendPath":
            path = get_category_path(data["category"])
            return make_response(json.dumps({"action": "setPath", "path": path}), 200,
                                 {"content_type": "application/json"})
        elif data["action"] == "sendCategoryInfo":
            info = get_category_info(data["category"])
            return make_response(json.dumps({"action": "setCategoryInfo", "info": info}), 200,
                                 {"content_type": "application/json"})
        elif data["action"] == "sendFilterValues":
            values = get_filter_values(data["category"])
            return make_response(json.dumps({"action": "setFilterValues", "values": values}), 200,
                                 {"content_type": "application/json"})
        elif data["action"] == "sendFilteredProducts":
            products = get_filtered_products(data)
            return make_response(json.dumps({"action": "setFilteredProducts", "products": products}), 200,
                                 {"content_type": "application/json"})
        elif data["action"] == "sendLowPricedProducts":
            products = get_low_priced_products(data)
            return make_response(json.dumps({"action": "setLowPricedProducts", "products": products}), 200,
                                 {"content_type": "application/json"})
        elif data["action"] == "sendHighPricedProducts":
            products = get_high_priced_products(data)
            return make_response(json.dumps({"action": "setHighPricedProducts", "products": products}), 200,
                                 {"content_type": "application/json"})
        elif data["action"] == "sendProductInfo":
            products = get_product_info(data["id"])
            return make_response(json.dumps({"action": "setHighPricedProducts", "products": products}), 200,
                                 {"content_type": "application/json"})
        elif data["action"] == "sendProductsByBrand":
            products = get_products_by_brand(data["id"])
            br_name = get_brand(data["id"])["name"]
            return make_response(json.dumps({"action": "setHighPricedProducts", "products": products, "name": br_name}),
                                 200, {"content_type": "application/json"})
        return make_response("ok")
    else:
        shop_info = get_shop_info()
        categories = get_categories()
        return render_template('MainPage.html', categories=json.dumps(categories), shop_info=json.dumps(shop_info))


@app.route('/owner', methods=["POST", "GET"])
@auth.login_required
def owner():
    if request.method == 'POST':
        data = json.loads(request.data.decode('utf-8').replace('\0', ''))
        if data["action"] == "addCategory":
            add_category(data)
            categories = get_categories()
            node_categories = get_node_categories()
            leaf_categories = get_leaf_categories()
            return make_response(json.dumps({"action": "setCategories", "node_categories": node_categories,
                                             "leaf_categories": leaf_categories, "categories": categories}), 200,
                                 {"content_type": "application/json"})
        elif data["action"] == "addProduct":
            add_product(data)
            products = get_all_products()
            return make_response(json.dumps({"action": "setProducts", "products": products}), 200,
                                 {"content_type": "application/json"})
        elif data["action"] == "addBrand":
            add_brand(data)
            brands = get_brands()
            return make_response(json.dumps({"action": "setBrands", "brands": brands}), 200,
                                 {"content_type": "application/json"})
        elif data["action"] == "updateCategory":
            update_category(data)
            categories = get_categories()
            node_categories = get_node_categories()
            leaf_categories = get_leaf_categories()
            return make_response(json.dumps({"action": "setCategories", "node_categories": node_categories,
                                             "leaf_categories": leaf_categories, "categories": categories}), 200,
                                 {"content_type": "application/json"})
        elif data["action"] == "updateProduct":
            update_product(data)
            products = get_all_products()
            return make_response(json.dumps({"action": "setProducts", "products": products}), 200,
                                 {"content_type": "application/json"})
        elif data["action"] == "updateBrand":
            update_brand(data)
            brands = get_brands()
            return make_response(json.dumps({"action": "setBrands", "brands": brands}), 200,
                                 {"content_type": "application/json"})
        elif data["action"] == "updateShop":
            update_shop_info(data)
            shop_info = get_shop_info()
            return make_response(json.dumps({"action": "setShopInfo", "shop_info": shop_info}), 200,
                                 {"content_type": "application/json"})
        elif data["action"] == "removeCategory":
            remove_category(data["id"])
            categories = get_categories()
            node_categories = get_node_categories()
            leaf_categories = get_leaf_categories()
            return make_response(json.dumps({"action": "setCategories", "node_categories": node_categories,
                                             "leaf_categories": leaf_categories, "categories": categories}), 200,
                                 {"content_type": "application/json"})
        elif data["action"] == "removeProduct":
            remove_product(data["id"])
            products = get_all_products()
            return make_response(json.dumps({"action": "setProducts", "products": products}), 200,
                                 {"content_type": "application/json"})
        elif data["action"] == "removeBrand":
            remove_brand(data["id"])
            brands = get_brands()
            return make_response(json.dumps({"action": "setBrands", "brands": brands}), 200,
                                 {"content_type": "application/json"})

        return make_response("ok")
    else:
        shop_info = get_shop_info()
        categories = get_categories()
        node_categories = get_node_categories()
        leaf_categories = get_leaf_categories()
        products = get_all_products()
        brands = get_brands()
        return render_template('OwnerPage.html',
                               categories=json.dumps(categories),
                               node_categories=json.dumps(node_categories),
                               leaf_categories=json.dumps(leaf_categories),
                               products=json.dumps(products),
                               brands=json.dumps(brands),
                               shop_info=json.dumps(shop_info))


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static/images'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@auth.get_password
def get_pw(username):
    if username == ADMIN:
        return PASSWORD
    return None


@app.route('/logout')
def logout():
    shop_info = get_shop_info()
    categories = get_categories()
    return render_template('MainPage.html', categories=json.dumps(categories), shop_info=json.dumps(shop_info)), 401


if __name__ == '__main__':
    app.run(debug=bool(DEBUG), port=int(APPPORT), host=APPHOST)
