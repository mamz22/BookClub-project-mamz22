import sqlite3

conn = sqlite3.connect('bookclub.db')
cursor = conn.cursor()

# Create User table
cursor.execute('''
CREATE TABLE IF NOT EXISTS User (
    UserID INTEGER PRIMARY KEY AUTOINCREMENT,
    Username TEXT NOT NULL UNIQUE
);
''')

# Create Book table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Book (
    BookID INTEGER PRIMARY KEY AUTOINCREMENT,
    Title TEXT,
    Author TEXT
);
''')

# Create BookClub table
cursor.execute('''
CREATE TABLE IF NOT EXISTS BookClub (
    ClubID INTEGER PRIMARY KEY AUTOINCREMENT,
    ClubName TEXT,
    ClubDescription TEXT
);
''')

# Create Membership table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Membership (
    MembershipID INTEGER PRIMARY KEY AUTOINCREMENT,
    UserID INTEGER,
    ClubID INTEGER,
    FOREIGN KEY (UserID) REFERENCES User(UserID),
    FOREIGN KEY (ClubID) REFERENCES BookClub(ClubID)
);
''')

# Create Owner table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Owner (
    OwnerID INTEGER PRIMARY KEY AUTOINCREMENT,
    UserID INTEGER,
    ClubID INTEGER,
    FOREIGN KEY (UserID) REFERENCES User(UserID),
    FOREIGN KEY (ClubID) REFERENCES BookClub(ClubID)
);
''')

# Create BookComment table
cursor.execute('''
CREATE TABLE IF NOT EXISTS BookComment (
    CommentID INTEGER PRIMARY KEY AUTOINCREMENT,
    Content TEXT,
    UserID INTEGER,
    BookID INTEGER,
    FOREIGN KEY (UserID) REFERENCES User(UserID),
    FOREIGN KEY (BookID) REFERENCES Book(BookID)
);
''')

# Create BookDiscussion table
cursor.execute('''
CREATE TABLE IF NOT EXISTS BookDiscussion (
    DiscussionID INTEGER PRIMARY KEY AUTOINCREMENT,
    Topic TEXT,
    ClubID INTEGER,
    FOREIGN KEY (ClubID) REFERENCES BookClub(ClubID)
);
''')

# Create DiscussionComment table
cursor.execute('''
CREATE TABLE IF NOT EXISTS DiscussionComment (
    DiscussionCommentID INTEGER PRIMARY KEY AUTOINCREMENT,
    DiscussionID INTEGER,
    UserID INTEGER,
    Content TEXT,
    FOREIGN KEY (DiscussionID) REFERENCES BookDiscussion(DiscussionID),
    FOREIGN KEY (UserID) REFERENCES User(UserID)
);
''')

# Create BookRating table
cursor.execute('''
CREATE TABLE IF NOT EXISTS BookRating (
    RatingID INTEGER PRIMARY KEY AUTOINCREMENT,
    UserID INTEGER,
    BookID INTEGER,
    Rating REAL CHECK (Rating >= 0.0 AND Rating <= 5.0),
    FOREIGN KEY (UserID) REFERENCES User(UserID),
    FOREIGN KEY (BookID) REFERENCES Book(BookID)
);
''')

conn.commit()
conn.close()

print("Database setup completed sucessfully.")