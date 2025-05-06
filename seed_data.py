from faker import Faker
from db_connection import get_connection
import random

fake = Faker()
conn = get_connection()
cursor = conn.cursor()

# --- Insert Users ---
print("Inserting users...")
for _ in range(10):
    username = fake.user_name()
    cursor.execute("INSERT INTO User (Username) VALUES (%s);", (username,))

# --- Insert Books ---
print("Inserting books...")
book_ids = []
for _ in range(8):
    title = fake.sentence(nb_words=3).rstrip('.')
    author = fake.name()
    cursor.execute("INSERT INTO Book (Title, Author) VALUES (%s, %s);", (title, author))
    book_ids.append(cursor.lastrowid)

# --- Insert Book Clubs ---
print("Creating book clubs...")
club_ids = []
for _ in range(3):
    name = fake.catch_phrase()
    description = fake.text(max_nb_chars=100)
    cursor.execute("INSERT INTO BookClub (ClubName, ClubDescription) VALUES (%s, %s);", (name, description))
    club_ids.append(cursor.lastrowid)

# Fetch 3 random existing user IDs to assign as club owners
print("Assigning club owners...")
cursor.execute("SELECT UserID FROM User ORDER BY RAND() LIMIT 3;")
owner_user_ids = [row[0] for row in cursor.fetchall()]

for user_id, club_id in zip(owner_user_ids, club_ids):
    cursor.execute("INSERT INTO Owner (UserID, ClubID) VALUES (%s, %s);", (user_id, club_id))

# --- Create Memberships (random assignments) ---
print("Adding members to clubs...")
# --- Get all valid user IDs from DB ---
cursor.execute("SELECT UserID FROM User;")
user_ids = [row[0] for row in cursor.fetchall()]


# --- Get all valid user IDs from DB ---
cursor.execute("SELECT UserID FROM User;")
user_ids = [row[0] for row in cursor.fetchall()]

# --- Add users to clubs randomly ---
print("Adding members to clubs...")
for user_id in user_ids:
    for club_id in random.sample(club_ids, k=random.randint(1, 2)):
        cursor.execute("INSERT INTO Membership (UserID, ClubID) VALUES (%s, %s);", (user_id, club_id))




# --- Insert Book Ratings ---
print("Adding ratings...")
print("Adding ratings...")
for _ in range(20):
    cursor.execute("INSERT INTO BookRating (UserID, BookID, Rating) VALUES (%s, %s, %s);", (
        random.choice(user_ids),
        random.choice(book_ids),
        round(random.uniform(1.0, 5.0), 1)
    ))

# --- Insert Book Comments ---
print("Adding comments on books...")
for _ in range(15):
    cursor.execute("INSERT INTO BookComment (Content, UserID, BookID) VALUES (%s, %s, %s);", (
        fake.sentence(nb_words=8),
        random.randint(1, 10),
        random.choice(book_ids)
    ))

# --- Create Book Discussions ---
print("Creating discussions...")
discussion_ids = []
for club_id in club_ids:
    for _ in range(2):
        topic = fake.sentence(nb_words=5).rstrip('.')
        cursor.execute("INSERT INTO BookDiscussion (Topic, ClubID) VALUES (%s, %s);", (topic, club_id))
        discussion_ids.append(cursor.lastrowid)

# --- Insert Discussion Comments ---
print("Adding comments to discussions...")
for _ in range(30):
    cursor.execute("INSERT INTO DiscussionComment (DiscussionID, UserID, Content) VALUES (%s, %s, %s);", (
        random.choice(discussion_ids),
        random.randint(1, 10),
        fake.sentence(nb_words=10)
    ))

# --- Commit everything ---
conn.commit()
cursor.close()
conn.close()

print("Test data inserted successfully.")
