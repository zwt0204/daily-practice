# LeetCode 0005 Longest Palindromic Substring

今日题目：LeetCode #5 Longest Palindromic Substring

题意简述：给你一个字符串 s，返回其中最长的回文子串。回文要求正反读一致，子串要求连续。

---

## 解法一：暴力枚举所有子串

### 思路要点
- 枚举所有子串 s[i:j+1]。
- 对每个子串判断是否回文。
- 记录最长答案。
- 这是最直观的做法，适合先建立题感，但性能最差。

### 时间/空间复杂度
- 时间复杂度：O(n^3)
  - 子串数量 O(n^2)
  - 每次判断回文最坏 O(n)
- 空间复杂度：O(1)
  - 若不计切片临时开销；若频繁切片，实际实现可能有额外代价

### 关键边界/易错点
- 空串或长度为 1 的字符串要直接返回自身。
- 子串必须是连续区间，不要和子序列混淆。
- 判断回文时，左右指针边界别写错。

### Python 代码
```python
class Solution:
    def longestPalindrome(self, s: str) -> str:
        n = len(s)
        if n <= 1:
            return s

        def is_pal(l: int, r: int) -> bool:
            while l < r:
                if s[l] != s[r]:
                    return False
                l += 1
                r -= 1
            return True

        ans_l, ans_r = 0, 0
        for l in range(n):
            for r in range(l, n):
                if r - l > ans_r - ans_l and is_pal(l, r):
                    ans_l, ans_r = l, r
        return s[ans_l:ans_r + 1]
```

---

## 解法二：枚举长度 + 双指针判断

### 思路要点
- 本质还是暴力，但优化枚举顺序：按子串长度从大到小枚举。
- 一旦找到某个长度的回文子串，立刻返回，因为已经是当前最大长度。
- 这样在很多实际输入下会比纯暴力快一些。

### 时间/空间复杂度
- 时间复杂度：最坏 O(n^3)
- 空间复杂度：O(1)

### 关键边界/易错点
- 长度枚举建议从 n 到 1，命中后立即返回。
- 注意右端点计算：r = l + length - 1。
- 这个做法只是“剪枝更早”，不是数量级优化。

### Python 代码
```python
class Solution:
    def longestPalindrome(self, s: str) -> str:
        n = len(s)
        if n <= 1:
            return s

        def is_pal(l: int, r: int) -> bool:
            while l < r:
                if s[l] != s[r]:
                    return False
                l += 1
                r -= 1
            return True

        for length in range(n, 0, -1):
            for l in range(0, n - length + 1):
                r = l + length - 1
                if is_pal(l, r):
                    return s[l:r + 1]
        return ""
```

---

## 解法三：动态规划

### 思路要点
- 定义 `dp[l][r]` 表示 `s[l:r+1]` 是否为回文。
- 转移条件：
  - `s[l] == s[r]`，且
  - `r - l <= 2`（长度为 1/2/3 时中间天然满足）或 `dp[l+1][r-1] == True`
- 按区间长度从小到大填表。
- 过程中维护最长区间。

### 时间/空间复杂度
- 时间复杂度：O(n^2)
- 空间复杂度：O(n^2)

### 关键边界/易错点
- 长度 1 一定是回文。
- 长度 2 和 3 是特殊情况，不能直接依赖 `dp[l+1][r-1]`。
- 遍历顺序要保证 `dp[l+1][r-1]` 已经算出来。

### Python 代码
```python
class Solution:
    def longestPalindrome(self, s: str) -> str:
        n = len(s)
        if n <= 1:
            return s

        dp = [[False] * n for _ in range(n)]
        start = 0
        max_len = 1

        for length in range(1, n + 1):
            for l in range(0, n - length + 1):
                r = l + length - 1
                if s[l] == s[r]:
                    if length <= 3 or dp[l + 1][r - 1]:
                        dp[l][r] = True
                        if length > max_len:
                            start = l
                            max_len = length

        return s[start:start + max_len]
```

---

## 解法四：中心扩展

### 思路要点
- 回文串一定有“中心”。
- 中心分两类：
  - 单字符中心，对应奇数长度回文
  - 双字符中心，对应偶数长度回文
- 以每个位置为中心向两边扩展，更新最长回文。
- 这是这题最常用、最好写、面试里最稳的解法。

### 时间/空间复杂度
- 时间复杂度：O(n^2)
- 空间复杂度：O(1)

### 关键边界/易错点
- 每个位置都要扩两次：`expand(i, i)` 和 `expand(i, i + 1)`。
- 返回左右边界时注意扩展结束后要回退一格。
- 当字符串全相同，例如 `aaaaa`，也要能正确返回整串。

