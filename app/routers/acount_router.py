from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.database import get_db
from app.schemas.accounts import (
    CountryBase, CountryOut,
    CurrencyBase, CurrencyOut,
    CategoryBase, CategoryOut,
    SubCategoryBase, SubCategoryOut,
)
from app.crud.account import (
    create_country, get_country, update_country, delete_country,
    create_currency, get_currency, update_currency, delete_currency,
    create_category, get_category, update_category, delete_category,
    create_subcategory, get_subcategory, update_subcategory, delete_subcategory
)

country_router = APIRouter(prefix='/country', tags=['Country'])


# ----- Country Endpoints -----

@country_router.post('/countries/', response_model=CountryOut, status_code=status.HTTP_201_CREATED)
def create_country_route(country: CountryBase, db: Session = Depends(get_db)):
    return create_country(db, country)


@country_router.get('/countries/', response_model=List[CountryOut])
def list_countries(db: Session = Depends(get_db)):
    return get_country(db)


@country_router.get('/countries/{country_id}', response_model=CountryOut)
def read_country(country_id: int, db: Session = Depends(get_db)):
    country = get_country(db, country_id)
    if not country:
        raise HTTPException(status_code=404, detail="Country not found")
    return country


@country_router.put('/countries/{country_id}', response_model=CountryOut)
def update_country_route(country_id: int, country: CountryBase, db: Session = Depends(get_db)):
    existing_country = get_country(db, country_id)
    if not existing_country:
        raise HTTPException(status_code=404, detail="Country not found")
    return update_country(db, country, country_id)


@country_router.delete('/countries/{country_id}', response_model=CountryOut)
def delete_country_route(country_id: int, db: Session = Depends(get_db)):
    existing_country = get_country(db, country_id)
    if not existing_country:
        raise HTTPException(status_code=404, detail="Country not found")
    return delete_country(db, country_id)


# ----- Currency Endpoints -----

# @router.post('/currencies/', response_model=CurrencyOut, status_code=status.HTTP_201_CREATED)
# def create_currency_route(currency: CurrencyBase, db: Session = Depends(get_db)):
#     return create_currency(db, currency)


# @router.get('/currencies/', response_model=List[CurrencyOut])
# def list_currencies(db: Session = Depends(get_db)):
#     return get_currency(db)


# @router.get('/currencies/{currency_id}', response_model=CurrencyOut)
# def read_currency(currency_id: int, db: Session = Depends(get_db)):
#     currency = get_currency(db, currency_id)
#     if not currency:
#         raise HTTPException(status_code=404, detail="Currency not found")
#     return currency


# @router.put('/currencies/{currency_id}', response_model=CurrencyOut)
# def update_currency_route(currency_id: int, currency: CurrencyBase, db: Session = Depends(get_db)):
#     existing_currency = get_currency(db, currency_id)
#     if not existing_currency:
#         raise HTTPException(status_code=404, detail="Currency not found")
#     return update_currency(db, currency, currency_id)


# @router.delete('/currencies/{currency_id}', response_model=CurrencyOut)
# def delete_currency_route(currency_id: int, db: Session = Depends(get_db)):
#     existing_currency = get_currency(db, currency_id)
#     if not existing_currency:
#         raise HTTPException(status_code=404, detail="Currency not found")
#     return delete_currency(db, currency_id)


# ----- Category Endpoints -----

# @router.post('/categories/', response_model=CategoryOut, status_code=status.HTTP_201_CREATED)
# def create_category_route(category: CategoryBase, db: Session = Depends(get_db)):
#     return create_category(db, category)


# @router.get('/categories/', response_model=List[CategoryOut])
# def list_categories(db: Session = Depends(get_db)):
#     return get_category(db)


# @router.get('/categories/{category_id}', response_model=CategoryOut)
# def read_category(category_id: int, db: Session = Depends(get_db)):
#     category = get_category(db, category_id)
#     if not category:
#         raise HTTPException(status_code=404, detail="Category not found")
#     return category


# @router.put('/categories/{category_id}', response_model=CategoryOut)
# def update_category_route(category_id: int, category: CategoryBase, db: Session = Depends(get_db)):
#     existing_category = get_category(db, category_id)
#     if not existing_category:
#         raise HTTPException(status_code=404, detail="Category not found")
#     return update_category(db, category, category_id)


# @router.delete('/categories/{category_id}', response_model=CategoryOut)
# def delete_category_route(category_id: int, db: Session = Depends(get_db)):
#     existing_category = get_category(db, category_id)
#     if not existing_category:
#         raise HTTPException(status_code=404, detail="Category not found")
#     return delete_category(db, category_id)


# # ----- SubCategory Endpoints -----

# @router.post('/subcategories/', response_model=SubCategoryOut, status_code=status.HTTP_201_CREATED)
# def create_subcategory_route(subcategory: SubCategoryBase, db: Session = Depends(get_db)):
#     return create_subcategory(db, subcategory)


# @router.get('/subcategories/', response_model=List[SubCategoryOut])
# def list_subcategories(db: Session = Depends(get_db)):
#     return get_subcategory(db)


# @router.get('/subcategories/{subcategory_id}', response_model=SubCategoryOut)
# def read_subcategory(subcategory_id: int, db: Session = Depends(get_db)):
#     subcategory = get_subcategory(db, subcategory_id)
#     if not subcategory:
#         raise HTTPException(status_code=404, detail="SubCategory not found")
#     return subcategory


# @router.put('/subcategories/{subcategory_id}', response_model=SubCategoryOut)
# def update_subcategory_route(subcategory_id: int, subcategory: SubCategoryBase, db: Session = Depends(get_db)):
#     existing_subcategory = get_subcategory(db, subcategory_id)
#     if not existing_subcategory:
#         raise HTTPException(status_code=404, detail="SubCategory not found")
#     return update_subcategory(db, subcategory, subcategory_id)


# @router.delete('/subcategories/{subcategory_id}', response_model=SubCategoryOut)
# def delete_subcategory_route(subcategory_id: int, db: Session = Depends(get_db)):
#     existing_subcategory = get_subcategory(db, subcategory_id)
#     if not existing_subcategory:
#         raise HTTPException(status_code=404, detail="SubCategory not found")
#     return delete_subcategory(db, subcategory_id)
