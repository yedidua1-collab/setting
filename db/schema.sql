CREATE TABLE IF NOT EXISTS leads (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  name TEXT NOT NULL,
  phone TEXT NOT NULL,
  field TEXT,
  status TEXT NOT NULL DEFAULT 'new',   -- new / contacted / call_scheduled / won / lost
  notes TEXT,
  email_sent INTEGER NOT NULL DEFAULT 0,
  email_error TEXT,
  user_agent TEXT,
  country TEXT
);

-- Onboarding questionnaire (/start)
CREATE TABLE IF NOT EXISTS intakes (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  token TEXT NOT NULL,                 -- secret used in image links sent by email
  full_name TEXT NOT NULL,             -- name + professional title as shown on the page
  license TEXT,
  locations TEXT,                      -- JSON array: clinic / online
  city TEXT,
  audience TEXT,
  help_text TEXT,
  approach TEXT,
  about TEXT,
  mood TEXT,                           -- calm / warm / clean / recommend
  phone TEXT NOT NULL,
  email TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'new',  -- new / in_progress / sketch_sent / live
  notes TEXT,
  email_sent INTEGER NOT NULL DEFAULT 0,
  email_error TEXT
);
CREATE TABLE IF NOT EXISTS intake_files (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  intake_id INTEGER NOT NULL REFERENCES intakes(id),
  kind TEXT NOT NULL,                  -- photo / logo
  mime TEXT NOT NULL,
  name TEXT,
  data TEXT NOT NULL                   -- base64 (resized in the browser)
);
