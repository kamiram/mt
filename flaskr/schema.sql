DROP TABLE IF EXISTS email;

CREATE TABLE email (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  uid TEXT NOT NULL,
  topic TEXT NOT NULL DEFAULT '',
  mail_from TEXT NOT NULL DEFAULT '',
  mail_to TEXT NOT NULL DEFAULT '',
  sent DATETIME NOT NULL DEFAULT current_timestamp,
  read DATETIME ,
  readcount INTEGER NOT NULL DEFAULT 0
);
