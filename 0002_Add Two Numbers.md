# LeetCode #2 Add Two Numbers

今日题目：LeetCode #2 Add Two Numbers

题意概述：
给你两个非空链表，分别表示两个非负整数。数字按**逆序**存储，每个节点只存一位。请把两数相加，并以相同逆序链表形式返回结果。

下面按“从能做出来，到写得稳、写得优”的顺序给 5 个解法。

---

## 解法 1：转整数后相加，再转回链表（最直接）

### 思路要点
- 先遍历 `l1`、`l2`，把逆序链表还原成整数。
- 两数相加得到 `total`。
- 再把 `total` 拆位，重新构造结果链表。
- 这是最容易想到的办法，但依赖大整数，不是面试最推荐写法。

### 时间/空间复杂度
- 时间复杂度：`O(m + n + k)`，其中 `m/n` 是两个链表长度，`k` 是结果位数。
- 空间复杂度：`O(k)`，用于结果链表；若把大整数位数也算进实现成本，可理解为额外依赖整数存储。

### 关键边界 / 易错点
- 输入是**逆序链表**，还原整数时要乘以 `1, 10, 100...`。
- `0 + 0` 时仍应返回单节点 `0`。
- Python 大整数能扛住，但很多语言会溢出，所以这个写法通用性差。

### Python 代码
```python
# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def addTwoNumbers(self, l1: ListNode, l2: ListNode) -> ListNode:
        def to_int(node: ListNode) -> int:
            base = 1
            num = 0
            while node:
                num += node.val * base
                base *= 10
                node = node.next
            return num

        total = to_int(l1) + to_int(l2)

        if total == 0:
            return ListNode(0)

        dummy = ListNode()
        cur = dummy
        while total > 0:
            cur.next = ListNode(total % 10)
            cur = cur.next
            total //= 10
        return dummy.next
```

---

## 解法 2：转成数组后做逐位加法

### 思路要点
- 先把两个链表读成数组，例如 `[2,4,3]`。
- 因为原链表本来就是逆序，所以数组下标天然对应个位、十位、百位。
- 再像手算加法一样，从前往后逐位相加并处理进位。
- 相比解法 1，更贴近题目本质，也避免整数溢出问题。

### 时间/空间复杂度
- 时间复杂度：`O(m + n)`
- 空间复杂度：`O(m + n)`，需要额外存数组

### 关键边界 / 易错点
- 两个数组长度可能不同，越界时按 0 处理。
- 循环结束后如果 `carry != 0`，还要补一个新节点。
- 结果链表构造时不要漏掉尾节点链接。

### Python 代码
```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def addTwoNumbers(self, l1: ListNode, l2: ListNode) -> ListNode:
        a, b = [], []

        while l1:
            a.append(l1.val)
            l1 = l1.next

        while l2:
            b.append(l2.val)
            l2 = l2.next

        i = 0
        carry = 0
        dummy = ListNode()
        cur = dummy

        while i < len(a) or i < len(b) or carry:
            x = a[i] if i < len(a) else 0
            y = b[i] if i < len(b) else 0
            s = x + y + carry
            carry = s // 10
            cur.next = ListNode(s % 10)
            cur = cur.next
            i += 1

        return dummy.next
```

---

## 解法 3：递归按位相加

### 思路要点
- 递归函数参数传入两个当前节点和进位 `carry`。
- 每次处理当前位，生成一个节点，然后递归处理下一位。
- 写法简洁，但本质上仍是逐位模拟加法。

### 时间/空间复杂度
- 时间复杂度：`O(m + n)`
- 空间复杂度：`O(m + n)`，递归栈开销

### 关键边界 / 易错点
- 递归终止条件必须同时考虑：`l1`、`l2`、`carry`。
- 链表很长时，递归可能有栈深限制，不如迭代稳。
- 取节点值时，空节点按 0 处理。

### Python 代码
```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def addTwoNumbers(self, l1: ListNode, l2: ListNode) -> ListNode:
        def dfs(n1: ListNode, n2: ListNode, carry: int) -> ListNode:
            if not n1 and not n2 and carry == 0:
                return None

            x = n1.val if n1 else 0
            y = n2.val if n2 else 0
            s = x + y + carry

            node = ListNode(s % 10)
            node.next = dfs(n1.next if n1 else None,
                            n2.next if n2 else None,
                            s // 10)
            return node

        return dfs(l1, l2, 0)
```

---

## 解法 4：迭代逐位相加 + 虚拟头节点（标准写法）

### 思路要点
- 用两个指针同步遍历 `l1`、`l2`。
- 每轮取当前位之和，再加上 `carry`。
- 新建结果节点挂到尾部。
- 这是最经典、最通用、面试最稳的版本。

