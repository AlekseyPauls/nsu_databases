from shop import conn


def get_categories():
    cursor = conn.cursor()
    cursor.execute("""select * from category""")
    records = cursor.fetchall()
    res = []
    for r in sorted(records, key=lambda x: len(x[0])):
        res.append({"id": r[0], "name": r[1]})
    return res


def get_node_categories():
    cursor = conn.cursor()
    cursor.execute("""select category.cat_num cat_num, category.cat_name from category where cat_num not in 
                  (select category.cat_num from product, category  where product.cat_num = category.cat_num)""")
    records = cursor.fetchall()
    res = []
    for r in sorted(records, key=lambda x: len(x[0])):
        res.append({"id": r[0], "name": r[1]})
    return res


def get_leaf_categories():
    cursor = conn.cursor()
    cursor.execute("""select cat_num, cat_name from category where cat_num not in (select distinct f.cat_num from 
                        category f, category f1 where f1.cat_num like f.cat_num || '.' || '%');""")
    records = cursor.fetchall()
    res = []
    for r in sorted(records, key=lambda x: len(x[0])):
        res.append({"id": r[0], "name": r[1]})
    return res


def get_category_path(cat_num):
    cursor = conn.cursor()
    res = ""
    while cat_num != "":
        cursor.execute("""select cat_name from category where cat_num = %(cat_num)s""", {"cat_num": cat_num})
        records = cursor.fetchall()
        res = records[0][0] + "/" + res
        cat_num = cat_num[:cat_num.rfind(".")]
    return res[:-1]


def get_category_info(cat_num):
    cursor = conn.cursor()
    cursor.execute("""select avg(price) from product where cat_num = %(cat_num)s""", {"cat_num": cat_num})
    records = cursor.fetchall()
    if records[0][0]:
        res = {"avg_price": round(float(records[0][0]), 2)}
    else:
        res = {"avg_price": 0}
    return res


def add_category(data):
    cursor = conn.cursor()
    cursor.callproc('add_category', [len(data["parent"].split(".")) + 1, data["name"], data["parent"], ])
    conn.commit()


def update_category(data):
    cursor = conn.cursor()
    cursor.execute("""update category set cat_name = %(cat_name)s where cat_num = %(cat_num)s""",
                   {"cat_name": data["name"], "cat_num": data["id"]})
    conn.commit()


def remove_category(id):
    cursor = conn.cursor()
    cursor.execute("""delete from category where cat_num = %(cat_num)s;""", {"cat_num": id})
    cursor.execute("""delete from list_brand_product where prod_id IN 
                        (select prod_id from product where cat_num = %(cat_num)s);""", {"cat_num": id})
    cursor.execute("""delete from product where cat_num = %(cat_num)s;""", {"cat_num": id})
    conn.commit()


def get_all_products():
    cursor = conn.cursor()
    cursor.execute("""select p.prod_id, p.prod_name, p.price, p.installment_plan, p.warranty_period, p.img_url, 
        p.description, p.cat_num, b.br_id from product p, list_brand_product l, brand b where 
        p.prod_id = l.prod_id and l.br_id = b.br_id;""")
    records = cursor.fetchall()
    res = []
    for r in records:
        res.append({"id": r[0], "name": r[1], "price": r[2], "installment_plan": r[3], "warranty_period": r[4],
                    "img_url": r[5], "description": r[6], "cat_num": r[7], "br_id": r[8]})
    return res


def get_products(cat_num):
    cursor = conn.cursor()
    cursor.execute("""select * from product where cat_num = %(cat_num)s order by price desc""", {"cat_num": cat_num})
    records = cursor.fetchall()
    res = []
    for r in records:
        res.append({"id": r[0], "name": r[1], "price": r[2], "installment_plan": r[3],
                    "warranty_period": r[4], "img_url": r[5], "description": r[6], "cat_num": r[7]})
    return res


def get_product_info(id):
    cursor = conn.cursor()
    cursor.execute(
        """select br_name from brand where br_id in (select br_id from list_brand_product where prod_id = %(id)s) """,
        {"id": id})
    records = cursor.fetchall()
    brand_name = records[0][0]
    cursor.execute(
        """select * from product where prod_id = %(id)s""",
        {"id": id})
    records = cursor.fetchall()
    res = {"id": records[0][0], "name": records[0][1], "price": records[0][2], "installment_plan": records[0][3],
           "warranty_period": records[0][4], "img_url": records[0][5], "description": records[0][6],
           "cat_num": records[0][7], "brand": brand_name}
    return res


def get_products_by_brand(br_id):
    cursor = conn.cursor()
    cursor.execute(
        """select * from product where prod_id in (select prod_id from list_brand_product where br_id = %(br_id)s) """,
        {"br_id": br_id})
    records = cursor.fetchall()
    res = []
    for r in records:
        res.append({"id": r[0], "name": r[1], "price": r[2], "installment_plan": r[3],
                    "warranty_period": r[4], "img_url": r[5], "description": r[6], "cat_num": r[7]})
    return res


def get_filtered_products(params):
    cursor = conn.cursor()
    cursor.execute("""select * from product where cat_num = %(category)s and 
        price >= %(minPrice)s and price <= %(maxPrice)s and warranty_period >= %(minWarranty)s and 
        warranty_period <= %(maxWarranty)s and installment_plan = %(installment)s order by price desc""", params)
    records = cursor.fetchall()
    res = []
    for r in records:
        res.append({"id": r[0], "name": r[1], "price": r[2], "installment_plan": r[3],
                    "warranty_period": r[4], "img_url": r[5], "description": r[6], "cat_num": r[7]})
    return res


