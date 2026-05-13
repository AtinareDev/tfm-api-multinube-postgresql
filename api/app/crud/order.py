from decimal import Decimal

from sqlalchemy.orm import Session, joinedload

from app.models.customer import Customer
from app.models.order import Order, OrderItem
from app.models.product import Product
from app.schemas.order import OrderCreate, OrderUpdate


def get_order(db: Session, order_id: int) -> Order | None:
    return (
        db.query(Order)
        .options(joinedload(Order.items))
        .filter(Order.id == order_id)
        .first()
    )


def get_orders(db: Session, skip: int = 0, limit: int = 100) -> list[Order]:
    return (
        db.query(Order)
        .options(joinedload(Order.items))
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_order(db: Session, order_in: OrderCreate) -> Order:
    try:
        customer = db.query(Customer).filter(Customer.id == order_in.customer_id).first()

        if not customer:
            raise ValueError("Cliente no encontrado.")

        order = Order(
            customer_id=order_in.customer_id,
            status="pending",
            total_amount=Decimal("0.00"),
        )

        db.add(order)
        db.flush()

        total_amount = Decimal("0.00")

        for item_in in order_in.items:
            product = db.query(Product).filter(Product.id == item_in.product_id).first()

            if not product:
                raise ValueError(f"Producto con ID {item_in.product_id} no encontrado.")

            if product.stock < item_in.quantity:
                raise ValueError(
                    f"Stock insuficiente para el producto '{product.name}'. "
                    f"Stock disponible: {product.stock}."
                )

            unit_price = product.price
            line_total = unit_price * item_in.quantity
            total_amount += line_total

            product.stock -= item_in.quantity

            order_item = OrderItem(
                order_id=order.id,
                product_id=product.id,
                quantity=item_in.quantity,
                unit_price=unit_price,
            )

            db.add(order_item)

        order.total_amount = total_amount

        db.commit()
        db.refresh(order)

        return get_order(db, order.id)

    except Exception:
        db.rollback()
        raise


def update_order(
    db: Session,
    order: Order,
    order_in: OrderUpdate,
) -> Order:
    update_data = order_in.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(order, field, value)

    db.commit()
    db.refresh(order)

    return get_order(db, order.id)


def delete_order(db: Session, order: Order) -> None:
    try:
        for item in order.items:
            product = db.query(Product).filter(Product.id == item.product_id).first()

            if product:
                product.stock += item.quantity

        db.delete(order)
        db.commit()

    except Exception:
        db.rollback()
        raise