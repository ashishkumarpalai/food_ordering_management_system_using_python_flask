from flask import Flask, render_template, request, redirect

app = Flask(__name__)
menu = [
    {"dish_id": 1, "dish_name": "Pizza", "price": 10.99, "availability": True},
    {"dish_id": 2, "dish_name": "Burger", "price": 5.99, "availability": True},
    {"dish_id": 3, "dish_name": "Pasta", "price": 8.99, "availability": False}
]

orders = {}
@app.route('/')
def home():
    return render_template('index.html', menu=menu)
@app.route('/add_dish', methods=['POST'])
def add_dish():
    dish_id = request.form.get('dish_id')
    dish_name = request.form.get('dish_name')
    price = float(request.form.get('price'))
    availability = request.form.get('availability') == 'on'

    # Check if the dish ID already exists
    for dish in menu:
        if dish['dish_id'] == int(dish_id):
            return "Dish ID already exists."

    # Add the new dish to the menu
    menu.append({
        "dish_id": int(dish_id),
        "dish_name": dish_name,
        "price": price,
        "availability": availability
    })

    return redirect('/')

@app.route('/remove_dish', methods=['POST'])
def remove_dish():
    dish_id = int(request.form.get('dish_id'))

    # Find the dish in the menu and remove it
    for dish in menu:
        if dish['dish_id'] == dish_id:
            menu.remove(dish)
            break

    return redirect('/')

@app.route('/update_availability', methods=['POST'])
def update_availability():
    dish_id = int(request.form.get('dish_id'))
    availability = request.form.get('availability') == 'on'

    # Find the dish in the menu and update its availability
    for dish in menu:
        if dish['dish_id'] == dish_id:
            dish['availability'] = availability
            break

    return redirect('/')


@app.route('/new_order', methods=['POST'])
def new_order():
    customer_name = request.form.get('customer_name')
    dish_ids = request.form.get('dish_ids').split(',')

    order_id = len(orders) + 1
    order = {
        'order_id': order_id,
        'customer_name': customer_name,
        'dish_ids': [],
        'status': 'received'
    }

    # Check if each dish is available and add it to the order
    for dish_id in dish_ids:
        dish_id = int(dish_id)
        dish_exists = False

        for dish in menu:
            if dish['dish_id'] == dish_id:
                dish_exists = True
                if dish['availability']:
                   order['dish_ids'].append(dish_id)
                else:
                    return f"Dish {dish['dish_name']} is not available."

        if not dish_exists:
            return f"Dish with ID {dish_id} does not exist."

    orders[order_id] = order
    return redirect('/view_orders')


@app.route('/update_order_status', methods=['POST'])
def update_order_status():
    order_id = int(request.form.get('order_id'))
    status = request.form.get('status')

    # Find the order and update its status
    if order_id in orders:
        orders[order_id]['status'] = status
    else:
        return "Invalid order ID."

    return redirect('/view_orders')



@app.route('/view_orders')
def view_orders():
    return render_template('orders.html', orders=orders, menu=menu)



if __name__ == '__main__':
    app.run(debug=True)