def get_low_priced_products(params):
    cursor = conn.cursor()
    cursor.execute("""select * from product where cat_num = %(category)s order by price asc limit %(n)s;""", params)
    records = cursor.fetchall()
    res = []
    for r in records:
        res.append({"id": r[0], "name": r[1], "price": r[2], "installment_plan": r[3],
                    "warranty_period": r[4], "img_url": r[5], "description": r[6], "cat_num": r[7]})
    return res


def get_high_priced_products(params):
    cursor = conn.cursor()
    cursor.execute("""select * from product where cat_num = %(category)s order by price desc limit %(n)s;""", params)
    records = cursor.fetchall()
    res = []
    for r in records:
        res.append({"id": r[0], "name": r[1], "price": r[2], "installment_plan": r[3],
                    "warranty_period": r[4], "img_url": r[5], "description": r[6], "cat_num": r[7]})
    return res


def get_filter_values(cat_num):
    cursor = conn.cursor()
    cursor.execute("""select min(price), max(price), min(warranty_period), max(warranty_period) 
        from product where cat_num = %(cat_num)s""", {"cat_num": cat_num})
    records = cursor.fetchall()
    res = {"minPrice": 0, "maxPrice": 0, "minWarranty": 0, "maxWarranty": 0}
    if records:
        res = {"minPrice": records[0][0], "maxPrice": records[0][1], "minWarranty": records[0][2],
               "maxWarranty": records[0][3]}
    return res


def add_product(data):
    cursor = conn.cursor()
    cursor.execute("""select max(prod_id) from product""")
    prod_id = cursor.fetchall()[0][0] + 1
    cursor.execute("""insert into product (prod_id, prod_name, price, installment_plan, warranty_period, cat_num, 
    img_url, description) values (%(id)s, %(name)s, %(price)s, %(plan)s, %(period)s, %(num)s, %(image)s, %(desc)s)""",
                   {"id": prod_id,
                    "name": data["name"],
                    "price": data["price"],
                    "plan": data["installment_plan"],
                    "period": data["warranty_period"],
                    "num": data["category"],
                    "image": data["img_url"],
                    "desc": data["description"],
                    })
    cursor.execute("""insert into list_brand_product (br_id, prod_id) values(%(br_id)s, %(prod_id)s);""",
                   {"br_id": data["brand"], "prod_id": prod_id})
    conn.commit()


def update_product(data):
    cursor = conn.cursor()
    cursor.execute("""update product set prod_name = %(name)s, price = %(price)s, 
    installment_plan = %(plan)s, warranty_period = %(period)s, img_url = %(image)s, description = %(desc)s, 
    cat_num = %(num)s where prod_id = %(id)s""",
                   {"id": data["id"],
                    "name": data["name"],
                    "price": data["price"],
                    "plan": data["installment_plan"],
                    "period": data["warranty_period"],
                    "num": data["category"],
                    "image": data["img_url"],
                    "desc": data["description"]
                    })
    cursor.execute("""delete from list_brand_product where prod_id = %(id)s""",
                   {"id": data["id"]})
    cursor.execute("""insert into list_brand_product(br_id, prod_id) values(%(br_id)s, %(prod_id)s)""",
                   {"br_id": data["brand"], "prod_id": data["id"]})
    conn.commit()


def remove_product(id):
    cursor = conn.cursor()
    cursor.execute("""delete from list_brand_product where prod_id = %(prod_id)s""", {"prod_id": id})
    cursor.execute("""delete from product where prod_id = %(prod_id)s""", {"prod_id": id})
    conn.commit()


def get_brands():
    cursor = conn.cursor()
    cursor.execute("""select * from brand""")
    records = cursor.fetchall()
    res = []
    for r in records:
        res.append({"id": r[0], "name": r[1], "description": r[2], "img_url": r[3]})
    return res


def get_brand(id):
    cursor = conn.cursor()
    cursor.execute(
        """select * from brand where br_id = %(id)s""", {"id": id})
    records = cursor.fetchall()
    res = {"id": records[0][0], "name": records[0][1], "description": records[0][2], "img_url": records[0][3]}
    return res


def add_brand(data):
    cursor = conn.cursor()
    cursor.execute("""select max(br_id) from brand""")
    br_id = cursor.fetchall()[0][0] + 1
    cursor.execute("""insert into brand (br_id, br_name, br_description, img_url) 
                      values (%(br_id)s, %(br_name)s, %(desc)s, %(img)s)""", {"br_id": br_id,
                                                                              "br_name": data["name"],
                                                                              "desc": data["description"],
                                                                              "img": data["img_url"]
                                                                              })
    conn.commit()


def update_brand(data):
    cursor = conn.cursor()
    cursor.execute("""update brand set br_name = %(br_name)s, br_description = %(desc)s, img_url = %(img)s 
                      where br_id = %(br_id)s""", {"br_id": data["id"],
                                                   "br_name": data["name"],
                                                   "desc": data["description"],
                                                   "img": data["img_url"]
                                                   })
    conn.commit()


def remove_brand(id):
    cursor = conn.cursor()
    cursor.execute("""delete from brand where br_id = %(br_id)s""", {"br_id": id})
    conn.commit()


def get_shop_info():
    cursor = conn.cursor()
    cursor.execute("""select * from shop""")
    records = cursor.fetchall()
    res = {"name": "None", "phone": "None", "address": "None"}
    if records:
        res = {"name": records[0][0], "phone": records[0][1], "address": records[0][2]}
    return res


def update_shop_info(data):
    cursor = conn.cursor()
    cursor.execute("""update shop set name = %(name)s, phone = %(phone)s, address = %(address)s""",
                   {"name": data["name"],
                    "phone": data["phone"],
                    "address": data["address"]
                    })
    conn.commit()
