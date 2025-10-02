#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>

// Signal handler for SIGHUP
void handle_sighup(int sig) {
    printf("Ouch!\n");
}

// Signal handler for SIGINT
void handle_sigint(int sig) {
    printf("Yeah!\n");
}

int main(int argc, char* argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <number_of_even_numbers>\n", argv[0]);
        return 1;
    }

    int n = atoi(argv[1]);
    if (n <= 0) {
        fprintf(stderr, "Please enter a positive integer\n");
        return 1;
    }

    // Setting up signal handlers
    signal(SIGHUP, handle_sighup);
    signal(SIGINT, handle_sigint);

    // Printing the first "n" even numbers with a 5-second delay between each
    for (int i = 0; i < n; i++) {
        printf("%d\n", i * 2);
        fflush(stdout); // Ensure the output is printed before sleeping
        sleep(5);
    }

    return 0;
}

