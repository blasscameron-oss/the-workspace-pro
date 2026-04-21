/**
 * Admin endpoint for managing subscribers.
 * Requires X-Admin-Token header matching env.ADMIN_TOKEN.
 * 
 * GET /api/admin/subscribers?page=1&limit=50
 * DELETE /api/admin/subscribers/:id
 * GET /api/admin/subscribers/export (CSV)
 */
export async function onRequest(context) {
  const { request, env } = context;
  const { method } = request;
  
  // Verify admin token
  const adminToken = request.headers.get('X-Admin-Token') || 
                     new URL(request.url).searchParams.get('token');
  
  if (!adminToken || adminToken !== env.ADMIN_TOKEN) {
    return Response.json(
      { success: false, message: 'Unauthorized' },
      { status: 401 }
    );
  }
  
  const db = env.SUBSCRIPTIONS_DB;
  
  // Route handlers
  if (method === 'GET') {
    const url = new URL(request.url);
    const pathname = url.pathname;
    
    // Export CSV
    if (pathname.endsWith('/export')) {
      return await handleExport(db);
    }
    
    // List subscribers
    return await handleList(db, url);
  }
  
  if (method === 'DELETE') {
    return await handleDelete(db, request);
  }
  
  return Response.json(
    { success: false, message: 'Method not allowed' },
    { status: 405 }
  );
}

/**
 * List subscribers with pagination
 */
async function handleList(db, url) {
  const page = parseInt(url.searchParams.get('page') || '1');
  const limit = parseInt(url.searchParams.get('limit') || '50');
  const offset = (page - 1) * limit;
  
  try {
    // Get total count
    const countResult = await db.prepare('SELECT COUNT(*) as total FROM subscribers').first();
    const total = countResult?.total || 0;
    
    // Get paginated subscribers
    const subscribers = await db.prepare(
      `SELECT id, email, consent, subscribed_at, ip_hash, user_agent, referrer, source
       FROM subscribers
       ORDER BY subscribed_at DESC
       LIMIT ? OFFSET ?`
    ).bind(limit, offset).all();
    
    return Response.json({
      success: true,
      data: subscribers.results || [],
      pagination: {
        page,
        limit,
        total,
        pages: Math.ceil(total / limit)
      }
    });
  } catch (error) {
    console.error('List error:', error);
    return Response.json(
      { success: false, message: 'Database error', error: error.message },
      { status: 500 }
    );
  }
}

/**
 * Delete a subscriber by ID
 */
async function handleDelete(db, request) {
  const url = new URL(request.url);
  const id = url.pathname.split('/').pop();
  
  if (!id || isNaN(parseInt(id))) {
    return Response.json(
      { success: false, message: 'Invalid subscriber ID' },
      { status: 400 }
    );
  }
  
  try {
    const result = await db.prepare(
      'DELETE FROM subscribers WHERE id = ?'
    ).bind(id).run();
    
    if (result.success && result.meta.changes > 0) {
      return Response.json({
        success: true,
        message: 'Subscriber deleted'
      });
    } else {
      return Response.json(
        { success: false, message: 'Subscriber not found' },
        { status: 404 }
      );
    }
  } catch (error) {
    console.error('Delete error:', error);
    return Response.json(
      { success: false, message: 'Database error', error: error.message },
      { status: 500 }
    );
  }
}

/**
 * Export all subscribers as CSV
 */
async function handleExport(db) {
  try {
    const subscribers = await db.prepare(
      `SELECT id, email, consent, subscribed_at, ip_hash, user_agent, referrer, source
       FROM subscribers
       ORDER BY subscribed_at DESC`
    ).all();
    
    const rows = subscribers.results || [];
    
    // CSV header
    const headers = ['ID', 'Email', 'Consent', 'Subscribed At', 'IP Hash', 'User Agent', 'Referrer', 'Source'];
    const csvRows = [
      headers.join(','),
      ...rows.map(row => [
        row.id,
        `"${row.email.replace(/"/g, '""')}"`, // Escape quotes
        row.consent ? 'yes' : 'no',
        `"${row.subscribed_at}"`,
        `"${row.ip_hash || ''}"`,
        `"${(row.user_agent || '').replace(/"/g, '""')}"`,
        `"${(row.referrer || '').replace(/"/g, '""')}"`,
        `"${row.source || ''}"`
      ].join(','))
    ];
    
    const csv = csvRows.join('\n');
    
    return new Response(csv, {
      headers: {
        'Content-Type': 'text/csv',
        'Content-Disposition': 'attachment; filename="workspace-pro-subscribers.csv"',
        'Cache-Control': 'no-store'
      }
    });
  } catch (error) {
    console.error('Export error:', error);
    return Response.json(
      { success: false, message: 'Export failed', error: error.message },
      { status: 500 }
    );
  }
}