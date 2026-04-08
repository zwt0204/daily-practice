# 今日题目

LeetCode #4 Median of Two Sorted Arrays

给定两个有序数组 `nums1` 和 `nums2`，返回这两个有序数组合并后的中位数。要求尽量做到比直接合并更优的时间复杂度。

---

# 5 个解法

## 解法 1：直接合并后排序（最直观暴力）

### 思路要点
- 先把两个数组拼接起来。
- 直接排序。
- 根据总长度奇偶，取中间一个数或中间两个数平均值。
- 这是最好理解、最容易写对的基线解法。

### 时间 / 空间复杂度
- 时间复杂度：`O((m+n) log(m+n))`
- 空间复杂度：`O(m+n)`

### 关键边界 / 易错点
- 总长度为偶数时，要返回浮点值 `(a+b)/2`。
- 一个数组为空时也应正常工作。
- 注意不要把中位数下标写错：奇数取 `n//2`，偶数取 `n//2-1` 和 `n//2`。

### Python 代码
```python
from typing import List

class Solution:
    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
        arr = nums1 + nums2
        arr.sort()
        n = len(arr)
        mid = n // 2
        if n % 2 == 1:
            return float(arr[mid])
        return (arr[mid - 1] + arr[mid]) / 2.0
```

---

## 解法 2：线性归并出完整有序数组

### 思路要点
- 利用两个数组本身有序这一条件，不再整体排序。
- 使用两个指针，像归并排序那样合并成一个新数组。
- 最后从新数组中取中位数。
- 比“拼接再排序”更合理，属于有序数组题的标准入门解法。

### 时间 / 空间复杂度
- 时间复杂度：`O(m+n)`
- 空间复杂度：`O(m+n)`

### 关键边界 / 易错点
- 某一个数组先走完后，要记得把另一个数组剩余部分追加进去。
- 比较时建议写成两个 while + 收尾逻辑，结构更清晰。
- 仍然要注意偶数长度时返回平均值。

### Python 代码
```python
from typing import List

class Solution:
    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
        i = j = 0
        merged = []
        
        while i < len(nums1) and j < len(nums2):
            if nums1[i] <= nums2[j]:
                merged.append(nums1[i])
                i += 1
            else:
                merged.append(nums2[j])
                j += 1
        
        while i < len(nums1):
            merged.append(nums1[i])
            i += 1
        
        while j < len(nums2):
            merged.append(nums2[j])
            j += 1
        
        n = len(merged)
        mid = n // 2
        if n % 2 == 1:
            return float(merged[mid])
        return (merged[mid - 1] + merged[mid]) / 2.0
```

---

## 解法 3：线性归并，但只保留走到中位数位置的元素

### 思路要点
- 其实没必要真的把整个合并数组都构造出来。
- 因为中位数只和中间位置有关，所以只需要模拟归并过程，走到第 `total//2` 个位置即可。
- 过程中只记录“当前值”和“前一个值”，用于处理偶数长度的情况。
- 这一步是典型的“空间优化但时间不变”。

### 时间 / 空间复杂度
- 时间复杂度：`O(m+n)`，但实际通常只走到中间，常数更小
- 空间复杂度：`O(1)`

### 关键边界 / 易错点
- 需要记录 `prev` 和 `curr` 两个值，否则偶数长度时没法取中间两个数。
- 当一个数组提前耗尽时，要继续从另一个数组取数。
- 循环次数要写成 `total // 2 + 1`，因为需要把中位位置的元素也取到。

### Python 代码
```python
from typing import List

class Solution:
    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
        m, n = len(nums1), len(nums2)
        total = m + n
        i = j = 0
        prev = curr = 0
        
        for _ in range(total // 2 + 1):
            prev = curr
            if i < m and (j >= n or nums1[i] <= nums2[j]):
                curr = nums1[i]
                i += 1
            else:
                curr = nums2[j]
                j += 1
        
        if total % 2 == 1:
            return float(curr)
        return (prev + curr) / 2.0
```

---

## 解法 4：找第 k 小元素（递归 / 迭代消去一半）

### 思路要点
- 中位数本质上是“第 k 小元素”问题。
- 若总长度为奇数，求第 `(m+n+1)//2` 小。
- 若总长度为偶数，求第 `(m+n)//2` 和第 `(m+n)//2+1` 小，再取平均。
- 每次比较两个数组各自第 `k//2` 个候选值，较小一侧的那一段不可能包含第 k 小元素，因此可以整体丢弃。
- 每轮能消掉大约一半目标规模，所以复杂度可到 `O(log(m+n))`。

### 时间 / 空间复杂度
- 时间复杂度：`O(log(m+n))`
- 空间复杂度：`O(1)`（若写成迭代）

### 关键边界 / 易错点
- 某个数组已经用完时，直接在另一个数组中取第 k 小。
- `k == 1` 时直接返回两个当前元素较小值。
- 计算新下标时不要越界，常用 `min(index + half, len) - 1`。
- 丢弃元素后，`k` 要同步减去被丢弃的数量。

