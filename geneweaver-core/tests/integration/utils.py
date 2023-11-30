"""
Utilities for integration tests.
这个工具函数是用于集成测试中的一个辅助函数。它的作用是能够按照指定的频率多次调用一个函数，并收集这些调用的结果。

函数解释如下：

- `func`: 这是一个可调用对象（如函数），是我们希望多次调用的目标函数。
- `num_times`: 这是一个整数，表示我们希望调用目标函数的次数。
- `rate`: 这是一个整数，表示我们每秒钟希望调用函数的次数。例如，如果`rate`是2，那么每0.5秒调用一次函数。
- `iterate_args`: 这是一个可选的序列，它包含了传递给函数的参数。如果提供了这个参数，每次调用时将使用序列中的相应元素作为参数。

函数的工作流程是：

1. 它首先初始化一个空列表`results`，用来存储每次函数调用的结果。
2. 然后，它进入一个循环，循环次数由`num_times`指定。
3. 在每次迭代开始时，记录当前时间`start_time`。
4. 然后，它调用`func`函数，如果提供了`iterate_args`参数，则将这些参数逐一传递给`func`。
5. 每次函数调用的结果都会被添加到`results`列表中。
6. 为了控制调用频率，它会计算出自上次迭代开始以来所经过的时间，并使用`time.sleep`暂停一段时间，以确保调用频率不超过`rate`指定的值。
7. 最后，函数返回包含所有调用结果的`results`列表。

这个工具函数在进行压力测试或评估API性能时非常有用，它能够帮助我们理解在高频调用下系统的表现，以及可能出现的性能瓶颈或错误。
"""
import time
from typing import Callable, Optional, Sequence


def call_function(
    func: Callable, num_times: int, rate: int, iterate_args: Optional[Sequence]
):  # noqa: ANN002
    """Call 'func' 'num_times' times at 'rate' times per second."""
    results = []

    for i in range(num_times):
        start_time = time.time()
        results.append(func(iterate_args[i]) if iterate_args else func())
        time.sleep(max(1 / rate - (time.time() - start_time), 0))

    return results
