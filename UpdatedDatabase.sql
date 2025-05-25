USE bookclub;

DROP DATABASE IF EXISTS bookclub;
CREATE DATABASE bookclub;
USE bookclub;

-- Create User table
CREATE TABLE User (
    UserID INT AUTO_INCREMENT PRIMARY KEY,
    Username VARCHAR(50) NOT NULL UNIQUE
);

-- Create Book table
CREATE TABLE Book (
    BookID INT AUTO_INCREMENT PRIMARY KEY,
    Title VARCHAR(100),
    Author VARCHAR(100)
);

-- Create BookClub table
CREATE TABLE BookClub (
    ClubID INT AUTO_INCREMENT PRIMARY KEY,
    ClubName VARCHAR(100),
    ClubDescription VARCHAR(500)
);

-- Create Membership table with Role
CREATE TABLE Membership (
    MembershipID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT,
    ClubID INT,
    Role ENUM('owner', 'member') DEFAULT 'member',
    FOREIGN KEY (UserID) REFERENCES User(UserID),
    FOREIGN KEY (ClubID) REFERENCES BookClub(ClubID)
);

-- Create BookComment table
CREATE TABLE BookComment (
    CommentID INT AUTO_INCREMENT PRIMARY KEY,
    Content VARCHAR(250),
    UserID INT,
    BookID INT,
    FOREIGN KEY (UserID) REFERENCES User(UserID),
    FOREIGN KEY (BookID) REFERENCES Book(BookID)
);

-- Create BookDiscussion table
CREATE TABLE BookDiscussion (
    DiscussionID INT AUTO_INCREMENT PRIMARY KEY,
    Topic VARCHAR(100),
    ClubID INT,
    FOREIGN KEY (ClubID) REFERENCES BookClub(ClubID)
);

-- Create DiscussionComment table
CREATE TABLE DiscussionComment (
    DiscussionCommentID INT AUTO_INCREMENT PRIMARY KEY,
    DiscussionID INT,
    UserID INT,
    Content VARCHAR(250),
    FOREIGN KEY (DiscussionID) REFERENCES BookDiscussion(DiscussionID),
    FOREIGN KEY (UserID) REFERENCES User(UserID)
);

-- Create BookRating table
CREATE TABLE BookRating (
    RatingID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT,
    BookID INT,
    Rating DECIMAL(2,1) CHECK (Rating >= 0.0 AND Rating <= 5.0),
    FOREIGN KEY (UserID) REFERENCES User(UserID),
    FOREIGN KEY (BookID) REFERENCES Book(BookID)
);

-- Trigger to set default rating
DELIMITER //
CREATE TRIGGER default_rating_before_insert
BEFORE INSERT ON BookRating
FOR EACH ROW
BEGIN
  IF NEW.Rating = 0 THEN
    SET NEW.Rating = 3.0;
  END IF;
END;
//
DELIMITER ;

/*
-- Function to count number of clubs a user is in
DELIMITER //
CREATE FUNCTION CountUserClubs(uid INT)
RETURNS INT
DETERMINISTIC
BEGIN
  DECLARE total INT;
  SELECT COUNT(*) INTO total FROM Membership WHERE UserID = uid;
  RETURN total;
END;
//
DELIMITER ;

-- testing trigger

INSERT INTO BookRating (UserID, BookID, Rating) VALUES (1, 1, 0);
SELECT * FROM BookRating WHERE UserID = 1 AND BookID = 1;

SELECT * FROM Book;
*/