<?php
header('Content-Type: application/json');

function sendVisitorEmail($data) {
    $to = 'sachinpatel34241@gmail.com';
    $subject = '🔔 New Visitor on sachinprofile.in';
    
    $message = "
    <html>
    <head>
        <style>
            body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
            .container { max-width: 600px; margin: 0 auto; padding: 20px; }
            .header { background: #06c1db; color: white; padding: 20px; text-align: center; }
            .content { padding: 20px; background: #f9f9f9; }
            table { width: 100%; border-collapse: collapse; }
            th, td { padding: 10px; text-align: left; border-bottom: 1px solid #ddd; }
            th { background: #eee; }
            .footer { text-align: center; padding: 10px; font-size: 12px; color: #777; }
        </style>
    </head>
    <body>
        <div class='container'>
            <div class='header'>
                <h2>🔔 New Profile Visitor</h2>
            </div>
            <div class='content'>
                <table>
                    <tr><th>Field</th><th>Details</th></tr>
                    <tr><td><b>IP Address</b></td><td>" . ($data['ip'] ?? 'N/A') . "</td></tr>
                    <tr><td><b>City</b></td><td>" . ($data['city'] ?? 'N/A') . "</td></tr>
                    <tr><td><b>Region</b></td><td>" . ($data['region'] ?? 'N/A') . "</td></tr>
                    <tr><td><b>Country</b></td><td>" . ($data['country'] ?? 'N/A') . "</td></tr>
                    <tr><td><b>Organization</b></td><td>" . ($data['org'] ?? 'N/A') . "</td></tr>
                    <tr><td><b>Device</b></td><td>" . ($data['platform'] ?? 'N/A') . "</td></tr>
                    <tr><td><b>Browser</b></td><td>" . ($data['userAgent'] ?? 'N/A') . "</td></tr>
                    <tr><td><b>Screen</b></td><td>" . ($data['screenWidth'] ?? 'N/A') . " x " . ($data['screenHeight'] ?? 'N/A') . "</td></tr>
                    <tr><td><b>Language</b></td><td>" . ($data['language'] ?? 'N/A') . "</td></tr>
                    <tr><td><b>Referrer</b></td><td>" . ($data['referrer'] ?? 'Direct') . "</td></tr>
                    <tr><td><b>Page URL</b></td><td>" . ($data['pageURL'] ?? 'N/A') . "</td></tr>
                    <tr><td><b>Time</b></td><td>" . ($data['timestamp'] ?? 'N/A') . "</td></tr>
                </table>
            </div>
            <div class='footer'>
                <p>Sent from sachinprofile.in visitor tracking system</p>
            </div>
        </div>
    </body>
    </html>";

    $headers = "MIME-Version: 1.0" . "\r\n";
    $headers .= "Content-type:text/html;charset=UTF-8" . "\r\n";
    $headers .= "From: noreply@sachinprofile.in" . "\r\n";
    $headers .= "X-Mailer: PHP/" . phpversion();

    return mail($to, $subject, $message, $headers);
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $json = file_get_contents('php://input');
    $data = json_decode($json, true);
    
    if ($data && sendVisitorEmail($data)) {
        echo json_encode(['success' => true, 'message' => 'Email sent successfully']);
    } else {
        echo json_encode(['success' => false, 'message' => 'Failed to send email']);
    }
} else {
    echo json_encode(['success' => false, 'message' => 'Invalid request method']);
}
?>