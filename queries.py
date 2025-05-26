from db_connection import get_connection

# Func to get all books avg ratings
def get_all_books_with_avg_rating():
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        SELECT  B.Title,
                B.Author,
                ROUND(AVG(R.Rating),2)  AS AvgRating,
                RatingLabel(AVG(R.Rating)) AS Label
        FROM    Book B
        LEFT JOIN BookRating R ON B.BookID = R.BookID
        GROUP BY B.BookID;
    """
    cursor.execute(query)
    results = cursor.fetchall()

    print("\nBooks with Average Ratings:")
    for title, author, avg, label in results:
        if avg is None:
            # handle books that truly have no rating rows
            print(f"- {title} by {author} | No ratings yet")
        else:
            print(f"- {title} by {author} | {avg:.2f} ({label})")

    cursor.close()
    conn.close()

# Func to get all users who are currently in club
def get_users_in_club(club_id):
    conn = get_connection()
    cursor = conn.cursor()
    query = '''
    SELECT User.Username
    FROM Membership
    JOIN User ON Membership.UserID = User.UserID
    WHERE Membership.ClubID = %s;
    '''
    cursor.execute(query, (club_id,))
    results = cursor.fetchall()
    print(f"\nUsers in Club ID {club_id}:")
    for (username,) in results:
        print(f"- {username}")
    cursor.close()
    conn.close()

# Func to display all comments for book
def get_comments_for_book(book_id):
    conn = get_connection()
    cursor = conn.cursor()
    query = '''
    SELECT 
        Book.Title, 
        BookComment.Content, 
        User.Username
    FROM BookComment
    JOIN Book ON BookComment.BookID = Book.BookID
    JOIN User ON BookComment.UserID = User.UserID
    WHERE Book.BookID = %s;
    '''
    cursor.execute(query, (book_id,))
    results = cursor.fetchall()
    print(f"\nComments for Book ID {book_id}:")
    for title, content, user in results:
        print(f"- {user} on '{title}': {content}")
    cursor.close()
    conn.close()

# Book to display all discussion comments for curtain discussion
def get_discussion_comments(club_id):
    conn = get_connection()
    cursor = conn.cursor()

    # First, show all discussions in the club
    print(f"\n Discussions in Club ID {club_id}:")
    cursor.execute('''
        SELECT 
            DiscussionID, 
            Topic
        FROM BookDiscussion
        WHERE ClubID = %s;
    ''', (club_id,))
    discussions = cursor.fetchall()
    if not discussions:
        print("No discussions found in this club.")
        cursor.close()
        conn.close()
        return

    for did, topic in discussions:
        print(f"- [{did}] {topic}")

    # Then show all comments under those discussions
    print(f"\nComments in Discussions for Club ID {club_id}:")
    cursor.execute('''
        SELECT BookDiscussion.Topic, DiscussionComment.Content, User.Username
        FROM BookDiscussion
        JOIN DiscussionComment ON BookDiscussion.DiscussionID = DiscussionComment.DiscussionID
        JOIN User ON DiscussionComment.UserID = User.UserID
        WHERE BookDiscussion.ClubID = %s;
    ''', (club_id,))
    comments = cursor.fetchall()
    if not comments:
        print("No comments yet.")
    else:
        for topic, comment, user in comments:
            print(f"- [{topic}] {user}: {comment}")

    cursor.close()
    conn.close()

# Top 3 active clubs func
def get_top_3_active_clubs():
    conn = get_connection()
    cursor = conn.cursor()
    query = '''
    SELECT BookClub.ClubName, COUNT(DiscussionComment.DiscussionCommentID) AS CommentCount
    FROM BookClub
    JOIN BookDiscussion ON BookClub.ClubID = BookDiscussion.ClubID
    JOIN DiscussionComment ON BookDiscussion.DiscussionID = DiscussionComment.DiscussionID
    GROUP BY BookClub.ClubID
    ORDER BY CommentCount DESC
    LIMIT 3;
    '''
    cursor.execute(query)
    results = cursor.fetchall()
    print("\nTop 3 Most Active Clubs:")
    for name, count in results:
        print(f"- {name}: {count} comments")
    cursor.close()
    conn.close()

# Get all books with avg rating >= 4
def get_top_rated_books():
    conn = get_connection()
    cursor = conn.cursor()
    query = '''
    SELECT  
        B.Title,
        B.Author,
        ROUND(AVG(R.Rating),2) AS AverageRating
    FROM Book B
    JOIN BookRating R ON B.BookID = R.BookID
    GROUP BY B.BookID
    HAVING AverageRating >= 4.0
    ORDER BY AverageRating DESC;
    '''
    cursor.execute(query)
    results = cursor.fetchall()
    print("\nTop Rated Books (Rating ≥ 4):")
    for title, author, rating in results:
        print(f"- {title} by {author}: {round(rating, 2)}")
    cursor.close()
    conn.close()

# Adding new user func
def add_user():
    conn = get_connection()
    cursor = conn.cursor()
    username = input("Enter new username: ")
    try:
        cursor.execute("INSERT INTO User (Username) VALUES (%s);", (username,))
        conn.commit()
        print("User added successfully.")
    except:
        print("Error: Username might already exist.")
    cursor.close()
    conn.close()

# Add new book func 
def add_book():
    conn = get_connection()
    cursor = conn.cursor()
    title = input("Enter book title: ")
    author = input("Enter author name: ")
    cursor.execute("INSERT INTO Book (Title, Author) VALUES (%s, %s);", (title, author))
    conn.commit()
    print("Book added.")
    cursor.close()
    conn.close()

# Join club func
def join_club():
    conn = get_connection()
    cursor = conn.cursor()
    user_id = input("Enter your User ID: ")
    club_id = input("Enter Club ID to join: ")
    cursor.execute("INSERT INTO Membership (UserID, ClubID) VALUES (%s, %s);", (user_id, club_id))
    conn.commit()
    print("Joined club successfully.")
    cursor.close()
    conn.close()

# Func for posting comment on specific book
def post_book_comment():
    conn = get_connection()
    cursor = conn.cursor()
    user_id = input("Enter your User ID: ")
    book_id = input("Enter Book ID: ")
    content = input("Enter your comment: ")
    cursor.execute("INSERT INTO BookComment (Content, UserID, BookID) VALUES (%s, %s, %s);", (content, user_id, book_id))
    conn.commit()
    print("Comment added.")
    cursor.close()
    conn.close()

# Func to rate a specific book
def rate_book():
    conn = get_connection()
    cursor = conn.cursor()
    user_id = input("Enter your User ID: ")
    book_id = input("Enter Book ID: ")
    rating = input("Enter rating (0.0 - 5.0): ")
    cursor.execute("INSERT INTO BookRating (UserID, BookID, Rating) VALUES (%s, %s, %s);", (user_id, book_id, rating))
    conn.commit()
    print("Rating submitted.")
    cursor.close()
    conn.close()

# Starting new discussion func
def start_discussion():
    conn = get_connection()
    cursor = conn.cursor()
    club_id = input("Enter Club ID: ")
    topic = input("Enter discussion topic: ")
    cursor.execute("INSERT INTO BookDiscussion (Topic, ClubID) VALUES (%s, %s);", (topic, club_id))
    conn.commit()
    print("Discussion started.")
    cursor.close()
    conn.close()

# Comment on specific club discussion func
def comment_on_discussion():
    conn = get_connection()
    cursor = conn.cursor()
    discussion_id = input("Enter Discussion ID: ")
    user_id = input("Enter your User ID: ")
    content = input("Enter your comment: ")
    cursor.execute("INSERT INTO DiscussionComment (DiscussionID, UserID, Content) VALUES (%s, %s, %s);", (discussion_id, user_id, content))
    conn.commit()
    print("Comment added to discussion.")
    cursor.close()
    conn.close()

# Get a user id by entering a username func
def find_user_id():
    conn = get_connection()
    cursor = conn.cursor()
    username = input("Enter your username: ")
    cursor.execute("SELECT UserID FROM User WHERE Username = %s;", (username,))
    result = cursor.fetchone()
    if result:
        print(f"Your User ID is: {result[0]}")
    else:
        print("Username not found.")
    cursor.close()
    conn.close()

# Same as find_user_id but for books
def find_book_id():
    conn = get_connection()
    cursor = conn.cursor()
    title = input("Enter the book title: ")
    query = "SELECT BookID, Author FROM Book WHERE Title LIKE %s;"
    cursor.execute(query, (f"%{title}%",))
    results = cursor.fetchall()

    if results:
        print(f"\nMatching books for '{title}':")
        for book_id, author in results:
            print(f"- ID: {book_id} | Author: {author}")
    else:
        print("No book found with that title.")
    
    cursor.close()
    conn.close()

# Func to create a new book club
def create_book_club():
    conn = get_connection()
    cursor = conn.cursor()
    club_name = input("Enter book club name: ")
    description = input("Enter a short description: ")
    try:
        cursor.execute(
            "INSERT INTO BookClub (ClubName, ClubDescription) VALUES (%s, %s);",
            (club_name, description)
        )
        conn.commit()
        print("Book club created successfully.")
    except Exception as e:
        print(f"Error creating book club: {e}")
    cursor.close()
    conn.close()

# Fun to view all book clubs
def view_all_book_clubs():
    conn = get_connection()
    cursor = conn.cursor()
    query = '''
    SELECT ClubID, ClubName FROM BookClub;
    '''
    cursor.execute(query)
    results = cursor.fetchall()
    
    print("\nAll Book Clubs:")
    if not results:
        print("No book clubs found.")
    else:
        for club_id, name in results:
            print(f"- ID: {club_id} | Name: {name}")
    
    cursor.close()
    conn.close()

def get_clubs_for_user():
    conn = get_connection()
    cursor = conn.cursor()
    user_id = input("Enter your User ID: ")
    query = '''
    SELECT BookClub.ClubName, Membership.Role
    FROM Membership
    JOIN BookClub ON Membership.ClubID = BookClub.ClubID
    WHERE Membership.UserID = %s;
    '''
    cursor.execute(query, (user_id,))
    results = cursor.fetchall()
    print(f"\nClubs for User ID {user_id}:")
    for name, role in results:
        print(f"- {name} ({role})")
    cursor.close()
    conn.close()
