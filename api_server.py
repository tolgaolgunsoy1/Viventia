#!/usr/bin/env python3
"""
Viventia HR API Server Launcher
API sunucusunu başlatmak için bu script'i çalıştırın.
"""

import sys
import os
import argparse

# Proje root'una path ekle
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.api.api_server import run_api_server
from src.utils.error_handler import error_handler

def main():
    parser = argparse.ArgumentParser(description='Viventia HR API Server')
    parser.add_argument('--host', default='localhost', help='Sunucu host adresi (varsayılan: localhost)')
    parser.add_argument('--port', type=int, default=5000, help='Sunucu port numarası (varsayılan: 5000)')
    parser.add_argument('--debug', action='store_true', help='Debug modunu etkinleştir')

    args = parser.parse_args()

    try:
        print("🚀 Viventia HR API Sunucusu başlatılıyor...")
        print(f"📍 Host: {args.host}")
        print(f"🔌 Port: {args.port}")
        print(f"🐛 Debug: {'Evet' if args.debug else 'Hayır'}")
        print("-" * 50)

        run_api_server(host=args.host, port=args.port, debug=args.debug)

    except KeyboardInterrupt:
        print("\n👋 API sunucusu durduruldu.")
    except Exception as e:
        error_handler.handle_error(e, "API server launcher")
        sys.exit(1)

if __name__ == '__main__':
    main()