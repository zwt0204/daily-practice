# LeetCode 0011 - Container With Most Water

## 今日题目

LeetCode #11 Container With Most Water

题意可概括为：给定一个数组 `height`，第 `i` 根竖线高度为 `height[i]`。从中选两根线，与 x 轴形成一个容器，容器可盛水量为：

`(right - left) * min(height[left], height[right])`

要求返回最大盛水量。

---

## 解法 1：双重枚举暴力

### 思路要点
- 枚举所有 `(i, j)` 组合。
- 对每一对下标直接计算面积。
- 保留最大值。
- 这是最直观的基线解，适合理解题意与校验样例。

### 时间/空间复杂度
- 时间复杂度：`O(n^2)`
- 空间复杂度：`O(1)`

### 关键边界 / 易错点
- 容器宽度是下标差 `j - i`，不是 `j - i + 1`。
- 高度取两边较小值，不是较大值。
- 数组长度若小于 2，无法形成容器，返回 0。

### Python 代码
```python
from typing import List

class Solution:
    def maxArea(self, height: List[int]) -> int:
        n = len(height)
        if n < 2:
            return 0

        ans = 0
        for i in range(n):
            for j in range(i + 1, n):
                area = (j - i) * min(height[i], height[j])
                ans = max(ans, area)
        return ans
```

---

## 解法 2：暴力 + 左端剪枝

### 思路要点
- 仍然枚举所有右端点，但对左端点增加一个简单剪枝。
- 如果 `height[i] * (n - 1 - i)` 都不可能超过当前答案，说明以 `i` 为左边界不值得继续枚举。
- 本质仍是暴力，只是减少一部分无效计算。

### 时间/空间复杂度
- 最坏时间复杂度：`O(n^2)`
- 空间复杂度：`O(1)`

### 关键边界 / 易错点
- 剪枝上界要取“最远宽度”乘“左边高度”，这是保守上界，不要写成当前 `j` 的宽度。
- 剪枝只能“少算”，不能改变正确性。
- 这类剪枝对某些数据有效，但最坏情况仍会退化到平方复杂度。

### Python 代码
```python
from typing import List

class Solution:
    def maxArea(self, height: List[int]) -> int:
        n = len(height)
        if n < 2:
            return 0

        ans = 0
        for i in range(n - 1):
            # 以 i 为左端，理论最大宽度是 n - 1 - i
            if height[i] * (n - 1 - i) <= ans:
                continue

            for j in range(i + 1, n):
                area = (j - i) * min(height[i], height[j])
                if area > ans:
                    ans = area
        return ans
```

---

## 解法 3：按宽度从大到小枚举

### 思路要点
- 容器面积 = 宽度 × 较短板高度。
- 可以先枚举宽度 `w`，从大到小尝试，再枚举对应的 `(i, i + w)`。
- 这样做的优点是更贴近“先看大宽度”的直觉，有助于理解后续双指针为什么有效。
- 但它本质仍然要遍历大量组合，性能并不理想。

### 时间/空间复杂度
- 时间复杂度：`O(n^2)`
- 空间复杂度：`O(1)`

### 关键边界 / 易错点
- 宽度循环要从 `n - 1` 到 `1`。
- 面积依然是 `w * min(height[i], height[i + w])`。
- 不要误以为“先枚举大宽度”就自动更优，它只是换了遍历顺序。

### Python 代码
```python
from typing import List

class Solution:
    def maxArea(self, height: List[int]) -> int:
        n = len(height)
        if n < 2:
            return 0

        ans = 0
        for w in range(n - 1, 0, -1):
            for i in range(n - w):
                j = i + w
                area = w * min(height[i], height[j])
                ans = max(ans, area)
        return ans
```

---

## 解法 4：双指针（标准最优）

### 思路要点
- 初始左右指针放在数组两端，这时宽度最大。
- 当前面积由短板决定：`(r - l) * min(height[l], height[r])`。
- 如果移动高的一侧，宽度变小，而短板未必变大，通常没有收益。
- 因此应该移动更短的那一侧，尝试寻找更高的短板。
- 这是本题的核心贪心思想，也是最经典解法。

