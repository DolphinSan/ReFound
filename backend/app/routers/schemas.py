from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from app.models import ItemCategory, ItemStatus, ReportType


# Auth
class UserCreate(BaseModel):
    nama: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    nama: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[int] = None


# Item
class ItemCreate(BaseModel):
    nama_barang: str
    deskripsi: Optional[str] = None
    kategori: ItemCategory
    lokasi: str
    tipe: ReportType

class ItemUpdate(BaseModel):
    nama_barang: Optional[str] = None
    deskripsi: Optional[str] = None
    kategori: Optional[ItemCategory] = None
    lokasi: Optional[str] = None
    status: Optional[ItemStatus] = None

class ItemOut(BaseModel):
    id: int
    nama_barang: str
    deskripsi: Optional[str]
    kategori: ItemCategory
    lokasi: str
    foto_url: Optional[str]
    tipe: ReportType
    status: ItemStatus
    user_id: int
    created_at: datetime
    owner: UserOut

    class Config:
        from_attributes = True

class DashboardStats(BaseModel):
    total_hilang: int
    total_ditemukan: int
    total_selesai: int
    laporan_terbaru: list[ItemOut]
    statistik_kategori: dict
