from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud.product import (
    create_product,
    delete_product,
    get_product,
    get_products,
    update_product,
)
from app.db.database import get_db
from app.schemas.product import ProductCreate, ProductRead, ProductUpdate

router = APIRouter(
    prefix="/products",
    tags=["products"],
)


@router.post(
    "",
    response_model=ProductRead,
    status_code=status.HTTP_201_CREATED,
)
def create_product_endpoint(
    product_in: ProductCreate,
    db: Session = Depends(get_db),
):
    return create_product(db, product_in)


@router.get(
    "",
    response_model=list[ProductRead],
)
def list_products_endpoint(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return get_products(db, skip=skip, limit=limit)


@router.get(
    "/{product_id}",
    response_model=ProductRead,
)
def get_product_endpoint(
    product_id: int,
    db: Session = Depends(get_db),
):
    product = get_product(db, product_id)

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado.",
        )

    return product


@router.put(
    "/{product_id}",
    response_model=ProductRead,
)
def update_product_endpoint(
    product_id: int,
    product_in: ProductUpdate,
    db: Session = Depends(get_db),
):
    product = get_product(db, product_id)

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado.",
        )

    return update_product(db, product, product_in)


@router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_product_endpoint(
    product_id: int,
    db: Session = Depends(get_db),
):
    product = get_product(db, product_id)

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado.",
        )

    delete_product(db, product)
    return None