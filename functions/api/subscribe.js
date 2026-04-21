/**
 * Newsletter subscription endpoint for The Workspace Pro.
 * POST /api/subscribe
 * 
 * Expects form data with:
 *   - email: valid email address
 *   - consent: "on" if checkbox checked
 *   - referrer: optional page URL
 * 
 * Returns JSON:
 *   { success: boolean, message: string, error?: string }
 */
export async function onRequestPost(context) {
  const { request, env } = context;
  
  // CORS headers for cross‑origin requests (if needed later)
  const corsHeaders = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Content-Type': 'application/json',
  };
  
  // Handle preflight OPTIONS request
  if (request.method === 'OPTIONS') {
    return new Response(null, { headers: corsHeaders });
  }
  
  try {
    // Parse form data
    const formData = await request.formData();
    const email = formData.get('email')?.toString().trim().toLowerCase();
    const consent = formData.get('consent') === 'on';
    const referrer = formData.get('referrer')?.toString() || '';
    const userAgent = request.headers.get('user-agent') || '';
    
    // Basic validation
    if (!email) {
      return Response.json(
        { success: false, message: 'Email is required', error: 'VALIDATION' },
        { status: 400, headers: corsHeaders }
      );
    }
    
    // Simple email regex (good enough for form validation)
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      return Response.json(
        { success: false, message: 'Please enter a valid email address', error: 'VALIDATION' },
        { status: 400, headers: corsHeaders }
      );
    }
    
    if (!consent) {
      return Response.json(
        { success: false, message: 'You must agree to the privacy policy', error: 'CONSENT' },
        { status: 400, headers: corsHeaders }
      );
    }
    
    // Hash IP for privacy (SHA‑256 of last octet only)
    const ip = request.headers.get('cf-connecting-ip') || '';
    const ipHash = ip ? await hashIP(ip) : null;
    
    // Insert into D1 database
    const db = env.SUBSCRIPTIONS_DB;
    
    try {
      const result = await db.prepare(
        `INSERT INTO subscribers (email, consent, ip_hash, user_agent, referrer, source)
         VALUES (?, ?, ?, ?, ?, 'homepage')`
      ).bind(email, consent ? 1 : 0, ipHash, userAgent, referrer).run();
      
      if (result.success) {
        return Response.json(
          { success: true, message: 'Thank you! You’re subscribed.' },
          { headers: corsHeaders }
        );
      } else {
        // Likely duplicate email (UNIQUE constraint)
        return Response.json(
          { success: false, message: 'This email is already subscribed', error: 'DUPLICATE' },
          { status: 409, headers: corsHeaders }
        );
      }
    } catch (dbError) {
      console.error('Database error:', dbError);
      // Check if it's a duplicate constraint violation
      if (dbError.message && dbError.message.includes('UNIQUE')) {
        return Response.json(
          { success: false, message: 'This email is already subscribed', error: 'DUPLICATE' },
          { status: 409, headers: corsHeaders }
        );
      }
      throw dbError; // Re‑throw for generic error handling
    }
    
  } catch (error) {
    console.error('Subscription error:', error);
    return Response.json(
      { success: false, message: 'Something went wrong. Please try again later.', error: 'SERVER' },
      { status: 500, headers: corsHeaders }
    );
  }
}

/**
 * Hash IP address for privacy (SHA‑256 of the IP).
 * In production you might only hash the last octet or use a salt.
 */
async function hashIP(ip) {
  // Simple approach: hash the entire IP
  const encoder = new TextEncoder();
  const data = encoder.encode(ip);
  const hashBuffer = await crypto.subtle.digest('SHA-256', data);
  const hashArray = Array.from(new Uint8Array(hashBuffer));
  return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
}