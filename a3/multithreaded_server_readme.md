# Multi-Threaded Network Server for Pattern Analysis

## Project Overview

This project implements a high-performance multi-threaded network server designed to manage concurrent connections, process text data streams, and perform real-time pattern analysis. The server demonstrates advanced concepts in concurrent programming, socket handling, and thread synchronization.

### Key Features

- **Concurrent Connection Handling**: Accepts and manages multiple simultaneous client connections using threading
- **Shared Data Structure**: Implements a thread-safe linked list shared across all threads
- **Pattern Analysis**: Real-time frequency analysis of search patterns across incoming text data
- **Non-blocking I/O**: Efficient data reception and processing
- **Producer-Consumer Model**: Utilizes condition variables for synchronized data processing

## Architecture

The server consists of four main components:

1. **Main Server Thread**: Accepts incoming connections and spawns client handler threads
2. **Client Handler Threads**: Receives book data from clients and adds to shared linked list
3. **Analysis Threads**: Processes data from the shared list and counts pattern occurrences
4. **Output Thread**: Periodically displays book titles sorted by pattern frequency

## Prerequisites

- **Python**: Version 3.6 or higher
- **netcat (nc)**: For sending test data to the server
- **Text Files**: Sample books from [Project Gutenberg](https://www.gutenberg.org) in UTF-8 format

### Installing netcat

- **Linux/macOS**: Usually pre-installed
- **Windows**: Install via WSL or download ncat from [nmap.org](https://nmap.org/ncat/)

## Project Structure

```
.
├── assignment3.py          # Main server implementation
├── Makefile               # Build and test automation
├── README.md              # This file
├── book_01.txt           # Sample input (downloaded from Gutenberg)
├── book_02.txt           # Sample input
└── book_03.txt           # Sample input
```

## Installation & Setup

1. **Clone or download the project files**

2. **Download sample books** from Project Gutenberg:
   ```bash
   # Example downloads (Linux/macOS)
   wget https://www.gutenberg.org/files/11/11-0.txt -O book_01.txt
   wget https://www.gutenberg.org/files/1342/1342-0.txt -O book_02.txt
   wget https://www.gutenberg.org/files/84/84-0.txt -O book_03.txt
   ```

3. **Ensure the first line of each book contains the title** for proper identification

## Usage

### Starting the Server

```bash
python assignment3.py -l <PORT> -p "<PATTERN>"
```

**Parameters:**
- `-l, --port`: Port number to listen on (must be > 1024)
- `-p, --pattern`: Search pattern to analyze in the text

**Example:**
```bash
python assignment3.py -l 12345 -p "happy"
```

This starts the server on port 12345, searching for the pattern "happy" in incoming text.

### Sending Data to Server

Use netcat to send book files to the server:

```bash
nc localhost 12345 < book_01.txt
```

For testing with delays between lines:
```bash
nc localhost 12345 -i 0.01 < book_01.txt
```

The `-i` flag adds a delay (in seconds) between each line sent.

### Testing with Multiple Connections

Open multiple terminal windows and send different books simultaneously:

**Terminal 1:**
```bash
nc localhost 12345 < book_01.txt
```

**Terminal 2:**
```bash
nc localhost 12345 < book_02.txt
```

**Terminal 3:**
```bash
nc localhost 12345 < book_03.txt
```

## Using the Makefile

The project includes a Makefile for automated testing:

```bash
# Start the server
make run

# Send test data (in separate terminal)
make send_data

# Clean generated files
make clean
```

**Note**: Modify the `BOOKS` variable in the Makefile to match your book filenames.

## Expected Output

### Server Console Output

1. **Connection Messages**:
   ```
   Server is listening on localhost:12345
   Accepted connection from ('127.0.0.1', 54321)
   Client 1 sent book title: Alice's Adventures in Wonderland
   ```

2. **Book Saved Messages**:
   ```
   Book saved for client 1 to book_01.txt
   ```

3. **Frequency Analysis** (every 5 seconds):
   ```
   Book: Alice's Adventures in Wonderland, Pattern: happy, Frequency: 15
   Book: Pride and Prejudice, Pattern: happy, Frequency: 23
   Book: Frankenstein, Pattern: happy, Frequency: 8
   ```

### Output Files

The server generates output files for each connection:
- `book_01.txt` - First connection's complete book
- `book_02.txt` - Second connection's complete book
- `book_03.txt` - Third connection's complete book
- etc.

## Testing Recommendations

### Basic Testing
1. Start server with a simple pattern: `python assignment3.py -l 12345 -p "the"`
2. Send 2-3 books simultaneously
3. Verify output files are created correctly
4. Check frequency analysis output

### Stress Testing
1. Test with 10+ simultaneous connections
2. Use larger books (> 1MB)
3. Try different patterns (case-sensitive)
4. Monitor thread synchronization

### Test Cases
```bash
# Test 1: Single connection
nc localhost 12345 < book_01.txt

# Test 2: Multiple connections with delay
for i in {1..10}; do
    (sleep $((i-1)); nc localhost 12345 < book_0${i}.txt) &
done

# Test 3: Pattern variations
python assignment3.py -l 12345 -p "love"
python assignment3.py -l 12345 -p "death"
```

## Code Structure

### Main Components

- **`Listnode`**: Node structure for the linked list containing book line data
- **`LinkedList`**: Shared linked list accessible by all threads
- **`Bookfrequency`**: Structure to track pattern frequency per book
- **`handleClient()`**: Thread function to handle individual client connections
- **`analysisThread()`**: Consumer thread that processes data and counts patterns
- **`printFrequencies()`**: Outputs sorted frequency results every 5 seconds

### Synchronization Mechanisms

- **`listLock`**: Mutex for protecting shared linked list
- **`listNoFull`**: Condition variable for producer threads
- **`listNoEmpty`**: Condition variable for consumer threads
- **`frequencyLock`**: Mutex for protecting frequency data structure

## Known Issues & Improvements

1. **Variable Naming**: Some inconsistencies in variable capitalization (e.g., `LinkedList` vs `linkedlist`)
2. **Buffer Size**: Currently uses fixed 1024-byte buffer; consider dynamic