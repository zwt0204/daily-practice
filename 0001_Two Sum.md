# 今日题目：LeetCode #1 Two Sum

给定整数数组 `nums` 和目标值 `target`，返回两个下标 `i, j`，使得 `nums[i] + nums[j] == target`，且不能重复使用同一个元素。

下面按“从暴力到最优”的顺序，给 5 种写法。这个题本质是：**在遍历到当前数时，快速判断“我需要的另一个数”是否已经出现过**。

---

## 解法 1：双重循环暴力枚举

### 思路要点
- 枚举所有 `(i, j)` 组合。
- 只要 `i < j` 且 `nums[i] + nums[j] == target`，立即返回。
- 优点是直观、稳定、几乎不容易写错；缺点是慢。

### 时间 / 空间复杂度
- 时间复杂度：`O(n^2)`
- 空间复杂度：`O(1)`

### 关键边界 / 易错点
- 内层循环必须从 `i + 1` 开始，避免重复使用同一个元素。
- 返回的是**下标**，不是数值。
- 题目通常保证有解；若写通用代码，最好兜底返回空列表。

### Python 代码
```python
from typing import List

class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        n = len(nums)
        for i in range(n):
            for j in range(i + 1, n):
                if nums[i] + nums[j] == target:
                    return [i, j]
        return []
```

---

## 解法 2：先固定一个数，再线性查找补数

### 思路要点
- 对每个 `nums[i]`，先算出 `need = target - nums[i]`。
- 在 `i` 后面的区间中线性查找 `need`。
- 本质上仍然是 `O(n^2)`，但思路更贴近“补数”模型。

### 时间 / 空间复杂度
- 时间复杂度：`O(n^2)`
- 空间复杂度：`O(1)`

### 关键边界 / 易错点
- 查找范围仍然只能是 `i + 1 ~ n-1`，否则可能命中自己。
- 这种写法只是表达方式更清晰，性能并没有本质提升。

### Python 代码
```python
from typing import List

class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        n = len(nums)
        for i in range(n):
            need = target - nums[i]
            for j in range(i + 1, n):
                if nums[j] == need:
                    return [i, j]
        return []
```

---

## 解法 3：排序后双指针（保留下标）

### 思路要点
- 直接对原数组排序会丢失原始下标，所以先构造 `(值, 下标)`。
- 按值排序后，用双指针 `l`、`r`：
  - 和太小，左指针右移；
  - 和太大，右指针左移；
  - 相等则返回对应原始下标。
- 这个思路对 `Two Sum II`、`3Sum`、`4Sum` 都很有迁移价值。

### 时间 / 空间复杂度
- 时间复杂度：`O(n log n)`
- 空间复杂度：`O(n)`

### 关键边界 / 易错点
- 题目要求返回原数组下标，不能直接返回排序后的指针位置。
- 有重复值时也没问题，因为我们保存了每个元素自己的原始下标。
- 返回顺序一般不限，但如果你有统一风格，可以返回升序下标。

### Python 代码
```python
from typing import List

class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        arr = [(num, idx) for idx, num in enumerate(nums)]
        arr.sort(key=lambda x: x[0])

        l, r = 0, len(arr) - 1
        while l < r:
            s = arr[l][0] + arr[r][0]
            if s == target:
                return [arr[l][1], arr[r][1]]
            elif s < target:
                l += 1
            else:
                r -= 1
        return []
```

---

## 解法 4：哈希表两遍扫描

### 思路要点
- 第一遍：把每个值及其下标放进哈希表。
- 第二遍：对每个 `nums[i]`，查 `target - nums[i]` 是否存在。
- 若存在，还要确保不是同一个下标。
- 这是很多人最容易想到、也很好解释的哈希解。

### 时间 / 空间复杂度
- 时间复杂度：`O(n)`
- 空间复杂度：`O(n)`

### 关键边界 / 易错点
- 若数组有重复值，例如 `[3, 3]`、`target = 6`，哈希表里只留最后一个下标也没关系，但判断时要确保 `i != j`。
- 两遍扫描比一遍扫描更啰嗦，但逻辑更分层，适合初学时写对。

### Python 代码
```python
from typing import List

class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        index_map = {}
        for i, num in enumerate(nums):
            index_map[num] = i

        for i, num in enumerate(nums):
            need = target - num
            if need in index_map and index_map[need] != i:
                return [i, index_map[need]]
        return []
```

---

## 解法 5：哈希表一遍扫描（最优常规解）

### 思路要点
- 一边遍历，一边把“已经看过的数”放进哈希表。
- 当前值是 `num`，先查 `need = target - num` 是否已出现。
- 如果已出现，直接返回 `[之前的下标, 当前下标]`。
- 如果未出现，再把当前值写入哈希表。
- 这是面试和实战里最推荐的写法：**单遍扫描 + 哈希查补数**。

### 时间 / 空间复杂度
- 时间复杂度：`O(n)`
- 空间复杂度：`O(n)`

### 关键边界 / 易错点
- **顺序不能反**：必须先查补数，再写当前值；否则在 `target = 2 * num` 时可能错误地用到自己。
- 对重复值场景要特别敏感，比如 `[3, 3]`。
- 题目若不保证一定有解，建议最后返回空列表。

### Python 代码
```python
from typing import List

class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        seen = {}
        for i, num in enumerate(nums):
            need = target - num
            if need in seen:
                return [seen[need], i]
            seen[num] = i
        return []
```

---

## 同类题目练习

### 15. 3Sum
- 推荐原因：从 `Two Sum` 升级到“三数之和”，典型套路是**排序 + 固定一个数 + 双指针做 Two Sum**。

### 16. 3Sum Closest
- 推荐原因：仍然是排序 + 双指针，但目标从“精确命中”变成“最接近目标值”，适合练习指针移动策略。

### 18. 4Sum
- 推荐原因：把 `Two Sum / 3Sum` 继续扩展到四数场景，训练多层枚举、去重和剪枝能力。

### 167. Two Sum II - Input Array Is Sorted
- 推荐原因：这是 `Two Sum` 的有序数组版本，最优解直接用**双指针**，可以对比哈希表方案。

### 560. Subarray Sum Equals K
- 推荐原因：题型从“两个数”切换到“连续子数组”，核心仍是“找补数”，但补数对象变成了**前缀和**。

---

## 复习 / 自测清单

把自己当成在写测试用例，至少过一遍下面这些点：

- 能不能清楚说出：为什么一遍哈希解法要“先查后存”？
- 输入 `nums = [2, 7, 11, 15], target = 9`，是否返回合法下标 `[0, 1]`？
- 输入 `nums = [3, 2, 4], target = 6`，是否正确处理“补数在后面出现”的情况？
- 输入 `nums = [3, 3], target = 6`，是否避免把同一个元素用两次？
- 输入包含负数时，例如 `[-1, -2, -3, -4, -5], target = -8`，逻辑是否仍然正确？
- 如果把题目改成“返回所有解对”，当前代码为什么不够用？需要补哪些去重逻辑？
- 如果数组已经有序，为什么双指针能做，哈希表又为什么仍然能做？
- 你是否能从 `Two Sum` 自然迁移到 `3Sum / 4Sum / 前缀和补数` 这几类题？

今天这题不难，但很基础。别把它当签到题，它是很多哈希、双指针、前缀和题的母题。