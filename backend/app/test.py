from database import engine, Base

try:
    with engine.connect() as conn:
        print("Test koneksi")
except Exception as e:
    print(f"Koneksi ayam")