-- Drop and recreate database
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
    Author VARCHAR(100),
    Rating DECIMAL(2,1) CHECK (Rating >= 0.0 AND Rating <= 5.0)
);

-- Create BookClub table
CREATE TABLE BookClub (
    ClubID INT AUTO_INCREMENT PRIMARY KEY,
    ClubName VARCHAR(100),
    ClubDescription VARCHAR(500)
);

-- Create Membership table
CREATE TABLE Membership (
    MembershipID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT,
    ClubID INT,
    FOREIGN KEY (UserID) REFERENCES User(UserID),
    FOREIGN KEY (ClubID) REFERENCES BookClub(ClubID)
);

-- Create Owner table
CREATE TABLE Owner (
    OwnerID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT,
    ClubID INT,
    FOREIGN KEY (UserID) REFERENCES User(UserID),
    FOREIGN KEY (ClubID) REFERENCES BookClub(ClubID)
);

-- Create BookComment table (with BookID!)
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

