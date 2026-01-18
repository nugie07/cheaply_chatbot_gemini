"""
Script untuk membuat dummy data untuk database Supabase
"""
from database import Database
import config

def create_dummy_data():
    """Buat dummy data untuk semua table"""
    db = Database()
    
    print("Creating dummy data...")
    
    # ========== MEMBER DATA ==========
    print("Creating Members...")
    members_data = [
        {"Nama Member": "Budi Santoso", "Nomer Hp": "081234567890", "password": "budi123"},
        {"Nama Member": "Siti Nurhaliza", "Nomer Hp": "081234567891", "password": "siti123"},
        {"Nama Member": "Ahmad Fauzi", "Nomer Hp": "081234567892", "password": "ahmad123"},
        {"Nama Member": "Dewi Sartika", "Nomer Hp": "081234567893", "password": "dewi123"},
        {"Nama Member": "Rudi Hartono", "Nomer Hp": "081234567894", "password": "rudi123"},
    ]
    
    for member in members_data:
        try:
            db.supabase.table("Member").insert(member).execute()
            print(f"  ✓ Created member: {member['Nama Member']}")
        except Exception as e:
            print(f"  ✗ Error creating member {member['Nama Member']}: {e}")
    
    # ========== MENU DATA ==========
    print("\nCreating Menus...")
    
    def generate_image_url(menu_name: str) -> str:
        """Generate image URL berdasarkan nama menu"""
        # Gunakan Unsplash atau placeholder service
        # Format: https://source.unsplash.com/400x300/?{keyword}
        keywords = {
            "Sushi": "sushi",
            "Sashimi": "sashimi",
            "Ramen": "ramen",
            "Tempura": "tempura",
            "Yakitori": "yakitori",
            "Gyoza": "gyoza",
            "Edamame": "edamame",
            "Miso Soup": "miso-soup",
            "Green Tea": "green-tea",
            "Ocha": "japanese-tea",
            "Sake": "sake",
            "Matcha Ice Cream": "matcha-ice-cream",
            "Mochi": "mochi"
        }
        
        # Cari keyword yang cocok
        for key, value in keywords.items():
            if key.lower() in menu_name.lower():
                return f"https://source.unsplash.com/400x300/?{value}"
        
        # Default: gunakan nama menu
        menu_slug = menu_name.lower().replace(" ", "-")
        return f"https://source.unsplash.com/400x300/?{menu_slug}"
    
    # Menu dengan favourite (beberapa menu populer)
    favourite_menus = ["Sushi Salmon", "Ramen Shoyu", "Tempura Udang", "Sashimi Salmon", "Matcha Ice Cream"]
    
    menus_data = [
        {"Nama Menu": "Sushi Salmon", "stock": 50, "Tipe": "Sushi", "Harga": 45000, "favourite": True, "gambar": generate_image_url("Sushi Salmon")},
        {"Nama Menu": "Sushi Tuna", "stock": 45, "Tipe": "Sushi", "Harga": 42000, "favourite": False, "gambar": generate_image_url("Sushi Tuna")},
        {"Nama Menu": "Sushi Ebi", "stock": 40, "Tipe": "Sushi", "Harga": 38000, "favourite": False, "gambar": generate_image_url("Sushi Ebi")},
        {"Nama Menu": "Sashimi Salmon", "stock": 30, "Tipe": "Sashimi", "Harga": 55000, "favourite": True, "gambar": generate_image_url("Sashimi Salmon")},
        {"Nama Menu": "Sashimi Tuna", "stock": 35, "Tipe": "Sashimi", "Harga": 52000, "favourite": False, "gambar": generate_image_url("Sashimi Tuna")},
        {"Nama Menu": "Ramen Shoyu", "stock": 60, "Tipe": "Ramen", "Harga": 35000, "favourite": True, "gambar": generate_image_url("Ramen Shoyu")},
        {"Nama Menu": "Ramen Miso", "stock": 55, "Tipe": "Ramen", "Harga": 37000, "favourite": False, "gambar": generate_image_url("Ramen Miso")},
        {"Nama Menu": "Ramen Tonkotsu", "stock": 50, "Tipe": "Ramen", "Harga": 40000, "favourite": False, "gambar": generate_image_url("Ramen Tonkotsu")},
        {"Nama Menu": "Tempura Udang", "stock": 40, "Tipe": "Tempura", "Harga": 32000, "favourite": True, "gambar": generate_image_url("Tempura Udang")},
        {"Nama Menu": "Tempura Sayur", "stock": 45, "Tipe": "Tempura", "Harga": 25000, "favourite": False, "gambar": generate_image_url("Tempura Sayur")},
        {"Nama Menu": "Yakitori Ayam", "stock": 50, "Tipe": "Yakitori", "Harga": 28000, "favourite": False, "gambar": generate_image_url("Yakitori Ayam")},
        {"Nama Menu": "Yakitori Sapi", "stock": 45, "Tipe": "Yakitori", "Harga": 35000, "favourite": False, "gambar": generate_image_url("Yakitori Sapi")},
        {"Nama Menu": "Gyoza", "stock": 55, "Tipe": "Appetizer", "Harga": 30000, "favourite": False, "gambar": generate_image_url("Gyoza")},
        {"Nama Menu": "Edamame", "stock": 70, "Tipe": "Appetizer", "Harga": 20000, "favourite": False, "gambar": generate_image_url("Edamame")},
        {"Nama Menu": "Miso Soup", "stock": 80, "Tipe": "Soup", "Harga": 15000, "favourite": False, "gambar": generate_image_url("Miso Soup")},
        {"Nama Menu": "Green Tea", "stock": 100, "Tipe": "Minuman", "Harga": 10000, "favourite": False, "gambar": generate_image_url("Green Tea")},
        {"Nama Menu": "Ocha", "stock": 100, "Tipe": "Minuman", "Harga": 8000, "favourite": False, "gambar": generate_image_url("Ocha")},
        {"Nama Menu": "Sake", "stock": 30, "Tipe": "Minuman", "Harga": 75000, "favourite": False, "gambar": generate_image_url("Sake")},
        {"Nama Menu": "Matcha Ice Cream", "stock": 40, "Tipe": "Dessert", "Harga": 25000, "favourite": True, "gambar": generate_image_url("Matcha Ice Cream")},
        {"Nama Menu": "Mochi", "stock": 35, "Tipe": "Dessert", "Harga": 20000, "favourite": False, "gambar": generate_image_url("Mochi")},
    ]
    
    menu_ids = []
    for menu in menus_data:
        try:
            response = db.supabase.table("Menu").insert(menu).execute()
            if response.data:
                menu_ids.append(response.data[0]["id"])
                print(f"  ✓ Created menu: {menu['Nama Menu']} (ID: {response.data[0]['id']})")
        except Exception as e:
            print(f"  ✗ Error creating menu {menu['Nama Menu']}: {e}")
    
    # ========== PROMO DATA ==========
    print("\nCreating Promos...")
    if menu_ids:
        promos_data = [
            {"Nama Promo": "Promo Sushi Set", "Menu": menu_ids[0], "Harga Promo": 40000},  # Sushi Salmon
            {"Nama Promo": "Promo Ramen Spesial", "Menu": menu_ids[5], "Harga Promo": 30000},  # Ramen Shoyu
            {"Nama Promo": "Promo Tempura Combo", "Menu": menu_ids[8], "Harga Promo": 28000},  # Tempura Udang
            {"Nama Promo": "Promo Dessert", "Menu": menu_ids[18], "Harga Promo": 20000},  # Matcha Ice Cream
        ]
        
        for promo in promos_data:
            try:
                db.supabase.table("Promo").insert(promo).execute()
                print(f"  ✓ Created promo: {promo['Nama Promo']}")
            except Exception as e:
                print(f"  ✗ Error creating promo {promo['Nama Promo']}: {e}")
    
    # ========== BOOKING DATA ==========
    print("\nCreating Sample Bookings...")
    # Ambil member IDs
    try:
        members = db.supabase.table("Member").select("id").limit(3).execute()
        member_ids = [m["id"] for m in members.data] if members.data else []
        
        from datetime import date, timedelta
        bookings_data = [
            {
                "Id_member": member_ids[0] if member_ids else 1,
                "tanggal_kedatangan": (date.today() + timedelta(days=1)).isoformat(),
                "jam_kedatangan": "12:00",
                "jumlah_tamu": 2
            },
            {
                "Id_member": member_ids[1] if len(member_ids) > 1 else 1,
                "tanggal_kedatangan": (date.today() + timedelta(days=1)).isoformat(),
                "jam_kedatangan": "13:00",
                "jumlah_tamu": 4
            },
            {
                "Id_member": member_ids[2] if len(member_ids) > 2 else 1,
                "tanggal_kedatangan": (date.today() + timedelta(days=2)).isoformat(),
                "jam_kedatangan": "18:00",
                "jumlah_tamu": 3
            },
        ]
        
        for booking in bookings_data:
            try:
                db.supabase.table("booking").insert(booking).execute()
                print(f"  ✓ Created booking for date: {booking['tanggal_kedatangan']}")
            except Exception as e:
                print(f"  ✗ Error creating booking: {e}")
    except Exception as e:
        print(f"  ✗ Error creating bookings: {e}")
    
    print("\n✓ Dummy data creation completed!")

