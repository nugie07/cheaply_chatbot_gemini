"""
Email Service untuk mengirim email konfirmasi booking
Menggunakan SMTP Gmail
"""
import os
from dotenv import load_dotenv
from typing import Dict, Optional
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()

# SMTP Gmail Configuration
MAIL_HOST = os.getenv("MAIL_HOST", "smtp.gmail.com")
MAIL_PORT = int(os.getenv("MAIL_PORT", "587"))
MAIL_USERNAME = os.getenv("MAIL_USERNAME", "")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", "")
MAIL_ENCRYPTION = os.getenv("MAIL_ENCRYPTION", "tls")
MAIL_FROM_ADDRESS = os.getenv("MAIL_FROM_ADDRESS", "")
MAIL_FROM_NAME = os.getenv("MAIL_FROM_NAME", "Cheaply Restaurant")

def get_email_template(booking_data: Dict, user_name: str, booking_id: str) -> str:
    """
    Generate HTML email template untuk konfirmasi booking
    
    Args:
        booking_data: Data booking dari database
        user_name: Nama user
        booking_id: ID booking yang sudah diformat
        
    Returns:
        HTML email template
    """
    # Format tanggal
    booking_date = booking_data.get('tanggal_kedatangan', 'N/A')
    if booking_date != 'N/A':
        try:
            if isinstance(booking_date, str):
                date_obj = datetime.strptime(booking_date, '%Y-%m-%d')
            else:
                date_obj = booking_date
            hari = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu'][date_obj.weekday()]
            bulan = ['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 
                    'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember'][date_obj.month - 1]
            tanggal_formatted = f"{hari}, {date_obj.day} {bulan} {date_obj.year}"
        except:
            tanggal_formatted = str(booking_date)
    else:
        tanggal_formatted = booking_date
    
    html_template = f"""
    <!DOCTYPE html>
    <html lang="id">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Konfirmasi Booking - Cheaply Restaurant</title>
    </head>
    <body style="margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f5f5f5;">
        <table role="presentation" style="width: 100%; border-collapse: collapse; background-color: #f5f5f5;">
            <tr>
                <td align="center" style="padding: 40px 20px;">
                    <table role="presentation" style="max-width: 600px; width: 100%; background-color: #ffffff; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                        <!-- Header -->
                        <tr>
                            <td style="padding: 40px 30px; text-align: center; background: linear-gradient(135deg, #4285f4 0%, #34a853 100%); border-radius: 8px 8px 0 0;">
                                <h1 style="margin: 0; color: #ffffff; font-size: 28px; font-weight: 500;">🍱 Cheaply Restaurant</h1>
                                <p style="margin: 10px 0 0 0; color: #ffffff; font-size: 16px;">Restoran All You Can Eat Style Jepang</p>
                            </td>
                        </tr>
                        
                        <!-- Content -->
                        <tr>
                            <td style="padding: 40px 30px;">
                                <h2 style="margin: 0 0 20px 0; color: #202124; font-size: 24px; font-weight: 500;">Konfirmasi Booking</h2>
                                
                                <p style="margin: 0 0 30px 0; color: #5f6368; font-size: 16px; line-height: 1.6;">
                                    Halo <strong style="color: #202124;">{user_name}</strong>!
                                </p>
                                
                                <p style="margin: 0 0 30px 0; color: #5f6368; font-size: 16px; line-height: 1.6;">
                                    Terima kasih telah melakukan booking di Cheaply Restaurant. Booking Anda telah berhasil dikonfirmasi!
                                </p>
                                
                                <!-- Booking Details -->
                                <table role="presentation" style="width: 100%; border-collapse: collapse; margin: 30px 0; background-color: #f8f9fa; border-radius: 8px; padding: 20px;">
                                    <tr>
                                        <td style="padding: 15px; border-bottom: 1px solid #e0e0e0;">
                                            <strong style="color: #202124; font-size: 14px;">ID Booking:</strong>
                                            <span style="color: #5f6368; font-size: 14px; margin-left: 10px;">{booking_id}</span>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 15px; border-bottom: 1px solid #e0e0e0;">
                                            <strong style="color: #202124; font-size: 14px;">Nama:</strong>
                                            <span style="color: #5f6368; font-size: 14px; margin-left: 10px;">{user_name}</span>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 15px; border-bottom: 1px solid #e0e0e0;">
                                            <strong style="color: #202124; font-size: 14px;">Tanggal:</strong>
                                            <span style="color: #5f6368; font-size: 14px; margin-left: 10px;">{tanggal_formatted}</span>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 15px; border-bottom: 1px solid #e0e0e0;">
                                            <strong style="color: #202124; font-size: 14px;">Waktu:</strong>
                                            <span style="color: #5f6368; font-size: 14px; margin-left: 10px;">{booking_data.get('jam_kedatangan', 'N/A')}</span>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 15px; border-bottom: 1px solid #e0e0e0;">
                                            <strong style="color: #202124; font-size: 14px;">Jumlah Tamu:</strong>
                                            <span style="color: #5f6368; font-size: 14px; margin-left: 10px;">{booking_data.get('jumlah_tamu', 'N/A')} orang</span>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 15px;">
                                            <strong style="color: #202124; font-size: 14px;">Menu yang Dipesan:</strong>
                                            <span style="color: #5f6368; font-size: 14px; margin-left: 10px;">{booking_data.get('menu_list', 'Belum ada menu yang dipesan')}</span>
                                        </td>
                                    </tr>
                                </table>
                                
                                <p style="margin: 30px 0 0 0; color: #5f6368; font-size: 16px; line-height: 1.6;">
                                    Kami sangat menantikan kedatangan Anda dan tamu-tamu di Cheaply Restaurant. Jika ada pertanyaan atau perubahan, jangan ragu untuk menghubungi kami.
                                </p>
                                
                                <p style="margin: 30px 0 0 0; color: #5f6368; font-size: 16px; line-height: 1.6;">
                                    Selamat menikmati! 🍱
                                </p>
                            </td>
                        </tr>
                        
                        <!-- Footer -->
                        <tr>
                            <td style="padding: 30px; text-align: center; background-color: #f8f9fa; border-radius: 0 0 8px 8px; border-top: 1px solid #e0e0e0;">
                                <p style="margin: 0 0 10px 0; color: #5f6368; font-size: 14px;">
                                    <strong>Cheaply Restaurant</strong><br>
                                    Restoran All You Can Eat Style Jepang
                                </p>
                                <p style="margin: 10px 0 0 0; color: #9aa0a6; font-size: 12px;">
                                    <strong>⚠️ NO REPLY EMAIL</strong><br>
                                    Email ini dikirim secara otomatis oleh sistem Cheaply Restaurant.<br>
                                    Mohon <strong>JANGAN membalas email ini</strong> karena email ini tidak dipantau.<br>
                                    Jika ada pertanyaan atau perubahan booking, silakan hubungi kami melalui aplikasi atau datang langsung ke restoran.
                                </p>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
    </body>
    </html>
    """
    return html_template

