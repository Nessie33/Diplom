from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Замените на ваш секретный ключ


products = []


@app.route('/')
def index():
    return render_template('products.html', products=products)


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        products.append({'id': len(products) + 1, 'name': name, 'price': float(price)})
        flash('Product added successfully!')
        return redirect(url_for('admin'))

    return render_template('admin.html')


@app.route('/delete/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    global products
    products = [p for p in products if p['id'] != product_id]
    flash('Product deleted successfully!')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)