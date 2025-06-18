-- Drop tables if they already exist
DROP TABLE IF EXISTS tickets;
DROP TABLE IF EXISTS events;
DROP TABLE IF EXISTS categories;
DROP TABLE IF EXISTS users;

-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    email TEXT NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('user', 'vip', 'admin'))
);

-- Categories table
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL
);

-- Events table
CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    category_id INTEGER REFERENCES categories(id),
    event_date DATE NOT NULL,
    is_vip_only BOOLEAN DEFAULT FALSE
);

-- Tickets table (not sure if I will need it yet)
CREATE TABLE tickets (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    event_id INTEGER REFERENCES events(id)
);

-- Seed users
INSERT INTO users (username, email, password, role) VALUES
('ivan', 'ivan@amatas.com', 'ivan123', 'user'),
('peter', 'peter@amatas.com', 'peter123', 'vip'),
('admin', 'admin@eventor.com', 'p@ssw0rd_admin', 'admin');

-- Seed categories
INSERT INTO categories (name) VALUES
('Music'),
('Food & Drink'),
('Sports'),
('Arts'),
('Technology'),
('Business');

-- Seed events
INSERT INTO events (title, description, category_id, event_date, is_vip_only) VALUES
('PRIVATE SECURITY BRIEFING - ADMIN ONLY', 'Admin-only event', 5, '2025-07-12', TRUE),
('Open Air Music Festival', 'Join us in the summer sun.', 1, '2025-08-12', FALSE),
('Wild Techno Rave', 'No different than Berghain.', 1, '2025-09-14', FALSE),
('Guns and Roses - Sofia', 'The legendary band is coming to Bulgaria.', 1, '2025-08-01', FALSE),
('Kitchen Dreams', 'Taste the best food by the best chefs.', 2, '2025-07-14', FALSE),
('Outdoor Picnic', 'Peaceful lunch in Vitosha.', 2, '2025-06-23', FALSE),
('Pick-up Basketball', 'Join us for a hoop session!', 3, '2025-06-15', FALSE),
('Pilates', 'Ladies, you are welcome!', 3, '2025-07-10', FALSE),
('Wine and Draw', 'Enjoy a glass of wine while you draw!', 4, '2025-10-10', FALSE),
('Vladimir Dimitrov - Maistora exhibition', 'See the works of one of the greatest Bulgarian artists!', 4, '2025-10-10', FALSE),
('Tech Talk 2025', 'Industry leaders speak on AI.', 5, '2025-07-01', FALSE),
('HACKER CONFERENCE: RED TEAM EDITION - VIP ONLY', 'VIP only', 5, '2025-06-15', TRUE),
('LAN Party', 'Bring your own rig!', 5, '2025-09-01', FALSE),
('Investing in 2025.', 'The world has changed, and we must too.', 6, '2025-07-16', FALSE),
('Tariffs - what now?', 'How to deal with the American tariffs?', 6, '2025-06-05', FALSE);