### 时间/空间复杂度
- 时间复杂度：`O(m + n)`
- 空间复杂度：`O(k)`，仅结果链表；若不算输出，一般认为额外空间 `O(1)`

### 关键边界 / 易错点
- 条件应写成 `while l1 or l2 or carry`，否则最后一个进位会漏。
- `l1` 或 `l2` 走到头后要按 0 继续算。
- `dummy` + `cur` 的组合能避免头节点判空分支。

### Python 代码
```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def addTwoNumbers(self, l1: ListNode, l2: ListNode) -> ListNode:
        dummy = ListNode()
        cur = dummy
        carry = 0

        while l1 or l2 or carry:
            x = l1.val if l1 else 0
            y = l2.val if l2 else 0
            s = x + y + carry

            carry = s // 10
            cur.next = ListNode(s % 10)
            cur = cur.next

            if l1:
                l1 = l1.next
            if l2:
                l2 = l2.next

        return dummy.next
```

---

## 解法 5：原地复用链表节点（进阶优化）

### 思路要点
- 如果题目/场景允许修改原链表，可以尽量复用 `l1` 的节点，减少新节点创建。
- 用 `l1` 作为主链表，把每一位计算结果直接写回原节点。
- 当 `l1` 提前结束但 `l2` 还有剩余时，把 `l2` 的剩余部分接过来继续算。
- 最后如果还有进位，再补一个尾节点。
- 这版更偏工程优化，不是最容易写对，但空间利用更激进。

### 时间/空间复杂度
- 时间复杂度：`O(m + n)`
- 空间复杂度：额外 `O(1)`（不算输出，且复用了原节点）

### 关键边界 / 易错点
- 这会**修改输入链表**，面试时最好先说明“是否允许原地修改”。
- 需要维护 `prev`，因为最后可能要挂新节点。
- 当 `l1` 为空但 `l2` 还有剩余时，不能断链。
- 若不允许修改输入，别用这版。

### Python 代码
```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def addTwoNumbers(self, l1: ListNode, l2: ListNode) -> ListNode:
        if not l1:
            return l2
        if not l2:
            return l1

        head = l1
        p1, p2 = l1, l2
        prev = None
        carry = 0

        while p1 or p2:
            if not p1:
                prev.next = p2
                p1 = p2
                p2 = None

            x = p1.val if p1 else 0
            y = p2.val if p2 else 0
            s = x + y + carry
            carry = s // 10
            p1.val = s % 10

            prev = p1
            p1 = p1.next
            if p2:
                p2 = p2.next

        if carry:
            prev.next = ListNode(carry)

        return head
```

---

## 同类题目练习

这题属于**链表加法 / 链表基础操作**，优先推荐下面几道：

1. **21. Merge Two Sorted Lists**  
   推荐理由：同样是双指针处理两个链表，适合练“合并、挂接、尾指针维护”。

2. **19. Remove Nth Node From End of List**  
   推荐理由：练链表删除和哑节点思维，顺手补齐链表边界处理能力。

3. **24. Swap Nodes in Pairs**  
   推荐理由：练链表局部重连。能不能写稳，基本看你指针操作是否真的清楚。

4. **206. Reverse Linked List**  
   推荐理由：链表题基本功。反转写不稳，后面大多数链表题都容易翻车。

5. **445. Add Two Numbers II**  
   推荐理由：这是本题的进阶版。区别在于数字按**正序**存储，通常要借助栈或反转链表处理。

---

## 复习 / 自测清单

按测试用例思维过一遍，别只看懂题解：

- [ ] 能否自己复述题意：为什么链表是逆序，结果为什么也要逆序？
- [ ] `l1 = [2,4,3]`, `l2 = [5,6,4]`，是否能手推得到 `[7,0,8]`？
- [ ] `l1 = [0]`, `l2 = [0]`，是否返回 `[0]` 而不是空链表？
- [ ] 两链表长度不同，如 `[9,9,9,9,9,9,9] + [9,9,9,9]`，是否还能正确处理？
- [ ] 最后一位产生进位时，是否会补新节点？例如 `[5] + [5] -> [0,1]`
- [ ] 是否清楚 `while l1 or l2 or carry` 这三个条件为什么缺一不可？
- [ ] 若让你不用转整数，是否能 3 分钟内默写出“迭代 + dummy + carry”标准解？
- [ ] 若面试官追问“还能优化吗”，你能否说明“可复用原节点，但会修改输入链表”的 trade-off？
- [ ] 若把题目改成正序存储，你是否能联想到 445 题和“栈/反转链表”解法？

今天这题不难，难点不在算法，而在**链表指针和进位细节能不能写稳**。真正容易丢分的，不是不会做，而是最后一个 `carry`、空指针判断、尾节点连接写漏。