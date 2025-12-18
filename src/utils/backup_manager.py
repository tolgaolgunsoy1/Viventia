import sqlite3
import shutil
import os
from datetime import datetime
import json

class BackupManager:
    def __init__(self, db_path="viventia.db"):
        self.db_path = db_path
        self.backup_dir = "backups"
        
        # Backup klasörü oluştur
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)
    
    def create_backup(self):
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"viventia_backup_{timestamp}.db"
            backup_path = os.path.join(self.backup_dir, backup_filename)
            
            # Veritabanını kopyala
            shutil.copy2(self.db_path, backup_path)
            
            # Backup bilgilerini kaydet
            backup_info = {
                'filename': backup_filename,
                'path': backup_path,
                'timestamp': timestamp,
                'size': os.path.getsize(backup_path),
                'created_date': datetime.now().isoformat()
            }
            
            info_file = os.path.join(self.backup_dir, f"backup_info_{timestamp}.json")
            with open(info_file, 'w', encoding='utf-8') as f:
                json.dump(backup_info, f, ensure_ascii=False, indent=2)
            
            return backup_path
            
        except Exception as e:
            raise Exception(f"Backup oluşturma hatası: {str(e)}")
    
    def restore_backup(self, backup_path):
        try:
            if not os.path.exists(backup_path):
                raise Exception("Backup dosyası bulunamadı!")
            
            # Mevcut veritabanını yedekle
            current_backup = f"{self.db_path}.restore_backup"
            shutil.copy2(self.db_path, current_backup)
            
            # Backup'ı geri yükle
            shutil.copy2(backup_path, self.db_path)
            
            return True
            
        except Exception as e:
            # Hata durumunda eski veritabanını geri yükle
            if os.path.exists(f"{self.db_path}.restore_backup"):
                shutil.copy2(f"{self.db_path}.restore_backup", self.db_path)
            raise Exception(f"Geri yükleme hatası: {str(e)}")
    
    def list_backups(self):
        backups = []
        
        if not os.path.exists(self.backup_dir):
            return backups
        
        for filename in os.listdir(self.backup_dir):
            if filename.endswith('.db'):
                filepath = os.path.join(self.backup_dir, filename)
                stat = os.stat(filepath)
                
                backups.append({
                    'filename': filename,
                    'path': filepath,
                    'size': stat.st_size,
                    'created_date': datetime.fromtimestamp(stat.st_ctime).isoformat()
                })
        
        return sorted(backups, key=lambda x: x['created_date'], reverse=True)
    
    def delete_old_backups(self, keep_count=5):
        backups = self.list_backups()
        
        if len(backups) > keep_count:
            for backup in backups[keep_count:]:
                try:
                    os.remove(backup['path'])
                    # Info dosyasını da sil
                    info_file = backup['path'].replace('.db', '.json').replace('viventia_backup_', 'backup_info_')
                    if os.path.exists(info_file):
                        os.remove(info_file)
                except Exception:
                    pass