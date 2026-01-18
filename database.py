"""
Module untuk koneksi dan operasi database Supabase
"""
import os

# Disable proxy environment variables SEBELUM import supabase
proxy_vars = ['HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy', 'ALL_PROXY', 'all_proxy']
for var in proxy_vars:
    os.environ.pop(var, None)

# Import setelah disable proxy
from supabase import create_client, Client
import config
from typing import List, Dict, Optional
from datetime import datetime, date, time

class Database:
    """Class untuk mengelola koneksi dan operasi database Supabase"""
    
    def __init__(self):
        """Inisialisasi koneksi ke Supabase"""
        if not config.SUPABASE_URL or not config.SUPABASE_KEY:
            raise ValueError(
                "SUPABASE_URL dan SUPABASE_KEY harus diatur di file .env\n"
                "Pastikan file .env ada di root project dan berisi:\n"
                "SUPABASE_URL=https://your-project.supabase.co\n"
                "SUPABASE_KEY=your_supabase_key"
            )
        
        # Strip whitespace dari URL dan Key
        supabase_url = config.SUPABASE_URL.strip()
        supabase_key = config.SUPABASE_KEY.strip()
        
        try:
            # Pastikan proxy vars sudah dihapus (sudah dilakukan di level module)
            for var in proxy_vars:
                os.environ.pop(var, None)
            
            # Create client - tidak pass proxy parameter
            self.supabase: Client = create_client(supabase_url, supabase_key)
            # Test connection dengan query sederhana
            self.supabase.table("Member").select("id").limit(1).execute()
        except Exception as e:
            error_msg = str(e)
            if "Invalid API key" in error_msg or "invalid" in error_msg.lower():
                raise ValueError(
                    f"❌ Invalid Supabase API Key!\n"
                    f"Error: {error_msg}\n\n"
                    f"Pastikan:\n"
                    f"1. SUPABASE_KEY di file .env sudah benar\n"
                    f"2. Key adalah 'anon' atau 'service_role' key dari Supabase Dashboard\n"
                    f"3. Tidak ada spasi atau karakter aneh di awal/akhir key\n"
                    f"4. Key masih aktif dan tidak expired"
                )
            elif "Failed to connect" in error_msg or "connection" in error_msg.lower():
                raise ValueError(
                    f"❌ Gagal terhubung ke Supabase!\n"
                    f"Error: {error_msg}\n\n"
                    f"Pastikan:\n"
                    f"1. SUPABASE_URL di file .env sudah benar\n"
                    f"2. Koneksi internet aktif\n"
                    f"3. Supabase project masih aktif"
                )
            else:
                raise ValueError(
                    f"❌ Error koneksi ke Supabase: {error_msg}\n\n"
                    f"Pastikan:\n"
                    f"1. SUPABASE_URL dan SUPABASE_KEY sudah benar\n"
                    f"2. Table sudah dibuat di Supabase\n"
                    f"3. Koneksi internet aktif"
                )
    
    # ========== MENU OPERATIONS ==========
    def get_all_menus(self) -> List[Dict]:
        """Ambil semua menu"""
        try:
            response = self.supabase.table("Menu").select("*").execute()
            return response.data if response.data else []
        except Exception as e:
            print(f"Error getting menus: {e}")
            return []
    
    def get_menu_by_id(self, menu_id: int) -> Optional[Dict]:
        """Ambil menu berdasarkan ID"""
        try:
            response = self.supabase.table("Menu").select("*").eq("id", menu_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error getting menu: {e}")
            return None
    
    def get_menu_by_name(self, nama: str) -> Optional[Dict]:
        """Ambil menu berdasarkan nama"""
        try:
            response = self.supabase.table("Menu").select("*").ilike("Nama Menu", f"%{nama}%").execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error getting menu by name: {e}")
            return None
    
    def get_menus_by_tipe(self, tipe: str) -> List[Dict]:
        """Ambil menu berdasarkan tipe"""
        try:
            response = self.supabase.table("Menu").select("*").eq("Tipe", tipe).execute()
            return response.data if response.data else []
        except Exception as e:
            print(f"Error getting menus by type: {e}")
            return []
    
    def get_favourite_menus(self) -> List[Dict]:
        """Ambil menu yang favourite"""
        try:
            response = self.supabase.table("Menu").select("*").eq("favourite", True).execute()
            return response.data if response.data else []
        except Exception as e:
            print(f"Error getting favourite menus: {e}")
            return []
    
    def update_menu_stock(self, menu_id: int, new_stock: int) -> bool:
        """Update stock menu"""
        try:
            self.supabase.table("Menu").update({"stock": new_stock}).eq("id", menu_id).execute()
            return True
        except Exception as e:
            print(f"Error updating menu stock: {e}")
            return False
    
    # ========== PROMO OPERATIONS ==========
    def get_all_promos(self) -> List[Dict]:
        """Ambil semua promo"""
        try:
            response = self.supabase.table("Promo").select("*, Menu(*)").execute()
            return response.data if response.data else []
        except Exception as e:
            print(f"Error getting promos: {e}")
            return []
    
    def get_promo_by_id(self, promo_id: int) -> Optional[Dict]:
        """Ambil promo berdasarkan ID"""
        try:
            response = self.supabase.table("Promo").select("*, Menu(*)").eq("id", promo_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error getting promo: {e}")
            return None
    
    # ========== MEMBER OPERATIONS ==========
    def get_member_by_phone(self, nomer_hp: str) -> Optional[Dict]:
        """Ambil member berdasarkan nomor HP"""
        try:
            response = self.supabase.table("Member").select("*").eq("Nomer Hp", nomer_hp).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error getting member: {e}")
            return None
    
    def verify_member(self, nomer_hp: str, password: str) -> Optional[Dict]:
        """Verifikasi member dengan nomor HP dan password"""
        try:
            member = self.get_member_by_phone(nomer_hp)
            if member and member.get("password") == password:
                return member
            return None
        except Exception as e:
            print(f"Error verifying member: {e}")
            return None
    
    def create_member(self, nama: str, nomer_hp: str, password: str) -> Optional[Dict]:
        """Buat member baru"""
        try:
            response = self.supabase.table("Member").insert({
                "Nama Member": nama,
                "Nomer Hp": nomer_hp,
                "password": password
            }).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error creating member: {e}")
            return None
    
    # ========== BOOKING OPERATIONS ==========
    def get_bookings_by_date(self, tanggal: date) -> List[Dict]:
        """Ambil semua booking untuk tanggal tertentu"""
        try:
            tanggal_str = tanggal.isoformat()
            response = self.supabase.table("booking").select("*").eq("tanggal_kedatangan", tanggal_str).execute()
            return response.data if response.data else []
        except Exception as e:
            print(f"Error getting bookings: {e}")
            return []
    
    def get_available_times(self, tanggal: date, jumlah_tamu: int = 1) -> List[str]:
        """Dapatkan waktu yang tersedia untuk tanggal tertentu"""
        try:
            bookings = self.get_bookings_by_date(tanggal)
            
            # Waktu operasional (11:00 - 22:00, setiap jam)
            all_times = [f"{hour:02d}:00" for hour in range(11, 23)]
            
            # Hitung kapasitas per waktu (asumsi maksimal 50 tamu per waktu)
            max_capacity = 50
            time_capacity = {time: 0 for time in all_times}
            
            for booking in bookings:
                jam = booking.get("jam_kedatangan", "")
                jumlah = booking.get("jumlah_tamu", 0)
                if jam in time_capacity:
                    time_capacity[jam] += jumlah
            
            # Filter waktu yang masih tersedia
            available_times = [
                time for time, capacity in time_capacity.items()
                if capacity + jumlah_tamu <= max_capacity
            ]
            
            return available_times[:5]  # Return 5 waktu terbaik
        except Exception as e:
            print(f"Error getting available times: {e}")
            return []
    
    def get_bookings_by_member(self, id_member: int) -> List[Dict]:
        """Ambil semua booking untuk member tertentu"""
        try:
            response = self.supabase.table("booking").select("*").eq("Id_member", id_member).order("tanggal_kedatangan", desc=False).execute()
            return response.data if response.data else []
        except Exception as e:
            print(f"Error getting bookings by member: {e}")
            return []
    
    def get_active_bookings_by_member(self, id_member: int) -> List[Dict]:
        """Ambil booking aktif (tanggal >= hari ini) untuk member tertentu"""
        try:
            today = date.today().isoformat()
            response = self.supabase.table("booking").select("*").eq("Id_member", id_member).gte("tanggal_kedatangan", today).order("tanggal_kedatangan", desc=False).execute()
            return response.data if response.data else []
        except Exception as e:
            print(f"Error getting active bookings by member: {e}")
            return []
    
    def create_booking(self, id_member: int, tanggal_kedatangan: date, jam_kedatangan: str, jumlah_tamu: int) -> Optional[Dict]:
        """Buat booking baru"""
        try:
            response = self.supabase.table("booking").insert({
                "Id_member": id_member,
                "tanggal_kedatangan": tanggal_kedatangan.isoformat(),
                "jam_kedatangan": jam_kedatangan,
                "jumlah_tamu": jumlah_tamu
            }).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error creating booking: {e}")
            return None
    
    # ========== ORDER OPERATIONS ==========
    def create_order(self, id_member: int, id_booking: Optional[int], menu_items: List[Dict]) -> Optional[List[Dict]]:
        """Buat order baru dengan multiple menu items"""
        try:
            # Buat order untuk setiap menu item
            orders = []
            for item in menu_items:
                order_data = {
                    "id_member": id_member,
                    "id_booking": id_booking if id_booking else None,
                    "menu": item.get("menu_id")
                }
                response = self.supabase.table("Order").insert(order_data).execute()
                if response.data:
                    orders.append(response.data[0])
            
            return orders if orders else None
        except Exception as e:
            print(f"Error creating order: {e}")
            return None
    
    def get_orders_by_member(self, id_member: int) -> List[Dict]:
        """Ambil semua order dari member"""
        try:
            response = self.supabase.table("Order").select("*, Menu(*), booking(*)").eq("id_member", id_member).execute()
            return response.data if response.data else []
        except Exception as e:
            print(f"Error getting orders: {e}")
            return []

