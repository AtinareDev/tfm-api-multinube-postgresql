from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud.order import (
    create_order,
    delete_order,
    get_order,
    get_orders,
    update_order,
)
from app.db.database import get_db
from app.schemas.order import OrderCreate, OrderRead, OrderUpdate

router = APIRouter(
    prefix="/orders",
    tags=["orders"],
)


@router.post(
    "",
    response_model=OrderRead,
    status_code=status.HTTP_201_CREATED,
)
def create_order_endpoint(
    order_in: OrderCreate,
    db: Session = Depends(get_db),
):
    try:
        return create_order(db, order_in)

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        )


@router.get(
    "",
    response_model=list[OrderRead],
)
def list_orders_endpoint(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return get_orders(db, skip=skip, limit=limit)


@router.get(
    "/{order_id}",
    response_model=OrderRead,
)
def get_order_endpoint(
    order_id: int,
    db: Session = Depends(get_db),
):
    order = get_order(db, order_id)

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pedido no encontrado.",
        )

    return order


@router.put(
    "/{order_id}",
    response_model=OrderRead,
)
def update_order_endpoint(
    order_id: int,
    order_in: OrderUpdate,
    db: Session = Depends(get_db),
):
    order = get_order(db, order_id)

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pedido no encontrado.",
        )

    return update_order(db, order, order_in)


@router.delete(
    "/{order_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_order_endpoint(
    order_id: int,
    db: Session = Depends(get_db),
):
    order = get_order(db, order_id)

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pedido no encontrado.",
        )

    delete_order(db, order)
    return None