#include <stdio.h>
#include <stdlib.h>

struct Node {
    int data;
    struct Node* next;
};

// Function with potential null pointer dereference
void print_list(struct Node* head) {
    struct Node* current = head;
    while (current->next != NULL) {  // Potential null pointer dereference
        printf("%d ", current->data);
        current = current->next;
    }
}

// Function with memory leak
struct Node* create_node(int value) {
    struct Node* node = (struct Node*)malloc(sizeof(struct Node));
    node->data = value;
    node->next = NULL;
    return node;  // Memory leak: no free() call
}

// Function with uninitialized variable
int sum_array(int arr[], int size) {
    int sum;  // Uninitialized variable
    for(int i = 0; i < size; i++) {
        sum += arr[i];  // Using uninitialized sum
    }
    return sum;
}

// Function with infinite loop
void infinite_counter() {
    int count = 0;
    while(1) {  // Infinite loop
        count++;
        printf("%d\n", count);
    }
}

// Function with buffer overflow
void copy_string(char* dest, char* src) {
    int i = 0;
    while(src[i] != '\0') {  // Potential buffer overflow
        dest[i] = src[i];
        i++;
    }
    dest[i] = '\0';
}

int main() {
    // Create a linked list with memory leak
    struct Node* head = create_node(1);
    head->next = create_node(2);
    
    // Call function with potential null pointer
    print_list(head);
    
    // Use uninitialized array
    int arr[5] = {1, 2, 3, 4, 5};
    int result = sum_array(arr, 5);
    
    // Buffer overflow example
    char small_buffer[5];
    char* long_string = "This string is too long for the buffer";
    copy_string(small_buffer, long_string);
    
    return 0;
} 