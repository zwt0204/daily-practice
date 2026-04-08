# 今日题目

LeetCode #19 Remove Nth Node From End of List

这题是典型的**链表双指针 / 快慢指针**题。核心不是“删节点”本身，而是怎么**稳定定位倒数第 n 个节点的前一个节点**。只要前驱节点找准，删除动作本身就是一次指针重连。

下面按“从直观到最优”的顺序给 5 个解法。严格说，工程里最推荐的是解法三或解法四；前两个更适合理解题意和训练链表感觉。

## 解法一：转数组后删除（最直观）

### 思路要点
- 先遍历链表，把每个节点引用放进数组。
- 链表长度记为 `m`，那么要删除的节点下标就是 `m - n`。
- 如果删除的是头节点，直接返回 `head.next`。
- 否则找到前一个节点 `nodes[m-n-1]`，执行跳过删除节点：`prev.next = prev.next.next`。

### 时间 / 空间复杂度
- 时间复杂度：`O(L)`
- 空间复杂度：`O(L)`

### 关键边界 / 易错点
- `n == 链表长度` 时，删除的是头结点。
- 数组里存的是**节点引用**，不是节点值；否则没法改链表指针。
- 单节点链表且 `n=1` 时，返回 `None`。

### Python 代码
```python
from typing import Optional

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        nodes = []
        cur = head
        while cur:
            nodes.append(cur)
            cur = cur.next

        m = len(nodes)
        idx = m - n

        if idx == 0:
            return head.next

        prev = nodes[idx - 1]
        prev.next = prev.next.next
        return head
```

## 解法二：先求长度，再二次遍历定位（经典两趟）

### 思路要点
- 第一趟遍历求出链表长度 `L`。
- 倒数第 `n` 个节点，等价于正数第 `L - n + 1` 个节点。
- 所以只要在第二趟走到它的前驱，也就是第 `L - n` 个节点。
- 用一个虚拟头节点 `dummy`，可以把“删头节点”和“删普通节点”统一处理。

### 时间 / 空间复杂度
- 时间复杂度：`O(L)`
- 空间复杂度：`O(1)`

### 关键边界 / 易错点
- 第二趟不是走到目标节点，而是走到**目标前驱**。
- `dummy` 很关键，不然删除头节点时要单独分支。
- for 循环次数容易 off-by-one，建议手工代一下 `L=5, n=2`。

### Python 代码
```python
from typing import Optional

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        dummy = ListNode(0, head)

        length = 0
        cur = head
        while cur:
            length += 1
            cur = cur.next

        prev = dummy
        for _ in range(length - n):
            prev = prev.next

        prev.next = prev.next.next
        return dummy.next
```

## 解法三：双指针单趟扫描（面试最优解）

### 思路要点
- 仍然使用 `dummy`。
- 让 `fast` 先走 `n+1` 步，`slow` 停在 `dummy`。
- 然后 `fast`、`slow` 一起走，直到 `fast` 走到空。
- 此时 `slow` 正好停在“待删除节点的前一个节点”。
- 直接 `slow.next = slow.next.next` 即可。

### 时间 / 空间复杂度
- 时间复杂度：`O(L)`
- 空间复杂度：`O(1)`

### 关键边界 / 易错点
- 为什么是 `n+1` 步而不是 `n` 步？因为我们要让 `slow` 落在**前驱节点**。
- `fast` 起点必须和 `slow` 一样从 `dummy` 出发，逻辑才统一。
- 删除头节点时，`slow` 最终会停在 `dummy`，依然能正确删除。

### Python 代码
```python
from typing import Optional

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        dummy = ListNode(0, head)
        fast = dummy
        slow = dummy

        for _ in range(n + 1):
            fast = fast.next

        while fast:
            fast = fast.next
            slow = slow.next

        slow.next = slow.next.next
        return dummy.next
```

## 解法四：递归回溯计数（从尾巴往前数）

### 思路要点
- 递归先一路走到尾部。
- 回溯时自然就是“从后往前”计数。
- 当回溯计数等于 `n` 时，说明当前节点就是倒数第 `n` 个节点；返回它的 `next`，相当于把它删掉。
- 用返回值接住新的子链表头，就能完成删除。

