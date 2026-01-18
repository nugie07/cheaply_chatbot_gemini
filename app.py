"""
Aplikasi Streamlit untuk Chatbot AI Restoran Cheaply
"""
import streamlit as st
import os
from dotenv import load_dotenv
from chatbot import RestaurantChatbot
from database import Database
import config
from datetime import date, datetime, timedelta
import json

# Load environment variables
load_dotenv()

# Konfigurasi halaman
st.set_page_config(
    page_title="Cheaply - Restoran All You Can Eat Jepang",
    page_icon="🍱",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Bootstrap CSS
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Google+Sans:wght@400;500;700&family=Roboto:wght@300;400;500;700&display=swap" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <style>
        /* Force Light Mode */
        :root {
            --background-color: #ffffff;
            --text-color: #202124;
        }
        .stApp {
            background-color: #ffffff !important;
            font-family: 'Google Sans', 'Roboto', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
        }
        .main {
            background-color: #ffffff !important;
        }
        [data-testid="stAppViewContainer"] {
            background-color: #ffffff !important;
        }
        @media (prefers-color-scheme: dark) {
            .stApp {
                background-color: #ffffff !important;
            }
            .main {
                background-color: #ffffff !important;
            }
        }
        
        /* Typography - Gemini Style */
        * {
            font-family: 'Google Sans', 'Roboto', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        }
        
        .main-header {
            font-size: 3rem;
            font-weight: 500;
            color: #202124;
            text-align: center;
            margin-bottom: 1rem;
            font-family: 'Google Sans', 'Roboto', sans-serif;
        }
        .sub-header {
            font-size: 1.2rem;
            color: #5f6368;
            text-align: center;
            margin-bottom: 2rem;
            font-weight: 400;
        }
        .welcome-container {
            background: linear-gradient(135deg, #4285f4 0%, #34a853 100%);
            padding: 3rem;
            border-radius: 1rem;
            color: white;
            text-align: center;
            margin-bottom: 2rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        .welcome-title {
            font-size: 2.5rem;
            font-weight: 500;
            margin-bottom: 1rem;
        }
        .welcome-subtitle {
            font-size: 1.2rem;
            margin-bottom: 2rem;
            font-weight: 400;
        }
        .btn-custom {
            padding: 0.75rem 2rem;
            font-size: 1rem;
            border-radius: 24px;
            margin: 0.5rem;
            border: none;
            cursor: pointer;
            transition: all 0.2s;
            font-weight: 500;
        }
        .btn-primary-custom {
            background-color: #4285f4;
            color: white;
        }
        .btn-primary-custom:hover {
            background-color: #3367d6;
            transform: translateY(-1px);
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        }
        .btn-secondary-custom {
            background-color: white;
            color: #4285f4;
            border: 1px solid #dadce0;
        }
        .btn-secondary-custom:hover {
            background-color: #f8f9fa;
            transform: translateY(-1px);
        }
        
        /* Chat Messages - Gemini Style */
        .chat-container {
            background-color: #ffffff;
            border-radius: 0;
            padding: 1rem 1.5rem;
            margin-bottom: 1rem;
            max-height: 600px;
            overflow-y: auto;
        }
        .chat-message {
            padding: 14px 18px;
            border-radius: 18px;
            margin-bottom: 12px;
            display: inline-block;
            max-width: 70%;
            min-width: 120px;
            word-wrap: break-word;
            word-break: break-word;
            overflow-wrap: break-word;
            box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24);
            line-height: 1.6;
            font-size: 15px;
            white-space: normal;
        }
        .user-message {
            background-color: #4285f4;
            color: #ffffff;
            margin-left: auto;
            margin-right: 0;
            text-align: left;
            border-bottom-right-radius: 4px;
            float: right;
            clear: both;
        }
        .user-message strong {
            color: #ffffff;
            font-weight: 500;
            font-size: 13px;
            opacity: 0.95;
            display: block;
            margin-bottom: 8px;
            letter-spacing: 0.3px;
        }
        .user-message div {
            word-wrap: break-word;
            word-break: break-word;
            overflow-wrap: break-word;
            white-space: pre-wrap;
        }
        .bot-message {
            background-color: #f1f3f4;
            color: #202124;
            margin-right: auto;
            margin-left: 0;
            border: none;
            border-bottom-left-radius: 4px;
            float: left;
            clear: both;
        }
        .bot-message strong {
            color: #202124;
            font-weight: 500;
            font-size: 13px;
            margin-bottom: 8px;
            display: block;
            letter-spacing: 0.3px;
        }
        .bot-message div {
            word-wrap: break-word;
            word-break: break-word;
            overflow-wrap: break-word;
            white-space: pre-wrap;
        }
        .bot-message p {
            color: #202124;
            margin: 0;
            word-wrap: break-word;
            word-break: break-word;
        }
        
        /* Clear float untuk chat container */
        .chat-container::after {
            content: "";
            display: table;
            clear: both;
        }
        
        /* Login Form */
        .login-form {
            background-color: white;
            padding: 2rem;
            border-radius: 8px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24);
            max-width: 400px;
            margin: 0 auto;
        }
        
        /* Fix judul Login - hitam */
        h3 {
            color: #202124 !important;
        }
        .login-form h3,
        form h3 {
            color: #202124 !important;
        }
        
        /* Fix text input - background putih, font hitam */
        [data-testid="stTextInput"] input,
        [data-testid="stTextInput"] textarea,
        input[type="text"],
        input[type="password"] {
            background-color: #ffffff !important;
            color: #202124 !important;
            border: 1px solid #dadce0 !important;
            border-radius: 8px !important;
            padding: 0.75rem !important;
        }
        [data-testid="stTextInput"] input::placeholder,
        [data-testid="stTextInput"] textarea::placeholder,
        input[type="text"]::placeholder,
        input[type="password"]::placeholder {
            color: #5f6368 !important;
            opacity: 1 !important;
        }
        [data-testid="stTextInput"] input:focus,
        [data-testid="stTextInput"] textarea:focus,
        input[type="text"]:focus,
        input[type="password"]:focus {
            border-color: #4285f4 !important;
            box-shadow: 0 0 0 2px rgba(66, 133, 244, 0.2) !important;
            outline: none !important;
        }
        
        /* Fix label text input - hitam */
        [data-testid="stTextInput"] label,
        label[data-testid="stTextInputLabel"],
        .stTextInput label,
        label[for*="text_input"] {
            color: #202124 !important;
            font-weight: 500 !important;
        }
        
        /* Fix semua text di form - hitam */
        form h3,
        form p,
        form label,
        form div,
        .stForm h3,
        .stForm label {
            color: #202124 !important;
        }
        
        /* Fix untuk semua input di form */
        .stForm input[type="text"],
        .stForm input[type="password"],
        form input[type="text"],
        form input[type="password"] {
            background-color: #ffffff !important;
            color: #202124 !important;
            -webkit-text-fill-color: #202124 !important;
            border: 1px solid #dadce0 !important;
        }
        
        .stButton>button {
            width: 100%;
            background-color: #4285f4;
            color: white;
            font-weight: 500;
            border-radius: 24px;
            padding: 0.75rem;
            border: none;
            font-size: 15px;
        }
        .stButton>button:hover {
            background-color: #3367d6;
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        }
        .info-box {
            background-color: #e8f0fe;
            padding: 1rem;
            border-radius: 8px;
            border-left: 4px solid #4285f4;
            margin: 1rem 0;
            color: #1967d2;
        }
        .success-box {
            background-color: #e6f4ea;
            padding: 1rem;
            border-radius: 8px;
            border-left: 4px solid #34a853;
            margin: 1rem 0;
            color: #137333;
        }
        
        /* Fix warna teks untuk st.info (recommendations) */
        [data-testid="stInfo"],
        [data-testid="stInfo"] > div,
        [data-testid="stInfo"] p,
        [data-testid="stInfo"] span,
        [data-testid="stInfo"] * {
            color: #202124 !important;
            -webkit-text-fill-color: #202124 !important;
        }
        
        /* Fix untuk semua elemen di dalam info box Streamlit */
        div[data-baseweb="notification"],
        div[data-baseweb="notification"] *,
        .stAlert,
        .stAlert *,
        .element-container [data-testid="stInfo"],
        .element-container [data-testid="stInfo"] * {
            color: #202124 !important;
            -webkit-text-fill-color: #202124 !important;
        }
        
        /* Input Chat - Gemini Style */
        [data-testid="stChatInput"] {
            background-color: #ffffff !important;
            border: 1px solid #dadce0 !important;
            border-radius: 24px !important;
            padding: 12px 16px !important;
        }
        [data-testid="stChatInput"]:focus {
            border-color: #4285f4 !important;
            box-shadow: 0 0 0 2px rgba(66, 133, 244, 0.2) !important;
        }
        
        /* Fix warna teks di input chat - semua elemen input */
        [data-testid="stChatInput"] input,
        [data-testid="stChatInput"] textarea,
        [data-testid="stChatInput"] input[type="text"],
        [data-testid="stChatInput"] * input,
        [data-testid="stChatInput"] * textarea {
            color: #202124 !important;
            background-color: #ffffff !important;
        }
        [data-testid="stChatInput"] input::placeholder,
        [data-testid="stChatInput"] textarea::placeholder,
        [data-testid="stChatInput"] input::input-placeholder,
        [data-testid="stChatInput"] textarea::input-placeholder {
            color: #5f6368 !important;
            opacity: 1 !important;
        }
        
        /* Fix untuk Streamlit chat input - semua variasi */
        .stChatInput input,
        .stChatInput textarea,
        .stChatInput * input,
        .stChatInput * textarea,
        div[data-testid="stChatInput"] input,
        div[data-testid="stChatInput"] textarea {
            color: #202124 !important;
            background-color: #ffffff !important;
        }
        .stChatInput input::placeholder,
        .stChatInput textarea::placeholder,
        div[data-testid="stChatInput"] input::placeholder,
        div[data-testid="stChatInput"] textarea::placeholder {
            color: #5f6368 !important;
            opacity: 1 !important;
        }
        
        /* Fix untuk semua input di dalam chat input container */
        [data-testid="stChatInput"] * {
            color: #202124 !important;
        }
        [data-testid="stChatInput"] input[type="text"]:not([readonly]),
        [data-testid="stChatInput"] textarea:not([readonly]) {
            color: #202124 !important;
            -webkit-text-fill-color: #202124 !important;
        }
        
        /* Scrollbar */
        .chat-container::-webkit-scrollbar {
            width: 8px;
        }
        .chat-container::-webkit-scrollbar-track {
            background: #f1f1f1;
        }
        .chat-container::-webkit-scrollbar-thumb {
            background: #dadce0;
            border-radius: 4px;
        }
        .chat-container::-webkit-scrollbar-thumb:hover {
            background: #bdc1c6;
        }
    </style>
""", unsafe_allow_html=True)

# Inisialisasi session state
if 'initialized' not in st.session_state:
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            st.session_state.initialized = False
            st.session_state.error = "GEMINI_API_KEY tidak ditemukan"
        else:
            db = Database()
            st.session_state.db = db
            st.session_state.chatbot = RestaurantChatbot(api_key, db)
            st.session_state.initialized = True
    except Exception as e:
        st.session_state.initialized = False
        st.session_state.error = str(e)

if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'user_logged_in' not in st.session_state:
    st.session_state.user_logged_in = False

if 'current_user' not in st.session_state:
    st.session_state.current_user = None

if 'view_as_guest' not in st.session_state:
    st.session_state.view_as_guest = False

if 'current_booking' not in st.session_state:
    st.session_state.current_booking = None

if 'current_orders' not in st.session_state:
    st.session_state.current_orders = []

if 'show_confirmation' not in st.session_state:
    st.session_state.show_confirmation = False

if 'greeting_shown' not in st.session_state:
    st.session_state.greeting_shown = False

# Cek inisialisasi
if not st.session_state.initialized:
    st.error(f"❌ Error: {st.session_state.get('error', 'Unknown error')}")
    st.info("""
    **Cara Setup:**
    1. Buat file `.env` di root project
    2. Tambahkan:
       - `GEMINI_API_KEY=your_gemini_api_key_here`
       - `SUPABASE_URL=your_supabase_url_here`
       - `SUPABASE_KEY=your_supabase_key_here`
    3. Dapatkan API key dari: https://makersuite.google.com/app/apikey
    4. Refresh halaman ini
    """)
    st.stop()

# ========== WELCOME PAGE ==========
if not st.session_state.user_logged_in and not st.session_state.view_as_guest:
    st.markdown("""
        <div class="welcome-container">
            <div class="welcome-title">🍱 Selamat Datang di Cheaply</div>
            <div class="welcome-subtitle">Restoran All You Can Eat Style Jepang</div>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
            <div style="text-align: center; margin: 2rem 0;">
                <h3>Pilih cara untuk melanjutkan:</h3>
            </div>
        """, unsafe_allow_html=True)
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("👤 View as Guest", use_container_width=True, type="secondary"):
                st.session_state.view_as_guest = True
                st.session_state.greeting_shown = False  # Reset greeting saat masuk guest mode
                st.rerun()
        
        with col_btn2:
            if st.button("🔐 Login", use_container_width=True, type="primary"):
                st.session_state.show_login = True
                st.rerun()
    
    # Login Form
    if st.session_state.get('show_login', False):
        st.markdown("---")
        with st.form("login_form"):
            st.markdown("### 🔐 Login")
            phone = st.text_input("Nomor HP", placeholder="081234567890")
            password = st.text_input("Password", type="password", placeholder="Masukkan password")
            
            col1, col2 = st.columns(2)
            with col1:
                submit_login = st.form_submit_button("Login", use_container_width=True)
            with col2:
                cancel_login = st.form_submit_button("Batal", use_container_width=True)
            
            if submit_login:
                if phone and password:
                    try:
                        user = st.session_state.db.verify_member(phone, password)
                        if user:
                            st.session_state.user_logged_in = True
                            st.session_state.current_user = user
                            st.session_state.view_as_guest = False
                            st.session_state.show_login = False
                            st.session_state.greeting_shown = False  # Reset greeting saat login
                            st.session_state.messages = []  # Clear messages saat login
                            if st.session_state.chatbot:
                                st.session_state.chatbot.clear_history()
                            st.success("Login berhasil! Selamat datang, " + user.get("Nama Member", "User"))
                            st.rerun()
                        else:
                            st.error("Nomor HP atau password salah!")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
                else:
                    st.warning("Harap isi nomor HP dan password!")
            
            if cancel_login:
                st.session_state.show_login = False
                st.rerun()

# ========== CHAT INTERFACE ==========
elif st.session_state.user_logged_in or st.session_state.view_as_guest:
    # Header
    user_info = ""
    if st.session_state.user_logged_in:
        user_info = f" | Logged in as: {st.session_state.current_user.get('Nama Member', 'User')}"
    
    st.markdown(f"""
        <div class="main-header">🍱 Cheaply Restaurant{user_info}</div>
        <div class="sub-header">Restoran All You Can Eat Style Jepang</div>
    """, unsafe_allow_html=True)
    
    # Logout button
    if st.session_state.user_logged_in:
        if st.button("🚪 Logout", use_container_width=False):
            st.session_state.user_logged_in = False
            st.session_state.current_user = None
            st.session_state.messages = []
            st.session_state.current_booking = None
            st.session_state.current_orders = []
            st.session_state.show_confirmation = False
            st.session_state.greeting_shown = False  # Reset greeting saat logout
            if st.session_state.chatbot:
                st.session_state.chatbot.clear_history()
            st.rerun()
    
    # Clear chat button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🗑️ Hapus Riwayat Chat", use_container_width=True):
            if st.session_state.chatbot:
                st.session_state.chatbot.clear_history()
            st.session_state.messages = []
            st.session_state.greeting_shown = False  # Reset greeting saat clear chat
            st.rerun()
    
    # Fungsi untuk mendapatkan greeting berdasarkan waktu
    def get_greeting():
        """Mendapatkan greeting berdasarkan waktu dan status login"""
        current_hour = datetime.now().hour
        
        if 5 <= current_hour < 12:
            waktu = "Pagi"
        elif 12 <= current_hour < 15:
            waktu = "Siang"
        elif 15 <= current_hour < 19:
            waktu = "Sore"
        else:
            waktu = "Malam"
        
        if st.session_state.user_logged_in:
            user_name = st.session_state.current_user.get('Nama Member', 'User')
            greeting = f"Halo Selamat {waktu} {user_name}, Selamat datang di Cheaply Restaurant.\n\nSaya siap membantu Anda untuk informasi menu, promo, atau reservasi meja."
        else:
            greeting = f"Halo Selamat {waktu}, Selamat datang di Cheaply Restaurant.\n\nSaya siap membantu Anda untuk informasi menu, promo, atau reservasi meja."
        
        return greeting
    
    # Tampilkan greeting otomatis saat pertama kali chat dibuka
    if not st.session_state.greeting_shown:
        greeting_message = get_greeting()
        st.session_state.messages.append({
            "role": "assistant",
            "content": greeting_message
        })
        st.session_state.greeting_shown = True
        st.rerun()
    
    # Info box
    if st.session_state.view_as_guest:
        st.markdown("""
            <div class="info-box">
                <strong>ℹ️ Mode Guest:</strong> Anda dapat menanyakan tentang menu dan ketersediaan booking. 
                Untuk melakukan booking, silakan login terlebih dahulu.
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div class="success-box">
                <strong>✅ Mode Member:</strong> Anda dapat menanyakan menu, melakukan booking, dan memesan makanan langsung melalui chatbot.
            </div>
        """, unsafe_allow_html=True)
    
    # Chat container
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.messages:
            role_class = "user-message" if message["role"] == "user" else "bot-message"
            
            # Format content dengan line breaks dan escape HTML
            import html
            content = html.escape(message['content'])
            content = content.replace('\n', '<br>')
            
            st.markdown(f"""
                <div class="chat-message {role_class}">
                    <strong>{'Anda' if message['role'] == 'user' else 'Cheaply Bot'}:</strong>
                    <div style="margin-top: 6px;">{content}</div>
                </div>
            """, unsafe_allow_html=True)
            
            # Tampilkan gambar menu jika ada
            if message["role"] == "assistant" and "menu_images" in message:
                st.markdown("---")
                cols = st.columns(min(len(message["menu_images"]), 3))
                for idx, menu_img in enumerate(message["menu_images"]):
                    with cols[idx]:
                        st.image(menu_img["image"], width=200, caption=menu_img["name"])
            
            # Tampilkan rekomendasi waktu jika ada
            if message["role"] == "assistant" and "recommendations" in message:
                st.markdown("---")
                for idx, rec in enumerate(message["recommendations"]):
                    # Cek apakah ini pesan login (untuk diubah menjadi tombol)
                    if rec.startswith("__LOGIN_BUTTON__:"):
                        # Tampilkan sebagai tombol login
                        col1, col2, col3 = st.columns([1, 2, 1])
                        with col2:
                            if st.button("🔐 Login untuk Booking", use_container_width=True, type="primary", key=f"login_btn_{len(st.session_state.messages)}_{idx}"):
                                # Kembali ke welcome page dan tampilkan form login
                                st.session_state.view_as_guest = False
                                st.session_state.show_login = True
                                st.session_state.messages = []  # Clear chat messages
                                if st.session_state.chatbot:
                                    st.session_state.chatbot.clear_history()
                                st.session_state.greeting_shown = False
                                st.rerun()
                    else:
                        # Tampilkan sebagai info biasa
                        st.info(rec)
    
    # Input chat
    if prompt := st.chat_input("Tuliskan pertanyaan atau pesanan Anda di sini..."):
        # Tambahkan pesan user ke history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Generate response
        with st.spinner("Sedang memproses..."):
            # Pass user info jika sudah login
            user_info = st.session_state.current_user if st.session_state.user_logged_in else None
            response = st.session_state.chatbot.get_response(prompt, user_info)
            
            # Cek apakah user ingin booking atau order
            prompt_lower = prompt.lower()
            recommendations = []
            booking_created = None
            
            # Deteksi intent membuat booking baru (bukan hanya menanyakan tentang booking)
            # Kata kunci untuk membuat booking baru
            create_booking_keywords = [
                "mau booking", "ingin booking", "saya mau booking", "saya ingin booking",
                "buat booking", "pesan meja", "reservasi meja", "mau reservasi",
                "ingin reservasi", "booking baru", "reservasi baru"
            ]
            
            # Kata kunci untuk menanyakan tentang booking (bukan membuat)
            query_booking_keywords = [
                "ada booking", "booking aktif", "booking saya", "reservasi saya",
                "punya booking", "punya reservasi", "cek booking", "lihat booking"
            ]
            
            # Cek apakah ini query tentang booking (bukan membuat booking baru)
            is_query_booking = any(keyword in prompt_lower for keyword in query_booking_keywords)
            
            # Cek apakah ini intent membuat booking baru
            is_booking_intent = any(keyword in prompt_lower for keyword in create_booking_keywords)
            
            # Jika hanya menanyakan tentang booking, jangan proses sebagai intent membuat booking
            if is_query_booking and not is_booking_intent:
                is_booking_intent = False
            
            # Cek apakah sedang dalam proses booking (ada data booking yang belum lengkap)
            has_booking_data = hasattr(st.session_state.chatbot, 'booking_data') and st.session_state.chatbot.booking_data
            
            # Jangan proses booking jika sudah ada booking yang berhasil dibuat di session ini
            if st.session_state.current_booking:
                is_booking_intent = False
                has_booking_data = False
            
            # Jika hanya menanyakan tentang booking (bukan membuat), jangan proses booking
            if is_query_booking and not is_booking_intent:
                is_booking_intent = False
                has_booking_data = False
            
            # Hanya proses booking jika benar-benar intent membuat booking baru
            if (is_booking_intent or has_booking_data) and not is_query_booking:
                # Jika user sudah login, proses booking via chatbot
                if st.session_state.user_logged_in:
                    booking_created, booking_message = st.session_state.chatbot.process_booking(
                        prompt,
                        st.session_state.current_user["id"]
                    )
                    if booking_created:
                        # Booking berhasil dibuat - override response dengan konfirmasi
                        st.session_state.current_booking = booking_created
                        
                        # Format tanggal untuk display
                        from datetime import datetime
                        booking_date = booking_created.get('tanggal_kedatangan', 'N/A')
                        if booking_date != 'N/A':
                            try:
                                date_obj = datetime.fromisoformat(booking_date) if isinstance(booking_date, str) else booking_date
                                if isinstance(date_obj, str):
                                    date_obj = datetime.strptime(booking_date, '%Y-%m-%d')
                                # Format tanggal Indonesia
                                hari = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu'][date_obj.weekday()]
                                bulan = ['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 
                                        'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember'][date_obj.month - 1]
                                tanggal_formatted = f"{hari}, {date_obj.day} {bulan} {date_obj.year}"
                            except:
                                tanggal_formatted = booking_date
                        else:
                            tanggal_formatted = booking_date
                        
                        # Generate booking ID
                        booking_id = f"CK{datetime.now().strftime('%Y%m%d')}-{str(booking_created.get('id', '001')).zfill(3)}"
                        
                        # Override response dengan konfirmasi booking
                        user_name = st.session_state.current_user.get('Nama Member', 'User')
                        
                        # Ambil menu yang sudah diorder
                        saved_menu_names = booking_created.get('saved_menu_names', [])
                        menu_info = ""
                        if saved_menu_names:
                            menu_list = ", ".join(saved_menu_names)
                            menu_info = f"* **Menu yang Dipesan:** {menu_list}\n"
                        else:
                            menu_info = "* **Menu yang Dipesan:** Belum ada menu yang dipesan\n"
                        
                        response = f"""Halo {user_name}! ✅ Booking Anda telah berhasil dibuat!

**[KONFIRMASI BOOKING]**

* **ID Booking:** {booking_id}
* **Nama:** {user_name}
* **Tanggal:** {tanggal_formatted}
* **Waktu:** {booking_created.get('jam_kedatangan', 'N/A')}
* **Jumlah Tamu:** {booking_created.get('jumlah_tamu', 'N/A')} orang
{menu_info}
Booking Anda sudah berhasil dikonfirmasi! Email konfirmasi akan dikirim ke alamat email Anda.

Kami tunggu kedatangan {user_name} dan teman-teman di Cheaply! Jika ada pertanyaan lebih lanjut, jangan ragu untuk menghubungi kami. Selamat menikmati!"""
                        
                        # Kirim email konfirmasi (jika email service sudah setup)
                        try:
                            from email_service import send_booking_confirmation_email
                            # Ambil email dari user (jika ada di database)
                            user_email = st.session_state.current_user.get('email') or st.session_state.current_user.get('Email')
                            
                            # Tambahkan menu list ke booking_data untuk email
                            booking_for_email = booking_created.copy()
                            saved_menu_names = booking_created.get('saved_menu_names', [])
                            if saved_menu_names:
                                booking_for_email['menu_list'] = ", ".join(saved_menu_names)
                            else:
                                booking_for_email['menu_list'] = "Belum ada menu yang dipesan"
                            
                            if user_email:
                                send_booking_confirmation_email(
                                    user_email,
                                    booking_for_email,
                                    user_name,
                                    booking_id
                                )
                            else:
                                print(f"⚠️ Email user tidak ditemukan di database. Email tidak dikirim.")
                        except Exception as e:
                            print(f"⚠️ Email tidak dikirim: {str(e)}")
                            import traceback
                            traceback.print_exc()
                        
                        # Reset booking data setelah berhasil
                        if hasattr(st.session_state.chatbot, 'booking_data'):
                            st.session_state.chatbot.booking_data = {}
                    else:
                        # Masih kurang info, tambahkan ke response HANYA jika bukan query tentang booking
                        if not is_query_booking:
                            response += f"\n\n{booking_message}"
                else:
                    # Guest mode - tidak bisa booking
                    # Reset booking data jika ada (untuk mencegah akumulasi data)
                    if hasattr(st.session_state.chatbot, 'booking_data'):
                        st.session_state.chatbot.booking_data = {}
                    
                    # Ambil rekomendasi waktu (5 waktu terbaik)
                    recs = st.session_state.chatbot.get_available_times_recommendations()
                    recommendations = []
                    if recs:
                        recommendations = [
                            f"📅 {rec['tanggal']}: {', '.join(rec['waktu'])}"
                            for rec in recs
                        ]
                    # Tambahkan flag khusus untuk tombol login
                    recommendations.append("__LOGIN_BUTTON__: Untuk melakukan booking, silakan login terlebih dahulu.")
                    
                    # Pastikan response chatbot juga mengarahkan untuk login
                    if "login" not in response.lower() and "masuk" not in response.lower():
                        response += "\n\n🔐 **Catatan:** Untuk melakukan booking, Anda perlu login terlebih dahulu. Silakan klik tombol 'Login' di halaman utama."
            
            # Extract gambar menu jika ada menu yang disebutkan
            menu_images = []
            if "menu" in prompt_lower or "makanan" in prompt_lower or "minuman" in prompt_lower or "favourite" in prompt_lower or "favorit" in prompt_lower:
                menus = st.session_state.db.get_all_menus()
                # Cari menu yang disebutkan dalam response chatbot (lebih akurat)
                mentioned_menus = []
                response_lower = response.lower()
                
                # Ambil kata kunci spesifik dari prompt (bukan kata umum)
                stop_words = ["menu", "makanan", "minuman", "ada", "apa", "yang", "saya", "ingin", "mau", "tolong", "bisa", "lihat", "tampilkan", "show", "list", "tentang", "dengan", "untuk", "tidak", "ada", "apakah"]
                prompt_keywords = [w for w in prompt_lower.split() if w not in stop_words and len(w) > 2]
                
                for menu in menus:
                    menu_name = menu.get("Nama Menu", "")
                    menu_name_lower = menu_name.lower()
                    
                    # Cek apakah nama menu lengkap disebutkan di response chatbot
                    is_mentioned = False
                    
                    # Prioritas 1: Jika response menyebutkan nama menu lengkap
                    if menu_name_lower in response_lower:
                        is_mentioned = True
                    # Prioritas 2: Jika ada kata kunci spesifik dari prompt dan menu mengandung semua kata kunci tersebut
                    elif prompt_keywords:
                        # Cek apakah menu mengandung SEMUA kata kunci dari prompt
                        # Contoh: query "salmon" -> hanya match menu yang mengandung "salmon"
                        # Tidak match "Sushi Tuna" karena tidak ada "salmon"
                        if all(keyword in menu_name_lower for keyword in prompt_keywords):
                            is_mentioned = True
                    
                    if is_mentioned and menu.get("gambar"):
                        mentioned_menus.append({
                            "name": menu.get("Nama Menu"),
                            "image": menu.get("gambar")
                        })
                
                # Tambahkan gambar ke message data
                if mentioned_menus:
                    menu_images = mentioned_menus[:3]  # Max 3 gambar
            
            # Simpan ke history
            message_data = {"role": "assistant", "content": response}
            if recommendations:
                message_data["recommendations"] = recommendations
            if menu_images:
                message_data["menu_images"] = menu_images
            
            st.session_state.messages.append(message_data)
            st.rerun()
    
    # Booking dilakukan sepenuhnya melalui chatbot, tidak ada form
    # Order form (jika user logged in)
    if st.session_state.user_logged_in and not st.session_state.show_confirmation:
        st.markdown("---")
        with st.expander("🍱 Pesan Menu", expanded=False):
            menus = st.session_state.db.get_all_menus()
            if menus:
                # Tampilkan keranjang saat ini jika ada
                if st.session_state.current_orders:
                    st.markdown("### 🛒 Keranjang Anda:")
                    total = 0
                    order_summary = {}
                    for order in st.session_state.current_orders:
                        menu_name = order['menu_name']
                        if menu_name not in order_summary:
                            order_summary[menu_name] = {"qty": 0, "harga": order['harga']}
                        order_summary[menu_name]["qty"] += 1
                    
                    for menu_name, info in order_summary.items():
                        subtotal = info["qty"] * info["harga"]
                        st.write(f"- {menu_name} x{info['qty']} - Rp {subtotal:,}")
                        total += subtotal
                    
                    st.markdown(f"**Total: Rp {total:,}**")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("🗑️ Kosongkan Keranjang", use_container_width=True):
                            st.session_state.current_orders = []
                            st.rerun()
                    with col2:
                        if st.button("✅ Konfirmasi Pesanan", use_container_width=True, type="primary"):
                            st.session_state.show_confirmation = True
                            st.rerun()
                    
                    st.markdown("---")
                
                st.markdown("### 📋 Daftar Menu:")
                for menu in menus:
                    if menu.get("stock", 0) > 0:
                        col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                        with col1:
                            st.write(f"**{menu['Nama Menu']}** ({menu['Tipe']})")
                            st.caption(f"Rp {menu['Harga']:,} | Stock: {menu.get('stock', 0)}")
                        with col2:
                            quantity = st.number_input(
                                "Qty",
                                min_value=0,
                                max_value=min(menu.get("stock", 0), 10),
                                value=0,
                                key=f"qty_{menu['id']}"
                            )
                        with col3:
                            if quantity > 0:
                                if st.button(f"➕ Tambah", key=f"add_{menu['id']}"):
                                    for _ in range(quantity):
                                        st.session_state.current_orders.append({
                                            "menu_id": menu["id"],
                                            "menu_name": menu["Nama Menu"],
                                            "harga": menu["Harga"]
                                        })
                                    st.success(f"✅ Ditambahkan {quantity}x {menu['Nama Menu']}")
                                    st.rerun()
                        with col4:
                            if menu.get("stock", 0) == 0:
                                st.warning("Habis")
                            else:
                                st.info("Tersedia")
    
    # ========== CONFIRMATION PAGE ==========
    if st.session_state.show_confirmation:
        st.markdown("---")
        st.markdown("## ✅ Konfirmasi Booking dan Pesanan")
        
        has_booking = st.session_state.current_booking is not None
        has_orders = len(st.session_state.current_orders) > 0
        
        if not has_booking and not has_orders:
            st.warning("Tidak ada booking atau pesanan untuk dikonfirmasi.")
            if st.button("Kembali"):
                st.session_state.show_confirmation = False
                st.rerun()
        else:
            # Tampilkan booking info
            if has_booking:
                st.markdown("### 📅 Informasi Booking:")
                booking = st.session_state.current_booking
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Tanggal:** {booking.get('tanggal_kedatangan', 'N/A')}")
                    st.write(f"**Jam:** {booking.get('jam_kedatangan', 'N/A')}")
                with col2:
                    st.write(f"**Jumlah Tamu:** {booking.get('jumlah_tamu', 'N/A')} orang")
            
            # Tampilkan order info
            if has_orders:
                st.markdown("### 🍱 Pesanan Anda:")
                total = 0
                order_summary = {}
                for order in st.session_state.current_orders:
                    menu_name = order['menu_name']
                    if menu_name not in order_summary:
                        order_summary[menu_name] = {"qty": 0, "harga": order['harga']}
                    order_summary[menu_name]["qty"] += 1
                
                for menu_name, info in order_summary.items():
                    subtotal = info["qty"] * info["harga"]
                    st.write(f"- {menu_name} x{info['qty']} = Rp {subtotal:,}")
                    total += subtotal
                
                st.markdown(f"**💰 Total: Rp {total:,}**")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Konfirmasi dan Simpan", use_container_width=True, type="primary"):
                try:
                    # Simpan order
                    if st.session_state.current_orders:
                        order_items = [{"menu_id": o["menu_id"]} for o in st.session_state.current_orders]
                        booking_id = st.session_state.current_booking.get("id") if st.session_state.current_booking else None
                        orders = st.session_state.db.create_order(
                            st.session_state.current_user["id"],
                            booking_id,
                            order_items
                        )
                        if orders:
                            st.success("✅ Booking dan Pesanan berhasil disimpan!")
                        else:
                            st.warning("⚠️ Pesanan gagal disimpan, silakan coba lagi.")
                    elif st.session_state.current_booking:
                        st.success("✅ Booking berhasil disimpan!")
                    
                    # Reset state
                    st.session_state.current_orders = []
                    st.session_state.current_booking = None
                    st.session_state.show_confirmation = False
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        
        with col2:
            if st.button("❌ Batal", use_container_width=True):
                st.session_state.show_confirmation = False
                st.rerun()

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666; font-size: 0.9rem; padding: 2rem;'>
        <p>🍱 <strong>Cheaply Restaurant</strong> - Restoran All You Can Eat Style Jepang</p>
        <p>💡 <strong>Tips:</strong> Tanyakan tentang menu, harga, promo, atau ketersediaan booking</p>
    </div>
""", unsafe_allow_html=True)

