from shop import conn


def get_categories():
    cursor = conn.cursor()
    cursor.execute("""select * from category""")
    records = cursor.fetchall()
    return sorted(records, key=lambda x: len(x[0]))


def get_category_path(cat_num):
    cursor = conn.cursor()
    res = ""
    while cat_num != "":
        cursor.execute("""select cat_name from category where cat_num = %(cat_num)s""", {"cat_num": cat_num})
        records = cursor.fetchall()
        res = records[0][0] + "/" + res
        cat_num = cat_num[:cat_num.rfind(".")]
    return res[:-1]


def get_products(cat_num):
    cursor = conn.cursor()
    cursor.execute("""select * from product where cat_num = %(cat_num)s order by price desc""", {"cat_num": cat_num})
    records = cursor.fetchall()
    res = []
    for r in records:
        res.append({"id": r[0], "name": r[1], "price": r[2], "installment_plan": r[3],
                    "warranty_period": r[4], "img_url": r[5], "cat_num": r[5]})
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
                    "warranty_period": r[4], "img_url": r[5], "cat_num": r[5]})
    return res


def get_low_priced_products(params):
    cursor = conn.cursor()
    cursor.execute("""select * from product where cat_num = %(category)s order by price asc limit %(n)s;""", params)
    records = cursor.fetchall()
    res = []
    for r in records:
        res.append({"id": r[0], "name": r[1], "price": r[2], "installment_plan": r[3],
                    "warranty_period": r[4], "img_url": r[5], "cat_num": r[5]})
    return res


def get_high_priced_products(params):
    cursor = conn.cursor()
    cursor.execute("""select * from product where cat_num = %(category)s order by price desc limit %(n)s;""", params)
    records = cursor.fetchall()
    res = []
    for r in records:
        res.append({"id": r[0], "name": r[1], "price": r[2], "installment_plan": r[3],
                    "warranty_period": r[4], "img_url": r[5], "cat_num": r[5]})
    return res


def get_filter_values(cat_num):
    cursor = conn.cursor()
    cursor.execute("""select min(price), max(price), min(warranty_period), max(warranty_period) 
        from product where cat_num = %(cat_num)s""", {"cat_num": cat_num})
    records = cursor.fetchall()
    res = {"minPrice": 0, "maxPrice": 0, "minWarranty": 0, "maxWarranty": 0}
    if records:
        res = {"minPrice": records[0][0], "maxPrice": records[0][1], "minWarranty": records[0][2], "maxWarranty": records[0][3]}
    return res


def get_shop_info():
    cursor = conn.cursor()
    cursor.execute("""select * from shop""")
    records = cursor.fetchall()
    res = {"name": "None", "phone": "None", "description": "None", "address": "None"}
    if records:
        res = {"name": records[0][0], "phone": records[0][1], "description": records[0][2], "address": records[0][3]}
    return res

