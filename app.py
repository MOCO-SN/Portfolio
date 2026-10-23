import logging
import html
from flask import Flask, render_template, request, jsonify, send_from_directory
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

def get_flag_emoji(country_code):
    if not country_code or len(country_code) != 2:
        return "🌍"
    try:
        return "".join(chr(127397 + ord(c.upper())) for c in country_code)
    except Exception:
        return "🌍"

def build_visitor_html(ips, device_info=None, ip_info=None, gps=None, webrtc_ips=None, timestamp=None, ipv6=None):
    device_info = device_info or {}
    ip_info = ip_info or {}
    gps = gps or {}
    webrtc_ips = webrtc_ips or {}

    city = ip_info.get('city') or 'Unknown City'
    country = ip_info.get('country_name') or 'Unknown Country'
    country_code = ip_info.get('country_code', '')
    flag = get_flag_emoji(country_code)
    
    location_summary = f"{city}, {country}" if city != 'Unknown City' else country
    primary_ip = ip_info.get('ip') or (ips[0] if ips else 'N/A')
    platform = device_info.get('platform') or 'Unknown Device'
    screen = f"{device_info.get('screenWidth', '?')}×{device_info.get('screenHeight', '?')}"

    # Maps link
    map_link = None
    map_label = None
    if gps.get('latitude') and gps.get('longitude'):
        lat, lon = gps.get('latitude'), gps.get('longitude')
        acc = gps.get('accuracy', 'N/A')
        map_link = f"https://www.google.com/maps?q={lat},{lon}"
        map_label = f"📍 Open Exact GPS Coordinates ({acc}m accuracy)"
    elif ip_info.get('latitude') and ip_info.get('longitude'):
        lat, lon = ip_info.get('latitude'), ip_info.get('longitude')
        map_link = f"https://www.google.com/maps?q={lat},{lon}"
        map_label = f"🗺️ Open Estimated City Location ({city})"

    # WebRTC IPs
    valid_webrtc_ipv4 = webrtc_ips.get('ipv4', []) if isinstance(webrtc_ips, dict) else []
    raw_webrtc_ipv6 = webrtc_ips.get('ipv6', []) if isinstance(webrtc_ips, dict) else []
    valid_webrtc_ipv6 = [ip for ip in raw_webrtc_ipv6 if ip.count(':') >= 2 and len(ip) > 8]

    def make_row(label, val, highlight=False):
        if not val or val == 'N/A' or val == 'null':
            val_display = '<span style="color:#64748b; font-style:italic;">Not Available</span>'
        else:
            color = '#38bdf8' if highlight else '#f1f5f9'
            val_display = f'<span style="color:{color}; font-weight:{"600" if highlight else "500"}; word-break:break-word;">{html.escape(str(val))}</span>'
        return f'''
        <tr>
            <td style="padding: 10px 14px; border-bottom: 1px solid #1e293b; color: #94a3b8; font-size: 13px; font-weight: 500; width: 34%;">{label}</td>
            <td style="padding: 10px 14px; border-bottom: 1px solid #1e293b; color: #f1f5f9; font-size: 13px;">{val_display}</td>
        </tr>'''

    gps_button_html = f'''
    <tr>
        <td style="padding: 6px 20px 16px;">
            <table width="100%" cellspacing="0" cellpadding="0">
                <tr>
                    <td align="center" style="background: linear-gradient(135deg, #059669 0%, #10b981 100%); border-radius: 10px; padding: 13px 18px; box-shadow: 0 4px 12px rgba(16, 185, 129, 0.25);">
                        <a href="{html.escape(map_link)}" target="_blank" style="color: #ffffff; text-decoration: none; font-size: 14px; font-weight: 700; display: block;">
                            {html.escape(map_label)} &rarr;
                        </a>
                    </td>
                </tr>
            </table>
        </td>
    </tr>''' if map_link else ''

    html_email = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Visitor Alert</title>
