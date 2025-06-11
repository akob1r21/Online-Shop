from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.product_model import Product, ProductItem, ProductPrice, ProductImage, Color
from app.models.models import SizeStock, ColorStock
from app.models.accounts import Currency, SubCategory
from app.schemas.product import *
from typing import List

router = APIRouter(prefix="/products", tags=["Products"])
product_item_router = APIRouter(prefix="/product-item", tags=["Product Items"])
product_price_router = APIRouter(prefix="/product-prices", tags=["Product Prices"])
product_image_router = APIRouter(prefix="/product-images", tags=["Product Images"])
color_router = APIRouter(prefix="/colors", tags=["Colors"])

@color_router.get("/", response_model=List[ColorOut])
def get_colors(db: Session = Depends(get_db)):
    return db.query(Color).all()

@color_router.post("/", response_model=ColorOut)
def create_color(color: ColorCreate, db: Session = Depends(get_db)):
    db_color = Color(**color.dict())
    db.add(db_color)
    db.commit()
    db.refresh(db_color)
    return db_color

@color_router.put("/{id}", response_model=ColorOut)
def update_color(id: int, color: ColorCreate, db: Session = Depends(get_db)):
    db_color = db.query(Color).get(id)
    if not db_color:
        raise HTTPException(status_code=404, detail="Color not found")
    for field, value in color.dict().items():
        setattr(db_color, field, value)
    db.commit()
    db.refresh(db_color)
    return db_color

@color_router.delete("/{id}")
def delete_color(id: int, db: Session = Depends(get_db)):
    db_color = db.query(Color).get(id)
    if not db_color:
        raise HTTPException(status_code=404, detail="Color not found")
    db.delete(db_color)
    db.commit()
    return {"detail": "Color deleted"}

@product_image_router.get("/{product_id}", response_model=List[ProductImageOut])
def get_product_images(product_id: int, db: Session = Depends(get_db)):
    items = db.query(ProductItem).filter(ProductItem.product_id == product_id).all()
    if not items:
        return []
    images = []
    for item in items:
        images += db.query(ProductImage).filter(ProductImage.product_item_id == item.id).all()
    return images

@product_image_router.post("/", response_model=ProductImageOut)
def create_product_image(image: ProductImageCreate, db: Session = Depends(get_db)):
    db_image = ProductImage(**image.dict())
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image

@product_image_router.delete("/{id}")
def delete_product_image(id: int, db: Session = Depends(get_db)):
    image = db.query(ProductImage).get(id)
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    db.delete(image)
    db.commit()
    return {"detail": "Image deleted"}

@product_price_router.get("/", response_model=List[ProductPriceOut])
def get_all_prices(db: Session = Depends(get_db)):
    prices = db.query(ProductPrice).all()
    for price in prices:
        product = db.query(Product).filter(Product.id == price.product_id).first()
        currency = db.query(Currency).filter(Currency.id == price.currencies_id).first()
        if product and currency:
            income_percentage = product.percentage / 100 if product.percentage else 0
            price.amount = float(price.price) * float(currency.currency_rate) * (1 + income_percentage)
    return prices