### 时间/空间复杂度
- 时间复杂度：`O(n)`
- 空间复杂度：`O(1)`

### 关键边界 / 易错点
- 只移动短板一侧；若两侧相等，移动任意一侧都可以。
- 每次都要先计算当前面积，再移动指针。
- 不要把“更高的一侧更有希望”理解反了，真正限制面积的是短板。

### Python 代码
```python
from typing import List

class Solution:
    def maxArea(self, height: List[int]) -> int:
        l, r = 0, len(height) - 1
        ans = 0

        while l < r:
            area = (r - l) * min(height[l], height[r])
            ans = max(ans, area)

            if height[l] < height[r]:
                l += 1
            else:
                r -= 1

        return ans
```

---

## 解法 5：双指针 + 跳过无效矮板（最优实现版）

### 思路要点
- 基于标准双指针继续优化。
- 当左边更短时，左指针右移到“第一个比当前左高的位置”；中间那些不更高的线即使参与，也因为宽度更小、短板不更高，不可能更优。
- 右边同理。
- 这个版本和标准双指针一样保持线性复杂度，但常数因子可能更好。

### 时间/空间复杂度
- 时间复杂度：`O(n)`
- 空间复杂度：`O(1)`

### 关键边界 / 易错点
- 跳过时要保存旧高度作为阈值。
- 不要跨过边界：循环里始终保持 `l < r`。
- 这类“跳过不可能更优状态”的写法，本质还是建立在标准双指针正确性上。

### Python 代码
```python
from typing import List

class Solution:
    def maxArea(self, height: List[int]) -> int:
        l, r = 0, len(height) - 1
        ans = 0

        while l < r:
            left_h, right_h = height[l], height[r]
            ans = max(ans, (r - l) * min(left_h, right_h))

            if left_h <= right_h:
                while l < r and height[l] <= left_h:
                    l += 1
            else:
                while l < r and height[r] <= right_h:
                    r -= 1

        return ans
```

---

## 同类题目练习

这题本质是：双指针 + 贪心地缩小搜索空间。不是滑窗，因为窗口是否合法不靠“频次约束”，而是靠“面积上界”来淘汰状态。

1. **LeetCode 15 - 3Sum**  
   推荐原因：排序后双指针的代表题，重点练“固定一个点 + 左右夹逼 + 去重”。

2. **LeetCode 16 - 3Sum Closest**  
   推荐原因：同样是排序后双指针，但目标从“找满足条件”变成“逼近最优值”，能强化指针移动直觉。

3. **LeetCode 167 - Two Sum II - Input Array Is Sorted**  
   推荐原因：最基础的有序数组双指针题，适合巩固“和偏大/偏小时移动哪边”。

4. **LeetCode 42 - Trapping Rain Water**  
   推荐原因：也是“高度数组 + 双指针/左右边界”类高频题，容易和本题一起对照复习。

5. **LeetCode 581 - Shortest Unsorted Continuous Subarray**  
   推荐原因：虽然不完全同型，但也是通过双端收缩/边界判断来缩小答案区间，适合训练边界意识。

6. **LeetCode 84 - Largest Rectangle in Histogram**  
   推荐原因：同样和“面积、宽度、高度”有关，但换成单调栈思路，适合做横向对比：什么时候双指针不够，什么时候需要结构化边界信息。

---

## 复习 / 自测清单

把这题当成一组测试用例来过：

- [ ] 我能否准确写出面积公式：`(j - i) * min(height[i], height[j])`
- [ ] 我是否清楚为什么取较短板，而不是较高板
- [ ] 我能否解释：为什么移动较高的一侧通常不会让答案变好
- [ ] 当 `height[left] == height[right]` 时，我是否知道任意移动一侧都可以
- [ ] 输入只有 2 根线时，我的代码是否能正确返回结果
- [ ] 输入单调递增 / 单调递减数组时，我是否验证过结果
- [ ] 输入存在大量重复高度时，我的双指针代码是否仍正确
- [ ] 我能否区分这题是“双指针贪心”而不是“滑动窗口”
- [ ] 我能否在 1 分钟内从暴力法推导到双指针最优解
- [ ] 我能否口头证明双指针解法不会漏掉最优答案