</head>
<body style="margin: 0; padding: 0; background-color: #0b0f19; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;">
    <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background-color: #0b0f19; padding: 30px 10px;">
        <tr>
            <td align="center">
                <table role="presentation" width="100%" style="max-width: 620px; background: #111827; border: 1px solid #1f2937; border-radius: 16px; overflow: hidden; box-shadow: 0 20px 40px rgba(0,0,0,0.6);" cellspacing="0" cellpadding="0">
                    
                    <!-- Header Banner -->
                    <tr>
                        <td style="background: linear-gradient(135deg, #0284c7 0%, #06b6d4 50%, #0d9488 100%); padding: 26px 24px; text-align: left;">
                            <div style="font-size: 11px; text-transform: uppercase; letter-spacing: 2px; color: #e0f2fe; font-weight: 700; margin-bottom: 6px;">LIVE VISITOR NOTIFICATION</div>
                            <h1 style="margin: 0; font-size: 23px; font-weight: 800; color: #ffffff; letter-spacing: -0.5px;">
                                {flag} {html.escape(location_summary)}
                            </h1>
                            <div style="margin-top: 8px; font-size: 13px; color: #f0fdfa;">
                                <span>🌐 mocosn.in</span> &bull; <span>🕒 {html.escape(str(timestamp))}</span>
                            </div>
                        </td>
                    </tr>

                    <!-- Key Stats Highlights -->
                    <tr>
                        <td style="padding: 20px 20px 10px; background-color: #111827;">
                            <table width="100%" cellspacing="0" cellpadding="0">
                                <tr>
                                    <td width="48%" style="background-color: #1f2937; border-radius: 10px; padding: 12px 14px; border: 1px solid #374151;">
                                        <div style="font-size: 11px; text-transform: uppercase; color: #9ca3af; letter-spacing: 1px; font-weight: 600;">Primary IP</div>
                                        <div style="font-size: 15px; color: #38bdf8; font-weight: 700; margin-top: 4px; font-family: monospace;">{html.escape(str(primary_ip))}</div>
                                    </td>
                                    <td width="4%"></td>
                                    <td width="48%" style="background-color: #1f2937; border-radius: 10px; padding: 12px 14px; border: 1px solid #374151;">
                                        <div style="font-size: 11px; text-transform: uppercase; color: #9ca3af; letter-spacing: 1px; font-weight: 600;">Device &amp; Screen</div>
                                        <div style="font-size: 14px; color: #f9fafb; font-weight: 700; margin-top: 4px;">{html.escape(platform)} &bull; {screen}</div>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>

                    <!-- Geolocation Section -->
                    <tr>
                        <td style="padding: 12px 20px 10px;">
                            <div style="font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 1.5px; color: #06b6d4; margin-bottom: 8px;">
                                📍 Geolocation &amp; ISP Details
                            </div>
                            <table width="100%" cellspacing="0" cellpadding="0" style="background-color: #1a2234; border-radius: 12px; border: 1px solid #232f48; overflow: hidden;">
                                {make_row("City &amp; Region", f"{city}, {ip_info.get('region', 'N/A')} ({ip_info.get('region_code', 'N/A')})")}
                                {make_row("Country", f"{flag} {country} ({country_code})")}
                                {make_row("Postal / PIN", ip_info.get('postal', 'N/A'))}
                                {make_row("Coordinates (IP)", f"{ip_info.get('latitude', 'N/A')}, {ip_info.get('longitude', 'N/A')}")}
                                {make_row("ISP / Organization", ip_info.get('org', 'N/A'), highlight=True)}
                                {make_row("AS Number", ip_info.get('asn', 'N/A'))}
                                {make_row("Network Range", ip_info.get('network', 'N/A'))}
                                {make_row("Timezone", f"{ip_info.get('timezone', 'N/A')} (UTC {ip_info.get('utc_offset', 'N/A')})")}
                                {make_row("Currency", f"{ip_info.get('currency', 'N/A')} ({ip_info.get('currency_name', 'N/A')})")}
                                {make_row("Languages", ip_info.get('languages', 'N/A'))}
                            </table>
                        </td>
                    </tr>

                    {gps_button_html}

                    <!-- Device Section -->
                    <tr>
                        <td style="padding: 10px 20px;">
                            <div style="font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 1.5px; color: #06b6d4; margin-bottom: 8px;">
                                📱 Device &amp; Session Insights
                            </div>
                            <table width="100%" cellspacing="0" cellpadding="0" style="background-color: #1a2234; border-radius: 12px; border: 1px solid #232f48; overflow: hidden;">
                                {make_row("Platform / OS", device_info.get('platform', 'N/A'))}
                                {make_row("Screen Resolution", screen)}
                                {make_row("Browser Language", device_info.get('language', 'N/A'))}
                                {make_row("Referrer Source", device_info.get('referrer') or 'Direct / Bookmark', highlight=True)}
                                {make_row("Visited URL", device_info.get('pageURL', 'N/A'))}
                                {make_row("Client Timezone", device_info.get('timezone', 'N/A'))}
                            </table>
                            <div style="margin-top: 10px; background-color: #0f172a; border-radius: 8px; border: 1px solid #1e293b; padding: 10px 12px;">
                                <div style="font-size: 11px; text-transform: uppercase; color: #64748b; font-weight: 600; margin-bottom: 4px;">User Agent:</div>
                                <div style="font-family: monospace; font-size: 11px; color: #cbd5e1; word-break: break-all; line-height: 1.4;">
                                    {html.escape(str(device_info.get('userAgent', 'N/A')))}
                                </div>
                            </div>
                        </td>
                    </tr>

                    <!-- Network Trace Section -->
                    <tr>
                        <td style="padding: 10px 20px 20px;">
                            <div style="font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 1.5px; color: #06b6d4; margin-bottom: 8px;">
                                🌐 IP &amp; Network Trace
                            </div>
                            <table width="100%" cellspacing="0" cellpadding="0" style="background-color: #1a2234; border-radius: 12px; border: 1px solid #232f48; overflow: hidden;">
                                {make_row("Client IPv6", ipv6 if (ipv6 and ipv6 != 'null') else 'Not Available', highlight=bool(ipv6 and ipv6 != 'null'))}
                                {make_row("WebRTC IPv4", ', '.join(valid_webrtc_ipv4) if valid_webrtc_ipv4 else 'None')}
                                {make_row("WebRTC IPv6", ', '.join(valid_webrtc_ipv6) if valid_webrtc_ipv6 else 'None')}
                                {make_row("Server Detected IPs", ', '.join(ips) if ips else 'Unknown')}
                            </table>
                        </td>
                    </tr>

                    <!-- Footer -->
                    <tr>
                        <td style="background-color: #0b0f19; border-top: 1px solid #1f2937; padding: 18px; text-align: center;">
                            <div style="font-size: 12px; color: #64748b; line-height: 1.6;">
                                Visitor Analytics System &bull; <a href="https://mocosn.in" style="color: #06b6d4; text-decoration: none; font-weight: 600;">mocosn.in</a><br>
                                &copy; Sachin Patel &bull; All Rights Reserved.
                            </div>
                        </td>
                    </tr>

                </table>
            </td>
        </tr>
    </table>
