from typing import List, Optional
from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)
from database import Base


class FormData(Base):
    __tablename__ = "form_data"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    category: Mapped[str] = mapped_column(String(255))
    related_office: Mapped[str] = mapped_column(String(255))
    related_secondary_office_1: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True
    )
    related_secondary_office_2: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True
    )
    other_offices: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    topic: Mapped[str] = mapped_column(String(255))
    query: Mapped[str] = mapped_column(Text)
    response: Mapped[str] = mapped_column(Text)
    attachments: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    links: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    related_law_policy_act: Mapped[Optional[str]] = mapped_column(Text)
    validated_by_name: Mapped[Optional[str]] = mapped_column(String(255))
    validated_by_office: Mapped[Optional[str]] = mapped_column(String(255))
    validated_by_position: Mapped[Optional[str]] = mapped_column(String(255))
    validated_by_address: Mapped[Optional[str]] = mapped_column(Text)

    files: Mapped[List["FileData"]] = relationship(
        "FileData", back_populates="form_data"
    )


class FileData(Base):
    __tablename__ = "file_data"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    file_name: Mapped[str] = mapped_column(String(255))
    file_path: Mapped[str] = mapped_column(String(255))
    form_data_id: Mapped[int] = mapped_column(ForeignKey("form_data.id"))

    form_data: Mapped["FormData"] = relationship("FormData", back_populates="files")


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
