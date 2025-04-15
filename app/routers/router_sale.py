from fastapi import  Request, HTTPException, status, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.dao.productsdao import ProductsDAO
from app.dao.recieptsdao import ReceiptsDAO, ReceiptItemDAO
from app.shemas.schemas import Order

router = APIRouter(prefix="/cass", tags=["Касса"])
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    products = await ProductsDAO.find_all()
    return templates.TemplateResponse("index.html", {"request": request, "products": products})

@router.post("/sale")
async def create_sale(order: Order):
    await ReceiptsDAO.add(total_amount=order.total,received_amount=order.receivedAmount,change=order.change)
    max_id = await ReceiptsDAO.get_max_id()
    for i in order.items:
        if i.quantity>0:
            await ReceiptItemDAO.add(
                receipt_id= max_id,
                product_id=i.product_id,
                quantity=i.quantity,
                price= i.item_total,
                            )

