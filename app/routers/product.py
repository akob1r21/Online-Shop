from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.product_model import *
from app.schemas.product import *
from typing import List
from fastapi import FastAPI



router = APIRouter(prefix="/products", tags=["Products"])
product_item_router = APIRouter(prefix='/product-item', tags=['Product Items'])
product_price_router = APIRouter(prefix="/product-prices", tags=["Product Prices"])
product_image_router = APIRouter(prefix="/product-images", tags=["Product Images"])
color_router = APIRouter(prefix="/colors", tags=["Colors"])

@color_router.get("/", response_model=list[ColorRead])
def get_colors(db: Session = Depends(get_db)):
    return db.query(Color).all()

@color_router.post("/", response_model=ColorRead)
def create_color(color: ColorCreate, db: Session = Depends(get_db)):
    db_color = Color(**color.dict())
    db.add(db_color)
    db.commit()
    db.refresh(db_color)
    return db_color

@color_router.put("/{id}", response_model=ColorRead)
def update_color(id: int, color: ColorUpdate, db: Session = Depends(get_db)):
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

@product_image_router.get("/{product_id}", response_model=list[ProductImageRead])
def get_product_images(product_id: int, db: Session = Depends(get_db)):
    items = db.query(ProductItem).filter(ProductItem.product_id == product_id).all()
    if not items:
        return []
    
    images = []
    for item in items:
        images += db.query(ProductImage).filter(ProductImage.product_item_id == item.id).all()
    return images

@product_image_router.post("/", response_model=ProductImageRead)
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

@product_price_router.get("/", response_model=list[ProductPriceRead])
def get_all_prices(db: Session = Depends(get_db)):
    return db.query(ProductPrice).all()

@product_price_router.post("/", response_model=ProductPriceRead)
def create_price(price_data: ProductPriceCreate, db: Session = Depends(get_db)):
    new_price = ProductPrice(**price_data.dict())
    db.add(new_price)
    db.commit()
    db.refresh(new_price)
    return new_price


@product_price_router.put("/{id}", response_model=ProductPriceRead)
def update_price(id: int, price_data: ProductPriceCreate, db: Session = Depends(get_db)):
    price = db.query(ProductPrice).filter(ProductPrice.id == id).first()
    if not price:
        raise HTTPException(status_code=404, detail="Price not found")
    for key, value in price_data.dict().items():
        setattr(price, key, value)
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



@product_item_router.post('/', response_model=ProductItemRead)
def create_product_item(item: ProductItemCreate, db: Session = Depends(get_db)):
    db_item = ProductItem(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@product_item_router.get('/', response_model=list[ProductItemRead])
def read_product_items(db: Session = Depends(get_db)):
    items = db.query(ProductItem).all()
    return items


@product_item_router.get('/{item_id}', response_model=ProductItemRead)
def read_product_item(item_id: int, db: Session = Depends(get_db)):
    item  = db.query(ProductItem).filter(ProductItem.id==item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail='Product item not found')
    return item

@product_item_router.put('/{item_id}', response_model=ProductItemRead)
def update_product_item(item_id: int,updated_item: ProductItemCreate, db: Session = Depends(get_db)):
    item = db.query(ProductItem).filter(ProductItem.id==item_id).first()
    if not item:
        raise HTTPException(status_code=404,  detail='Product item not found')
    for key, value in updated_item.dict().items():
        setattr(item, key, value)
    db.commit()
    db.refresh(item)
    return item

@product_item_router.delete('/{item_id}')
def delete_product_item(item_id: int, db: Session =Depends(get_db)):
    item = db.query(ProductItem).filter(ProductItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404,  detail='Product item not found')
    db.delete(item)
    db.commit()
    return {'detail': 'Deleted successfully'}


@router.post("/", response_model=ProductOut)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    new_product = Product(**product.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


@router.get("/", response_model=List[ProductOut])
def get_all_products(db: Session = Depends(get_db)):
    return db.query(Product).all()



@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product



@router.put("/{product_id}", response_model=ProductOut)
def update_product(product_id: int, updated: ProductUpdate, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    for key, value in updated.dict().items():
        setattr(product, key, value)
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
    return {"message": "Product deleted "}