### 时间 / 空间复杂度
- 时间复杂度：`O(L)`
- 空间复杂度：`O(L)`（递归栈）

### 关键边界 / 易错点
- Python 递归层数有限，链表很长时有栈溢出风险。
- 回溯计数要写清楚，否则很容易把“当前节点删掉”和“当前节点下一个删掉”搞混。
- 这类写法思路漂亮，但工程稳定性不如迭代版。

### Python 代码
```python
from typing import Optional

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        self.k = 0

        def dfs(node: Optional[ListNode]) -> Optional[ListNode]:
            if not node:
                return None

            node.next = dfs(node.next)
            self.k += 1

            if self.k == n:
                return node.next
            return node

        return dfs(head)
```

## 解法五：栈保存前驱路径（介于数组法与双指针之间）

### 思路要点
- 用 `dummy` 作为统一入口。
- 遍历链表时，把所有节点（含 `dummy`）压入栈。
- 然后弹出 `n` 次，弹出的最后一个就是要删除的目标节点；再弹一次得到它的前驱。
- 最后执行 `prev.next = target.next`。

### 时间 / 空间复杂度
- 时间复杂度：`O(L)`
- 空间复杂度：`O(L)`

### 关键边界 / 易错点
- 栈里最好把 `dummy` 也压进去，不然删头节点不好统一。
- 弹栈顺序别写反：先拿到目标，再拿前驱。
- 与数组法本质类似，都是“显式保存路径”，但更贴近“从尾部往前找”的思路。

### Python 代码
```python
from typing import Optional

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        dummy = ListNode(0, head)
        stack = []

        cur = dummy
        while cur:
            stack.append(cur)
            cur = cur.next

        target = None
        for _ in range(n):
            target = stack.pop()

        prev = stack.pop()
        prev.next = target.next
        return dummy.next
```

## 同类题目练习

1. **21 / Merge Two Sorted Lists**  
   推荐理由：链表基础拼接题，练“指针重连”和 dummy 节点的使用。

2. **19 / Remove Nth Node From End of List**  
   推荐理由：原题复刷。重点看自己能不能不看答案写出双指针单趟版。

3. **24 / Swap Nodes in Pairs**  
   推荐理由：继续训练前驱节点控制。很多人不是不会交换，而是不会稳定维护 `prev / first / second / next_pair` 之间的关系。

4. **206 / Reverse Linked List**  
   推荐理由：链表指针修改的基本功，能帮助你把“断开 / 重连 / 保存 next”这件事练熟。

5. **445 / Add Two Numbers II**  
   推荐理由：同样是链表题，但从“倒序处理”切到“正序处理 + 栈/反转”，很适合对比不同辅助结构的取舍。

6. **2 / Add Two Numbers**  
   推荐理由：也是 Hot100 高频链表题，适合对比“逐位构造新链表”和“在原链表上做局部删除/修改”的不同套路。

## 复习 / 自测清单

把自己当成在写测试用例，至少覆盖这些点：

- [ ] 单节点链表，`n = 1`，结果是否为 `None`
- [ ] 删除头节点：如 `[1,2,3,4,5], n=5`
- [ ] 删除尾节点：如 `[1,2,3,4,5], n=1`
- [ ] 删除中间节点：如 `[1,2,3,4,5], n=2`
- [ ] 两节点链表删除第一个：`[1,2], n=2`
- [ ] 两节点链表删除第二个：`[1,2], n=1`
- [ ] 双指针方案里，能否解释清楚为什么 `fast` 要先走 `n+1` 步
- [ ] 能否手画一遍 `dummy -> 1 -> 2 -> 3 -> 4 -> 5` 的移动过程
- [ ] 写代码时是否统一用 `dummy`，避免头节点特殊分支
- [ ] 是否明确区分“目标节点”与“目标前驱节点”，避免 off-by-one

---

今天这题不难，但很适合练“链表操作的稳定性”。如果你双指针版本能在 2 分钟内默写出来，而且不出 off-by-one，这题才算真的过关。
