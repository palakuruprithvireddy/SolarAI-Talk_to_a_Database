few_shots = [
    {
        'Question': "How many columns do we have in the 'complex' table?",
        'SQLQuery': "SELECT COUNT(*) FROM information_schema.columns WHERE table_name = 'complex';",
        'SQLResult': "The query should return the count of columns in the table.",
        'Answer': "The 'complex' table has 3 columns."
    },

    {
        'Question': "What is the average size of granule in complex?",
        'SQLQuery': "SELECT AVG(ST_Area(geometry)) FROM complex;",
        'SQLResult': "Result of the SQL query",
        'Answer': " 3632.22." 
    },

    {
        'Question': "How many granules have an area less than 10000?",
        'SQLQuery': "SELECT COUNT(*) FROM complex WHERE ST_Area(geometry) < 10000;",
        'SQLResult': "Result of the SQL query",
        'Answer': "174293."  
    },

    {
        'Question': "What percentage of granules have an area less than 1000?",
        'SQLQuery': "SELECT (COUNT(*) * 100.0) / (SELECT COUNT(*) FROM complex) FROM complex WHERE ST_Area(geometry) < 1000;",
        'SQLResult': "Result of the SQL query",
        'Answer': "78.35"  
    },
    {
        'Question': "What is the largest size of a granule in complex?",
        'SQLQuery': "SELECT MAX(ST_Area(geometry)) FROM complex;",
        'SQLResult': "Result of the SQL query",
        'Answer': "574754"  
    },
    {
        'Question': "What is the largest size of a granule in complex?",
        'SQLQuery': "SELECT MIN(ST_Area(geometry)) FROM complex;",
        'SQLResult': "Result of the SQL query",
        'Answer': "16"  
    }
]




