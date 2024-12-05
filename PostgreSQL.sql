-- PostgreSQL

-- PostgreSQL is an object-relational database management system (ORDMBS)
-- PostgreSQL is free and open-source.
-- PostgreSQL supports both relational (SQL) and non-relational (JSON) queries.

-- Foreign Keys:
-- A primary key is a column or set of columns in a relational database table that uniquely identifies each row.
-- A foreign key is a column or set of columns in one table that references the primary key in another table,
-- establishing a link between the two tables.

-- The table containing the foreign key is known as the “child table” and the table to which it refers is known as the “parent table".

-- It enforces referential integrity, ensuring valid re32lationships between tables.


	-- Key Features

		-- creates a link between two tables by ensuring that any data entered into the foreign key column must already exist in the parent table. 
		-- This helps maintain data integrity by preventing orphan records and ensuring that relationships between data remain consistent.
		-- Enforces cascading updates or deletions via ON DELETE or ON UPDATE actions.
		-- ON DELETE and ON UPDATE actions are used to define the behavior of foreign key relationships when the parent record is deleted or updated.
		
		-- Example:	
	
				CREATE TABLE departments (
				id SERIAL PRIMARY KEY,
				name VARCHAR(100)
			);

				CREATE TABLE employees (
				id SERIAL PRIMARY KEY,
				name VARCHAR(100),
				department_id INT,
				FOREIGN KEY (department_id) REFERENCES departments (id)
			);

		-- Example: ON DELETE CASCADE

				CREATE TABLE parent (
					id SERIAL PRIMARY KEY,
					name VARCHAR(50)
				);

				CREATE TABLE child (
					id SERIAL PRIMARY KEY,
					parent_id INT REFERENCES parent(id) ON DELETE CASCADE,
					description VARCHAR(100)
				);

		-- Inserting Data:

				INSERT INTO parent (name) VALUES ('Parent 1'), ('Parent 2');
				INSERT INTO child (parent_id, description) VALUES (1, 'Child of Parent 1'), (2, 'Child of Parent 2');

		-- Deleting a Parent Row:

				DELETE FROM parent WHERE id = 1;

			-- The row with parent_id = 1 in the child table will also be deleted automatically.


		-- Example: ON UPDATE CASCADE

				CREATE TABLE parent (
					id SERIAL PRIMARY KEY,
					name VARCHAR(50)
				);

				CREATE TABLE child (
					id SERIAL PRIMARY KEY,
					parent_id INT REFERENCES parent(id) ON UPDATE CASCADE,
					description VARCHAR(100)
				);

				-- Inserting Data:

				INSERT INTO parent (name) VALUES ('Parent 1'), ('Parent 2');
				INSERT INTO child (parent_id, description) VALUES (1, 'Child of Parent 1'), (2, 'Child of Parent 2');

				-- Updating a Parent Row:

				UPDATE parent SET id = 10 WHERE id = 1;

					•	Effect: The parent_id in the child table will automatically update to 10 for the corresponding child row.

	
-- Transactions:

	-- A transaction is a sequence of operations performed as a single, atomic unit. 
	-- PostgreSQL supports transactions to ensure ACID properties (Atomicity, Consistency, Isolation, Durability).

	-- Atomicity: Guarantees that all parts of a transaction are completed successfully. If any part fails, the entire transaction is rolled back (the “all or nothing” principle).
	-- Consistency: Ensures that a transaction can only bring the database from one valid state to another, maintaining database invariants.
	-- Isolation: Provides the illusion that each transaction is the only one interacting with the database, thereby preventing transactions from interfering with each other.
	-- Durability: Once a transaction has been committed, it will remain so, even in the event of a system failure. This ensures that the effects of the transaction are permanently recorded in the database.

	-- Commands

		-- BEGIN: Start a transaction.
		-- COMMIT: Save changes made during the transaction.
		-- ROLLBACK: Revert changes if an error occurs.

	-- Example:

		BEGIN;  -- Starts a transaction

		INSERT INTO accounts (account_id, balance) VALUES (1, 1000);
		INSERT INTO accounts (account_id, balance) VALUES (2, 2000);

		COMMIT;  -- Saves the changes

	-- Example:

		BEGIN;
    	DELETE FROM BankStatements WHERE customer_id = 1;     
    	SELECT customer_id, full_name, balance
        FROM BankStatements;      
		ROLLBACK; --  Reverts all the changes 


	-- Savepoints in Transactions

		-- Savepoints allow partial rollbacks within a transaction:

		BEGIN;

		INSERT INTO accounts (id, balance) VALUES (4, 5000);

		SAVEPOINT savepoint_1;

		-- Attempting an invalid operation
		INSERT INTO accounts (id, balance) VALUES (4, 6000); -- Duplicate ID

		-- Rolls back to the savepoint
		ROLLBACK TO SAVEPOINT savepoint_1;

		-- Continues with other operations
		INSERT INTO accounts (id, balance) VALUES (5, 7000);

		COMMIT;

		-- The transaction continues after rolling back to the savepoint.


