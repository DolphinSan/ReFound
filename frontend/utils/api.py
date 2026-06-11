import requests
import streamlit as st

BASE_URL = "https://refound-production-7f96.up.railway.app"


def get_headers():
    token = st.session_state.get("token")
    if token:
        return {"Authorization": f"Bearer {token}"}
    return {}


# ── Auth ──────────────────────────────────────────────────────────────────────

def register(nama: str, email: str, password: str):
    try:
        res = requests.post(f"{BASE_URL}/auth/register", json={
            "nama": nama,
            "email": email,
            "password": password,
        })
        return res.json(), res.status_code
    except Exception as e:
        return {"detail": str(e)}, 500


def login(email: str, password: str):
    try:
        res = requests.post(f"{BASE_URL}/auth/login", json={
            "email": email,
            "password": password,
        })
        return res.json(), res.status_code
    except Exception as e:
        return {"detail": str(e)}, 500


def get_me():
    try:
        res = requests.get(f"{BASE_URL}/auth/me", headers=get_headers())
        return res.json(), res.status_code
    except Exception as e:
        return {"detail": str(e)}, 500


# ── Items ─────────────────────────────────────────────────────────────────────

def get_items(tipe=None, kategori=None, status=None, lokasi=None, search=None, skip=0, limit=20):
    params = {"skip": skip, "limit": limit}
    if tipe:
        params["tipe"] = tipe
    if kategori:
        params["kategori"] = kategori
    if status:
        params["status"] = status
    if lokasi:
        params["lokasi"] = lokasi
    if search:
        params["search"] = search
    try:
        res = requests.get(f"{BASE_URL}/items/", params=params)
        return res.json(), res.status_code
    except Exception as e:
        return {"detail": str(e)}, 500


def get_item(item_id: int):
    try:
        res = requests.get(f"{BASE_URL}/items/{item_id}")
        return res.json(), res.status_code
    except Exception as e:
        return {"detail": str(e)}, 500


def create_item(nama_barang, deskripsi, kategori, lokasi, tipe, foto=None):
    try:
        data = {
            "nama_barang": nama_barang,
            "kategori": kategori,
            "lokasi": lokasi,
            "tipe": tipe,
        }
        if deskripsi:
            data["deskripsi"] = deskripsi

        files = {}
        if foto is not None:
            files["foto"] = (foto.name, foto.getvalue(), foto.type)

        res = requests.post(
            f"{BASE_URL}/items/",
            data=data,
            files=files if files else None,
            headers=get_headers(),
        )
        return res.json(), res.status_code
    except Exception as e:
        return {"detail": str(e)}, 500


def update_item(item_id: int, data: dict):
    try:
        res = requests.put(
            f"{BASE_URL}/items/{item_id}",
            json=data,
            headers=get_headers(),
        )
        return res.json(), res.status_code
    except Exception as e:
        return {"detail": str(e)}, 500


def update_status(item_id: int, status: str):
    try:
        res = requests.patch(
            f"{BASE_URL}/items/{item_id}/status",
            params={"status": status},
            headers=get_headers(),
        )
        return res.json(), res.status_code
    except Exception as e:
        return {"detail": str(e)}, 500


def delete_item(item_id: int):
    try:
        res = requests.delete(
            f"{BASE_URL}/items/{item_id}",
            headers=get_headers(),
        )
        return res.status_code
    except Exception as e:
        return 500


# ── Dashboard ─────────────────────────────────────────────────────────────────

def get_dashboard_stats():
    try:
        res = requests.get(f"{BASE_URL}/dashboard/stats")
        return res.json(), res.status_code
    except Exception as e:
        return {"detail": str(e)}, 500