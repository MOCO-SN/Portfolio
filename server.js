import http from 'http';
import fs from 'fs';
import path from 'path';
import { Resend } from 'resend';

const resend = new Resend({ apiKey: process.env.RESEND_API_KEY || 're_test_xxx' });

const PORT = process.env.PORT || 3000;

const MIME_TYPES = {
  '.html': 'text/html',
  '.js': 'application/javascript',
  '.css': 'text/css',
  '.json': 'application/json',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.pdf': 'application/pdf',
  '.svg': 'image/svg+xml',
};

async function sendVisitorEmail(data) {
  const emailHtml = `
<!DOCTYPE html>
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
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h2>🔔 New Profile Visitor</h2>
        </div>
        <div class="content">
            <table>
                <tr><th>Field</th><th>Details</th></tr>
                <tr><td><b>IP Address</b></td><td>${data.ip || 'N/A'}</td></tr>
                <tr><td><b>City</b></td><td>${data.city || 'N/A'}</td></tr>
                <tr><td><b>Region</b></td><td>${data.region || 'N/A'}</td></tr>
                <tr><td><b>Country</b></td><td>${data.country || 'N/A'}</td></tr>
                <tr><td><b>Device</b></td><td>${data.platform || 'N/A'}</td></tr>
                <tr><td><b>Screen</b></td><td>${data.screenWidth || 'N/A'} x ${data.screenHeight || 'N/A'}</td></tr>
                <tr><td><b>Time</b></td><td>${data.timestamp || 'N/A'}</td></tr>
            </table>
        </div>
    </div>
</body>
</html>`;

  try {
    const email = await resend.emails.send({
      from: 'Visitor <onboarding@resend.dev>',
      to: ['sachinpatel34241@gmail.com'],
      subject: '🔔 New Visitor on sachinprofile.in',
      html: emailHtml,
    });
    console.log('✅ Email sent:', email);
    return { success: true, data: email };
  } catch (error) {
    console.error('❌ Email error:', error);
    return { success: false, error: error.message };
  }
}

const server = http.createServer(async (req, res) => {
  console.log(`${req.method} ${req.url}`);

  // API route for sending email
  if (req.url === '/api/send_visitor_email' && req.method === 'POST') {
    let body = '';
    req.on('data', chunk => body += chunk);
    req.on('end', async () => {
      try {
        const data = JSON.parse(body);
        const result = await sendVisitorEmail(data);
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify(result));
      } catch (e) {
        res.writeHead(400, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ success: false, error: e.message }));
      }
    });
    return;
  }

  // Serve static files
  let filePath = req.url === '/' ? '/index.html' : req.url;
  const ext = path.extname(filePath);
  const contentType = MIME_TYPES[ext] || 'text/plain';
  
  fs.readFile(filePath, (err, content) => {
    if (err) {
      res.writeHead(404);
      res.end('Not Found');
    } else {
      res.writeHead(200, { 'Content-Type': contentType });
      res.end(content);
    }
  });
});

server.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
});