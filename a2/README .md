# Virtual Memory Page Replacement Simulator

## Introduction
This project implements a virtual memory management simulator (`memsim.c`) that evaluates the performance of different **page replacement algorithms** when processing memory access traces from real applications.

The simulator models a single-level page table with a fixed **page size of 4KB**. It supports the following replacement policies:

- **rand**: Random replacement  
- **fifo**: First-In-First-Out  
- **lru**: Least Recently Used  
- **clock**: Clock (Second-Chance) algorithm  

The simulator records the number of **page faults, disk reads, disk writes**, and calculates the **page fault rate**.

---

## Compilation
Use `gcc` to compile the simulator:

```bash
gcc -o memsim memsim.c
```

This will generate the executable `memsim`.

---

## Usage
The simulator requires **4 arguments**:

```
./memsim <trace_file> <num_frames> <replacement_policy> <mode>
```

Arguments:
1. **trace_file**: Memory access trace file (e.g., `gcc.trace`)  
2. **num_frames**: Number of page frames in simulated memory (positive integer)  
3. **replacement_policy**: `rand` / `fifo` / `lru` / `clock`  
4. **mode**: `quiet` or `debug`  
   - `quiet`: Only prints final summary statistics  
   - `debug`: Prints detailed information for each memory access (for testing and debugging)  

---

## Example
### Decompress the trace file
```bash
gunzip -d gcc.trace.gz
```

### Run the simulator
```bash
# Example: 64 frames, LRU replacement, quiet mode
./memsim gcc.trace 64 lru quiet
```

### Sample Output
```
total memory frames:  64
events in trace:      1000000
total disk reads:     53241
total disk writes:    18792
page fault rate:      0.0532
```

---

## Notes
- Provided memory traces (`*.trace.gz`) are compressed and must be decompressed before use.  
- The simulator does not perform real disk operations; instead, it counts simulated disk reads/writes.  
