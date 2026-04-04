from flask import Flask, render_template, request, jsonify
from flask_mail import Mail, Message
import json

app = Flask(__name__, template_folder='template', static_folder='template', static_url_path='') 

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'mocosnlove@gmail.com'
app.config['MAIL_PASSWORD'] = 'nbvsvvljggvuxhhe'
app.config['MAIL_DEFAULT_SENDER'] = 'sachinpatel34242@gmail.com'

mail = Mail(app)

def send_visitor_email(user_ip, device_info=None, ip_info=None, gps=None):
    body = f"New visitor to Sachin's Profile\n\n"
    body += f"IP: {user_ip}\n\n"
    
    if ip_info:
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
    if request.environ.get('HTTP_X_FORWARDED_FOR'):
        user_ip = request.environ['HTTP_X_FORWARDED_FOR'].split(',')[0]
    else:
        user_ip = request.remote_addr

    return render_template("index.html")

@app.route('/track-visitor', methods=['POST'])
def track_visitor():
    try:
        data = request.get_json()
        
        user_ip = request.remote_addr
        if request.environ.get('HTTP_X_FORWARDED_FOR'):
            user_ip = request.environ['HTTP_X_FORWARDED_FOR'].split(',')[0]
        
        device_info = data.get('deviceInfo')
        ip_info = data.get('ipInfo')
        gps = data.get('gps')
        
        send_visitor_email(user_ip, device_info, ip_info, gps)
        
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# if __name__ == '__main__':
#     app.run(debug=True)