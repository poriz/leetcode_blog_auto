# Consecutive Numbers: LeetCode Problem Solution

## 문제와 테이블에 대한 정보

### 문제:

문제는 "Consecutive Numbers"라는 이름의 LeetCode 문제입니다. 이 문제에서는 `Logs` 테이블이 주어지며, 이는 데이터가 일련의 번호로 구성되어 있다고 가정합니다.

**테이블 & 예제:**

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

다음은 문제의 설명:

> Find all numbers that appear at least three times consecutively.

즉, 이 문제에서는 `num` 컬럼에서 최소 세 번 이상 연속해서 나타나는 모든 수를 찾으라는 것을 의미합니다. 

## 풀이 및 피드백

### 내 코드:

내가 작성한 코드는 다음과 같습니다:
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

이 코드를 설명하면, 다음과 같습니다:
- `temp`라는 별칭을 사용하여 각 행의 ID와 그 다음 두 개의 ID를 계산하고 이를 포함하는 시퀀스로 구성된 테이블을 만듭니다.
- 그런 다음 해당 시퀀스가 일련의 수를 이루고 있는지 확인합니다. 이는 `id1`과 `id` 사이의 차이가 1이고, `id2`, `id1` 사이의 차이도 1이며, 동일한 숫자가 세 번 연속 나타나도록 합니다.

### 피드백:

각각의 코드 요소에 대한 간단한 피드백은 다음과 같습니다:
- **데이터 처리:** 코드는 원하는 결과를 얻기 위해 데이터를 적절하게 처리하고 있습니다. 
- **적용성:** 코드는 SQL 서브쿼리와 window functions를 사용하여 문제를 효과적으로 해결합니다.
  
다음은 개선점에 대한 단계적인 피드백입니다:
1. **데이터의 효율성:** 데이터가 큰 테이블일 때, 이 쿼리는 시간 복잡도가 높을 수 있습니다. `Logs` 테이블의 ID를 먼저 정렬하고 그 후로 처리하는 방법을 고려해 보는 것이 유용할 수 있습니다.
2. **문법적 개선:** 코드 내부에서 사용된 컨텍스트에 따라 다양한 SQL 문법을 고려할 필요가 있을 수 있습니다. 예를 들어, `LEAD` 함수는 각 레코드를 포함하는 동안 다음의 ID나 값들을 찾는데 사용됩니다.
3. **문맥과 로직 이해:** 코드는 매우 명확하게 작성되어 있지만, 추가적인 주석이 있으면 훨씬 더 독자에게 명확한 정보를 전달할 수 있습니다.

### 개선된 코드 예시:

다음은 코드의 한 가지 가능한 개선 사항을 반영한 코드입니다:
```sql
WITH temp AS (
    SELECT id, num,
        LAG(id) OVER (ORDER BY id) as prev_id, -- 앞 행 ID를 얻어오기 위함
        LEAD(id) OVER (ORDER BY id) as next_id, -- 다음 행의 ID를 얻어오기 위함
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

이 코드는 `prev_id`, `next_id`, `prev_num1`, `prev_num2`, `next_num1`, `next_num2`를 사용하여 각 행의 이전 ID와 다음 ID, 그리고 그 값들을 얻어오는 것을 보완하고 있습니다. 이렇게 하면 원래의 코드가 더 효율적이며 명확한 로직을 유지하면서 코드를 개선하였습니다.