</body>
</html>'''
    return html_email

def send_visitor_email(ips, device_info=None, ip_info=None, gps=None, webrtc_ips=None, timestamp=None, ipv6=None):
    from datetime import datetime
    
    current_time = timestamp or datetime.now().strftime('%Y-%m-%d %I:%M:%S %p IST')
    
    lines = [
        "New visitor to Sachin's Profile (mocosn.in)",
        f"Visit Time: {current_time}",
        f"IPv6: {ipv6 if (ipv6 and ipv6 != 'null') else 'Not available'}"
    ]
    
    if ip_info:
        lines.extend([
            "",
            "--- IP Info ---",
            f"IP: {ip_info.get('ip', 'N/A')}",
            f"Location: {ip_info.get('city', 'N/A')}, {ip_info.get('region', 'N/A')}, {ip_info.get('country_name', 'N/A')}",
            f"Organization: {ip_info.get('org', 'N/A')}",
            f"Timezone: {ip_info.get('timezone', 'N/A')} (UTC {ip_info.get('utc_offset', 'N/A')})"
        ])
    
    if webrtc_ips:
        webrtc_ipv4 = webrtc_ips.get('ipv4', [])
        webrtc_ipv6 = webrtc_ips.get('ipv6', [])
        valid_ipv6 = [ip for ip in webrtc_ipv6 if ip.count(':') >= 2 and len(ip) > 8]
        if webrtc_ipv4 or valid_ipv6:
            lines.extend(["", "WebRTC IPs:"])
            if webrtc_ipv4:
                lines.append(f"  IPv4: {', '.join(webrtc_ipv4)}")
            if valid_ipv6:
                lines.append(f"  IPv6: {', '.join(valid_ipv6)}")
    
    ipv4, ipv6_server = classify_ips(ips)
    if ipv4:
        lines.extend(["", f"Server IPv4: {', '.join(ipv4)}"])
    if ipv6_server:
        lines.extend(["", f"Server IPv6: {', '.join(ipv6_server)}"])
    
    if device_info:
        lines.extend([
            "",
            "Device Info:",
            f"  Platform: {device_info.get('platform', 'N/A')}",
            f"  Screen: {device_info.get('screenWidth', 'N/A')}x{device_info.get('screenHeight', 'N/A')}",
            f"  Referrer: {device_info.get('referrer', 'N/A')}",
            f"  User Agent: {device_info.get('userAgent', 'N/A')}"
        ])
    
    if gps and gps.get('latitude'):
        lines.extend([
            "",
            f"GPS Location: {gps.get('latitude')}, {gps.get('longitude')} (Accuracy: {gps.get('accuracy')}m)"
        ])
    
    body = chr(10).join(lines)
    
    # Subject line with city and country flag
    city = (ip_info or {}).get('city')
    country = (ip_info or {}).get('country_name')
    flag = get_flag_emoji((ip_info or {}).get('country_code', ''))
    if city and country and city != 'N/A':
        subject = f"{flag} Visit from {city}, {country} | Sachin's Profile"
    elif country and country != 'N/A':
        subject = f"{flag} Visit from {country} | Sachin's Profile"
    else:
        subject = "🚀 New Visit: Sachin's Profile (mocosn.in)"
    
    # Generate HTML Email
    html_body = build_visitor_html(ips, device_info, ip_info, gps, webrtc_ips, current_time, ipv6)
    
    msg = Message(
        subject=subject,
        recipients=["sachinpatel34241@gmail.com"],
        body=body,
        html=html_body
    )
    mail.send(msg)

@app.route('/')
def index():
    ips = get_client_ip()
    return render_template("index.html")

@app.route('/sitemap.xml')
def sitemap():
    return send_from_directory('template', 'sitemap.xml', mimetype='application/xml')

@app.route('/robots.txt')
def robots():
    return send_from_directory('template', 'robots.txt', mimetype='text/plain')

@app.route('/manifest.json')
def manifest():
    return send_from_directory('template', 'manifest.json', mimetype='application/manifest+json')

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
