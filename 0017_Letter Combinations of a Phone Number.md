# 今日题目

LeetCode #17 Letter Combinations of a Phone Number

题意简述：给定一个仅包含数字 `2-9` 的字符串 `digits`，返回它能表示的所有字母组合。映射关系与手机九宫格一致，例如 `2 -> abc`，`3 -> def`。

---

# 解法 1：递归暴力拼接（每层直接生成新字符串）

## 思路要点

最直观的做法就是按位展开。

- 处理到第 `i` 位时，取出当前数字对应的所有字母。
- 对每个字母，都把它拼到当前路径后面。
- 递归进入下一位。
- 到达末尾时，把当前组合加入答案。

这是最基础的 DFS / 回溯写法，适合理解题目结构。

## 复杂度

- 时间复杂度：`O(3^m * 4^n * L)`
  - 其中 `m` 是映射为 3 个字母的数字个数，`n` 是映射为 4 个字母的数字个数。
  - `L = len(digits)`。
  - 额外的 `L` 主要来自字符串拼接与结果拷贝。
- 空间复杂度：`O(L)`（递归栈，不含结果集）

## 关键边界 / 易错点

- `digits == ""` 时要返回 `[]`，不是 `[""]`。
- 题目通常只会给 `2-9`，如果代码要写得更稳，可以跳过非法字符或直接返回空。
- 频繁做 `path + ch` 会创建新字符串，虽然可读性高，但性能不是最好。

## Python 代码

```python
from typing import List

class Solution:
    def letterCombinations(self, digits: str) -> List[str]:
        if not digits:
            return []

        mp = {
            '2': 'abc', '3': 'def', '4': 'ghi', '5': 'jkl',
            '6': 'mno', '7': 'pqrs', '8': 'tuv', '9': 'wxyz'
        }
        ans = []

        def dfs(i: int, path: str) -> None:
            if i == len(digits):
                ans.append(path)
                return
            for ch in mp[digits[i]]:
                dfs(i + 1, path + ch)

        dfs(0, "")
        return ans
```

---

# 解法 2：回溯 + 可变路径数组（减少字符串重复创建）

## 思路要点

还是 DFS，但是把路径改成列表：

- `path.append(ch)` 进入下一层
- 回来时 `path.pop()` 撤销选择
- 到叶子节点时再 `''.join(path)`

这比每次都 `path + ch` 更贴近标准回溯模板，也更省中间对象。

## 复杂度

- 时间复杂度：`O(3^m * 4^n * L)`
- 空间复杂度：`O(L)`（递归栈 + 当前路径，不含结果集）

## 关键边界 / 易错点

- `append` 后一定要 `pop`，否则路径污染。
- 只有在到达叶子节点时才 `join`，不要每层都 `join`。
- 如果 digits 很长，结果数量会指数级增长，这是题目本质，不是代码问题。

## Python 代码

```python
from typing import List

class Solution:
    def letterCombinations(self, digits: str) -> List[str]:
        if not digits:
            return []

        mp = {
            '2': 'abc', '3': 'def', '4': 'ghi', '5': 'jkl',
            '6': 'mno', '7': 'pqrs', '8': 'tuv', '9': 'wxyz'
        }
        ans = []
        path = []

        def backtrack(i: int) -> None:
            if i == len(digits):
                ans.append(''.join(path))
                return

            for ch in mp[digits[i]]:
                path.append(ch)
                backtrack(i + 1)
                path.pop()

        backtrack(0)
        return ans
```

---

# 解法 3：迭代笛卡尔积（逐层扩展答案）

## 思路要点

不走递归，直接迭代构造：

- 初始结果设为 `[""]`
- 读到一个数字，就把当前所有前缀与该数字的所有字母做笛卡尔积
- 新的一轮结果替换旧结果
- 全部处理完，得到最终答案

这本质上是“层序展开”，和 BFS 的层扩展很像。

## 复杂度

- 时间复杂度：`O(3^m * 4^n * L)`
- 空间复杂度：`O(3^m * 4^n * L)`
  - 因为中间层和最终答案都要存下来

## 关键边界 / 易错点

- 空输入仍然返回 `[]`。
- 初始必须是 `[""]`，这样第一层才能正常扩展。
- 不要一边遍历 `res` 一边原地追加到 `res`，要生成新列表。

## Python 代码

```python
from typing import List

class Solution:
    def letterCombinations(self, digits: str) -> List[str]:
        if not digits:
            return []

        mp = {
            '2': 'abc', '3': 'def', '4': 'ghi', '5': 'jkl',
            '6': 'mno', '7': 'pqrs', '8': 'tuv', '9': 'wxyz'
        }

        res = [""]
        for d in digits:
            next_res = []
            for prefix in res:
                for ch in mp[d]:
                    next_res.append(prefix + ch)
            res = next_res

        return res
```

---

# 解法 4：队列式 BFS（按层扩展组合）

## 思路要点

把问题显式写成 BFS：

