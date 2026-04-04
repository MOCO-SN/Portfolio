export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ success: false, message: 'Method not allowed' });
  }

  const data = req.body;

  if (!data) {
    return res.status(400).json({ success: false, message: 'No data provided' });
  }

  const visitorInfo = {
    ip: data.ip || 'N/A',
    city: data.city || 'N/A',
    region: data.region || 'N/A',
    country: data.country || 'N/A',
    org: data.org || 'N/A',
    platform: data.platform || 'N/A',
    userAgent: data.userAgent ? data.userAgent.substring(0, 80) + '...' : 'N/A',
    screen: `${data.screenWidth || 'N/A'} x ${data.screenHeight || 'N/A'}`,
    language: data.language || 'N/A',
    referrer: data.referrer || 'Direct',
    pageURL: data.pageURL || 'N/A',
    timestamp: data.timestamp || 'N/A'
  };

  console.log('🔔 NEW VISITOR:', JSON.stringify(visitorInfo, null, 2));

  return res.status(200).json({ 
    success: true, 
    message: 'Visitor notification logged',
    visitor: visitorInfo
  });
}