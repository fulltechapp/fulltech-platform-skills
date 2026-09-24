import http.server
import socket
import socketserver
import os
import sys

PORT = 8080
PROFILE_PATH = os.path.join(os.path.dirname(__file__), "..", "profiles", "adguard_dns.mobileconfig")

def get_lan_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

class MobileConfigHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path in ['/', '/adguard', '/adguard.mobileconfig']:
            if not os.path.exists(PROFILE_PATH):
                self.send_error(404, "Profile not found")
                return
            with open(PROFILE_PATH, 'rb') as f:
                data = f.read()
            self.send_response(200)
            self.send_header('Content-Type', 'application/x-apple-aspen-config')
            self.send_header('Content-Disposition', 'attachment; filename="adguard_dns.mobileconfig"')
            self.send_header('Content-Length', str(len(data)))
            self.end_headers()
            self.wfile.write(data)
        else:
            self.send_error(404, "Not Found")

    def log_message(self, format, *args):
        sys.stderr.write(f"[ProfileServer] {format % args}\n")

if __name__ == '__main__':
    lan_ip = get_lan_ip()
    url = f"http://{lan_ip}:{PORT}/adguard.mobileconfig"
    print("=" * 60)
    print(" 🍏 FULLTECH IOS SANITIZER - PROFILE SERVER")
    print("=" * 60)
    print(f"Abra o Safari no seu iPhone e acesse:")
    print(f"👉 {url}")
    print("\nO iOS exibirá: 'Este site está tentando baixar um perfil de configuração'.")
    print("Toque em 'Permitir'. Depois vá em:")
    print("Ajustes > Perfil Baixado > Instalar.")
    print("=" * 60)
    print("Pressione Ctrl+C para encerrar o servidor após a instalação.\n")
    
    with socketserver.TCPServer(("", PORT), MobileConfigHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServidor encerrado.")
