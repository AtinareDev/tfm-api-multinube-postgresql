from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud.customer import (
    create_customer,
    delete_customer,
    get_customer,
    get_customer_by_email,
    get_customers,
    update_customer,
)
from app.db.database import get_db
from app.schemas.customer import CustomerCreate, CustomerRead, CustomerUpdate

router = APIRouter(
    prefix="/customers",
    tags=["customers"],
)


@router.post(
    "",
    response_model=CustomerRead,
    status_code=status.HTTP_201_CREATED,
)
def create_customer_endpoint(
    customer_in: CustomerCreate,
    db: Session = Depends(get_db),
):
    existing_customer = get_customer_by_email(db, customer_in.email)

    if existing_customer:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un cliente con ese email.",
        )

    return create_customer(db, customer_in)


@router.get(
    "",
    response_model=list[CustomerRead],
)
def list_customers_endpoint(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return get_customers(db, skip=skip, limit=limit)


@router.get(
    "/{customer_id}",
    response_model=CustomerRead,
)
def get_customer_endpoint(
    customer_id: int,
    db: Session = Depends(get_db),
):
    customer = get_customer(db, customer_id)

    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente no encontrado.",
        )

    return customer


@router.put(
    "/{customer_id}",
    response_model=CustomerRead,
)
def update_customer_endpoint(
    customer_id: int,
    customer_in: CustomerUpdate,
    db: Session = Depends(get_db),
):
    customer = get_customer(db, customer_id)

    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente no encontrado.",
        )

    if customer_in.email and customer_in.email != customer.email:
        existing_customer = get_customer_by_email(db, customer_in.email)

        if existing_customer:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe un cliente con ese email.",
            )

    return update_customer(db, customer, customer_in)


@router.delete(
    "/{customer_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_customer_endpoint(
    customer_id: int,
    db: Session = Depends(get_db),
):
    customer = get_customer(db, customer_id)

    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente no encontrado.",
        )

    delete_customer(db, customer)
    return None