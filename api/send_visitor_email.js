importResend from "resend";

const resend = new Resend(process.env.RESEND_API_KEY);

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ success: false, message: 'Method not allowed' });
  }

  const data = req.body;

  if (!data) {
    return res.status(400).json({ success: false, message: 'No data provided' });
  }

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
                <tr><td><b>Organization</b></td><td>${data.org || 'N/A'}</td></tr>
                <tr><td><b>Device</b></td><td>${data.platform || 'N/A'}</td></tr>
                <tr><td><b>Screen</b></td><td>${data.screenWidth || 'N/A'} x ${data.screenHeight || 'N/A'}</td></tr>
                <tr><td><b>Language</b></td><td>${data.language || 'N/A'}</td></tr>
                <tr><td><b>Referrer</b></td><td>${data.referrer || 'Direct'}</td></tr>
                <tr><td><b>Time</b></td><td>${data.timestamp || 'N/A'}</td></tr>
            </table>
        </div>
    </div>
</body>
</html>`;

  try {
    const email = await resend.emails.send({
      from: 'sachinprofile <onboarding@resend.dev>',
      to: ['sachinpatel34241@gmail.com'],
      subject: '🔔 New Visitor on sachinprofile.in',
      html: emailHtml,
    });

    console.log('✅ Email sent:', email);
    return res.status(200).json({ success: true, message: 'Email sent', data: email });
  } catch (error) {
    console.error('❌ Email error:', error);
    return res.status(500).json({ success: false, message: 'Failed to send email', error: error.message });
  }
}