from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum


class ItemCategory(str, enum.Enum):
    elektronik = "elektronik"
    dokumen = "dokumen"
    pakaian = "pakaian"
    aksesoris = "aksesoris"
    alat_tulis = "alat_tulis"
    tas = "tas"
    lainnya = "lainnya"


class ItemStatus(str, enum.Enum):
    aktif = "aktif"
    selesai = "selesai"
    diproses = "diproses"


class ReportType(str, enum.Enum):
    hilang = "hilang"
    ditemukan = "ditemukan"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    nama = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    items = relationship("Item", back_populates="owner")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    nama_barang = Column(String(200), nullable=False)
    deskripsi = Column(Text, nullable=True)
    kategori = Column(Enum(ItemCategory), nullable=False)
    lokasi = Column(String(255), nullable=False)
    foto_url = Column(String(500), nullable=True)
    tipe = Column(Enum(ReportType), nullable=False)  # hilang / ditemukan
    status = Column(Enum(ItemStatus), default=ItemStatus.aktif)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    owner = relationship("User", back_populates="items")