if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    
    # Load environment variables
    load_dotenv()
    
    # Check if .env file exists
    if not os.path.exists(".env"):
        print("❌ ERROR: File .env tidak ditemukan!")
        print("\nLangkah perbaikan:")
        print("1. Buat file .env di root project")
        print("2. Copy isi dari env.template ke .env")
        print("3. Atau rename env.template menjadi .env")
        print("\nContoh isi .env:")
        print("GEMINI_API_KEY=your_key_here")
        print("SUPABASE_URL=your_url_here")
        print("SUPABASE_KEY=your_key_here")
        exit(1)
    
    # Check if required env vars are set
    supabase_url = os.getenv("SUPABASE_URL", "")
    supabase_key = os.getenv("SUPABASE_KEY", "")
    
    if not supabase_url or not supabase_key:
        print("❌ ERROR: SUPABASE_URL atau SUPABASE_KEY tidak ditemukan di file .env!")
        print("\nPastikan file .env berisi:")
        print("SUPABASE_URL=https://your-project.supabase.co")
        print("SUPABASE_KEY=your_supabase_key")
        exit(1)
    
    try:
        create_dummy_data()
    except ValueError as e:
        print(f"❌ ERROR: {e}")
        print("\nPastikan:")
        print("1. File .env sudah diisi dengan SUPABASE_URL dan SUPABASE_KEY yang benar")
        print("2. Table di Supabase sudah dibuat dengan struktur yang benar")
        print("3. Supabase URL dan Key sudah benar (tanpa spasi di awal/akhir)")
    except Exception as e:
        print(f"❌ ERROR: {e}")
        print("\nDetail error:")
        import traceback
        traceback.print_exc()
        print("\nPastikan:")
        print("1. File .env sudah diisi dengan SUPABASE_URL dan SUPABASE_KEY")
        print("2. Table di Supabase sudah dibuat dengan struktur yang benar")
        print("3. Koneksi internet aktif")
        print("4. Supabase project masih aktif")

