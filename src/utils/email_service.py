import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import json
import os
from datetime import datetime
from ..utils.error_handler import error_handler

class EmailService:
    """E-posta gönderme servisi"""

    def __init__(self):
        self.config_file = "email_config.json"
        self.config = self.load_config()

    def load_config(self):
        """E-posta yapılandırmasını yükler"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                # Varsayılan yapılandırma
                return {
                    "smtp_server": "smtp.gmail.com",
                    "smtp_port": 587,
                    "username": "",
                    "password": "",
                    "from_email": "",
                    "use_tls": True
                }
        except Exception as e:
            error_handler.handle_error(e, "E-posta yapılandırması yükleme", show_user=False)
            return {}

    def save_config(self, config):
        """E-posta yapılandırmasını kaydeder"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            self.config = config
            error_handler.log_info("E-posta yapılandırması kaydedildi")
        except Exception as e:
            error_handler.handle_error(e, "E-posta yapılandırması kaydetme")

    def test_connection(self):
        """SMTP bağlantısını test eder"""
        try:
            server = smtplib.SMTP(self.config.get('smtp_server'), self.config.get('smtp_port'))
            server.ehlo()

            if self.config.get('use_tls', True):
                server.starttls()
                server.ehlo()

            server.login(self.config.get('username'), self.config.get('password'))
            server.quit()

            return True, "SMTP bağlantısı başarılı"
        except Exception as e:
            return False, f"SMTP bağlantı hatası: {str(e)}"

    def send_email(self, to_email, subject, body, html_body=None, attachments=None):
        """E-posta gönderir"""
        try:
            if not self.config.get('username') or not self.config.get('password'):
                raise ValueError("E-posta yapılandırması eksik")

            # E-posta mesajını oluştur
            msg = MIMEMultipart()
            msg['From'] = self.config.get('from_email', self.config.get('username'))
            msg['To'] = to_email
            msg['Subject'] = subject

            # Metin gövdesi
            if html_body:
                msg.attach(MIMEText(body, 'plain'))
                msg.attach(MIMEText(html_body, 'html'))
            else:
                msg.attach(MIMEText(body, 'plain'))

            # Ekler
            if attachments:
                for attachment in attachments:
                    if os.path.exists(attachment):
                        part = MIMEBase('application', 'octet-stream')
                        with open(attachment, 'rb') as f:
                            part.set_payload(f.read())
                        encoders.encode_base64(part)
                        part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(attachment)}')
                        msg.attach(part)

            # SMTP bağlantısı
            server = smtplib.SMTP(self.config.get('smtp_server'), self.config.get('smtp_port'))
            server.ehlo()

            if self.config.get('use_tls', True):
                server.starttls()
                server.ehlo()

            server.login(self.config.get('username'), self.config.get('password'))
            server.sendmail(msg['From'], to_email, msg.as_string())
            server.quit()

            error_handler.log_info(f"E-posta gönderildi: {to_email} - {subject}")
            return True

        except Exception as e:
            error_handler.handle_error(e, f"E-posta gönderme: {to_email}")
            return False

    def send_leave_notification(self, employee_email, employee_name, leave_details):
        """İzin talebi bildirimi gönderir"""
        subject = "İzin Talebi Bildirimi - Viventia HR"

        body = f"""
        Sayın {employee_name},

        İzin talebiniz başarıyla alındı.

        İzin Detayları:
        - Başlangıç Tarihi: {leave_details['start_date']}
        - Bitiş Tarihi: {leave_details['end_date']}
        - İzin Türü: {leave_details['leave_type']}
        - Sebep: {leave_details['reason']}
        - Durum: Bekliyor

        Talebiniz yönetici onayından sonra işleme alınacaktır.

        Saygılarımla,
        Viventia İnsan Kaynakları Sistemi
        """

        html_body = f"""
        <html>
        <body>
            <h2>İzin Talebi Bildirimi</h2>
            <p>Sayın <strong>{employee_name}</strong>,</p>

            <p>İzin talebiniz başarıyla alındı.</p>

            <h3>İzin Detayları:</h3>
            <ul>
                <li><strong>Başlangıç Tarihi:</strong> {leave_details['start_date']}</li>
                <li><strong>Bitiş Tarihi:</strong> {leave_details['end_date']}</li>
                <li><strong>İzin Türü:</strong> {leave_details['leave_type']}</li>
                <li><strong>Sebep:</strong> {leave_details['reason']}</li>
                <li><strong>Durum:</strong> <span style="color: orange;">Bekliyor</span></li>
            </ul>

            <p>Talebiniz yönetici onayından sonra işleme alınacaktır.</p>

            <p>Saygılarımla,<br>Viventia İnsan Kaynakları Sistemi</p>
        </body>
        </html>
        """

        return self.send_email(employee_email, subject, body, html_body)

    def send_leave_approval(self, employee_email, employee_name, leave_details, approved=True):
        """İzin onay/red bildirimi gönderir"""
        status = "Onaylandı" if approved else "Reddedildi"
        color = "green" if approved else "red"

        subject = f"İzin Talebi {status} - Viventia HR"

        body = f"""
        Sayın {employee_name},

        İzin talebiniz {status.lower()}.

        İzin Detayları:
        - Başlangıç Tarihi: {leave_details['start_date']}
        - Bitiş Tarihi: {leave_details['end_date']}
        - İzin Türü: {leave_details['leave_type']}

        Saygılarımla,
        Viventia İnsan Kaynakları Sistemi
        """

        html_body = f"""
        <html>
        <body>
            <h2>İzin Talebi {status}</h2>
            <p>Sayın <strong>{employee_name}</strong>,</p>

            <p>İzin talebiniz <span style="color: {color}; font-weight: bold;">{status.lower()}</span>.</p>

            <h3>İzin Detayları:</h3>
            <ul>
                <li><strong>Başlangıç Tarihi:</strong> {leave_details['start_date']}</li>
                <li><strong>Bitiş Tarihi:</strong> {leave_details['end_date']}</li>
                <li><strong>İzin Türü:</strong> {leave_details['leave_type']}</li>
            </ul>

            <p>Saygılarımla,<br>Viventia İnsan Kaynakları Sistemi</p>
        </body>
        </html>
        """

        return self.send_email(employee_email, subject, body, html_body)

    def send_payroll_notification(self, employee_email, employee_name, payroll_data):
        """Bordro bildirimi gönderir"""
        subject = "Bordro Bilgileri - Viventia HR"

        body = f"""
        Sayın {employee_name},

        {payroll_data['month']} ayı bordro bilgileriniz hazır.

        Bordro Özeti:
        - Brüt Maaş: {payroll_data['base_salary']:.2f} ₺
        - Prim: {payroll_data.get('bonus', 0):.2f} ₺
        - Kesintiler: {payroll_data.get('deductions', 0):.2f} ₺
        - Net Maaş: {payroll_data['net_salary']:.2f} ₺

        Detaylı bordro bilgilerinize sistem üzerinden ulaşabilirsiniz.

        Saygılarımla,
        Viventia İnsan Kaynakları Sistemi
        """

        html_body = f"""
        <html>
        <body>
            <h2>Bordro Bilgileri</h2>
            <p>Sayın <strong>{employee_name}</strong>,</p>

            <p>{payroll_data['month']} ayı bordro bilgileriniz hazır.</p>

            <h3>Bordro Özeti:</h3>
            <table border="1" style="border-collapse: collapse;">
                <tr>
                    <td><strong>Brüt Maaş:</strong></td>
                    <td>{payroll_data['base_salary']:.2f} ₺</td>
                </tr>
                <tr>
                    <td><strong>Prim:</strong></td>
                    <td>{payroll_data.get('bonus', 0):.2f} ₺</td>
                </tr>
                <tr>
                    <td><strong>Kesintiler:</strong></td>
                    <td>{payroll_data.get('deductions', 0):.2f} ₺</td>
                </tr>
                <tr style="background-color: #f0f0f0;">
                    <td><strong>Net Maaş:</strong></td>
                    <td><strong>{payroll_data['net_salary']:.2f} ₺</strong></td>
                </tr>
            </table>

            <p>Detaylı bordro bilgilerinize sistem üzerinden ulaşabilirsiniz.</p>

            <p>Saygılarımla,<br>Viventia İnsan Kaynakları Sistemi</p>
        </body>
        </html>
        """

        return self.send_email(employee_email, subject, body, html_body)

    def send_system_notification(self, to_emails, subject, message):
        """Sistem bildirimi gönderir"""
        success_count = 0

        for email in to_emails:
            if self.send_email(email, subject, message):
                success_count += 1

        error_handler.log_info(f"Sistem bildirimi {success_count}/{len(to_emails)} kullanıcıya gönderildi")
        return success_count

# Global email service instance
email_service = EmailService()