from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Замените на ваш секретный ключ


products = []


@app.route('/')
def index():
    return render_template('products.html', products=products)


@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if product is None:
        flash('Товар не найден')
        return redirect(url_for('index'))
    return render_template('product_detail.html', product=product)


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    global products
    if request.method == 'POST':
        if 'add' in request.form:
            name = request.form['name']
            price = request.form['price']
            products.append({'id': len(products) + 1, 'name': name, 'price': float(price)})
            flash('Товар успешно добавлен!')
        elif 'delete' in request.form:
            name = request.form['delete_name']
            products_to_delete = next((p for p in products if p['name'] == name), None)
            if products_to_delete:
                products.remove(products_to_delete)
                flash(f'Товар "{name}" успешно удалён!')
            else:
                flash(f'Товар "{name}" не найден')
        return redirect(url_for('admin'))

    return render_template('admin.html')


if __name__ == '__main__':
    app.run(debug=True)