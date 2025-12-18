from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import jwt
import datetime
from functools import wraps
from ..database.database import Database, DatabaseError
from ..security.auth_manager import AuthManager
from ..utils.error_handler import error_handler
import json

app = Flask(__name__)
CORS(app)

# JWT Secret Key
app.config['SECRET_KEY'] = 'viventia_hr_secret_key_2024'

# Global instances
db = Database()
auth_manager = AuthManager()

def token_required(f):
    """JWT token kontrolü decorator'ı"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({'message': 'Token eksik!'}), 401

        try:
            # Bearer token'ı ayır
            if token.startswith('Bearer '):
                token = token[7:]

            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = data['user']
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token süresi dolmuş!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Geçersiz token!'}), 401

        return f(current_user, *args, **kwargs)
    return decorated

@app.route('/api/login', methods=['POST'])
def login():
    """Kullanıcı girişi"""
    try:
        data = request.get_json()

        if not data or not data.get('username') or not data.get('password'):
            return jsonify({'message': 'Kullanıcı adı ve şifre gerekli!'}), 400

        if auth_manager.login(data['username'], data['password']):
            # JWT token oluştur
            token = jwt.encode({
                'user': data['username'],
                'role': auth_manager.current_user['role'],
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
            }, app.config['SECRET_KEY'], algorithm='HS256')

            return jsonify({
                'message': 'Giriş başarılı!',
                'token': token,
                'user': {
                    'username': auth_manager.current_user['username'],
                    'role': auth_manager.current_user['role']
                }
            }), 200
        else:
            return jsonify({'message': 'Geçersiz kullanıcı adı veya şifre!'}), 401

    except Exception as e:
        error_handler.handle_error(e, "API login", show_user=False)
        return jsonify({'message': 'Sunucu hatası!'}), 500

@app.route('/api/employees', methods=['GET'])
@token_required
def get_employees(current_user):
    """Çalışan listesi"""
    try:
        employees = db.get_employees()

        # Hassas bilgileri filtrele (sadece temel bilgiler)
        filtered_employees = []
        for emp in employees:
            filtered_employees.append({
                'id': emp[0],
                'name': emp[1],
                'department': emp[2],
                'position': emp[3],
                'salary': emp[4],
                'hire_date': emp[5],
                'status': emp[6],
                'email': emp[7] if emp[7] else None
            })

        return jsonify({
            'employees': filtered_employees,
            'total': len(filtered_employees)
        }), 200

    except DatabaseError as e:
        return jsonify({'message': f'Veritabanı hatası: {str(e)}'}), 500
    except Exception as e:
        error_handler.handle_error(e, "API get employees", show_user=False)
        return jsonify({'message': 'Sunucu hatası!'}), 500

@app.route('/api/employees/<int:employee_id>', methods=['GET'])
@token_required
def get_employee(current_user, employee_id):
    """Tek çalışan bilgisi"""
    try:
        employees = db.get_employees()
        employee = next((emp for emp in employees if emp[0] == employee_id), None)

        if not employee:
            return jsonify({'message': 'Çalışan bulunamadı!'}), 404

        return jsonify({
            'employee': {
                'id': employee[0],
                'name': employee[1],
                'department': employee[2],
                'position': employee[3],
                'salary': employee[4],
                'hire_date': employee[5],
                'status': employee[6],
                'email': employee[7] if employee[7] else None,
                'phone': employee[8] if employee[8] else None
            }
        }), 200

    except DatabaseError as e:
        return jsonify({'message': f'Veritabanı hatası: {str(e)}'}), 500
    except Exception as e:
        error_handler.handle_error(e, "API get employee", show_user=False)
        return jsonify({'message': 'Sunucu hatası!'}), 500

@app.route('/api/employees', methods=['POST'])
@token_required
def create_employee(current_user):
    """Yeni çalışan ekleme"""
    try:
        data = request.get_json()

        required_fields = ['name', 'department', 'position', 'salary', 'hire_date', 'email']
        for field in required_fields:
            if field not in data:
                return jsonify({'message': f'{field} alanı zorunludur!'}), 400

        # Veri validasyonu
        from ..utils.validators import Validators
        if not Validators.validate_name(data['name']):
            return jsonify({'message': 'Geçersiz isim!'}), 400

        if not Validators.validate_email(data['email']):
            return jsonify({'message': 'Geçersiz e-posta!'}), 400

        if not Validators.validate_salary(str(data['salary'])):
            return jsonify({'message': 'Geçersiz maaş!'}), 400

        employee_data = {
            'name': data['name'],
            'department': data['department'],
            'position': data['position'],
            'salary': float(data['salary']),
            'hire_date': data['hire_date'],
            'email': data['email'],
            'phone': data.get('phone', '')
        }

        employee_id = db.add_employee(employee_data)

        # Audit log
        auth_manager.log_action("CREATE_EMPLOYEE", "employees", employee_id)

        return jsonify({
            'message': 'Çalışan başarıyla eklendi!',
            'employee_id': employee_id
        }), 201

    except DatabaseError as e:
        return jsonify({'message': f'Veritabanı hatası: {str(e)}'}), 500
    except Exception as e:
        error_handler.handle_error(e, "API create employee", show_user=False)
        return jsonify({'message': 'Sunucu hatası!'}), 500

@app.route('/api/leaves', methods=['GET'])
@token_required
def get_leaves(current_user):
    """İzin talepleri"""
    try:
        leaves = db.get_leaves()

        return jsonify({
            'leaves': [{
                'id': leave[0],
                'employee_name': leave[1],
                'leave_type': leave[2],
                'start_date': leave[3],
                'end_date': leave[4],
                'reason': leave[5],
                'status': leave[6]
            } for leave in leaves],
            'total': len(leaves)
        }), 200

    except DatabaseError as e:
        return jsonify({'message': f'Veritabanı hatası: {str(e)}'}), 500
    except Exception as e:
        error_handler.handle_error(e, "API get leaves", show_user=False)
        return jsonify({'message': 'Sunucu hatası!'}), 500

@app.route('/api/leaves', methods=['POST'])
@token_required
def create_leave_request(current_user):
    """İzin talebi oluşturma"""
    try:
        data = request.get_json()

        required_fields = ['employee_id', 'start_date', 'end_date', 'leave_type', 'reason']
        for field in required_fields:
            if field not in data:
                return jsonify({'message': f'{field} alanı zorunludur!'}), 400

        leave_data = {
            'employee_id': data['employee_id'],
            'start_date': data['start_date'],
            'end_date': data['end_date'],
            'leave_type': data['leave_type'],
            'reason': data['reason']
        }

        db.add_leave_request(leave_data)

        # Audit log
        auth_manager.log_action("CREATE_LEAVE_REQUEST", "leaves")

        return jsonify({'message': 'İzin talebi başarıyla oluşturuldu!'}), 201

    except DatabaseError as e:
        return jsonify({'message': f'Veritabanı hatası: {str(e)}'}), 500
    except Exception as e:
        error_handler.handle_error(e, "API create leave request", show_user=False)
        return jsonify({'message': 'Sunucu hatası!'}), 500

@app.route('/api/stats', methods=['GET'])
@token_required
def get_stats(current_user):
    """Genel istatistikler"""
    try:
        total, active, pending_leaves = db.get_employee_stats()

        return jsonify({
            'total_employees': total,
            'active_employees': active,
            'pending_leaves': pending_leaves,
            'inactive_employees': total - active
        }), 200

    except DatabaseError as e:
        return jsonify({'message': f'Veritabanı hatası: {str(e)}'}), 500
    except Exception as e:
        error_handler.handle_error(e, "API get stats", show_user=False)
        return jsonify({'message': 'Sunucu hatası!'}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """API sağlık kontrolü"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.datetime.utcnow().isoformat(),
        'version': '1.0.0'
    }), 200

@app.errorhandler(404)
def not_found(error):
    return jsonify({'message': 'Endpoint bulunamadı!'}), 404

@app.errorhandler(500)
def internal_error(error):
    error_handler.handle_error(error, "API 500 error", show_user=False)
    return jsonify({'message': 'Sunucu hatası!'}), 500

def run_api_server(host='localhost', port=5000, debug=False):
    """API sunucusunu başlatır"""
    try:
        error_handler.log_info(f"API sunucusu başlatılıyor: {host}:{port}")
        app.run(host=host, port=port, debug=debug, threaded=True)
    except Exception as e:
        error_handler.handle_error(e, "API sunucu başlatma")

if __name__ == '__main__':
    run_api_server(debug=True)