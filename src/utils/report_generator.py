import sqlite3
from datetime import datetime
import json

class ReportGenerator:
    def __init__(self, db_path="viventia.db"):
        self.db_path = db_path
    
    def generate_employee_report(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                COUNT(*) as total,
                COUNT(CASE WHEN status = 'Aktif' THEN 1 END) as active,
                AVG(salary) as avg_salary,
                department,
                COUNT(*) as dept_count
            FROM employees 
            GROUP BY department
        """)
        
        data = cursor.fetchall()
        conn.close()
        
        report = {
            'title': 'Personel Raporu',
            'date': datetime.now().isoformat(),
            'departments': []
        }
        
        for row in data:
            report['departments'].append({
                'name': row[3],
                'count': row[4],
                'avg_salary': row[2] or 0
            })
        
        return report
    
    def generate_leave_report(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                l.leave_type,
                COUNT(*) as count,
                l.status,
                AVG(julianday(l.end_date) - julianday(l.start_date) + 1) as avg_days
            FROM leaves l
            GROUP BY l.leave_type, l.status
        """)
        
        data = cursor.fetchall()
        conn.close()
        
        report = {
            'title': 'İzin Raporu',
            'date': datetime.now().isoformat(),
            'leave_stats': []
        }
        
        for row in data:
            report['leave_stats'].append({
                'type': row[0],
                'count': row[1],
                'status': row[2],
                'avg_days': round(row[3] or 0, 1)
            })
        
        return report
    
    def export_to_json(self, report, filename):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        return filename
    
    def export_to_txt(self, report, filename):
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"{report['title']}\n")
            f.write("=" * 50 + "\n")
            f.write(f"Tarih: {report['date']}\n\n")
            
            if 'departments' in report:
                f.write("Departman Dağılımı:\n")
                f.write("-" * 30 + "\n")
                for dept in report['departments']:
                    f.write(f"{dept['name']}: {dept['count']} kişi (Ort. Maaş: {dept['avg_salary']:,.0f} ₺)\n")
            
            if 'leave_stats' in report:
                f.write("İzin İstatistikleri:\n")
                f.write("-" * 30 + "\n")
                for stat in report['leave_stats']:
                    f.write(f"{stat['type']} ({stat['status']}): {stat['count']} adet (Ort. {stat['avg_days']} gün)\n")
        
        return filename