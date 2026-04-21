-- Create subscribers table for The Workspace Pro newsletter
CREATE TABLE subscribers (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  email TEXT UNIQUE NOT NULL,
  consent BOOLEAN NOT NULL DEFAULT 0,
  subscribed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  ip_hash TEXT,               -- SHA‑256 hash of IP (for privacy)
  user_agent TEXT,
  referrer TEXT,
  source TEXT DEFAULT 'homepage'
);

-- Index for email lookups
CREATE INDEX idx_subscribers_email ON subscribers(email);

-- Index for time‑based queries
CREATE INDEX idx_subscribers_subscribed_at ON subscribers(subscribed_at);