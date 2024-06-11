# Consecutive Numbers: LeetCode Problem Solution

## ������ ���̺� ���� ����

### ����:

������ "Consecutive Numbers"��� �̸��� LeetCode �����Դϴ�. �� ���������� `Logs` ���̺��� �־�����, �̴� �����Ͱ� �Ϸ��� ��ȣ�� �����Ǿ� �ִٰ� �����մϴ�.

**���̺� & ����:**

```sql
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| id          | int     |
| num         | varchar |
+-------------+---------+
In SQL, id is the primary key for this table.
id is an autoincrement column.
```

������ ������ ����:

> Find all numbers that appear at least three times consecutively.

��, �� ���������� `num` �÷����� �ּ� �� �� �̻� �����ؼ� ��Ÿ���� ��� ���� ã����� ���� �ǹ��մϴ�. 

## Ǯ�� �� �ǵ��

### �� �ڵ�:

���� �ۼ��� �ڵ�� ������ �����ϴ�:
```sql
WITH temp AS (
    SELECT id,num,
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

�� �ڵ带 �����ϸ�, ������ �����ϴ�:
- `temp`��� ��Ī�� ����Ͽ� �� ���� ID�� �� ���� �� ���� ID�� ����ϰ� �̸� �����ϴ� �������� ������ ���̺��� ����ϴ�.
- �׷� ���� �ش� �������� �Ϸ��� ���� �̷�� �ִ��� Ȯ���մϴ�. �̴� `id1`�� `id` ������ ���̰� 1�̰�, `id2`, `id1` ������ ���̵� 1�̸�, ������ ���ڰ� �� �� ���� ��Ÿ������ �մϴ�.

### �ǵ��:

������ �ڵ� ��ҿ� ���� ������ �ǵ���� ������ �����ϴ�:
- **������ ó��:** �ڵ�� ���ϴ� ����� ��� ���� �����͸� �����ϰ� ó���ϰ� �ֽ��ϴ�. 
- **���뼺:** �ڵ�� SQL ���������� window functions�� ����Ͽ� ������ ȿ�������� �ذ��մϴ�.
  
������ �������� ���� �ܰ����� �ǵ���Դϴ�:
1. **�������� ȿ����:** �����Ͱ� ū ���̺��� ��, �� ������ �ð� ���⵵�� ���� �� �ֽ��ϴ�. `Logs` ���̺��� ID�� ���� �����ϰ� �� �ķ� ó���ϴ� ����� ����� ���� ���� ������ �� �ֽ��ϴ�.
2. **������ ����:** �ڵ� ���ο��� ���� ���ؽ�Ʈ�� ���� �پ��� SQL ������ ����� �ʿ䰡 ���� �� �ֽ��ϴ�. ���� ���, `LEAD` �Լ��� �� ���ڵ带 �����ϴ� ���� ������ ID�� ������ ã�µ� ���˴ϴ�.
3. **���ư� ���� ����:** �ڵ�� �ſ� ��Ȯ�ϰ� �ۼ��Ǿ� ������, �߰����� �ּ��� ������ �ξ� �� ���ڿ��� ��Ȯ�� ������ ������ �� �ֽ��ϴ�.

### ������ �ڵ� ����:

������ �ڵ��� �� ���� ������ ���� ������ �ݿ��� �ڵ��Դϴ�:
```sql
WITH temp AS (
    SELECT id, num,
        LAG(id) OVER (ORDER BY id) as prev_id, -- �� �� ID�� ������ ����
        LEAD(id) OVER (ORDER BY id) as next_id, -- ���� ���� ID�� ������ ����
        LAG(num, 2) OVER (ORDER BY id) as prev_num1,
        LAG(num, 3) OVER (ORDER BY id) as prev_num2,
        LEAD(num, 2) OVER (ORDER BY id) as next_num1,
        LEAD(num, 3) OVER (ORDER BY id) as next_num2
    FROM Logs
)
SELECT DISTINCT(num) AS ConsecutiveNums 
FROM temp
WHERE (prev_id + 1 = id AND prev_num1 = num AND prev_num2 = num) OR (id - 1 = prev_id AND next_id - id = 1 AND num = next_num1 AND num = next_num2);
```

�� �ڵ�� `prev_id`, `next_id`, `prev_num1`, `prev_num2`, `next_num1`, `next_num2`�� ����Ͽ� �� ���� ���� ID�� ���� ID, �׸��� �� ������ ������ ���� �����ϰ� �ֽ��ϴ�. �̷��� �ϸ� ������ �ڵ尡 �� ȿ�����̸� ��Ȯ�� ������ �����ϸ鼭 �ڵ带 �����Ͽ����ϴ�.