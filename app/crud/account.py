from sqlalchemy.orm import Session
from app.models.accounts import User, Country, Currency, Category, SubCategory
from app.schemas.accounts import (
    UserLogin, UserRegister, UserOut,
    CountryBase, CountryOut, CurrencyBase,
    CurrencyOut, CategoryBase, CategoryOut,
    SubCategoryBase, SubCategoryOut
)


def create_country(db: Session, country_data: CountryBase) -> Country:
    country = Country(**country_data.dict())
    db.add(country)
    db.commit()
    db.refresh(country)
    return country


def get_country(db: Session, country_id: int = None) -> Country:
    if country_id is None:
        return db.query(Country).all()
    else:
        return db.query(Country).filter(Country.id == country_id).first()


def update_country(db: Session, country_data: CountryBase, country_id: int) -> Country:
    country = db.query(Country).filter(Country.id == country_data.id).first()
    country.title = country_data.title
    db.commit()
    db.refresh(country)
    return country


def delete_country(db: Session, country_id: int ) -> Country:
    country = db.query(Country).filter(Country.id==country_id).first()
    db.delete(country)
    db.commit()
    return country


def create_currency(db: Session, currency_data: CurrencyBase) -> Currency:
    currency = Currency(**currency_data.dict())
    db.add(currency)
    db.commit()
    db.refresh(currency)
    return currency


def get_currency(db: Session, id: int = None ) -> Currency:
    if id is None :
        return db.query(Currency).all()
    else :
        return db.query(Currency).filter(Currency.id==id).first()


def update_currency(db: Session, currency_data: CurrencyBase, id: int) -> Currency:
    currency = db.query(Currency).filter(Currency.id==id).first()
    currency.country_id = currency_data.country_id
    currency.currency_rate = currency_data.currency_rate
    db.commit()
    db.refresh(currency)
    return currency


def delete_currency(db: Session, id: int) -> Currency:
    currency = db.query(Currency).filter(Currency.id == id).first()
    db.delete(currency)
    db.commit()
    return currency


def create_category(db: Session, category_date: CategoryBase) -> Category:
    category = Category(**category_date.dict())
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

def get_category(db: Session, id: int = None) -> Category:
    if id is None:
        return db.query(Category).all()
    else:
        return db.query(Category).filter(Category.id == id).first()
    

def update_category(db: Session, category_data: CategoryBase, id: int) -> Category:
    category = db.query(Category).filter(Category.id==id).first()
    category.title = category_data.title
    category.description = category_data.description
    category.image = category_data.image
    category.is_active = category_data.is_active
    db.commit()
    db.refresh(category)
    return category


def delete_category(db: Session, id: int) -> Category:
    category = db.query(Category).filter(Category.id==id).first()
    db.delete(category)
    db.commit()
    return category