**Korean Blog Post**
===============

** Problem Description **

Recently, I encountered a problem on LeetCode, which is to find all numbers that appear at least three times consecutively. The problem is defined as follows:

* Table: `Logs`
* Columns:
	+ id (int): primary key, auto-increment
	+ num (varchar): number to be checked for consecutive appearances

The task is to write a SQL query that returns the result table in any order.

**Example**

Let's consider an example input and output:

Input:
```sql
Logs table:
+----+-----+
| id | num |
+----+-----+
| 1  | 1   |
| 2  | 1   |
| 3  | 1   |
| 4  | 2   |
| 5  | 1   |
| 6  | 2   |
| 7  | 2   |
+----+-----+
```

Output:
```sql
ConsecutiveNums table:
+-----------------+
| ConsecutiveNums |
+-----------------+
| 1               |
+-----------------+
```

Explanation: The number 1 is the only number that appears consecutively for at least three times.

**My SQL Code**

Here's my solution using a common table expression (CTE):
```sql
WITH temp AS (
    SELECT id, num,
    LEAD(id) OVER (ORDER BY id) AS id1,
    LEAD(num) OVER (ORDER BY id) AS num1,
    LEAD(id,2) OVER (ORDER BY id) AS id2,
    LEAD(num,2) OVER (ORDER BY id) AS num2
    FROM Logs
)
SELECT DISTINCT(num) AS ConsecutiveNums
FROM temp
WHERE (id1 - id) = 1 AND (id2 - id1) = 1 AND num = num1 AND num1 = num2;
```

**Evaluation of My Code**

My code uses a CTE to generate a temporary table that includes the current row's values, as well as the next two rows' values. The `LEAD` function is used to get the values of the next row and the row after that.

The query then selects distinct numbers from this temporary table, where the difference between consecutive ids is 1, and the number is the same for three consecutive rows.

**Better Code?**

Here's an alternative solution using a window function:
```sql
WITH temp AS (
    SELECT id, num,
    LAG(num) OVER (ORDER BY id) AS prev_num,
    LEAD(num) OVER (ORDER BY id) AS next_num
    FROM Logs
)
SELECT DISTINCT(num) AS ConsecutiveNums
FROM temp
WHERE prev_num = num AND next_num = num;
```

This code uses the `LAG` function to get the previous row's value, and the `LEAD` function to get the next row's value. The query then selects distinct numbers where the current number is the same as the previous and next numbers.

Both solutions should work correctly, but the second solution is more concise and easier to read.