CREATE TABLE User (
    UserID INT AUTO_INCREMENT PRIMARY KEY,
    Username VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE Book (
    BookID INT AUTO_INCREMENT PRIMARY KEY,
    Title  VARCHAR(100),
    Author VARCHAR(100)
);

CREATE TABLE BookClub (
    ClubID           INT AUTO_INCREMENT PRIMARY KEY,
    ClubName         VARCHAR(100),
    ClubDescription  VARCHAR(500)
);

CREATE TABLE Membership (
    MembershipID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT,
    ClubID INT,
    Role ENUM('owner','member') DEFAULT 'member',
    FOREIGN KEY (UserID) REFERENCES User(UserID),
    FOREIGN KEY (ClubID) REFERENCES BookClub(ClubID)
);

CREATE TABLE BookComment (
    CommentID INT AUTO_INCREMENT PRIMARY KEY,
    Content   VARCHAR(250),
    UserID INT,
    BookID INT,
    FOREIGN KEY (UserID) REFERENCES User(UserID),
    FOREIGN KEY (BookID) REFERENCES Book(BookID)
);

CREATE TABLE BookDiscussion (
    DiscussionID INT AUTO_INCREMENT PRIMARY KEY,
    Topic  VARCHAR(100),
    ClubID INT,
    FOREIGN KEY (ClubID) REFERENCES BookClub(ClubID)
);

CREATE TABLE DiscussionComment (
    DiscussionCommentID INT AUTO_INCREMENT PRIMARY KEY,
    DiscussionID INT,
    UserID       INT,
    Content      VARCHAR(250),
    FOREIGN KEY (DiscussionID) REFERENCES BookDiscussion(DiscussionID),
    FOREIGN KEY (UserID)       REFERENCES User(UserID)
);

CREATE TABLE BookRating (
    RatingID INT AUTO_INCREMENT PRIMARY KEY,
    UserID  INT,
    BookID  INT,
    Rating  DECIMAL(2,1) CHECK (Rating >= 0.0 AND Rating <= 5.0),
    FOREIGN KEY (UserID) REFERENCES User(UserID),
    FOREIGN KEY (BookID) REFERENCES Book(BookID)
);


DROP TRIGGER IF EXISTS default_rating_before_insert;
DELIMITER //
CREATE TRIGGER default_rating_before_insert
BEFORE INSERT ON BookRating
FOR EACH ROW
BEGIN
    IF NEW.Rating IS NULL OR NEW.Rating <= 0 THEN
        SET NEW.Rating = 3.0;
    END IF;
END;
//
DELIMITER ;

DROP TRIGGER IF EXISTS autofill_rating_after_book;
DELIMITER //
CREATE TRIGGER autofill_rating_after_book
AFTER INSERT ON Book
FOR EACH ROW
BEGIN
    INSERT INTO BookRating (UserID, BookID, Rating)
    VALUES (NULL, NEW.BookID, 0); 
END;
//
DELIMITER ;

DROP FUNCTION IF EXISTS RatingLabel;
DELIMITER //
CREATE FUNCTION RatingLabel(p DECIMAL(3,1))
RETURNS VARCHAR(12)  DETERMINISTIC
BEGIN
    RETURN CASE
        WHEN p IS NULL        THEN 'No rating'
        WHEN p >= 4.5         THEN 'Excellent'
        WHEN p >= 3.5         THEN 'Good'
        WHEN p >= 2.5         THEN 'Okay'
        WHEN p >= 1.5         THEN 'Poor'
        ELSE                       'Bad'
    END;
END;//
DELIMITER ;