-- Security:

	-- PostgreSQL provides robust security mechanisms, including authentication, authorization, and row-level security (RLS).

	-- Key Concepts

		-- Authentication: PostgreSQL supports multiple authentication methods, including: 
			-- Password-based: md5, scram-sha-256
			-- Certificates: SSL/TLS
			-- External systems: LDAP, Kerberos
	
		-- Authorization:
			-- Access is managed via roles and privileges.
			-- Commands: GRANT and REVOKE.
	
		-- Row-Level Security (RLS):
			--Policies restrict access to specific rows. 
		--Role Based Acces Control(RBAC):
			-- Roles
			-- A role represents an entity with specific privileges within a database.
			-- Roles can act as users (with login capabilities), groups (aggregating users for permissions), or a combination of both. 
  			-- we can create the roles and alter the roles drop the roles and grant a role to another role(role inheritance).
  
  			-- Permissions
  			-- Permissions define what a role can do with database objects such as tables, views, and schemas.
  			-- the GRANT statement is a powerful tool used to assign privileges to a role, allowing it to alter database objects like tables, views, functions, and more.
  			-- The GRANT statement is not limited to tables. we can grant privileges on other object types such as sequences, functions, schemas, and databases.
  			-- Privileges granted can also be revoked using the REVOKE statement.
  			-- REVOKE statement plays a crucial role in managing database security by removing previously granted privileges from roles or users.
			
			-- Create a Role:

				CREATE ROLE readonly_user WITH LOGIN PASSWORD 'securepassword';
				-- WITH LOGIN: Allows the role to log in as a user.
				-- PASSWORD: Sets a password for the role.

			-- Grant Database Access:

				GRANT CONNECT ON DATABASE mydb TO readonly_user;

				-- This allows the user to connect to the mydb database.

			-- Grant Schema and Table Permissions:

				GRANT USAGE ON SCHEMA public TO readonly_user;
				GRANT SELECT ON ALL TABLES IN SCHEMA public TO readonly_user;

				-- USAGE allows access to objects in the schema.
				-- SELECT allows reading data from all tables in the schema.

			-- Set Default Privileges:

				ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO readonly_user;

				-- Ensures that future tables created in the public schema automatically grant SELECT to readonly_user.

  		-- RLS
			-- RLS allows database administrators to define policies that restrict access to specific rows in a table
			-- based on the executing user’s identity or other session variables. 
			-- Policies are created using the CREATE POLICY command, specifying conditions under which rows are accessible.
			-- Enabling RLS:

				ALTER TABLE employees ENABLE ROW LEVEL SECURITY;

				-- This activates RLS on the employees table.

			-- Createing a Policy:

				CREATE POLICY hr_policy ON employees USING (department = current_setting('app.current_department'));

				-- USING clause defines the condition for access. In this case, only rows where the department matches the current application setting are visible.

			-- Setting Application Context:

				SET app.current_department = 'HR';

				-- This ensures the session only sees rows belonging to the HR department.

			-- Testing the Policy:

				SELECT * FROM employees;

				-- The user will only see rows where department = 'HR'.
  
  
  -- Performance Tuning:
  	-- Performance tuning ensures PostgreSQL operates efficiently under load. Its performance can be optimized to achieve optimal results. 
	-- Here are some key strategies for tuning PostgreSQL database

  	--Techniques
  
		-- Analyzing and Optimizing Queries
			-- Using EXPLAIN and EXPLAIN ANALYZE: These commands show the execution plan for queries and help identify bottlenecks like slow joins or table scans.
			-- Avoid Sequential Scans (when unnecessary): Use indexes for filtering data instead of scanning entire tables.
			-- Reduce Joins and Subqueries: Simplify queries by breaking complex subqueries into smaller steps or materialized views.
			-- Use Proper JOINs: Choose appropriate join types (e.g., INNER JOIN, LEFT JOIN) based on the requirement.
			-- Limit SELECT Columns: Select only necessary columns instead of using SELECT *.
			-- We can use EXPLAIN ANALYZE to Analyze Queries
			-- Example:

				EXPLAIN ANALYZE
				SELECT * FROM orders WHERE order_date >= '2023-01-01';

				-- Identifies slow steps (e.g., sequential scans).
				-- We need to rewrite the query or create appropriate indexes.

				-- Avoid this:
				SELECT * FROM orders;

				-- Use this:
				SELECT order_id, customer_id FROM orders;

	
		--Indexing
			-- Create Indexes: We can add indexes on columns frequently used in WHERE, JOIN, GROUP BY, or ORDER BY clauses.
				CREATE INDEX idx_name ON table_name (column_name);
			-- Use Partial Indexes: Index only the rows that meet a specific condition.
				CREATE INDEX idx_name ON table_name (column_name) WHERE condition;
			-- Use Composite Indexes: For queries filtering on multiple columns, create multi-column indexes.
				CREATE INDEX idx_name ON table_name (column1, column2);
			-- Index Types: Choosing index types like B-Tree (default), GIN, or GiST based on query patterns.
				-- B-tree Index (default): Efficient for equality and range queries.
				-- GIN Index: Best for full-text search.
				-- BRIN Index: Efficient for large tables with sequential data.
			-- Creatig an Index:

				-- Without an index
				SELECT * FROM orders WHERE customer_id = 12345;

				-- Creating an index on customer_id
				CREATE INDEX idx_customer_id ON orders(customer_id);

				-- Now the query will use the index for faster lookups
				EXPLAIN ANALYZE
				SELECT * FROM orders WHERE customer_id = 12345;
	
		-- Vacuum and Analyze
			-- VACUUM and ANALYZE are two essential commands in PostgreSQL for maintaining database health and performance
			-- Run VACUUM Regularly: Reclaims disk space by removing dead tuples (rows that have been deleted but not yet physically removed).
				-- Reorganizes data to improve query performance.
				-- We can use when the database has a high rate of inserts, updates, and deletes.
				-- We can use when we notice a significant increase in disk usage.

				VACUUM table_name;
					-- Does not shrink the table size: The reclaimed space is kept within the table for future use.
					-- Non-blocking: It doesn’t lock the table, so other queries can run simultaneously.
					--Lightweight and fast: Suitable for routine maintenance.
				VACUUM FULL table_name;
					-- Shrinks the table size: Frees up disk space by rewriting the entire table.
		            -- Exclusive table lock: The table is locked during the operation, making it unavailable for other queries.
					-- Resource-intensive: Takes longer and consumes more resources compared to standard VACUUM.

			-- Run ANALYZE to Update Statistics: Collects statistics about the contents of tables, such as the number of rows, minimum and maximum values, and data distribution.
				-- The query planner uses these statistics to optimize query execution plans.
				-- we can use after significant data modifications (inserts, updates, deletes).
				-- we can use after creating or modifying indexes.
				-- we can use When query performance degrades.

				ANALYZE table_name;  
				-- Analyses a specific table
				ANALYZE;  
				--  Analyses the entire database

			-- Enable Autovacuum: Ensure autovacuum is running for automatic maintenance.
	
		-- Table Partitioning: Divide large tables into smaller, more manageable pieces.
			CREATE TABLE orders (
				id SERIAL,
				customer_id INT,
				order_date DATE
			) PARTITION BY RANGE (order_date);

			CREATE TABLE orders_2023 PARTITION OF orders FOR VALUES FROM ('2023-01-01') TO ('2023-12-31');
			CREATE TABLE orders_2024 PARTITION OF orders FOR VALUES FROM ('2024-01-01') TO ('2024-12-31');

			-- This ensures queries on specific date ranges only scan relevant partitions.

		-- Parallel Queries: Enable parallel execution for large queries.

			-- Example: Configure Parallel Workers

				-- Enables parallel execution
				SET max_parallel_workers_per_gather = 4;

				-- Query that benefits from parallelism
				SELECT COUNT(*) FROM large_table;

		-- Avoid Over-Indexing: Too many indexes can slow down writes (e.g., INSERT, UPDATE).

			-- Example:

				-- Keep only necessary indexes
				DROP INDEX idx_unnecessary_index;
					
		


		

