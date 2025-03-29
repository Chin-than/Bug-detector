CREATE TABLE IF NOT EXISTS code_samples (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_name TEXT NOT NULL,
    code_content TEXT NOT NULL,
    has_bugs BOOLEAN NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS bugs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code_sample_id INTEGER,
    bug_type TEXT NOT NULL,
    description TEXT,
    line_number INTEGER,
    severity TEXT,
    FOREIGN KEY (code_sample_id) REFERENCES code_samples(id)
);

CREATE TABLE IF NOT EXISTS fixes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bug_id INTEGER,
    fixed_code TEXT NOT NULL,
    fix_description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (bug_id) REFERENCES bugs(id)
); 