# LeetCode Problem Solving: Product Price at a Given Date (문제번호) 

## 문제와 테이블

### 문제 및 설명

<code>Product Price at a Given Date</code>(문제번호)는 다음과 같은 구조를 갖습니다. 이 문제에서는 특정 날짜에 따른 제품 가격을 확인해야 합니다.

<p>
- **테이블: Products**

  <pre>
+---------------+---------+
| Column Name   | Type    |
+---------------+---------+
| product_id    | int     |
| new_price     | int     |
| change_date   | date    |
+---------------+---------+
(product_id, change_date)는 이 테이블의 주 키이며, 각 행은 제품의 가격이 변경되는 날짜와 해당 날짜에 적용된 가격을 나타냅니다.
  </pre>
  
### 문제 설명
  
주어진 `change_date`가 `2019-08-16`일 경우 각 제품의 가격을 찾는 것이 목표입니다. 만약 어떤 제품의 가격이 변경되었던 적이 없거나, 그 날짜 이후에 가격을 확인하는 것이 필요하다면 기본 가격으로 10을 사용합니다.

---

## 풀이 및 피드백

### 풀이

제가 제시한 SQL 구문은 다음과 같습니다. 

```sql
WITH temp AS (
    SELECT
        product_id,
        new_price,
        change_date,
        max(change_date) OVER (PARTITION BY product_id ORDER BY product_id)AS recent_date
    FROM
        products
    WHERE 
        change_date <= '2019-08-16'
)

SELECT product_id, new_price AS price
FROM temp
WHERE change_date = recent_date

UNION

SELECT
    DISTINCT(product_id),
    10 AS price
FROM products
GROUP BY product_id
HAVING min(change_date) > '2019-08-16'

```

### 피드백 및 개선점

제가 선택한 방법론은 매우 효율적인 해결책입니다.

1. `WITH` 절을 사용하여 <code>change_date</code>가 `2019-08-16`보다 작거나 같고, 제품의 가격이 가장 최근에 변경된 날짜를 찾는 데 사용한 '최대값' 기능을 활용했습니다.
   
2. 두 가지 경우를 별도로 처리하는 SQL 구문은 매우 직관적입니다: 

    - 첫 번째 부분은 주어진 일자 이후의 최신 가격을 선택합니다.

    - 두 번째 부분에서는 주어진 날짜보다 이른 시점에서 가격이 변경되지 않은 제품에 대해 기본 가격을 적용하였습니다. 이를 위해 `GROUP BY`와 `HAVING` 구문을 사용하여 그룹별로 최소한의 change_date를 확인했습니다.

### 내 코드 설명

제가 제안한 방법은 성능면에서도 효율적인 풀이 방식입니다. 이 문제에서는 특정 날짜 이후의 가격 변경 사항에 초점을 맞춘 것이 중요합니다. `WITH` 절을 이용하여 최적화된 쿼리를 작성하였고 이를 두 개의 부분으로 나눈 것입니다.

제가 선택한 방법은 기본 가격과 변경된 가격 사이에서 올바른 결정을 내리는데 유용했습니다. 이 문제를 풀면서 SQL의 `OVER` 및 `PARTITION BY`, `GROUP BY`, `HAVING` 등의 기능에 대해 잘 이해하는 것이 중요하였습니다.

## 결론

이 문제는 효율적인 데이터 분석 기술과 SQL의 여러 고급 기능을 활용한 좋은 연습이었습니다. 이와 같은 방법을 통해 다양한 상황에 대처하고 필요한 정보를 빠르고 정확하게 추출할 수 있다는 것을 배울 수 있었습니다.