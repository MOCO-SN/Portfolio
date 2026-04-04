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

def send_visitor_email(ips, device_info=None, ip_info=None, gps=None):
    ipv4, ipv6 = classify_ips(ips)
    
    body = f"New visitor to Sachin's Profile\n\n"
    
    if ipv4:
        body += f"IPv4: {', '.join(ipv4)}\n"
    if ipv6:
        body += f"IPv6: {', '.join(ipv6)}\n"
    
    if ip_info:
        body += f"\n--- IPAPI Info ---\n"
        body += f"API IP: {ip_info.get('ip', 'N/A')}\n"
        body += f"IP Type: {ip_info.get('version', 'N/A')}\n"
        body += f"Location: {ip_info.get('city', 'N/A')}, {ip_info.get('region', 'N/A')}, {ip_info.get('country_name', 'N/A')}\n"
        body += f"Organization: {ip_info.get('org', 'N/A')}\n\n"
    
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
        subject="New Website Visit: Sachin's Profile",
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
        
        ips = get_client_ip()
        
        device_info = data.get('deviceInfo')
        ip_info = data.get('ipInfo')
        gps = data.get('gps')
        
        send_visitor_email(ips, device_info, ip_info, gps)
        
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# if __name__ == '__main__':
#     app.run(debug=True)