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

# def send_visitor_email(ips, device_info=None, ip_info=None, gps=None, webrtc_ips=None, timestamp=None, ipv6=None):
#     from datetime import datetime
    
#     body = f"New visitor to Sachin's Profile\n\n"
#     body += f"Visit Time: {timestamp or datetime.now().strftime('%Y-%m-%d %H:%M:%S IST')}\n\n"
    
#     # IPv6 from JS client
#     if ipv6 and ipv6 != "null":
#         body += f"IPv6: {ipv6}\n"
#     else:
#         body += f"IPv6: Not available\n"
    
#     # All IP Info from ipapi
#     if ip_info:
#         body += f"\n--- IP Info ---\n"
#         body += f"IP: {ip_info.get('ip', 'N/A')}\n"
#         body += f"Version: {ip_info.get('version', 'N/A')}\n"
#         body += f"City: {ip_info.get('city', 'N/A')}\n"
#         body += f"Region: {ip_info.get('region', 'N/A')} ({ip_info.get('region_code', 'N/A')})\n"
#         body += f"Country: {ip_info.get('country_name', 'N/A')} ({ip_info.get('country_code', 'N/A')})\n"
#         body += f"Continent: {ip_info.get('continent_code', 'N/A')}\n"
#         body += f"Latitude: {ip_info.get('latitude', 'N/A')}\n"
#         body += f"Longitude: {ip_info.get('longitude', 'N/A')}\n"
#         body += f"Timezone: {ip_info.get('timezone', 'N/A')} (UTC {ip_info.get('utc_offset', 'N/A')})\n"
#         body += f"Network: {ip_info.get('network', 'N/A')}\n"
#         body += f"Organization: {ip_info.get('org', 'N/A')}\n"
#         body += f"AS: {ip_info.get('asn', 'N/A')}\n"
#         body += f"Postal: {ip_info.get('postal', 'N/A')}\n"
#         body += f"Languages: {ip_info.get('languages', 'N/A')}\n"
#         body += f"Currency: {ip_info.get('currency', 'N/A')} ({ip_info.get('currency_name', 'N/A')})\n\n"
    
#     # WebRTC IPs (skip invalid ones)
#     if webrtc_ips:
#         webrtc_ipv4 = webrtc_ips.get('ipv4', [])  
#         webrtc_ipv6 = webrtc_ips.get('ipv6', [])
        
#         # Filter valid IPv6 (must have at least 3 colons or proper format)
#         valid_ipv6 = [ip for ip in webrtc_ipv6 if ip.count(':') >= 2 and len(ip) > 8]
        
#         if webrtc_ipv4 or valid_ipv6:
#             body += f"WebRTC IPs:\n"
#             if webrtc_ipv4:
#                 body += f"  IPv4: {', '.join(webrtc_ipv4)}\n"
#             if valid_ipv6:
#                 body += f"  IPv6: {', '.join(valid_ipv6)}\n\n"
    
#     # Server IPs (fallback)
#     ipv4, ipv6_server = classify_ips(ips)
#     if ipv4:
#         body += f"Server IPv4: {', '.join(ipv4)}\n"
#     if ipv6_server:
#         body += f"Server IPv6: {', '.join(ipv6_server)}\n"
    
#     if device_info:
#         body += f"Device Info:\n"
#         body += f"  Platform: {device_info.get('platform', 'N/A')}\n"
#         body += f"  Language: {device_info.get('language', 'N/A')}\n"
#         body += f"  Screen: {device_info.get('screenWidth', 'N/A')}x{device_info.get('screenHeight', 'N/A')}\n"
#         body += f"  Timezone: {device_info.get('timezone', 'N/A')}\n"
#         body += f"  Referrer: {device_info.get('referrer', 'N/A')}\n"
#         body += f"  Page URL: {device_info.get('pageURL', 'N/A')}\n"
#         body += f"  User Agent: {device_info.get('userAgent', 'N/A')}\n\n"
    
#     if gps and gps.get('latitude'):
#         body += f"GPS Location: {gps.get('latitude')}, {gps.get('longitude')} (Accuracy: {gps.get('accuracy')}m)\n"
    
#     msg = Message(
#         subject="New Visit: Sachin's Profile(mocosn.in)",
#         recipients=["sachinpatel34241@gmail.com"],
#         body=body
#     )
#     mail.send(msg)



# New Html

