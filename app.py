import logging
from flask import Flask, render_template, request, jsonify
from flask_mail import Mail, Message

# Suppress 304 Not Modified logs
log = logging.getLogger('werkzeug')
log.setLevel(logging.WARNING)

app = Flask(__name__, template_folder='template', static_folder='template', static_url_path='')

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'mocosnlove@gmail.com'
app.config['MAIL_PASSWORD'] = 'nbvsvvljggvuxhhe'
app.config['MAIL_DEFAULT_SENDER'] = 'sachinpatel34242@gmail.com'

mail = Mail(app)

def get_client_ip():
    ips = []
    
    # Try to get all IPs from X-Forwarded-For (can contain both IPv4 and IPv6)
    if request.environ.get('HTTP_X_FORWARDED_FOR'):
        forwarded = request.environ['HTTP_X_FORWARDED_FOR'].split(',')
        ips.extend([ip.strip() for ip in forwarded])
    
    # Check X-Real-IP
    if request.environ.get('HTTP_X_REAL_IP'):
        real_ip = request.environ['HTTP_X_REAL_IP'].strip()
        if real_ip not in ips:
            ips.append(real_ip)
    
    # Fallback to remote_addr
    if request.environ.get('REMOTE_ADDR'):
        remote_ip = request.environ['REMOTE_ADDR'].strip()
        if remote_ip not in ips:
            ips.append(remote_ip)
    
    return ips if ips else ["Unknown"]

def is_ipv6(ip):
    if not ip:
        return False
    return ':' in ip

def classify_ips(ips):
    ipv4 = []
    ipv6 = []
    for ip in ips:
        if is_ipv6(ip):
            ipv6.append(ip)
        else:
            ipv4.append(ip)
    return ipv4, ipv6

def send_visitor_email(ips, device_info=None, ip_info=None, gps=None, webrtc_ips=None, timestamp=None, ipv6=None):
    from datetime import datetime
    
    body = f"New visitor to Sachin's Profile\n\n"
    body += f"Visit Time: {timestamp or datetime.now().strftime('%Y-%m-%d %H:%M:%S IST')}\n\n"
    
    # IPv6 from JS client
    if ipv6 and ipv6 != "null":
        body += f"IPv6: {ipv6}\n"
    else:
        body += f"IPv6: Not available\n"
    
    # All IP Info from ipapi
    if ip_info:
        body += f"\n--- IP Info ---\n"
        body += f"IP: {ip_info.get('ip', 'N/A')}\n"
        body += f"Version: {ip_info.get('version', 'N/A')}\n"
        body += f"City: {ip_info.get('city', 'N/A')}\n"
        body += f"Region: {ip_info.get('region', 'N/A')} ({ip_info.get('region_code', 'N/A')})\n"
        body += f"Country: {ip_info.get('country_name', 'N/A')} ({ip_info.get('country_code', 'N/A')})\n"
        body += f"Continent: {ip_info.get('continent_code', 'N/A')}\n"
        body += f"Latitude: {ip_info.get('latitude', 'N/A')}\n"
        body += f"Longitude: {ip_info.get('longitude', 'N/A')}\n"
        body += f"Timezone: {ip_info.get('timezone', 'N/A')} (UTC {ip_info.get('utc_offset', 'N/A')})\n"
        body += f"Network: {ip_info.get('network', 'N/A')}\n"
        body += f"Organization: {ip_info.get('org', 'N/A')}\n"
        body += f"AS: {ip_info.get('asn', 'N/A')}\n"
        body += f"Postal: {ip_info.get('postal', 'N/A')}\n"
        body += f"Languages: {ip_info.get('languages', 'N/A')}\n"
        body += f"Currency: {ip_info.get('currency', 'N/A')} ({ip_info.get('currency_name', 'N/A')})\n\n"
    
    # WebRTC IPs (skip invalid ones)
    if webrtc_ips:
        webrtc_ipv4 = webrtc_ips.get('ipv4', [])
        webrtc_ipv6 = webrtc_ips.get('ipv6', [])
        
        # Filter valid IPv6 (must have at least 3 colons or proper format)
        valid_ipv6 = [ip for ip in webrtc_ipv6 if ip.count(':') >= 2 and len(ip) > 8]
        
        if webrtc_ipv4 or valid_ipv6:
            body += f"WebRTC IPs:\n"
            if webrtc_ipv4:
                body += f"  IPv4: {', '.join(webrtc_ipv4)}\n"
            if valid_ipv6:
                body += f"  IPv6: {', '.join(valid_ipv6)}\n\n"
    
    # Server IPs (fallback)
    ipv4, ipv6_server = classify_ips(ips)
    if ipv4:
        body += f"Server IPv4: {', '.join(ipv4)}\n"
    if ipv6_server:
        body += f"Server IPv6: {', '.join(ipv6_server)}\n"
    
    if device_info:
        body += f"Device Info:\n"
        body += f"  Platform: {device_info.get('platform', 'N/A')}\n"
        body += f"  Language: {device_info.get('language', 'N/A')}\n"
        body += f"  Screen: {device_info.get('screenWidth', 'N/A')}x{device_info.get('screenHeight', 'N/A')}\n"
        body += f"  Timezone: {device_info.get('timezone', 'N/A')}\n"
        body += f"  Referrer: {device_info.get('referrer', 'N/A')}\n"
        body += f"  Page URL: {device_info.get('pageURL', 'N/A')}\n"
        body += f"  User Agent: {device_info.get('userAgent', 'N/A')}\n\n"
    
    if gps and gps.get('latitude'):
        body += f"GPS Location: {gps.get('latitude')}, {gps.get('longitude')} (Accuracy: {gps.get('accuracy')}m)\n"
    
    msg = Message(
        subject="New Visit: Sachin's Profile(mocosn.in)",
        recipients=["sachinpatel34241@gmail.com"],
        body=body
    )
    mail.send(msg)

@app.route('/')
def index():
    ips = get_client_ip()
    return render_template("index.html")

@app.route('/track-visitor', methods=['POST'])
def track_visitor():
    try:
        data = request.get_json()
        
        print("Received data:", data)  # Debug log
        
        ips = get_client_ip()
        
        device_info = data.get('deviceInfo')
        ip_info = data.get('ipInfo')
        gps = data.get('gps')
        webrtc_ips = data.get('webRTCIPs')
        timestamp = data.get('timestamp')
        ipv6 = data.get('ipv6')
        
        print(f"IPv6 from JS: {ipv6}")  # Debug log
        
        send_visitor_email(ips, device_info, ip_info, gps, webrtc_ips, timestamp, ipv6)
        
        return jsonify({"status": "success"})
    except Exception as e:
        print(f"Error: {e}")  # Debug log
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)