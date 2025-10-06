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


## Running and Testing

### Task 1: even.c
Run Example:
```bash
./even 5


Output:

0
2
4
6
8

(5 seconds between each number)

Signal Test:
bash
ps aux | grep even # Find the process PID
kill -HUP <pid> # Output "Ouch!"
kill -INT <pid> # Output "Yeah!"


### Task 2: minishell.c
Run Minishell:
`bash
./minishell


Example:
```bash
ls -l
pwd
cd ..
pwd
sleep 10 &


- `sleep 10 &` will run in the background, the shell will immediately return to the prompt, and when completed will display:

[1]+ Done sleep 10


## Notes
- `minishell` does not support full Bash functionality and is only for educational demonstrations.
- When `execvp` cannot find a command, an error message will be printed (for example, when entering `foobar`).
- Background processes will be automatically detected and cleaned up after completion.