def send_booking_confirmation_email(to_email: str, booking_data: Dict, user_name: str, booking_id: str) -> bool:
    """
    Kirim email konfirmasi booking menggunakan SMTP Gmail
    
    Args:
        to_email: Email penerima
        booking_data: Data booking dari database
        user_name: Nama user
        booking_id: ID booking yang sudah diformat
        
    Returns:
        True jika berhasil, False jika gagal
    """
    if not MAIL_USERNAME or not MAIL_PASSWORD:
        print("⚠️ MAIL_USERNAME atau MAIL_PASSWORD tidak ditemukan di .env. Email tidak dikirim.")
        return False
    
    if not MAIL_FROM_ADDRESS:
        print("⚠️ MAIL_FROM_ADDRESS tidak ditemukan di .env. Email tidak dikirim.")
        return False
    
    try:
        # Generate HTML email
        html_content = get_email_template(booking_data, user_name, booking_id)
        
        # Create message
        message = MIMEMultipart('alternative')
        message['From'] = f"{MAIL_FROM_NAME} <{MAIL_FROM_ADDRESS}>"
        message['To'] = to_email
        message['Reply-To'] = "noreply@cheaply.com"  # Set reply-to ke noreply untuk mencegah reply
        message['Subject'] = f"Konfirmasi Booking - {booking_id} - Cheaply Restaurant"
        
        # Attach HTML content
        html_part = MIMEText(html_content, 'html')
        message.attach(html_part)
        
        # Connect to SMTP server
        print(f"📧 Mencoba mengirim email ke {to_email}...")
        print(f"   From: {MAIL_FROM_ADDRESS}")
        print(f"   Host: {MAIL_HOST}:{MAIL_PORT}")
        
        if MAIL_ENCRYPTION.lower() == 'tls':
            server = smtplib.SMTP(MAIL_HOST, MAIL_PORT)
            server.set_debuglevel(1)  # Enable debug untuk melihat detail
            server.starttls()
        else:
            server = smtplib.SMTP_SSL(MAIL_HOST, MAIL_PORT)
            server.set_debuglevel(1)  # Enable debug untuk melihat detail
        
        # Login and send email
        print(f"🔐 Mencoba login ke SMTP server...")
        server.login(MAIL_USERNAME, MAIL_PASSWORD)
        print(f"✅ Login berhasil!")
        
        print(f"📤 Mengirim email...")
        server.send_message(message)
        server.quit()
        
        print(f"✅ Email konfirmasi berhasil dikirim ke {to_email}")
        print(f"   ⚠️ Jika email tidak muncul di inbox, cek folder Spam/Junk")
        print(f"   ⚠️ Email mungkin membutuhkan beberapa menit untuk sampai")
        return True
        
    except smtplib.SMTPAuthenticationError:
        print("❌ Gagal autentikasi SMTP. Pastikan MAIL_USERNAME dan MAIL_PASSWORD benar.")
        print("   Untuk Gmail, pastikan menggunakan App Password, bukan password biasa.")
        return False
    except smtplib.SMTPException as e:
        print(f"❌ Error SMTP: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ Error mengirim email: {str(e)}")
        return False
