CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    national_id VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

ALTER TABLE users
ADD COLUMN last_login TIMESTAMPTZ;

CREATE INDEX idx_users_national_id ON users(national_id);


CREATE TABLE question_definitions (
  question_key TEXT PRIMARY KEY,
  question_text TEXT NOT NULL
);

INSERT INTO question_definitions (question_key, question_text) VALUES
  ('q1', 'When you look at the mole, does one half look different from the other half in shape or thickness?'),
  ('q2', 'Have you noticed if the edges of the mole look ragged, notched, or blurred rather than smooth?'),
  ('q3', 'Do you see more than one color in the mole, such as brown, black, red, white, or blue?'),
  ('q4', 'Would you say it is larger than about 6 millimeters, roughly the size of a pencil eraser?'),
  ('q5', 'Has the mole changed recently in size, shape, color, or caused any new symptoms like itching, bleeding, or crusting?');

  CREATE TABLE mole_questionnaires (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  national_id TEXT NOT NULL,
  timestamp TIMESTAMPTZ DEFAULT now(),
  q1 BOOLEAN NOT NULL,
  q2 BOOLEAN NOT NULL,
  q3 BOOLEAN NOT NULL,
  q4 BOOLEAN NOT NULL,
  q5 BOOLEAN NOT NULL
);


CREATE TABLE ham_metadata (
  image_id TEXT PRIMARY KEY,
  image_url TEXT,
  lesion_id TEXT,
  dx TEXT,
  dx_type TEXT,
  age REAL,
  sex TEXT,
  localization TEXT,
  uploaded_at TIMESTAMPTZ DEFAULT now()
);

ALTER TABLE ham_metadata ADD COLUMN embedding FLOAT[];

select count(*) from ham_metadata;-- 10015 as needed, but only 99 of them have embeddings

CREATE TABLE cnn_results (
  national_id VARCHAR(255) PRIMARY KEY REFERENCES users(national_id),
  timestamp TIMESTAMPTZ DEFAULT now(),
  cnn_result FLOAT NOT NULL,
  embedding FLOAT[] NOT NULL
);

  ALTER TABLE cnn_results DROP CONSTRAINT cnn_results_pkey;
  ALTER TABLE cnn_results ADD PRIMARY KEY (national_id, timestamp);


select dx, count(*) from ham_metadata where embedding is not null
group by dx;-- 52 mel, 31 nv, 16 other

CREATE TABLE similar_moles_ann_user (
  national_id VARCHAR(255) NOT NULL,
  timestamp TIMESTAMPTZ NOT NULL DEFAULT now(),
  image_id1 TEXT,
  image_id2 TEXT,
  image_id3 TEXT,
  PRIMARY KEY (national_id, timestamp),
  FOREIGN KEY (national_id) REFERENCES users(national_id)
);

CREATE TABLE final_recommendation (
  national_id VARCHAR(255) NOT NULL,
  "timestamp" TIMESTAMPTZ NOT NULL DEFAULT now(),
  recommendation TEXT,
  PRIMARY KEY (national_id, "timestamp"),
  CONSTRAINT fk_national_id
    FOREIGN KEY(national_id) 
    REFERENCES users(national_id)
);