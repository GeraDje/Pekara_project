from fastapi import  Request, Form, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import List, Optional
from app.dao.productsdao import ProductsDAO
from app.dao.recieptsdao import ReceiptItemDAO, ReceiptsDAO


router = APIRouter()

templates = Jinja2Templates(directory="app/templates")
#
# Работающий код
@router.post("/cart", response_class=HTMLResponse)
async def cart(
        request: Request,
        product_ids: Optional[List[int]] = Form(...),
        quantities: Optional[List[int]] = Form(...)
               ):

    cart_items = []
    total_price = 0
    if product_ids and quantities:
        try:
            products = await ProductsDAO.find_all()
            products_dict = {p['id']: p for p in products}
            # print(f"=============products_dict{products_dict}================")

            for product_id, quantity in zip(product_ids, quantities):
                if quantity > 0:
                    product = products_dict.get(product_id)
                    if product:
                        item_price = int(product['price'])
                        item_total = item_price * quantity
                        total_price += item_total
                        cart_items.append({
                            'product_id': product['id'],
                            'name': product['name'],
                            'price': item_price,
                            'quantity': quantity,
                            'item_total': item_total,

                        })
            # print(f"=============cart_items: {cart_items}================")
            await ReceiptsDAO.add(total_amount=total_price)
            max_id = await ReceiptsDAO.get_max_id()
            for cart_item in cart_items:
                await ReceiptItemDAO.add(
                    receipt_id= max_id,
                    product_id=int(cart_item["product_id"]),
                    quantity=int(cart_item["quantity"]),
                    price= int(cart_item["item_total"])
                )


        except Exception as e:
            print(f"Ошибка при обработке корзины: {e}")
            return HTMLResponse(content="Произошла ошибка при обработке корзины", status_code=500)

    return templates.TemplateResponse(
        "cart.html",
        {
            "request": request,
            "cart_items": cart_items,
            "total_price": total_price,
         }
    )




@router.get("/products", response_class=HTMLResponse)
async def index(
        request: Request,
        ):
    return templates.TemplateResponse(
        "products.html",
        {
            "request": request,
            "products": await  ProductsDAO.find_all(),
        }
    )


