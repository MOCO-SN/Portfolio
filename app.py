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
    <meta charset="UTF-8">

    <style>

    body {{
        margin: 0;
        padding: 30px;
        background: #030712;
        font-family: Arial, sans-serif;
        color: white;
    }}

    .main {{
        max-width: 850px;
        margin: auto;
    }}

    .container {{
        background: #0f172a;
        border-radius: 30px;
        overflow: hidden;
        border: 1px solid rgba(255,255,255,0.08);
        box-shadow:
            0 0 50px rgba(59,130,246,0.18),
            0 0 120px rgba(139,92,246,0.12);
    }}

    .hero {{
        padding: 50px 35px;
        text-align: center;
        background:
            radial-gradient(circle at top left, #2563eb, transparent 40%),
            radial-gradient(circle at bottom right, #7c3aed, transparent 40%),
            linear-gradient(135deg, #111827, #0f172a);
    }}

    .hero-icon {{
        font-size: 58px;
        margin-bottom: 15px;
    }}

    .hero h1 {{
        margin: 0;
        font-size: 34px;
        font-weight: bold;
        color: white;
    }}

    .hero p {{
        margin-top: 12px;
        color: #cbd5e1;
        font-size: 15px;
    }}

    .live {{
        display: inline-block;
        margin-top: 18px;
        background: linear-gradient(135deg,#2563eb,#7c3aed);
        padding: 8px 16px;
        border-radius: 999px;
        font-size: 12px;
        font-weight: bold;
    }}

    .content {{
        padding: 30px;
    }}

    .section {{
        margin-bottom: 35px;
    }}

    .section-title {{
        font-size: 20px;
        font-weight: bold;
        color: #60a5fa;
        margin-bottom: 18px;
    }}

    .grid {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(240px,1fr));
        gap: 15px;
    }}

    .card {{
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 20px;
        padding: 18px;
    }}

    .label {{
        font-size: 12px;
        color: #94a3b8;
        margin-bottom: 10px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }}

    .value {{
        font-size: 15px;
        font-weight: bold;
        color: white;
        word-break: break-word;
    }}

    .large-card {{
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 20px;
        padding: 20px;
        margin-top: 15px;
    }}

    .footer {{
        text-align: center;
        padding: 25px;
        border-top: 1px solid rgba(255,255,255,0.06);
        color: #64748b;
        font-size: 13px;
    }}

    .highlight {{
        color: #60a5fa;
    }}

    @media(max-width:700px) {{

        body {{
            padding: 10px;
        }}

        .hero {{
            padding: 35px 20px;
        }}

        .hero h1 {{
            font-size: 26px;
        }}

        .content {{
            padding: 18px;
        }}

    }}

    </style>
    </head>

    <body>

    <div class="main">

    <div class="container">

    <!-- HERO -->
    <div class="hero">

    <div class="hero-icon">🔥</div>

    <h1>
        New Visitor Detected
    </h1>

    <p>
        Real-time visitor analytics from mocosn.in
    </p>

    <div class="live">
        ● LIVE TRACKING ENABLED
    </div>

    </div>

    <div class="content">

    <!-- VISIT -->
    <div class="section">

    <div class="section-title">
    📅 Visit Information
    </div>

    <div class="grid">

    <div class="card">
    <div class="label">Visit Time</div>
    <div class="value">{visit_time}</div>
    </div>

    <div class="card">
    <div class="label">IPv6</div>
    <div class="value">
    {ipv6 if ipv6 and ipv6 != "null" else "Not Available"}
    </div>
    </div>

    </div>
    </div>
    """

    # IP INFO
    if ip_info:
        html += f"""
        <div class="section">

        <div class="section-title">
        🌍 IP Information
        </div>

        <div class="grid">

        <div class="card">
        <div class="label">IP Address</div>
        <div class="value">{ip_info.get('ip', 'N/A')}</div>
        </div>

        <div class="card">
        <div class="label">Country</div>
        <div class="value">{ip_info.get('country_name', 'N/A')}</div>
        </div>

        <div class="card">
        <div class="label">Region</div>
        <div class="value">{ip_info.get('region', 'N/A')}</div>
        </div>

        <div class="card">
        <div class="label">City</div>
        <div class="value">{ip_info.get('city', 'N/A')}</div>
        </div>

        <div class="card">
        <div class="label">Timezone</div>
        <div class="value">{ip_info.get('timezone', 'N/A')}</div>
        </div>

        <div class="card">
        <div class="label">ISP / Org</div>
        <div class="value">{ip_info.get('org', 'N/A')}</div>
        </div>

        </div>

        </div>
        """

    # WEBRTC
    if webrtc_ips:
        html += f"""
        <div class="section">

        <div class="section-title">
        📡 WebRTC Information
        </div>

        <div class="grid">

        <div class="card">
        <div class="label">IPv4</div>
        <div class="value">
        {', '.join(webrtc_ips.get('ipv4', [])) if webrtc_ips.get('ipv4') else 'N/A'}
        </div>
        </div>

        <div class="card">
        <div class="label">IPv6</div>
        <div class="value">
        {', '.join(webrtc_ips.get('ipv6', [])) if webrtc_ips.get('ipv6') else 'N/A'}
        </div>
        </div>

        </div>

        </div>
        """

    # DEVICE INFO
    if device_info:
        html += f"""
        <div class="section">

        <div class="section-title">
        📱 Device Information
        </div>

        <div class="grid">

        <div class="card">
        <div class="label">Platform</div>
        <div class="value">{device_info.get('platform', 'N/A')}</div>
        </div>

        <div class="card">
        <div class="label">Language</div>
        <div class="value">{device_info.get('language', 'N/A')}</div>
        </div>

        <div class="card">
        <div class="label">Screen Size</div>
        <div class="value">
        {device_info.get('screenWidth', 'N/A')} × {device_info.get('screenHeight', 'N/A')}
        </div>
        </div>

        <div class="card">
        <div class="label">Timezone</div>
        <div class="value">{device_info.get('timezone', 'N/A')}</div>
        </div>

        </div>

        <div class="large-card">

        <div class="label">
        User Agent
        </div>

        <div class="value" style="font-size:13px; line-height:1.8;">
        {device_info.get('userAgent', 'N/A')}
        </div>

        </div>

        </div>
        """

    # GPS
    if gps and gps.get('latitude'):
        html += f"""
        <div class="section">

        <div class="section-title">
        📍 GPS Location
        </div>

        <div class="grid">

        <div class="card">
        <div class="label">Latitude</div>
        <div class="value">{gps.get('latitude')}</div>
        </div>

        <div class="card">
        <div class="label">Longitude</div>
        <div class="value">{gps.get('longitude')}</div>
        </div>

        <div class="card">
        <div class="label">Accuracy</div>
        <div class="value">{gps.get('accuracy')} meters</div>
        </div>

        </div>

        </div>
    """

    html += """

    </div>

    <div class="footer">
        Generated automatically by mocosn.in analytics system
    </div>

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