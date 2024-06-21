CREATE SCHEMA [Schema1];
CREATE SCHEMA [Schema2];

CREATE TABLE [Schema1].[Table1] (
    ID INT,
    Name VARCHAR(100)
);

CREATE TABLE [Schema2].[Table2] (
    ID INT,
    Description VARCHAR(255)
);

SELECT * FROM [Schema1].[Table1];
SELECT * FROM [Schema2].[Table2];

UPDATE [Schema1].[Table1] SET Name = 'Naman' WHERE ID = 1;
UPDATE [Schema2].[Table2] SET Description = 'Practice' WHERE ID = 2;

SELECT '[Schema1].table1' AS Practice FROM [Schema1].[Table1];
SELECT '[Schema2].table2' AS Practice FROM [Schema2].[Table2];