### Python 代码
```python
class Solution:
    def longestPalindrome(self, s: str) -> str:
        n = len(s)
        if n <= 1:
            return s

        def expand(l: int, r: int):
            while l >= 0 and r < n and s[l] == s[r]:
                l -= 1
                r += 1
            return l + 1, r - 1

        ans_l, ans_r = 0, 0
        for i in range(n):
            l1, r1 = expand(i, i)
            l2, r2 = expand(i, i + 1)

            if r1 - l1 > ans_r - ans_l:
                ans_l, ans_r = l1, r1
            if r2 - l2 > ans_r - ans_l:
                ans_l, ans_r = l2, r2

        return s[ans_l:ans_r + 1]
```

---

## 解法五：Manacher 算法

### 思路要点
- 目标是把中心扩展从 O(n^2) 优化到 O(n)。
- 先对原串做预处理，在字符间插入分隔符，例如 `abba -> ^#a#b#b#a#$`，统一奇偶回文。
- `p[i]` 表示以 `i` 为中心的回文半径。
- 维护当前最右回文边界 `right` 及其中心 `center`。
- 若 `i < right`，可以利用镜像位置 `mirror = 2 * center - i` 的结果进行加速。
- 最终从最大半径还原原串区间。
- 这是最优解，但代码复杂，面试里如果时间紧，中心扩展通常更划算。

### 时间/空间复杂度
- 时间复杂度：O(n)
- 空间复杂度：O(n)

### 关键边界/易错点
- 预处理后的索引与原串索引转换最容易错。
- 分隔符和哨兵字符要保证不会越界。
- 半径、右边界、镜像点的定义要统一。

### Python 代码
```python
class Solution:
    def longestPalindrome(self, s: str) -> str:
        if not s:
            return ""

        t = "^#" + "#".join(s) + "#$"
        n = len(t)
        p = [0] * n
        center = 0
        right = 0

        for i in range(1, n - 1):
            mirror = 2 * center - i
            if i < right:
                p[i] = min(right - i, p[mirror])

            while t[i + 1 + p[i]] == t[i - 1 - p[i]]:
                p[i] += 1

            if i + p[i] > right:
                center = i
                right = i + p[i]

        max_len = 0
        center_index = 0
        for i in range(1, n - 1):
            if p[i] > max_len:
                max_len = p[i]
                center_index = i

        start = (center_index - max_len) // 2
        return s[start:start + max_len]
```

---

## 同类题目练习

1. `647 / Palindromic Substrings`
   - 为什么推荐练：同样是“回文中心扩展”的直接应用，但目标从“找最长”变成“统计总数”，能验证你是否真正掌握中心扩展模板。

2. `131 / Palindrome Partitioning`
   - 为什么推荐练：把“回文判断”与“DFS/回溯切分”结合起来，适合练习如何把回文预处理复用到搜索问题里。

3. `132 / Palindrome Partitioning II`
   - 为什么推荐练：继续围绕回文串，但升级成“最少切割次数”，适合练习区间 DP 与状态设计。

4. `516 / Longest Palindromic Subsequence`
   - 为什么推荐练：名字很像，但子串和子序列完全不同，特别适合用来校验自己有没有把“连续”这个条件吃透。

5. `5 / Longest Palindromic Substring` 的变体：自己补练“返回所有最长回文”“只返回长度”“统计不同回文子串”
   - 为什么推荐练：这些变体能逼你把边界、重复、索引转换彻底搞清楚。

---

## 复习 / 自测清单

- 我能否明确说出“子串”和“子序列”的区别？
- 我能否手写中心扩展，并同时覆盖奇数中心与偶数中心？
- 对输入 `s = "babad"`，我是否知道返回 `"bab"` 或 `"aba"` 都算对？
- 对输入 `s = "cbbd"`，我是否能正确得到偶数长度答案 `"bb"`？
- 对输入 `s = "a"`、`"ac"`、`"aaaa"`，代码是否都能正确处理？
- 我能否解释 DP 状态 `dp[l][r]` 的定义与转移条件？
- 我是否知道为什么长度 `<= 3` 时可以单独处理？
- 我能否说明中心扩展为什么通常比 DP 更适合面试手写？
- 我是否理解 Manacher 的收益点是“复用对称信息”，而不是单纯换一种写法？
- 如果让你像测试用例一样补充验证，你是否会覆盖：空串、单字符、全相同、无长度>1回文、奇偶长度回文、多个同长度答案并存？