- 队列中保存当前层已生成的字符串
- 每处理一个数字，就把当前层所有字符串依次取出
- 对每个字符串追加当前数字映射的所有字母，再放回队列
- 处理完最后一层后，队列里就是答案

和解法 3 的区别不在复杂度，而在表达方式：
- 解法 3 更像“列表推导式扩展”
- 解法 4 更像“显式分层搜索”

## 复杂度

- 时间复杂度：`O(3^m * 4^n * L)`
- 空间复杂度：`O(3^m * 4^n * L)`

## 关键边界 / 易错点

- 每一层扩展前要固定当前队列长度，否则会把新入队的节点也在本层处理掉。
- 如果 digits 为空，直接返回 `[]`。
- BFS 不会比 DFS 更优，只是另一种稳定写法。

## Python 代码

```python
from collections import deque
from typing import List

class Solution:
    def letterCombinations(self, digits: str) -> List[str]:
        if not digits:
            return []

        mp = {
            '2': 'abc', '3': 'def', '4': 'ghi', '5': 'jkl',
            '6': 'mno', '7': 'pqrs', '8': 'tuv', '9': 'wxyz'
        }

        q = deque([""])
        for d in digits:
            size = len(q)
            for _ in range(size):
                prefix = q.popleft()
                for ch in mp[d]:
                    q.append(prefix + ch)

        return list(q)
```

---

# 解法 5：回溯最优写法（预映射 + 原地填充字符数组）

## 思路要点

这题无法突破指数级输出下界，因为你就是要把所有结果列出来。

所以“最优”通常指：
- 代码清晰
- 常数开销小
- 回溯结构标准
- 尽量避免无意义中间对象

做法：
- 先把每一位对应的字母串预取出来，减少递归里重复字典查找
- 用固定长度字符数组 `path` 原地写入
- 到叶子节点时再一次性 `join`

这是工程上最推荐的版本。

## 复杂度

- 时间复杂度：`O(3^m * 4^n * L)`
- 空间复杂度：`O(L)`（不含结果集）

## 关键边界 / 易错点

- 输出规模就是指数级，别试图“优化”成线性，那不可能。
- `path[i] = ch` 是覆盖写，不需要 `append/pop`。
- 若输入含非法字符，生产代码可加校验；LeetCode 环境一般默认合法。

## Python 代码

```python
from typing import List

class Solution:
    def letterCombinations(self, digits: str) -> List[str]:
        if not digits:
            return []

        mp = {
            '2': 'abc', '3': 'def', '4': 'ghi', '5': 'jkl',
            '6': 'mno', '7': 'pqrs', '8': 'tuv', '9': 'wxyz'
        }

        groups = [mp[d] for d in digits]
        n = len(groups)
        path = [''] * n
        ans = []

        def dfs(i: int) -> None:
            if i == n:
                ans.append(''.join(path))
                return
            for ch in groups[i]:
                path[i] = ch
                dfs(i + 1)

        dfs(0)
        return ans
```

---

# 同类题目练习

因为这题本质是**回溯 / DFS / 组合枚举 / 字符串状态展开**，建议顺手练这些：

1. **LeetCode 22 / Generate Parentheses**  
   为什么推荐练：同样是“逐位构造合法字符串”，但多了合法性剪枝，比本题更进一步。

2. **LeetCode 39 / Combination Sum**  
   为什么推荐练：从“枚举所有组合”过渡到“有约束的组合搜索”，回溯模板很典型。

3. **LeetCode 46 / Permutations**  
   为什么推荐练：训练“路径 + 已使用元素”这一类回溯状态设计。

4. **LeetCode 78 / Subsets**  
   为什么推荐练：练最基础的组合枚举框架，理解“选 / 不选”分支。

5. **LeetCode 79 / Word Search**  
   为什么推荐练：从一维组合扩展到二维网格 DFS，回溯中的 visited 管理很关键。

6. **LeetCode 131 / Palindrome Partitioning**  
   为什么推荐练：训练“切分型回溯”，理解路径不是单字符，而是若干片段。

---

# 复习 / 自测清单

可以像测功能一样过一遍：

- [ ] 输入为空字符串 `""`，是否返回 `[]`
- [ ] 输入只有一位，如 `"2"`，是否返回 `['a', 'b', 'c']`
- [ ] 输入两位，如 `"23"`，结果数量是否为 `3 * 3 = 9`
- [ ] 输入包含 `7` 或 `9`，是否正确处理 4 个字母分支
- [ ] 是否出现漏组合、重组合
- [ ] DFS / 回溯写法里，路径恢复是否正确（有没有忘记 `pop`）
- [ ] BFS 写法里，是否按层处理，避免把下一层节点提前消费
- [ ] 是否理解这题的最优复杂度受“输出规模”限制，无法低于指数级
- [ ] 能否在不看题解的情况下，手写出 DFS 回溯模板
- [ ] 能否说清楚：这题为什么适合回溯，而不是动态规划
