from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import TEXT, ENUM, DATE

from db.models.model_base import Base
from scraping.pilkanoznapl import categories

category_enum = ENUM(*categories.values(), name="pilkanoznapl_article_category", create_type=False)


class Article(Base):
    __tablename__ = 'pilkanoznapl'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    date = Column(DATE)
    link = Column(String(300))
    category = Column(category_enum)
    text = Column(TEXT)
    summary = Column(TEXT)
