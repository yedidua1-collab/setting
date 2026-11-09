CREATE TABLE IF NOT EXISTS leads (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  name TEXT NOT NULL,
  phone TEXT NOT NULL,
  field TEXT,
  status TEXT NOT NULL DEFAULT 'new',   -- new / contacted / call_scheduled / won / lost
  notes TEXT,
  email_sent INTEGER NOT NULL DEFAULT 0,
  user_agent TEXT,
  country TEXT
);
