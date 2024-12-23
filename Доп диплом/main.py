from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel


app = FastAPI()
templates = Jinja2Templates(directory="templates")


products = []


class Product(BaseModel):
    id: int
    name: str
    price: float


@app.get('/', response_class=HTMLResponse)
async def read_products(request: Request) -> HTMLResponse:
    return templates.TemplateResponse('products.html', {'request': request, 'products': products})


@app.get('/product/{product_id}', response_class=HTMLResponse)
async def read_product(request: Request, product_id: int) -> HTMLResponse:
    for product in products:
        if product.id == product_id:
            return templates.TemplateResponse('products.html', {'request': request, 'product': product})
    raise HTTPException(status_code=404, detail='Product not found')


@app.post('/product/{name}/{price}', response_model=Product)
async def create_product(name: str, price: float) -> Product:
    new_id = (products[-1].id + 1) if products else 1
    new_product = Product(id=new_id, name=name, price=price)
    products.append(new_product)
    return new_product


@app.put('/product/{product_id}/{name}/{price}', response_model=Product)
async def update_product(product_id: int, name: str, price: float) -> Product:
    for product in products:
        if product.id == product_id:
            product.name = name
            product.price = price
            return product
    raise HTTPException(status_code=404, detail='Product not found')


@app.delete('/product/{product_id}', response_model=Product)
async def delete_product(product_id: int) -> Product:
    for index, product in enumerate(products):
        if product.id == product_id:
            deleted_product = products.pop(index)
            return deleted_product
    raise HTTPException(status_code=404, detail='Product not found')