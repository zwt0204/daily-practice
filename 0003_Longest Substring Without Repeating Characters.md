# LeetCode #3 Longest Substring Without Repeating Characters

今日题目：LeetCode #3 Longest Substring Without Repeating Characters

题意一句话：给定一个字符串 `s`，返回**不含重复字符的最长子串长度**。

---

## 解法1：暴力枚举所有子串

### 思路要点
- 枚举每个起点 `i` 和终点 `j`，截取子串 `s[i:j+1]`。
- 再判断这个子串是否有重复字符。
- 如果无重复，就更新最大长度。
- 这是最直观的基线解法，优点是好想，缺点是慢。

### 时间/空间复杂度
- 时间复杂度：`O(n^3)`
  - 两层枚举子串是 `O(n^2)`
  - 每次判断是否重复约 `O(n)`
- 空间复杂度：`O(n)`

### 关键边界/易错点
- 空串要返回 `0`。
- 子串是连续的，不能把不连续字符拼起来。
- `len(sub) == len(set(sub))` 虽然好写，但大数据下很慢。

### Python 代码
```python
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        n = len(s)
        ans = 0

        for i in range(n):
            for j in range(i, n):
                sub = s[i:j + 1]
                if len(sub) == len(set(sub)):
                    ans = max(ans, j - i + 1)

        return ans
```

---

## 解法2：固定左端点，向右扩展直到重复

### 思路要点
- 仍然枚举左端点 `i`。
- 但从 `i` 出发向右扫时，用一个集合 `seen` 记录当前窗口字符。
- 一旦发现重复字符，就可以直接停止当前起点的扩展，因为再往后也不可能让这个以 `i` 开头的窗口继续合法。
- 比完整暴力好一些，但本质仍是二重扫描。

### 时间/空间复杂度
- 时间复杂度：`O(n^2)`
- 空间复杂度：`O(min(n,字符集大小))`

### 关键边界/易错点
- 每换一个新的左端点，都要重新初始化 `seen`。
- 遇到重复字符时要 `break`，因为当前起点下更长子串一定也不合法。
- 对于 `"bbbbb"` 这种重复密集字符串，能很快结束单轮扫描，但总复杂度仍然是平方级。

### Python 代码
```python
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        n = len(s)
        ans = 0

        for i in range(n):
            seen = set()
            for j in range(i, n):
                if s[j] in seen:
                    break
                seen.add(s[j])
                ans = max(ans, j - i + 1)

        return ans
```

---

## 解法3：滑动窗口 + 集合

### 思路要点
- 用双指针维护一个无重复窗口 `[left, right]`。
- 每次尝试把 `s[right]` 放进窗口。
- 如果发现重复，就不断移动 `left`，并把左侧字符从集合中删掉，直到窗口重新无重复。
- 然后更新答案。
- 这是经典滑窗模板，适合理解“窗口收缩”的过程。

### 时间/空间复杂度
- 时间复杂度：`O(n)`
  - 每个字符最多进窗口一次、出窗口一次
- 空间复杂度：`O(min(n,字符集大小))`

### 关键边界/易错点
- 收缩窗口时必须先删 `s[left]`，再 `left += 1`。
- `while s[right] in seen:` 不能写成 `if`，因为可能要连续删多个字符。
- 更新答案通常放在窗口合法之后。

### Python 代码
```python
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        seen = set()
        left = 0
        ans = 0

        for right, ch in enumerate(s):
            while ch in seen:
                seen.remove(s[left])
                left += 1
            seen.add(ch)
            ans = max(ans, right - left + 1)

        return ans
```

---

## 解法4：滑动窗口 + 哈希表记录最后出现位置

### 思路要点
- 进一步优化滑窗：没必要一个个删除左边字符。
- 用字典 `last` 记录每个字符最后一次出现的下标。
- 当扫描到 `s[right] = ch`：
  - 如果 `ch` 在当前窗口中出现过，那么直接把 `left` 跳到 `last[ch] + 1`。
- 这样避免了逐个删除，代码更短，思路更“索引化”。

### 时间/空间复杂度
- 时间复杂度：`O(n)`
- 空间复杂度：`O(min(n,字符集大小))`

### 关键边界/易错点
- `left = max(left, last[ch] + 1)`，这里必须取 `max`。
- 如果不取 `max`，`left` 可能被错误地往回拉，导致窗口失真。
- 典型例子：`"abba"`。