@product_price_router.post("/", response_model=ProductPriceOut)
def create_price(price_data: ProductPriceCreate, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == price_data.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    currency = db.query(Currency).filter(Currency.id == price_data.currencies_id).first()
    if not currency:
        raise HTTPException(status_code=404, detail="Currency not found")
    
    income_percentage = product.percentage / 100 if product.percentage else 0
    amount = float(price_data.price) * float(currency.currency_rate) * (1 + income_percentage)
    
    new_price = ProductPrice(
        product_id=price_data.product_id,
        currencies_id=price_data.currencies_id,
        price=price_data.price,
        amount=amount
    )
    db.add(new_price)
    db.commit()
    db.refresh(new_price)
    return new_price

@product_price_router.put("/{id}", response_model=ProductPriceOut)
def update_price(id: int, price_data: ProductPriceCreate, db: Session = Depends(get_db)):
    price = db.query(ProductPrice).filter(ProductPrice.id == id).first()
    if not price:
        raise HTTPException(status_code=404, detail="Price not found")
    product = db.query(Product).filter(Product.id == price_data.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    currency = db.query(Currency).filter(Currency.id == price_data.currencies_id).first()
    if not currency:
        raise HTTPException(status_code=404, detail="Currency not found")
    
    for key, value in price_data.dict().items():
        setattr(price, key, value)
    
    income_percentage = product.percentage / 100 if product.percentage else 0
    price.amount = float(price.price) * float(currency.currency_rate) * (1 + income_percentage)
    
    db.commit()
    db.refresh(price)
    return price

@product_price_router.delete("/{id}")
def delete_price(id: int, db: Session = Depends(get_db)):
    price = db.query(ProductPrice).filter(ProductPrice.id == id).first()
    if not price:
        raise HTTPException(status_code=404, detail="Price not found")
    db.delete(price)
    db.commit()
    return {"detail": "Price deleted"}

@product_item_router.post("/", response_model=ProductItemOut)
def create_product_item(item: ProductItemCreate, db: Session = Depends(get_db)):
    db_item = ProductItem(product_id=item.product_id, code=item.code)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    
    for image_data in item.images:
        db_image = ProductImage(
            product_item_id=db_item.id,
            color_id=image_data.color_id,
            image=image_data.image
        )
        db.add(db_image)
    
    for size_stock in item.size_stocks:
        db_size_stock = SizeStock(
            product_item=db_item.product_id,
            size_id=size_stock.size_id,
            quantity=size_stock.quantity
        )
        db.add(db_size_stock)
    
    for color_stock in item.color_stocks:
        db_color_stock = ColorStock(
            product_item=db_item.product_id,
            color_id=color_stock.color_id,
            quantity=color_stock.quantity
        )
        db.add(db_color_stock)
    
    db.commit()
    db.refresh(db_item)
    return db_item

@product_item_router.get("/", response_model=List[ProductItemOut])
def read_product_items(db: Session = Depends(get_db)):
    return db.query(ProductItem).all()

@product_item_router.get("/{item_id}", response_model=ProductItemOut)
def read_product_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(ProductItem).filter(ProductItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Product item not found")
    return item

@product_item_router.put("/{item_id}", response_model=ProductItemOut)
def update_product_item(item_id: int, updated_item: ProductItemCreate, db: Session = Depends(get_db)):
    item = db.query(ProductItem).filter(ProductItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Product item not found")
    
    for key, value in updated_item.dict(exclude={"images", "size_stocks", "color_stocks"}).items():
        setattr(item, key, value)
    
    db.query(ProductImage).filter(ProductImage.product_item_id == item_id).delete()
    db.query(SizeStock).filter(SizeStock.product_item == item.product_id).delete()
    db.query(ColorStock).filter(ColorStock.product_item == item.product_id).delete()
    
    for image_data in updated_item.images:
        db_image = ProductImage(
            product_item_id=item_id,
            color_id=image_data.color_id,
            image=image_data.image
        )
        db.add(db_image)
    
    for size_stock in updated_item.size_stocks:
        db_size_stock = SizeStock(
            product_item=item.product_id,
            size_id=size_stock.size_id,
            quantity=size_stock.quantity
        )
        db.add(db_size_stock)
    
    for color_stock in updated_item.color_stocks:
        db_color_stock = ColorStock(
            product_item=item.product_id,
            color_id=color_stock.color_id,
            quantity=color_stock.quantity
        )
        db.add(db_color_stock)
    
    db.commit()
    db.refresh(item)
    return item

@product_item_router.delete("/{item_id}")
def delete_product_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(ProductItem).filter(ProductItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Product item not found")
    db.delete(item)
    db.commit()
    return {"detail": "Deleted successfully"}

@router.post("/", response_model=ProductOut)
def create_product(product_data: ProductCreate, db: Session = Depends(get_db)):
    db_product = Product(
        subcategory_id=product_data.subcategory_id,
        title=product_data.title,
        description=product_data.description,
        percentage=product_data.percentage
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    for price_data in product_data.prices:
        currency = db.query(Currency).filter(Currency.id == price_data.currencies_id).first()
        if not currency:
            raise HTTPException(status_code=400, detail=f"Currency with ID {price_data.currencies_id} not found")
        
        income_percentage = db_product.percentage / 100 if db_product.percentage else 0
        amount = float(price_data.price) * float(currency.currency_rate) * (1 + income_percentage)
        
        db_price = ProductPrice(
            product_id=db_product.id,
            currencies_id=price_data.currencies_id,
            price=price_data.price,
            amount=amount
        )
        db.add(db_price)

    for item_data in product_data.items:
        db_item = ProductItem(
            product_id=db_product.id,
            code=item_data.code
        )
        db.add(db_item)
        db.commit()
        db.refresh(db_item)

        for image_data in item_data.images:
            db_image = ProductImage(
                product_item_id=db_item.id,
                color_id=image_data.color_id,
                image=image_data.image
            )
            db.add(db_image)

        for size_stock in item_data.size_stocks:
            db_size_stock = SizeStock(
                product_item=db_product.id,
                size_id=size_stock.size_id,
                quantity=size_stock.quantity
            )
            db.add(db_size_stock)

        for color_stock in item_data.color_stocks:
            db_color_stock = ColorStock(
                product_item=db_product.id,
                color_id=color_stock.color_id,
                quantity=color_stock.quantity
            )
            db.add(db_color_stock)

    db.commit()
    db.refresh(db_product)

    prices = db.query(ProductPrice).filter(ProductPrice.product_id == db_product.id).all()
    if prices:
        total_amount = sum(float(price.amount) for price in prices)
        db_product.amount = total_amount / len(prices)

    db.commit()
    db.refresh(db_product)
    return db_product

@router.get("/", response_model=List[ProductOut])
def get_all_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    for product in products:
        prices = db.query(ProductPrice).filter(ProductPrice.product_id == product.id).all()
        if prices:
            total_amount = sum(float(price.amount) for price in prices)
            product.amount = total_amount / len(prices) if prices else 0
    return products

@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    prices = db.query(ProductPrice).filter(ProductPrice.product_id == product.id).all()
    if prices:
        total_amount = sum(float(price.amount) for price in prices)
        product.amount = total_amount / len(prices) if prices else 0
    
    return product



@router.get("/{product_id}/colors", response_model=List[ProductColorImageOut])
def get_colors_with_images(product_id: int, db: Session = Depends(get_db)):
    product_items = db.query(ProductItem).filter(ProductItem.product_id == product_id).all()
    result = []
    for item in product_items:
        images = db.query(ProductImage).filter(ProductImage.product_item_id == item.id).all()
        for image in images:
            result.append({
                "color_id": image.color.id,
                "color_name": image.color.color_name,
                "color_code": image.color.color_code,
                "image": image.image
            })
    return result


@router.put("/{product_id}", response_model=ProductOut)
def update_product(product_id: int, updated: ProductCreate, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    for key, value in updated.dict(exclude={"prices", "items"}).items():
        setattr(product, key, value)
    
    db.query(ProductPrice).filter(ProductPrice.product_id == product_id).delete()
    db.query(ProductItem).filter(ProductItem.product_id == product_id).delete()
    
    for price_data in updated.prices:
        currency = db.query(Currency).filter(Currency.id == price_data.currencies_id).first()
        if not currency:
            raise HTTPException(status_code=400, detail=f"Currency with ID {price_data.currencies_id} not found")
        
        income_percentage = product.percentage / 100 if product.percentage else 0
        amount = float(price_data.price) * float(currency.currency_rate) * (1 + income_percentage)
        
        db_price = ProductPrice(
            product_id=product_id,
            currencies_id=price_data.currencies_id,
            price=price_data.price,
            amount=amount
        )
        db.add(db_price)

    for item_data in updated.items:
        db_item = ProductItem(
            product_id=product_id,
            code=item_data.code
        )
        db.add(db_item)
        db.commit()
        db.refresh(db_item)

        for image_data in item_data.images:
            db_image = ProductImage(
                product_item_id=db_item.id,
                color_id=image_data.color_id,
                image=image_data.image
            )
            db.add(db_image)

        for size_stock in item_data.size_stocks:
            db_size_stock = SizeStock(
                product_item=product_id,
                size_id=size_stock.size_id,
                quantity=size_stock.quantity
            )
            db.add(db_size_stock)

        for color_stock in item_data.color_stocks:
            db_color_stock = ColorStock(
                product_item=product_id,
                color_id=color_stock.color_id,
                quantity=color_stock.quantity
            )
            db.add(db_color_stock)

    prices = db.query(ProductPrice).filter(ProductPrice.product_id == product_id).all()
    if prices:
        total_amount = sum(float(price.amount) for price in prices)
        product.amount = total_amount / len(prices)
    
    db.commit()
    db.refresh(product)
    return product

@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
    return {"message": "Product deleted"}