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
    PaperID INT,
    AuthorOrder INT,
    PRIMARY KEY (AuthorID, PaperID)
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
    PaperID INT,
    PRIMARY KEY (EditorID, PaperID),
    FOREIGN KEY (EditorID) REFERENCES Editors(EditorID),
    FOREIGN KEY (PaperID) REFERENCES Papers(PaperID)
);

-- Publication
CREATE TABLE Publications (
    PublicationID INT PRIMARY KEY AUTO_INCREMENT,
    Title VARCHAR(1024) NOT NULL,
    Key VARCHAR(50) NOT NULL,
    Year INT,
    CDate VARCHAR(50),
    MDate VARCHAR(50),
    Volume VARCHAR(50),
    Number VARCHAR(50),
    Pages VARCHAR(50),
    DOI VARCHAR(100) UNIQUE,
    ISBN VARCHAR(20) UNIQUE,
    URL VARCHAR(255),
    EE VARCHAR(255),
    School VARCHAR(50),
    CiteKey VARCHAR(100),
    Address VARCHAR(255),
    Series VARCHAR(50),
    Journal VARCHAR(50),
    CDROM VARCHAR(50),
    Cite VARCHAR(255),
    Publisher INT,
    Chapter VARCHAR(50),
    Publnr VARCHAR(50),
    Rel VARCHAR(50),
    Note VARCHAR(255),
    Stream VARCHAR(255),
    Type ENUM('Article', 'InProceedings', 'Book', 'InCollection', 'PhDThesis', 'MasterThesis', 'www') NOT NULL
);

-- CrossRef
CREATE TABLE CrossRefs (
    ProceedingsID INT,
    PublicationsID INT,
    FOREIGN KEY (ProceedingsID),
    FOREIGN KEY (PublicationID)
);

-- Proceedings
CREATE TABLE Proceedings (
    ProceedingsID INT PRIMARY KEY AUTO_INCREMENT,
    Key VARCHAR(255) NOT NULL UNIQUE,
    Name VARCHAR(255) NOT NULL,
    Year INT NOT NULL,
    PublisherID INT,
    Location VARCHAR(255),
    URL VARCHAR(255)
);


