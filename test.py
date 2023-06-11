products_names = [('Alpha 15',), ('Alpha 17',), ('Katana gf76',)]

names = []
for i in range(len(products_names)):
    print(f"i is {i}")
    value = str(products_names[i])
    print(f"value: {value}")
    element = "".join(i for i in value if (i.isdigit() or i.isalpha()) or i == ' ')
    print(element)
    names.append(element)
print(names)
print(names[0])


products_prices = [(67000,), (70000,), (60000,)]
prices = []
for i in range(len(products_prices)):
    value = str(products_prices[i])
    print(value)
    element = "".join(i for i in value if i.isdigit())
    prices.append(element)
print(prices)

from app import db, app
with app.app_context():
    pr_type = db.engine.execute(f"SELECT product_type FROM products WHERE product_identifier = 1;").all()
print(pr_type)
type_product = "".join(i for i in str(pr_type) if i.isalpha())
print(type_product)