### Python 代码
```python
from typing import List

class Solution:
    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
        def get_kth(k: int) -> int:
            i = j = 0
            while True:
                if i == len(nums1):
                    return nums2[j + k - 1]
                if j == len(nums2):
                    return nums1[i + k - 1]
                if k == 1:
                    return min(nums1[i], nums2[j])
                
                half = k // 2
                ni = min(i + half, len(nums1)) - 1
                nj = min(j + half, len(nums2)) - 1
                
                if nums1[ni] <= nums2[nj]:
                    k -= (ni - i + 1)
                    i = ni + 1
                else:
                    k -= (nj - j + 1)
                    j = nj + 1
        
        total = len(nums1) + len(nums2)
        if total % 2 == 1:
            return float(get_kth(total // 2 + 1))
        left = get_kth(total // 2)
        right = get_kth(total // 2 + 1)
        return (left + right) / 2.0
```

---

## 解法 5：二分划分（最优经典解）

### 思路要点
- 这是这道题的标志性最优解。
- 核心不是“合并”，而是“把两个数组切成左右两半”，并满足：
  - 左半部分元素总数等于右半部分，或者多 1 个；
  - `max(left_part) <= min(right_part)`。
- 设在 `nums1` 中切一刀位置 `i`，则在 `nums2` 中切刀位置自然是 `j = (m+n+1)//2 - i`。
- 然后用二分法在较短数组上找合适的 `i`。
- 找到后：
  - 奇数长度，中位数就是左半最大值；
  - 偶数长度，中位数是左半最大值与右半最小值的平均值。

### 时间 / 空间复杂度
- 时间复杂度：`O(log(min(m,n)))`
- 空间复杂度：`O(1)`

### 关键边界 / 易错点
- 一定要在较短数组上二分，否则边界处理更麻烦，甚至可能越界。
- 切在边界时，左边或右边可能为空，需要用 `-inf` / `inf` 兜底。
- `j` 的计算常见 off-by-one 错误，推荐固定使用 `(m+n+1)//2 - i`。
- 这是最容易“看懂了但写错”的题，建议自己手推至少 3 组样例：
  - 一个数组为空
  - 总长度奇数
  - 两数组长度差很大

### Python 代码
```python
from typing import List

class Solution:
    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
        # 保证 nums1 是更短的数组
        if len(nums1) > len(nums2):
            nums1, nums2 = nums2, nums1
        
        m, n = len(nums1), len(nums2)
        left, right = 0, m
        half = (m + n + 1) // 2
        
        while left <= right:
            i = (left + right) // 2
            j = half - i
            
            nums1_left = float('-inf') if i == 0 else nums1[i - 1]
            nums1_right = float('inf') if i == m else nums1[i]
            nums2_left = float('-inf') if j == 0 else nums2[j - 1]
            nums2_right = float('inf') if j == n else nums2[j]
            
            if nums1_left <= nums2_right and nums2_left <= nums1_right:
                if (m + n) % 2 == 1:
                    return float(max(nums1_left, nums2_left))
                return (max(nums1_left, nums2_left) + min(nums1_right, nums2_right)) / 2.0
            elif nums1_left > nums2_right:
                right = i - 1
            else:
                left = i + 1
        
        raise ValueError("Input arrays are not sorted or invalid")
```

---

# 同类题目练习

这题属于“有序数组上的二分 / 第 k 小元素 / 分割法”一类。推荐继续练这些：

1. **LeetCode 33 / Search in Rotated Sorted Array**  
   推荐原因：同样是“数组整体有序，但不能用普通线性思维”，训练你在有序结构上做二分判断。

2. **LeetCode 34 / Find First and Last Position of Element in Sorted Array**  
   推荐原因：强化二分边界处理，尤其是左边界 / 右边界模板，适合治 off-by-one。

3. **LeetCode 35 / Search Insert Position**  
   推荐原因：二分入门模板题，能帮你把“返回位置而不是值”的意识练扎实。

4. **LeetCode 153 / Find Minimum in Rotated Sorted Array**  
   推荐原因：继续训练“局部有序 + 条件判断 + 缩小区间”的能力，和本题一样重边界。

5. **LeetCode 4 / Median of Two Sorted Arrays（重写一遍）**  
   推荐原因：这题本身就值得二刷。第一次看懂思路不算会，能不看题解独立写出二分划分才算真的掌握。

6. **LeetCode 215 / Kth Largest Element in an Array**  
   推荐原因：虽然不再是有序数组，但“第 k 个元素”的问题意识是共通的，能帮助你建立选择问题的统一视角。

---

# 复习 / 自测清单

像做测试用例一样，把下面这些点自己过一遍：

- [ ] 我能说清楚“中位数”为什么能转化成“第 k 小元素”。
- [ ] 我能解释为什么二分划分里要在更短数组上做二分。
- [ ] 我知道 `j = (m+n+1)//2 - i` 为什么这样算。
- [ ] 我能处理一个数组为空、另一个数组非空的情况。
- [ ] 我能处理总长度为奇数和偶数两种返回逻辑。
- [ ] 我不会把左右分区的边界值写反。
- [ ] 我会用 `-inf` / `inf` 处理切割点落在数组两端的情况。
- [ ] 我能手推下面样例并验证代码：
  - `nums1 = [1, 3], nums2 = [2]` → `2.0`
  - `nums1 = [1, 2], nums2 = [3, 4]` → `2.5`
  - `nums1 = [], nums2 = [1]` → `1.0`
  - `nums1 = [0, 0], nums2 = [0, 0]` → `0.0`
  - `nums1 = [2], nums2 = []` → `2.0`
- [ ] 我能在不看答案的前提下，独立写出 `O(log(min(m,n)))` 解法。

今天这题的重点不是背代码，是把“分割视角”真正建立起来。你如果只能写出归并版，说明基础没问题；你如果能稳定写出二分划分版，才算把这题拿下。