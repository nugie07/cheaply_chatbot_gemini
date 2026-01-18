"""
Modul Chatbot AI untuk Restoran Cheaply
Menggunakan Gemini AI untuk pemrosesan bahasa alami
"""
import google.generativeai as genai
from typing import List, Dict, Optional
import config
from database import Database
from datetime import datetime, date, timedelta
import re

class RestaurantChatbot:
    """Chatbot untuk customer service restoran dengan Gemini AI"""
    
    def __init__(self, api_key: str, db: Database):
        """
        Inisialisasi chatbot
        
        Args:
            api_key: API key untuk Gemini AI
            db: Instance Database untuk akses data
        """
        if not api_key:
            raise ValueError("GEMINI_API_KEY tidak ditemukan. Silakan set di file .env")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(
            model_name='gemini-2.0-flash',
            generation_config={
                'temperature': config.CHATBOT_CONFIG['temperature'],
                'max_output_tokens': config.CHATBOT_CONFIG['max_tokens'],
            }
        )
        
        self.conversation_history: List[Dict[str, str]] = []
        self.system_prompt = config.get_system_prompt()
        self.enable_memory = config.CHATBOT_CONFIG['enable_memory']
        self.api_key = api_key
        self.db = db
        self.booking_data: Dict = {}  # Untuk menyimpan data booking sementara
    
    def _get_menu_context(self, query: str) -> str:
        """Ambil informasi menu berdasarkan query"""
        context = ""
        query_lower = query.lower()
        
        # Cek apakah menanyakan menu favourite
        is_favourite_query = "favourite" in query_lower or "favorit" in query_lower or "populer" in query_lower or "terlaris" in query_lower
        
        # Ambil semua menu
        menus = self.db.get_all_menus()
        
        # Filter favourite jika diminta
        if is_favourite_query:
            menus = [m for m in menus if m.get("favourite", False)]
            context += "\n\n[MENU FAVOURITE/POPULER]\n"
        
        # Cek apakah query menanyakan menu tertentu
        menu_matches = []
        for menu in menus:
            menu_name = menu.get("Nama Menu", "").lower()
            if any(word in query_lower for word in menu_name.split()):
                menu_matches.append(menu)
        
        if menu_matches:
            context += "\n\n[INFORMASI MENU YANG DITANYAKAN]\n"
            for menu in menu_matches[:3]:  # Maksimal 3 menu
                context += f"Nama: {menu.get('Nama Menu')}\n"
                context += f"Tipe: {menu.get('Tipe')}\n"
                context += f"Harga: Rp {menu.get('Harga', 0):,}\n"
                context += f"Stock: {menu.get('stock', 0)}\n"
                context += f"Status: {'Tersedia' if menu.get('stock', 0) > 0 else 'Habis'}\n"
                # Jangan tampilkan Favourite dan Gambar dalam text response
                context += "\n"
        elif "menu" in query_lower or "makanan" in query_lower or "minuman" in query_lower or is_favourite_query:
            # Jika hanya menanyakan menu secara umum atau favourite
            context += "\n\n[DAFTAR MENU]\n"
            for menu in menus[:10]:  # Tampilkan 10 menu pertama
                # Jangan tampilkan favourite mark dan gambar dalam text response
                context += f"- {menu.get('Nama Menu')} ({menu.get('Tipe')}) - Rp {menu.get('Harga', 0):,}\n"
        
        return context
    
    def _get_promo_context(self) -> str:
        """Ambil informasi promo"""
        context = ""
        promos = self.db.get_all_promos()
        
        if promos:
            context += "\n\n[PROMO YANG TERSEDIA]\n"
            for promo in promos:
                menu_info = promo.get("Menu", {})
                context += f"Nama Promo: {promo.get('Nama Promo')}\n"
                context += f"Menu: {menu_info.get('Nama Menu', 'N/A') if isinstance(menu_info, dict) else 'N/A'}\n"
                context += f"Harga Promo: Rp {promo.get('Harga Promo', 0):,}\n\n"
        
        return context
    
    def _get_booking_context(self, query: str) -> str:
        """Ambil informasi booking berdasarkan query"""
        context = ""
        query_lower = query.lower()
        
        # Deteksi tanggal dalam query (sederhana)
        from datetime import date, timedelta
        
        # Cek apakah menanyakan ketersediaan booking
        if "booking" in query_lower or "reservasi" in query_lower or "kedatangan" in query_lower:
            # Default: cek untuk hari ini dan beberapa hari ke depan
            available_times_list = []
            for day_offset in range(0, 7):
                check_date = date.today() + timedelta(days=day_offset)
                times = self.db.get_available_times(check_date)
                if times:
                    available_times_list.append({
                        "tanggal": check_date.strftime("%d/%m/%Y"),
                        "waktu": times
                    })
            
            if available_times_list:
                context += "\n\n[WAKTU KEDATANGAN YANG TERSEDIA]\n"
                for item in available_times_list[:5]:  # 5 tanggal terbaik
                    context += f"Tanggal: {item['tanggal']}\n"
                    context += f"Waktu Tersedia: {', '.join(item['waktu'])}\n\n"
        
        return context
    
    def _get_user_booking_context(self, user_id: int) -> str:
        """Ambil booking aktif user dari database"""
        context = ""
        try:
            # Ambil booking aktif (tanggal >= hari ini)
            active_bookings = self.db.get_active_bookings_by_member(user_id)
            
            if active_bookings:
                context += "\n\n[BOOKING AKTIF USER DARI DATABASE]\n"
                context += f"User memiliki {len(active_bookings)} booking aktif:\n\n"
                
                for idx, booking in enumerate(active_bookings, 1):
                    tanggal = booking.get('tanggal_kedatangan', 'N/A')
                    jam = booking.get('jam_kedatangan', 'N/A')
                    jumlah_tamu = booking.get('jumlah_tamu', 'N/A')
                    booking_id = booking.get('id', 'N/A')
                    
                    # Format tanggal untuk display
                    try:
                        if isinstance(tanggal, str):
                            date_obj = datetime.strptime(tanggal, '%Y-%m-%d').date()
                        else:
                            date_obj = tanggal
                        hari = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu'][date_obj.weekday()]
                        bulan = ['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 
                                'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember'][date_obj.month - 1]
                        tanggal_formatted = f"{hari}, {date_obj.day} {bulan} {date_obj.year}"
                    except:
                        tanggal_formatted = str(tanggal)
                    
                    context += f"Booking {idx}:\n"
                    context += f"- ID Booking: {booking_id}\n"
                    context += f"- Tanggal: {tanggal_formatted}\n"
                    context += f"- Waktu: {jam}\n"
                    context += f"- Jumlah Tamu: {jumlah_tamu} orang\n\n"
            else:
                context += "\n\n[BOOKING AKTIF USER DARI DATABASE]\n"
                context += "User TIDAK memiliki booking aktif di database.\n"
                context += "Semua booking user sudah lewat atau belum ada booking.\n\n"
        except Exception as e:
            print(f"Error getting user booking context: {e}")
            context += "\n\n[BOOKING AKTIF USER DARI DATABASE]\n"
            context += "Error mengambil data booking dari database.\n\n"
        
        return context
    
    def _get_order_history_context(self, query: str, user_id: Optional[int] = None) -> str:
        """Ambil riwayat pesanan dari database"""
        context = ""
        query_lower = query.lower()
        
        # Cek apakah menanyakan riwayat pesanan
        order_keywords = [
            "riwayat", "history", "pesanan", "order", "pemesanan",
            "pesan saya", "pesanan saya", "riwayat pesanan", "history order"
        ]
        
        if any(keyword in query_lower for keyword in order_keywords) and user_id:
            try:
                orders = self.db.get_orders_by_member(user_id)
                
                if orders:
                    context += "\n\n[RIWAYAT PESANAN DARI DATABASE]\n"
                    context += f"Total pesanan: {len(orders)}\n\n"
                    
                    # Group orders by created_at date
                    from collections import defaultdict
                    orders_by_date = defaultdict(list)
                    
                    for order in orders:
                        created_at = order.get("created_at", "")
                        menu_info = order.get("Menu", {})
                        booking_info = order.get("booking", {})
                        
                        if isinstance(menu_info, dict):
                            menu_name = menu_info.get("Nama Menu", "Unknown")
                            menu_price = menu_info.get("Harga", 0)
                        else:
                            menu_name = "Unknown"
                            menu_price = 0
                        
                        # Parse date
                        if created_at:
                            try:
                                if isinstance(created_at, str):
                                    date_part = created_at.split("T")[0] if "T" in created_at else created_at.split(" ")[0]
                                    orders_by_date[date_part].append({
                                        "menu": menu_name,
                                        "harga": menu_price,
                                        "booking": booking_info
                                    })
                            except:
                                pass
                    
                    # Format output
                    total_all = 0
                    for date_key, order_list in list(orders_by_date.items())[:5]:  # Max 5 tanggal terakhir
                        context += f"Tanggal: {date_key}\n"
                        total_date = 0
                        for item in order_list:
                            context += f"  - {item['menu']} - Rp {item['harga']:,}\n"
                            total_date += item['harga']
                        context += f"  Total: Rp {total_date:,}\n\n"
                        total_all += total_date
                    
                    if total_all > 0:
                        context += f"Total semua pesanan: Rp {total_all:,}\n"
                else:
                    context += "\n\n[RIWAYAT PESANAN DARI DATABASE]\n"
                    context += "Tidak ada riwayat pesanan di database.\n"
                    context += "PENTING: Jangan membuat data pesanan fiktif! Jika tidak ada data, katakan bahwa belum ada pesanan.\n"
            except Exception as e:
                context += f"\n\n[ERROR MENGAMBIL RIWAYAT PESANAN]\nError: {str(e)}\n"
        elif any(keyword in query_lower for keyword in order_keywords) and not user_id:
            context += "\n\n[RIWAYAT PESANAN]\n"
            context += "User belum login. Untuk melihat riwayat pesanan, user perlu login terlebih dahulu.\n"
        
        return context
    
    def _get_context_info(self, query: str, user_id: Optional[int] = None) -> str:
        """
        Ambil informasi konteks tambahan berdasarkan query
        
        Args:
            query: Query dari pengguna
            user_id: ID user yang login (optional)
            
        Returns:
            String dengan informasi konteks tambahan
        """
        context = ""
        
        # Tambahkan informasi menu
        context += self._get_menu_context(query)
        
        # Tambahkan informasi promo jika ditanyakan
        query_lower = query.lower()
        if "promo" in query_lower or "diskon" in query_lower or "harga" in query_lower:
            context += self._get_promo_context()
        
        # Tambahkan informasi booking
        context += self._get_booking_context(query)
        
        # Tambahkan booking aktif user jika ditanyakan dan user sudah login
        booking_query_keywords = [
            "booking", "reservasi", "aktif", "ada booking", "booking saya", 
            "reservasi saya", "booking aktif", "ada reservasi", "punya booking"
        ]
        if user_id and any(keyword in query_lower for keyword in booking_query_keywords):
            context += self._get_user_booking_context(user_id)
        
        # Tambahkan riwayat pesanan jika ditanyakan
        context += self._get_order_history_context(query, user_id)
        
        return context
    
    def get_response(self, user_message: str, user_info: Optional[Dict] = None) -> str:
        """
        Dapatkan respons dari chatbot
        
        Args:
            user_message: Pesan dari pengguna
            user_info: Informasi user yang login (optional)
            
        Returns:
            Respons dari chatbot
        """
        # Ambil user_id jika user sudah login
        user_id = user_info.get("id") if user_info else None
        
        # Tambahkan konteks informasi menu/promo/booking/order history jika relevan
        context_info = self._get_context_info(user_message, user_id)
        
        # Tambahkan informasi user jika sudah login, atau informasi guest mode
        user_context = ""
        if user_info:
            user_name = user_info.get("Nama Member", "User")
            user_context = f"\n\n[INFORMASI USER]\n"
            user_context += f"User sudah LOGIN sebagai member.\n"
            user_context += f"Nama Member: {user_name}\n"
            user_context += f"ID Member: {user_info.get('id', 'N/A')}\n"
            user_context += f"PENTING: User SUDAH LOGIN, jadi TIDAK perlu menanyakan apakah sudah login.\n"
            user_context += f"User BISA melakukan booking dan order.\n"
            user_context += f"Gunakan nama '{user_name}' dalam percakapan untuk personalisasi.\n"
            user_context += f"Contoh: 'Halo {user_name}', 'Baik {user_name}', dll.\n"
        else:
            # Guest mode
            user_context = f"\n\n[INFORMASI USER]\n"
            user_context += f"User sedang dalam MODE GUEST (tidak login).\n"
            user_context += f"PENTING: User GUEST MODE TIDAK BISA melakukan booking atau order.\n"
            user_context += f"Jika user meminta booking atau reservasi, WAJIB arahkan untuk login terlebih dahulu.\n"
            user_context += f"User guest mode HANYA bisa:\n"
            user_context += f"- Menanyakan tentang menu dan harga\n"
            user_context += f"- Menanyakan tentang promo\n"
            user_context += f"- Menanyakan ketersediaan booking (hanya informasi, tidak bisa booking)\n"
            user_context += f"- Melihat rekomendasi waktu yang tersedia\n"
            user_context += f"JANGAN memproses booking atau order untuk guest mode. WAJIB minta login dulu.\n"
        
        # Buat prompt lengkap
        full_prompt = self.system_prompt + context_info + user_context
        
        # Tambahkan history percakapan jika memory diaktifkan
        if self.enable_memory and self.conversation_history:
            conversation_text = "\n".join([
                f"User: {msg['user']}\nAssistant: {msg['assistant']}"
                for msg in self.conversation_history[-5:]  # Ambil 5 percakapan terakhir
            ])
            full_prompt += f"\n\n[RIWAYAT PERCAKAPAN]\n{conversation_text}\n\n"
        
        full_prompt += f"\n\nUser: {user_message}\nAssistant:"
        
        try:
            # Generate response dari Gemini
            response = self.model.generate_content(full_prompt)
            bot_response = response.text.strip()
            
            # Simpan ke history
            if self.enable_memory:
                self.conversation_history.append({
                    'user': user_message,
                    'assistant': bot_response
                })
                # Batasi history maksimal 10 percakapan
                if len(self.conversation_history) > 10:
                    self.conversation_history = self.conversation_history[-10:]
            
            return bot_response
            
        except Exception as e:
            return f"Maaf, terjadi kesalahan: {str(e)}. Silakan coba lagi."
    
    def get_available_times_recommendations(self, tanggal_str: str = None) -> List[Dict]:
        """
        Dapatkan rekomendasi waktu kedatangan yang tersedia
        
        Args:
            tanggal_str: Tanggal dalam format YYYY-MM-DD (optional)
            
        Returns:
            List rekomendasi waktu dengan format [{"tanggal": "...", "waktu": [...]}]
        """
        from datetime import date, timedelta
        
        recommendations = []
        
        if tanggal_str:
            try:
                check_date = date.fromisoformat(tanggal_str)
                times = self.db.get_available_times(check_date)
                if times:
                    recommendations.append({
                        "tanggal": check_date.strftime("%d/%m/%Y"),
                        "waktu": times
                    })
            except:
                pass
        else:
            # Cek untuk 7 hari ke depan
            for day_offset in range(0, 7):
                check_date = date.today() + timedelta(days=day_offset)
                times = self.db.get_available_times(check_date)
                if times:
                    recommendations.append({
                        "tanggal": check_date.strftime("%d/%m/%Y"),
                        "waktu": times
                    })
                    if len(recommendations) >= 5:
                        break
        
        return recommendations
    
    def clear_history(self):
        """Hapus riwayat percakapan"""
        self.conversation_history = []
        self.booking_data = {}
    
    def extract_booking_info(self, user_message: str) -> Dict:
        """
        Extract informasi booking dari pesan user
        Returns dict dengan keys: tanggal, jam, jumlah_tamu, menu_items
        """
        info = {}
        message_lower = user_message.lower()
        
        # Mapping nama bulan Indonesia ke angka
        bulan_map = {
            'januari': 1, 'februari': 2, 'maret': 3, 'april': 4,
            'mei': 5, 'juni': 6, 'juli': 7, 'agustus': 8,
            'september': 9, 'oktober': 10, 'november': 11, 'desember': 12
        }
        
        # Extract tanggal
        # Format: "besok", "lusa", "tanggal 25", "25 desember", "sabtu minggu depan", dll
        today = date.today()
        current_weekday = today.weekday()  # 0=Monday, 6=Sunday
        
        # Mapping hari Indonesia ke weekday number
        hari_map = {
            'senin': 0, 'selasa': 1, 'rabu': 2, 'kamis': 3,
            'jumat': 4, 'sabtu': 5, 'minggu': 6
        }
        
        if "besok" in message_lower or "tomorrow" in message_lower:
            info['tanggal'] = (today + timedelta(days=1)).isoformat()
        elif "lusa" in message_lower:
            info['tanggal'] = (today + timedelta(days=2)).isoformat()
        elif "minggu depan" in message_lower or "next week" in message_lower:
            # Cari hari dalam minggu depan (contoh: "sabtu minggu depan")
            for hari_nama, hari_num in hari_map.items():
                if hari_nama in message_lower:
                    # Hitung hari target di minggu depan
                    days_ahead = (hari_num - current_weekday + 7) % 7
                    if days_ahead == 0:  # Jika hari ini, tambah 7 hari
                        days_ahead = 7
                    else:
                        days_ahead += 7  # Minggu depan
                    info['tanggal'] = (today + timedelta(days=days_ahead)).isoformat()
                    break
            # Jika tidak ada hari spesifik, default ke 7 hari lagi
            if 'tanggal' not in info:
                info['tanggal'] = (today + timedelta(days=7)).isoformat()
        elif "minggu ini" in message_lower or "this week" in message_lower:
            # Cari hari dalam minggu ini
            for hari_nama, hari_num in hari_map.items():
                if hari_nama in message_lower:
                    days_ahead = (hari_num - current_weekday) % 7
                    if days_ahead == 0:  # Hari ini
                        days_ahead = 0
                    info['tanggal'] = (today + timedelta(days=days_ahead)).isoformat()
                    break
        else:
            # Cari pola tanggal dengan format DD/MM/YYYY atau DD-MM-YYYY
            date_pattern_ddmm = r'(\d{1,2})[/-](\d{1,2})[/-](\d{2,4})'
            match = re.search(date_pattern_ddmm, message_lower)
            if match:
                try:
                    day, month, year = match.groups()
                    if len(year) == 2:
                        year = "20" + year
                    info['tanggal'] = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
                except:
                    pass
            
            # Jika belum ketemu, cari pola tanggal dengan nama bulan
            if 'tanggal' not in info:
                # Pattern untuk: "19 januari 2026" atau "tanggal 19 januari 2026" atau "hari senin tanggal 19 januari 2026"
                # Pattern ini lebih fleksibel, bisa menangkap dengan atau tanpa kata "tanggal" di depannya
                date_pattern_nama_bulan = r'(?:tanggal\s+)?(\d{1,2})\s+(januari|februari|maret|april|mei|juni|juli|agustus|september|oktober|november|desember)(?:\s+(\d{4}))?'
                match = re.search(date_pattern_nama_bulan, message_lower)
                if match:
                    try:
                        day = int(match.group(1))
                        bulan_nama = match.group(2)
                        month = bulan_map.get(bulan_nama, 1)
                        year = match.group(3) if match.group(3) else str(today.year)
                        info['tanggal'] = f"{year}-{month:02d}-{day:02d}"
                    except Exception as e:
                        print(f"Error parsing date: {e}")
                        pass
        
        # Extract jam
        time_pattern = r'(\d{1,2})[:.](\d{2})|(\d{1,2})\s*(pagi|siang|sore|malam)'
        time_match = re.search(time_pattern, message_lower)
        if time_match:
            if time_match.group(1) and time_match.group(2):
                hour = int(time_match.group(1))
                minute = int(time_match.group(2))
                info['jam'] = f"{hour:02d}:{minute:02d}"
            elif time_match.group(3):
                hour = int(time_match.group(3))
                if "pagi" in message_lower:
                    info['jam'] = f"{hour:02d}:00"
                elif "siang" in message_lower:
                    info['jam'] = f"{hour+12 if hour < 12 else hour:02d}:00"
                elif "sore" in message_lower or "malam" in message_lower:
                    info['jam'] = f"{hour+12 if hour < 12 else hour:02d}:00"
        
        # Extract jumlah tamu
        jumlah_patterns = [
            r'(\d+)\s*(orang|tamu|person)',
            r'untuk\s*(\d+)',
            r'(\d+)\s*orang',
        ]
        for pattern in jumlah_patterns:
            match = re.search(pattern, message_lower)
            if match:
                info['jumlah_tamu'] = int(match.group(1))
                break
        
        # Extract menu items (untuk disimpan ke order)
        # Cari menu yang disebutkan dalam pesan
        menu_items = []
        all_menus = self.db.get_all_menus()
        message_words = set(message_lower.split())
        
        # Kata kunci umum yang tidak perlu di-match langsung
        stop_words = {"menu", "yang", "akan", "saya", "mau", "order", "pesan", "dipesan", "masing", "masing2"}
        message_keywords = [w for w in message_words if w not in stop_words and len(w) > 2]
        
        for menu in all_menus:
            menu_name = menu.get("Nama Menu", "").lower()
            menu_words = set(menu_name.split())
            
            # Cek apakah ada kata kunci menu yang match
            # Prioritas: exact match atau sebagian besar kata match
            matched_words = menu_words.intersection(message_keywords)
            if matched_words and len(matched_words) >= 1:
                # Jika match minimal 1 kata penting, tambahkan
                menu_items.append({
                    "menu_id": menu.get("id"),
                    "menu_name": menu.get("Nama Menu")
                })
            elif menu_name in message_lower:
                # Exact match nama menu
                menu_items.append({
                    "menu_id": menu.get("id"),
                    "menu_name": menu.get("Nama Menu")
                })
        
        if menu_items:
            info['menu_items'] = menu_items
        
        return info
    
    def process_booking(self, user_message: str, user_id: int) -> tuple[Optional[Dict], str]:
        """
        Process booking dari conversation
        Returns (booking dict jika sudah lengkap, message untuk user)
        """
        # Extract info dari pesan
        new_info = self.extract_booking_info(user_message)
        self.booking_data.update(new_info)
        
        # Debug: print extracted info
        if new_info:
            print(f"DEBUG: Extracted booking info: {new_info}")
        print(f"DEBUG: Current booking_data: {self.booking_data}")
        
        # Cek apakah semua info sudah lengkap
        required = ['tanggal', 'jam', 'jumlah_tamu']
        missing = [field for field in required if field not in self.booking_data]
        
        if not missing:
            # Semua info lengkap, buat booking
            try:
                booking_date = date.fromisoformat(self.booking_data['tanggal'])
                booking = self.db.create_booking(
                    user_id,
                    booking_date,
                    self.booking_data['jam'],
                    self.booking_data['jumlah_tamu']
                )
                if booking:
                    # Simpan menu items ke order jika ada
                    menu_items = self.booking_data.get('menu_items', [])
                    saved_menu_names = []
                    if menu_items:
                        order_items = [{"menu_id": item.get("menu_id")} for item in menu_items if item.get("menu_id")]
                        if order_items:
                            orders = self.db.create_order(
                                user_id,
                                booking.get("id"),
                                order_items
                            )
                            # Ambil nama menu yang berhasil disimpan
                            if orders:
                                for order in orders:
                                    menu_id = order.get("menu")
                                    if menu_id:
                                        # Ambil nama menu dari database
                                        all_menus = self.db.get_all_menus()
                                        for menu in all_menus:
                                            if menu.get("id") == menu_id:
                                                saved_menu_names.append(menu.get("Nama Menu", "Unknown"))
                                                break
                    
                    # Simpan menu names ke booking untuk ditampilkan
                    booking['saved_menu_names'] = saved_menu_names
                    
                    # Reset booking data
                    booking_info = self.booking_data.copy()
                    self.booking_data = {}
                    return booking, "Booking berhasil dibuat!"
            except Exception as e:
                return None, f"Error: {str(e)}"
        
        # Masih kurang info, buat message untuk menanyakan
        missing_questions = {
            'tanggal': "Kapan Anda ingin datang? (contoh: besok, lusa, atau tanggal tertentu)",
            'jam': "Jam berapa Anda ingin datang? (contoh: 12:00, 18:00)",
            'jumlah_tamu': "Untuk berapa orang?"
        }
        
        questions = [missing_questions[field] for field in missing]
        message = "Untuk menyelesaikan booking, saya perlu informasi berikut:\n" + "\n".join([f"- {q}" for q in questions])
        
        return None, message

