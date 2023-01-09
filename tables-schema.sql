CREATE TABLE quiz (
  quiz_id INTEGER PRIMARY KEY,
  quiz_name TEXT NOT NULL,
  quiz_text TEXT,
  quiz_dificulty INTEGER
);

CREATE TABLE questions (
  question_id INTEGER PRIMARY KEY,
  quiz_id INTEGER NOT NULL,
  question_text TEXT ,
  question_dificulty INTEGER NOT NULL,
  question_multianswer INTEGER NOT NULL,
  is_active INTEGER,
  FOREIGN KEY (quiz_id) REFERENCES quiz (quiz_id) ON DELETE CASCADE ON UPDATE NO ACTION
);

CREATE TABLE answers (
  answer_id INTEGER PRIMARY KEY,
  question_id INTEGER NOT NULL,
  question_answer TEXT NOT NULL,
  question_correct INTEGER NOT NULL,
  FOREIGN KEY (question_id) REFERENCES questions (question_id) ON DELETE CASCADE ON UPDATE NO ACTION
);

CREATE TABLE person_answers (
  person_answers_id INTEGER PRIMARY KEY,
  question_id INTEGER NOT NULL,
  quiz_id INTEGER NOT NULL,
  participant_id INTEGER NOT NULL,  
  answer_id TEXT NOT NULL,
  question_time_start REAL,
  question_time_end REAL,
  FOREIGN KEY (question_id) REFERENCES questions (question_id) ON DELETE CASCADE ON UPDATE NO ACTION,
  FOREIGN KEY (quiz_id) REFERENCES quiz (quiz_id) ON DELETE CASCADE ON UPDATE NO ACTION,
  FOREIGN KEY (participant_id) REFERENCES participants (participant_id) ON DELETE CASCADE ON UPDATE NO ACTION,
  FOREIGN KEY (answer_id) REFERENCES answers (answers_id) ON DELETE CASCADE ON UPDATE NO ACTION
);

CREATE TABLE participants (
  participant_id INTEGER PRIMARY KEY,
  quiz_id INTEGER NOT NULL,
  user_id INTEGER NOT NULL,
  time_start REAL,
  time_end REAL,
  score INTEGER,
  FOREIGN KEY (quiz_id) REFERENCES quiz (quiz_id) ON DELETE CASCADE ON UPDATE NO ACTION,
  FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE ON UPDATE NO ACTION
);

CREATE TABLE users (
  user_uid TEXT PRIMARY KEY,
  register_time REAL NOT NULL,
  last_login REAL NOT NULL,
  --h(which data tapes) 
  user_name TEXT NOT NULL,
  user_email TEXT NOT NULL,
  user_password TEXT NOT NULL
);