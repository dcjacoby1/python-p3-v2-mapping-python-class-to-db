from __init__ import CURSOR, CONN


class Department:

    def __init__(self, name, location, id=None):
        self.id = id
        self.name = name
        self.location = location

    def __repr__(self):
        return f"<Department {self.id}: {self.name}, {self.location}>"
    
    #call with Department.create_table() or any other name 
    #can confirm the table is created with the code in debugger: 
    #CURSOR.execute("PRAGMA table_info(departments)").fetchall()
    @classmethod
    def create_table(cls):
        """ Create a new table to persist the attributes of Department instances """
        sql = """
            CREATE TABLE IF NOT EXISTS departments (
            id INTEGER PRIMARY KEY,
            name TEXT,
            location TEXT)
        """
        CURSOR.execute(sql)
        #commit saves to the DB
        CONN.commit()

    #call with Department.drop_table() or any other name 
    @classmethod
    def drop_table(cls):
        """ Drop the table that persists Department instances """
        sql = """
            DROP TABLE IF EXISTS departments;
        """
        CURSOR.execute(sql)
        CONN.commit()

    #this instance method will save each characteristic of self as a row entry
    #example: self.name and self.age will both be part of the same row entry
    #question mark allows for plug in play for self. values
    def save(self):
        """ Insert a new row with the name and location values of the current Department instance.
        Update object id attribute using the primary key value of new row.
        """
        sql = """
            INSERT INTO departments (name, location)
            VALUES (?, ?)
        """

        CURSOR.execute(sql, (self.name, self.location))
        CONN.commit()

        #sets the id equal to the last row primary key of the DB
        self.id = CURSOR.lastrowid

        #example of .save():
        #payroll = Department("Payroll", "Building A, 5th Floor")
        #print(payroll)  # <Department None: Payroll, Building A, 5th Floor>
        #payroll.save()  # Persist to db, assign object id attribute
        #print(payroll)  # <Department 1: Payroll, Building A, 5th Floor>

    #executes the init and save in one method
    @classmethod
    def create(cls, name, location):
        """ Initialize a new Department instance and save the object to the database """
        department = cls(name, location)
        department.save()
        return department

    #updates    
    def update(self):
        """Update the table row corresponding to the current Department instance."""
        sql = """
            UPDATE departments
            SET name = ?, location = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.name, self.location, self.id))
        CONN.commit()

    #delete
    def delete(self):
        """Delete the table row corresponding to the current Department instance"""
        sql = """
            DELETE FROM departments
            WHERE id = ?
        """

        CURSOR.execute(sql, (self.id,))
        CONN.commit()

