-- Authors
CREATE TABLE Authors (
    AuthorID INT PRIMARY KEY AUTO_INCREMENT,
    FirstName VARCHAR(100) NOT NULL,
    LastName VARCHAR(100),
    AuthorOCRID CHAR(20),
);

-- Relation table betweeen authors and papers
CREATE TABLE AuthorsPapers (
    AuthorID INT,
    PublicationKey INT,
    PRIMARY KEY (AuthorID, PublicationKey)
    -- To be added after read data
);

-- Editors
CREATE TABLE Editors (
    EditorID INT PRIMARY KEY AUTO_INCREMENT,
    FirstName VARCHAR(100) NOT NULL,
    LastName VARCHAR(100),
    EditorOCRID CHAR(20),
);

-- Relation table between editors and papers
CREATE TABLE PapersEditors (
    EditorID INT,
    PublicationKey INT,
    PRIMARY KEY (EditorID, PublicationKey),
    FOREIGN KEY (EditorID) REFERENCES Editors(EditorID),
);

-- Publications, table for parent class
-- Key source largest length 9 reference
-- Key name largest length 22 
-- Publtype largest length 16
-- Note largest length 953
-- Title largest length 1359
CREATE TABLE Publications (
    PublicationKey VARCHAR(64) PRIMARY KEY,
    KeySource VARCHAR(10),
    KeyName VARCHAR(23),
    Mdate Date,
    Publtype VARCHAR(16),
    Title VARCHAR(1536),
    Note VARCHAR(1024),
    Year INT,
    EE VARCHAR(255),
);

-- Cdate is date
-- Journal Max Length 62
-- CDROM Max Length 88
-- Publnr Max Length 8
-- Article
CREATE TABLE Articles (
    PublicationKey VARCHAR(50) FOREIGN KEY REFERENCES Publications(PublicationKey),
    Cdate DATE,
    BookTitle VARCHAR(255),
    Pages VARCHAR(100),
    Journal VARCHAR(100),
    Volume VARCHAR(50),
    Number VARCHAR(50),
    Month VARCHAR(50),
    URL VARCHAR(1024),
    CDROM VARCHAR(100),
    Cite VARCHAR(MAX),
    Publisher VARCHAR(255),
    Publnr VARCHAR(20),
    Stream VARCHAR(50),
);

-- InProceedings
CREATE TABLE InProceedings (
    PublicationKey VARCHAR(50) FOREIGN KEY REFERENCES Publications(PublicationKey),
    BookTitle VARCHAR(255),
    Pages VARCHAR(100),
    Volume VARCHAR(50),
    Number VARCHAR(50),
    Month VARCHAR(50),
    URL VARCHAR(1024),
    CDROM VARCHAR(100),
    Cite VARCHAR(MAX),
    Stream VARCHAR(50),
);

-- Book
CREATE TABLE Books (
    PublicationKey VARCHAR(50) FOREIGN KEY REFERENCES Publications(PublicationKey),
    BookTitle VARCHAR(255),
    Pages VARCHAR(100),
    Journal VARCHAR(100),
    Volume VARCHAR(50),
    Month VARCHAR(50),
    URL VARCHAR(1024),
    CDROM VARCHAR(100),
    Cite VARCHAR(MAX),
    Publisher VARCHAR(255),
    ISBN VARCHAR(100),
    Series VARCHAR(255),
    School VARCHAR(255),
);

-- Chapter INT
-- InCollection
CREATE TABLE InCollections (
    PublicationKey VARCHAR(50) FOREIGN KEY REFERENCES Publications(PublicationKey),
    BookTitle VARCHAR(255),
    Pages VARCHAR(100),
    Number VARCHAR(50),    
    URL VARCHAR(1024),
    CDROM VARCHAR(100),
    Cite VARCHAR(MAX),
    Publisher VARCHAR(255),
    Chapter INT,
);

-- Publisher Max Length 155
-- Volume Max Length 31
-- Number Max Length 21
-- Month Max Length 25
-- ISBN Max Length 68, note that ISBN is not unique
-- School Max Length 205
-- Series Max Length 135
-- PhDThesis
CREATE TABLE PhDThesis (
    PublicationKey VARCHAR(50) FOREIGN KEY REFERENCES Publications(PublicationKey),
    Pages VARCHAR(50),
    Volume VARCHAR(50),
    Number VARCHAR(50),
    Month VARCHAR(50),
    Publisher VARCHAR(255),
    ISBN VARCHAR(100),
    Series VARCHAR(255),
    School VARCHAR(255),
);

-- MasterThesis
CREATE TABLE MasterThesis (
    PublicationKey VARCHAR(50) FOREIGN KEY REFERENCES Publications(PublicationKey),
    Pages VARCHAR(50),
    Volume VARCHAR(50),
    Number VARCHAR(50),
    Month VARCHAR(50)
    Publisher VARCHAR(255),
    ISBN VARCHAR(100),
    Series VARCHAR(255),
    School VARCHAR(255),
);

-- URL Max Length 889
-- Cite Max Length 13919
-- Depend on which DBMS we use, the following code uses SQL server format
-- www
CREATE TABLE www (
    PublicationKey VARCHAR(50) FOREIGN KEY REFERENCES Publications(PublicationKey),
    URL VARCHAR(1024),
    Cite VARCHAR(MAX),
);

-- Note that Data is a SQL saved word, use quotation marks
-- Rel Max Length 147
-- Stream Max Length 34
-- Data
CREATE TABLE 'Data' (
    PublicationKey VARCHAR(50) FOREIGN KEY REFERENCES Publications(PublicationKey),
    Number VARCHAR(50),
    Month VARCHAR(50),
    Publisher VARCHAR(255),
    Stream VARCHAR(50),
    Rel VARCHAR(200),
);

-- Booktitle Max Length 206
-- Pages Max Length 91
-- Address Max Length 8
-- Note that here we also have Cite
-- Proceedings
CREATE TABLE Proceedings (
    PublicationKey VARCHAR(50) FOREIGN KEY REFERENCES Publications(PublicationKey),
    BookTitle VARCHAR(255),
    Pages VARCHAR(100),
    Address VARCHAR(50),
    Journal VARCHAR(100),
    Volume VARCHAR(50),
    Number VARCHAR(50),
    URL VARCHAR(1024),
    Cite VARCHAR(MAX),
    Publisher VARCHAR(255),
    ISBN VARCHAR(100),
    Series VARCHAR(255),
    School VARCHAR(255),
    Stream VARCHAR(50),
);

-- Crossref Max Length 38
-- CrossRef
CREATE TABLE CrossRefs (
    PublicationKey VARCHAR(50) FOREIGN KEY REFERENCES Publications(PublicationKey)
    ReferenceKey VARCHAR(50),
);