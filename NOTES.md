# Notes on Algorithms

## Regular Expressions - Deterministic (DFAs) / Non-deterministic (NFAs) Finite Automata (Machines)

![](https://swtch.com/~rsc/regexp/grep1p.png)

*DFA (red and similar lines) vs NFA (blue and neighboring lines)*


Example of DFA ![](https://swtch.com/~rsc/regexp/fig11.png)


and NFA working diagram ![](https://swtch.com/~rsc/regexp/fig20.png) ![](https://swtch.com/~rsc/regexp/fig12.png)


and cached NFA ![](https://swtch.com/~rsc/regexp/fig21.png)


The engines that drive regular expression (as an interface / language) functionalities in popular languages nowadays have a surprising quirk that cost exponential time on specific inputs.

```python
import re

n = 23
pattern = 'a?' * n + 'a' * n
string = 'a' * n
re.match(pattern, string)
```

Try to change n to slightly larger numbers (30 or more) and your computer (or super-computer) might be brought down to it knees. It won't complete in a life-time or two.

Read [Russ's amazing article](https://swtch.com/~rsc/regexp/regexp1.html) to have a basic understanding of how regular expressions are implemented and why they won't work as efficiently as expected in some (rare) cases.

Basically NFA is better overall, but in some specific cases, especially for long string with specifically designed branching (starts with an asterisk), it is less efficient than backtracking / DFA methods. DFA is good for cases where backtracking is limited (again less than 23 **asterisks**) and unmatched strings (and hence they will fail fast). Whereas in NFA if branching is early and the path is long (long strings), the effects of branching is serious.

I suspect the cost of NFA would be O(n<sup>2</sup>) while DFA would be O(n<sup>g(k)</sup>) where `g(k)` is a parameter dependent on the number of asterisk operators. That explains the exponential growth of DFAs vs NFAs. It also explains why DFA still be able to achieve near-linear cost (k is small, `g(k)` is small accordingly) even for large n, and why NFAs would perform in quadratic order in large n.