### Python 代码
```python
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        last = {}
        left = 0
        ans = 0

        for right, ch in enumerate(s):
            if ch in last:
                left = max(left, last[ch] + 1)
            last[ch] = right
            ans = max(ans, right - left + 1)

        return ans
```

---

## 解法5：滑动窗口 + 定长数组（字符集已知时更实用）

### 思路要点
- 如果题目输入主要是 ASCII 字符，可以把哈希表换成定长数组。
- 用 `pos[ord(ch)]` 存最后出现位置，初始设为 `-1`。
- 相比字典，常数更稳，面试里也能体现你知道“哈希表还能继续压常数”。
- 本质仍是“最后出现位置 + 左边界跳跃”。

### 时间/空间复杂度
- 时间复杂度：`O(n)`
- 空间复杂度：`O(1)`（若字符集固定为 ASCII/扩展 ASCII）

### 关键边界/易错点
- 只有在字符集范围明确时，这个写法才更合适。
- 如果输入可能包含任意 Unicode，字典版更稳妥。
- 初始值建议设为 `-1`，便于统一处理首字符。

### Python 代码
```python
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        pos = [-1] * 128  # 若担心非 ASCII，可改回 dict
        left = 0
        ans = 0

        for right, ch in enumerate(s):
            idx = ord(ch)
            if idx < 128:
                left = max(left, pos[idx] + 1)
                pos[idx] = right
            else:
                # 非 ASCII 时退化处理：这里给出稳妥写法思路
                # 实战中更建议直接使用上一种 dict 解法
                raise ValueError("Non-ASCII character encountered; use dict solution instead.")
            ans = max(ans, right - left + 1)

        return ans
```

---

## 推荐怎么选
- 想讲清楚题目演进：按“暴力 -> 剪枝 -> 滑窗”讲。
- 面试正式作答：优先写**解法4（滑动窗口 + 最后出现位置）**。
- 如果面试官追问常数优化，再补**解法5**。

---

## 同类题目练习

1. **76. Minimum Window Substring**  
   为什么推荐练：同样是滑动窗口，但从“窗口内不能重复”升级为“窗口要满足覆盖条件”，能练收缩时机和计数维护。

2. **438. Find All Anagrams in a String**  
   为什么推荐练：固定长度滑窗代表题，适合对比“本题是可变窗口、该题是定长窗口”的差异。

3. **567. Permutation in String**  
   为什么推荐练：和 438 很像，但更强调“是否存在”而不是“找所有位置”，适合巩固定长窗口模板。

4. **159. Longest Substring with At Most Two Distinct Characters**  
   为什么推荐练：把“不能重复”改成“最多两种字符”，能练会“窗口约束变化，但滑窗骨架不变”。

5. **340. Longest Substring with At Most K Distinct Characters**  
   为什么推荐练：159 的泛化版，能真正形成“可变窗口 + 计数器”的统一套路。

---

## 复习 / 自测清单

把自己当成在做测试，不要只背模板，至少过一遍这些检查点：

- [ ] 我能明确说出“子串”和“子序列”的区别。
- [ ] 我知道为什么暴力法是 `O(n^3)`，改良后为什么能到 `O(n^2)`。
- [ ] 我能解释滑动窗口为什么总体是 `O(n)`，而不是 `O(n^2)`。
- [ ] 我能说清楚集合滑窗里为什么要用 `while` 收缩，不能只用 `if`。
- [ ] 我知道字典跳跃写法里为什么必须 `left = max(left, last[ch] + 1)`。
- [ ] 我能手推样例：`"abcabcbb" -> 3`。
- [ ] 我能手推样例：`"bbbbb" -> 1`。
- [ ] 我能手推样例：`"pwwkew" -> 3`，并确认答案对应的是子串 `"wke"` 而不是不连续字符组合。
- [ ] 我能手推易错样例：`"abba" -> 2`，并验证 `left` 不会回退。
- [ ] 我能处理空串 `"" -> 0`。
- [ ] 如果输入包含中文或任意 Unicode，我知道应优先用 `dict` 版而不是 ASCII 数组版。

今天这题的关键，不是“背一个滑窗模板”，而是把这几个问题想透：
1. 窗口什么时候扩？
2. 窗口什么时候收？
3. 用什么结构表示“当前窗口是否合法”？
4. 左边界能不能一次跳跃，而不是一步步挪？

这四个点想清楚，字符串滑窗题会顺很多。