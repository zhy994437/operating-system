# Unix Programming Assignment
# Unix Programming Assignment

## Project Overview
This project consists of two main tasks, designed to help you understand **C programming, Unix system calls, process management, signal handling**, and **basic shell implementation**.

### Task 1 - even.c (30%)
- A C program that receives the command line argument `n` and prints the first `n` even numbers.
- The program pauses for 5 seconds (`sleep(5)`) after each print to facilitate testing signal handling.
- Program signal handling:
- Receive `SIGHUP` → Print `"Ouch!"` and continue running.
- Receive `SIGINT` → Print `"Yeah!"` and continue running.

### Task 2 - minishell.c (70%)
- A simplified command line interpreter (shell) that supports basic Unix command execution.
- Feature improvements:
- Recognize and run commands preceded by `&` in the background, reporting completion.
- Correctly handle the `cd` builtin command.
- Print `perror` messages when system calls fail.
- Ensure child processes exit properly when `exec` calls fail.

---

## Compilation Method
In Linux/Unix, enter the source code directory and compile using `gcc`:

```bash
# Compile Task 1
gcc -o even even.c

# Compile Task 2
gcc -o minishell minishell.c
```

---

## Running and Testing

### Task 1: even.c
Run Example:
```bash
./even 5
```

Output:
```
0
2
4
6
8
```
(5 seconds between each number)

Signal Test:
```bash
ps aux | grep even # Find the process PID
kill -HUP <pid> # Output "Ouch!"
kill -INT <pid> # Output "Yeah!"
```

---

### Task 2: minishell.c
Run Minishell:
```bash
./minishell
```

Example:
```bash
ls -l
pwd
cd ..
pwd
sleep 10 &
```

- `sleep 10 &` will run in the background, the shell will immediately return to the prompt, and when completed will display:
```
[1]+ Done sleep 10
```

---

## Notes
- `minishell` does not support full Bash functionality and is only for educational demonstrations.
- When `execvp` cannot find a command, an error message will be printed (for example, when entering `foobar`).
- Background processes will be automatically detected and cleaned up after completion.



## 项目概述
本项目包含两个主要任务，旨在帮助理解 **C 语言编程、Unix 系统调用、进程管理、信号处理** 以及 **Shell 的基本实现**。

### 任务 1 - even.c (30%)
- 一个 C 程序，从命令行接收参数 `n`，并打印前 `n` 个偶数。
- 每次打印后程序会暂停 5 秒 (`sleep(5)`)，便于测试信号处理。
- 程序信号处理：
  - 收到 `SIGHUP` → 打印 `"Ouch!"` 并继续运行。
  - 收到 `SIGINT` → 打印 `"Yeah!"` 并继续运行。

### 任务 2 - minishell.c (70%)
- 一个简化版的命令行解释器（shell），支持基本的 Unix 命令执行。
- 功能改进：
  - 能够识别并在后台运行带 `&` 的命令，并在完成时报告。
  - 正确处理内建命令 `cd`。
  - 系统调用失败时输出 `perror` 信息。
  - 确保 `exec` 调用失败时子进程能正确退出。

---

## 编译方法
在 Linux / Unix 环境下，进入源代码目录，使用 `gcc` 编译：

```bash
# 编译任务1
gcc -o even even.c

# 编译任务2
gcc -o minishell minishell.c
```

---

## 运行与测试

### 任务 1: even.c
运行示例：
```bash
./even 5
```

输出：
```
0
2
4
6
8
```
（每个数字之间间隔 5 秒）

信号测试：
```bash
ps aux | grep even    # 找到进程 PID
kill -HUP <pid>       # 输出 "Ouch!"
kill -INT <pid>       # 输出 "Yeah!"
```

---

### 任务 2: minishell.c
运行 minishell：
```bash
./minishell
```

示例操作：
```bash
ls -l
pwd
cd ..
pwd
sleep 10 &
```

- `sleep 10 &` 将在后台运行，shell 会立即返回提示符，并在完成时显示：
  ```
  [1]+ Done            sleep 10
  ```

---

## 注意事项
- `minishell` 不支持完整的 Bash 功能，仅用于教学演示。
- 当 `execvp` 找不到命令时，会打印错误信息（例如输入 `foobar`）。
- 后台进程完成后会被自动检测并清理。
