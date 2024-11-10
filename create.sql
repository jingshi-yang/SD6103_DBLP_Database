-- Authors
CREATE TABLE Authors (
    AuthorID INT PRIMARY KEY AUTO_INCREMENT,
    FirstName VARCHAR(100) NOT NULL,
    LastName VARCHAR(100) NOT NULL,
    FullName VARCHAR(200) NOT NULL UNIQUE,
    Affiliation VARCHAR(255),
    Homepage VARCHAR(255)
);

-- Publishers
CREATE TABLE Publishers (
    PublisherID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(255) NOT NULL UNIQUE,
    Location VARCHAR(255)
);

-- Relation table betweeen authors and papers
CREATE TABLE AuthorsPapers (
    AuthorID INT,
    PublicationKey INT,
    AuthorOrder INT,
    PRIMARY KEY (AuthorID, PublicationKey)
    -- To be added after read data
);

-- Editors
CREATE TABLE Editors (
    EditorID INT PRIMARY KEY AUTO_INCREMENT,
    FirstName VARCHAR(100) NOT NULL,
    LastName VARCHAR(100) NOT NULL,
    FullName VARCHAR(200) NOT NULL UNIQUE,
    Affiliation VARCHAR(255)
);

-- Relation table between editors and papers
CREATE TABLE PapersEditors (
    EditorID INT,
    PublicationKey INT,
    PRIMARY KEY (EditorID, PublicationKey),
    FOREIGN KEY (EditorID) REFERENCES Editors(EditorID),
);

-- Article
CREATE TABLE Articles (
    PublicationKey VARCHAR(50) PRIMARY KEY,
    Title VARCHAR(1024) NOT NULL,
    Year INT,
    Month VARCHAR(50),
    MDate VARCHAR(50),
    Volume VARCHAR(50),
    Number VARCHAR(50),
    Pages VARCHAR(50),
    DOI VARCHAR(100) UNIQUE,
    URL VARCHAR(255),
    EE VARCHAR(255),
    Journal VARCHAR(50),
    CDROM VARCHAR(50),
    Cite VARCHAR(255),
    Publisher INT,
    Publnr VARCHAR(50),
    Note VARCHAR(255),
    Stream VARCHAR(255),
);

-- InProceedings
CREATE TABLE InProceedings (
    PublicationKey VARCHAR(50) PRIMARY KEY,
    Title VARCHAR(1024) NOT NULL,
    BookTitle VARCHAR(1024),
    Year INT,
    Number VARCHAR(50),
    Pages VARCHAR(50),
    DOI VARCHAR(100) UNIQUE,
    URL VARCHAR(255),
    EE VARCHAR(255),
    CDROM VARCHAR(50),
    Cite VARCHAR(255),
    Publnr VARCHAR(50),
    Note VARCHAR(255),
    Stream VARCHAR(255),
);

-- Book
CREATE TABLE Books (
    PublicationKey VARCHAR(50) PRIMARY KEY,
    Title VARCHAR(1024) NOT NULL,
    BookTitle VARCHAR(1024),
    Year INT,
    Volume VARCHAR(50),
    Pages VARCHAR(50),
    DOI VARCHAR(100) UNIQUE,
    ISBN VARCHAR(20) UNIQUE,
    URL VARCHAR(255),
    EE VARCHAR(255),
    School VARCHAR(50),
    Series VARCHAR(50),
    Cite VARCHAR(255),
    Publisher INT,
    Note VARCHAR(255),
);

-- InCollection
CREATE TABLE InCollections (
    PublicationKey VARCHAR(50) PRIMARY KEY,
    Title VARCHAR(1024) NOT NULL,
    BookTitle VARCHAR(1024),
    Year INT,
    Pages VARCHAR(50),
    DOI VARCHAR(100) UNIQUE,
    URL VARCHAR(255),
    EE VARCHAR(255),
    CDROM VARCHAR(50),
    Cite VARCHAR(255),
    Publisher INT,
    Note VARCHAR(255),
);

-- PhDThesis
CREATE TABLE PhDThesis (
    PublicationKey VARCHAR(50) PRIMARY KEY,
    Title VARCHAR(1024) NOT NULL,
    Year INT,
    Volume VARCHAR(50),
    Pages VARCHAR(50),
    DOI VARCHAR(100) UNIQUE,
    ISBN VARCHAR(20) UNIQUE,
    EE VARCHAR(255),
    School VARCHAR(50),
    Address VARCHAR(255),
    Series VARCHAR(50),
    Publisher INT,
);

-- MasterThesis
CREATE TABLE MasterThesis (
    PublicationKey VARCHAR(50) PRIMARY KEY,
    Title VARCHAR(1024) NOT NULL,
    Year INT,
    Pages VARCHAR(50),
    DOI VARCHAR(100) UNIQUE,
    ISBN VARCHAR(20) UNIQUE,
    EE VARCHAR(255),
    School VARCHAR(50),
    Address VARCHAR(255),
    Publisher INT,
    Note VARCHAR(255),
);

-- www
CREATE TABLE www (
    PublicationKey VARCHAR(50) PRIMARY KEY,
    Title VARCHAR(1024) NOT NULL,
    Year INT,
    DOI VARCHAR(100) UNIQUE,
    ISBN VARCHAR(20) UNIQUE,
    URL VARCHAR(255),
    Cite VARCHAR(255),
    Note VARCHAR(255),
);

-- Data
CREATE TABLE Data (
    PublicationKey VARCHAR(50) PRIMARY KEY,
    Title VARCHAR(1024) NOT NULL,
    Year INT,
    Number VARCHAR(50),
    DOI VARCHAR(100) UNIQUE,
    EE VARCHAR(255),
    School VARCHAR(50),
    Series VARCHAR(50),
    Publisher INT,
    Rel VARCHAR(50),
    Stream VARCHAR(255),
);

-- Proceedings
CREATE TABLE Proceedings (
    PublicationKey VARCHAR(50) PRIMARY KEY AUTO_INCREMENT,
    Key VARCHAR(255) NOT NULL UNIQUE,
    Title VARCHAR(255) NOT NULL,
    BookTitkle VARCHAR(1024),
    Year INT NOT NULL,
    PublisherID INT,
    Location VARCHAR(255),
    URL VARCHAR(255)
);


-- CrossRef
CREATE TABLE CrossRefs (
    PublicationKey INT,
    ProceedingsKEY INT,
    FOREIGN KEY (PublicationKey),
    FOREIGN KEY (ProceedingsKey)
);