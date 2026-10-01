CREATE TABLE association (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE member (
    id INTEGER PRIMARY KEY,
    association_id INTEGER NOT NULL REFERENCES association(id),
    email TEXT NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('member', 'manager'))
);

CREATE TABLE room (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    capacity INTEGER NOT NULL
);

CREATE TABLE booking (
    id INTEGER PRIMARY KEY,
    room_id INTEGER NOT NULL REFERENCES room(id),
    association_id INTEGER NOT NULL REFERENCES association(id),
    member_id INTEGER NOT NULL REFERENCES member(id),
    start TEXT NOT NULL,
    end TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('pending', 'validated', 'refused', 'cancelled')),
    created_at TEXT NOT NULL
);