def send_visitor_email(ips, device_info=None, ip_info=None, gps=None,
                       webrtc_ips=None, timestamp=None, ipv6=None):

    from datetime import datetime

    visit_time = timestamp or datetime.now().strftime('%Y-%m-%d %H:%M:%S IST')

    ipv4, ipv6_server = classify_ips(ips)

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                background: #0f172a;
                color: #ffffff;
                font-family: Arial, sans-serif;
                padding: 20px;
            }}

            .container {{
                max-width: 700px;
                margin: auto;
                background: #111827;
                border-radius: 16px;
                overflow: hidden;
                box-shadow: 0 0 25px rgba(0,0,0,0.4);
            }}

            .header {{
                background: linear-gradient(135deg, #2563eb, #7c3aed);
                padding: 25px;
                text-align: center;
            }}

            .header h1 {{
                margin: 0;
                font-size: 28px;
            }}

            .section {{
                padding: 20px;
                border-bottom: 1px solid #1f2937;
            }}

            .title {{
                font-size: 18px;
                margin-bottom: 15px;
                color: #60a5fa;
            }}

            .card {{
                background: #1e293b;
                padding: 14px;
                border-radius: 10px;
                margin-bottom: 10px;
            }}

            .label {{
                color: #93c5fd;
                font-weight: bold;
            }}

            .footer {{
                text-align: center;
                padding: 20px;
                font-size: 13px;
                color: #9ca3af;
            }}

            .badge {{
                display: inline-block;
                padding: 5px 10px;
                border-radius: 20px;
                background: #2563eb;
                color: white;
                font-size: 12px;
            }}

            a {{
                color: #60a5fa;
                text-decoration: none;
            }}
        </style>
    </head>

    <body>

    <div class="container">

        <div class="header">
            <h1>🔥 New Visitor Detected</h1>
            <p>Sachin's Profile Tracker</p>
        </div>

        <div class="section">
            <div class="title">📅 Visit Information</div>

            <div class="card">
                <span class="label">Visit Time:</span> {visit_time}
            </div>

            <div class="card">
                <span class="label">IPv6:</span>
                {ipv6 if ipv6 and ipv6 != "null" else "Not Available"}
            </div>
        </div>
    """

    # IP INFO
    if ip_info:
        html += f"""
        <div class="section">
            <div class="title">🌍 IP Information</div>

            <div class="card"><span class="label">IP:</span> {ip_info.get('ip', 'N/A')}</div>
            <div class="card"><span class="label">Version:</span> {ip_info.get('version', 'N/A')}</div>
            <div class="card"><span class="label">Country:</span> {ip_info.get('country_name', 'N/A')}</div>
            <div class="card"><span class="label">Region:</span> {ip_info.get('region', 'N/A')}</div>
            <div class="card"><span class="label">City:</span> {ip_info.get('city', 'N/A')}</div>
            <div class="card"><span class="label">Postal:</span> {ip_info.get('postal', 'N/A')}</div>
            <div class="card"><span class="label">Timezone:</span> {ip_info.get('timezone', 'N/A')}</div>
            <div class="card"><span class="label">Latitude:</span> {ip_info.get('latitude', 'N/A')}</div>
            <div class="card"><span class="label">Longitude:</span> {ip_info.get('longitude', 'N/A')}</div>
            <div class="card"><span class="label">Organization:</span> {ip_info.get('org', 'N/A')}</div>
            <div class="card"><span class="label">ASN:</span> {ip_info.get('asn', 'N/A')}</div>
        </div>
        """

    # WEBRTC
    if webrtc_ips:
        webrtc_ipv4 = webrtc_ips.get('ipv4', [])
        webrtc_ipv6 = webrtc_ips.get('ipv6', [])

        html += f"""
        <div class="section">
            <div class="title">📡 WebRTC IPs</div>

            <div class="card">
                <span class="label">IPv4:</span>
                {', '.join(webrtc_ipv4) if webrtc_ipv4 else 'N/A'}
            </div>

            <div class="card">
                <span class="label">IPv6:</span>
                {', '.join(webrtc_ipv6) if webrtc_ipv6 else 'N/A'}
            </div>
        </div>
        """

    # SERVER IPS
    html += f"""
    <div class="section">
        <div class="title">🖥 Server Detected IPs</div>

        <div class="card">
            <span class="label">IPv4:</span>
            {', '.join(ipv4) if ipv4 else 'N/A'}
        </div>

        <div class="card">
            <span class="label">IPv6:</span>
            {', '.join(ipv6_server) if ipv6_server else 'N/A'}
        </div>
    </div>
    """

    # DEVICE INFO
    if device_info:
        html += f"""
        <div class="section">
            <div class="title">📱 Device Information</div>

            <div class="card"><span class="label">Platform:</span> {device_info.get('platform', 'N/A')}</div>
            <div class="card"><span class="label">Language:</span> {device_info.get('language', 'N/A')}</div>
            <div class="card"><span class="label">Screen:</span> {device_info.get('screenWidth', 'N/A')}x{device_info.get('screenHeight', 'N/A')}</div>
            <div class="card"><span class="label">Timezone:</span> {device_info.get('timezone', 'N/A')}</div>
            <div class="card"><span class="label">Referrer:</span> {device_info.get('referrer', 'N/A')}</div>
            <div class="card"><span class="label">Page:</span> {device_info.get('pageURL', 'N/A')}</div>

            <div class="card">
                <span class="label">User Agent:</span><br><br>
                {device_info.get('userAgent', 'N/A')}
            </div>
        </div>
        """

    # GPS
    if gps and gps.get('latitude'):
        html += f"""
        <div class="section">
            <div class="title">📍 GPS Location</div>

            <div class="card">
                <span class="label">Latitude:</span> {gps.get('latitude')}
            </div>

            <div class="card">
                <span class="label">Longitude:</span> {gps.get('longitude')}
            </div>

            <div class="card">
                <span class="label">Accuracy:</span> {gps.get('accuracy')} meters
            </div>
        </div>
        """

    html += """
        <div class="footer">
            Generated automatically from mocosn.in visitor tracker
        </div>

    </div>
    </body>
    </html>
    """

    msg = Message(
        subject="🔥 New Visitor - mocosn.in",
        recipients=["sachinpatel34241@gmail.com"]
    )

    msg.html = html

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

# if __name__ == '__main__':
#     app.run(debug=True)