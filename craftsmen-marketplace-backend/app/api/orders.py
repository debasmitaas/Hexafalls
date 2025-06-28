from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.models import Order, OrderItem, Product
from app.schemas.schemas import OrderCreate, OrderResponse, OrderUpdate
from app.services.ai_service import AIService

router = APIRouter(prefix="/orders", tags=["orders"])

ai_service = AIService()


@router.post("/", response_model=OrderResponse)
async def create_order(order_data: OrderCreate, db: Session = Depends(get_db)):
    """Create a new order"""
    
    # Calculate total amount
    total_amount = 0
    order_items_data = []
    
    for item in order_data.items:
        # Verify product exists
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found")
        
        if not product.is_active:
            raise HTTPException(status_code=400, detail=f"Product {product.name} is not available")
        
        # Use current product price if not specified
        item_price = item.price if item.price else product.price
        item_total = item_price * item.quantity
        total_amount += item_total
        
        order_items_data.append({
            "product_id": item.product_id,
            "quantity": item.quantity,
            "price": item_price
        })
    
    # Create order
    db_order = Order(
        customer_name=order_data.customer_name,
        customer_phone=order_data.customer_phone,
        customer_email=order_data.customer_email,
        delivery_address=order_data.delivery_address,
        notes=order_data.notes,
        total_amount=total_amount
    )
    
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    
    # Create order items
    for item_data in order_items_data:
        db_order_item = OrderItem(
            order_id=db_order.id,
            **item_data
        )
        db.add(db_order_item)
    
    db.commit()
    
    # Refresh to get relationships
    db.refresh(db_order)
    
    return OrderResponse.from_orm(db_order)


@router.get("/", response_model=List[OrderResponse])
async def get_orders(
    skip: int = 0,
    limit: int = 100,
    status: str = None,
    customer_id: int = None,
    db: Session = Depends(get_db)
):
    """Get list of orders with optional filtering"""
    
    query = db.query(Order)
    
    if status:
        query = query.filter(Order.status == status)
    
    if customer_id:
        query = query.filter(Order.customer_id == customer_id)
    
    orders = query.offset(skip).limit(limit).all()
    return [OrderResponse.from_orm(order) for order in orders]


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(order_id: int, db: Session = Depends(get_db)):
    """Get a specific order"""
    
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    return OrderResponse.from_orm(order)


@router.put("/{order_id}", response_model=OrderResponse)
async def update_order(
    order_id: int,
    order_update: OrderUpdate,
    db: Session = Depends(get_db)
):
    """Update an order"""
    
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Update fields
    update_data = order_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(order, field, value)
    
    db.commit()
    db.refresh(order)
    
    return OrderResponse.from_orm(order)


@router.post("/{order_id}/confirm")
async def confirm_order(order_id: int, db: Session = Depends(get_db)):
    """Confirm an order"""
    
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    order.status = "confirmed"
    db.commit()
    
    return {"message": "Order confirmed successfully"}


@router.post("/{order_id}/complete")
async def complete_order(order_id: int, db: Session = Depends(get_db)):
    """Mark an order as completed"""
    
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    order.status = "completed"
    db.commit()
    
    return {"message": "Order completed successfully"}


@router.post("/{order_id}/cancel")
async def cancel_order(order_id: int, db: Session = Depends(get_db)):
    """Cancel an order"""
    
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    if order.status in ["completed", "cancelled"]:
        raise HTTPException(
            status_code=400, 
            detail=f"Cannot cancel order with status: {order.status}"
        )
    
    order.status = "cancelled"
    db.commit()
    
    return {"message": "Order cancelled successfully"}
