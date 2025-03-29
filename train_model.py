from ml.bug_detector import BugDetector
from database.db_handler import DatabaseHandler

# Sample training data
training_samples = [
    {
        'code_content': '''
            int* ptr = malloc(sizeof(int));
            *ptr = 42;
            return ptr;
        ''',
        'bugs': [{'bug_type': 'memory_leak', 'line_number': 1}]
    },
    {
        'code_content': '''
            struct Node* node;
            node->data = 42;
        ''',
        'bugs': [{'bug_type': 'null_pointer', 'line_number': 2}]
    },
    {
        'code_content': '''
            char buffer[5];
            strcpy(buffer, "This is too long");
        ''',
        'bugs': [{'bug_type': 'buffer_overflow', 'line_number': 2}]
    },
    {
        'code_content': '''
            int sum;
            for(int i = 0; i < 10; i++) {
                sum += i;
            }
        ''',
        'bugs': [{'bug_type': 'uninitialized_var', 'line_number': 1}]
    },
    {
        'code_content': '''
            while(1) {
                printf("Forever");
            }
        ''',
        'bugs': [{'bug_type': 'infinite_loop', 'line_number': 1}]
    },
    {
        'code_content': '''
            int get_value() {
                int x = 42;
            }
        ''',
        'bugs': [{'bug_type': 'missing_return', 'line_number': 1}]
    },
    # Add some non-buggy samples
    {
        'code_content': '''
            int* ptr = malloc(sizeof(int));
            *ptr = 42;
            free(ptr);
            return 0;
        ''',
        'bugs': []
    },
    {
        'code_content': '''
            int sum = 0;
            for(int i = 0; i < 10; i++) {
                sum += i;
            }
            return sum;
        ''',
        'bugs': []
    }
]

def main():
    # Initialize the detector and database
    detector = BugDetector()
    db = DatabaseHandler()
    
    # Store samples in database
    for sample in training_samples:
        code_sample_id = db.add_code_sample(
            file_name='training_sample.c',
            code_content=sample['code_content'],
            has_bugs=len(sample['bugs']) > 0
        )
        
        for bug in sample.get('bugs', []):
            db.add_bug(
                code_sample_id=code_sample_id,
                bug_type=bug['bug_type'],
                description=f"Training sample bug: {bug['bug_type']}",
                line_number=bug['line_number'],
                severity='medium'
            )
    
    # Train the model
    detector.train(training_samples)
    
    # Save the trained model
    detector.save_model()
    
    print("Model trained and saved successfully!")

if __name__ == "__main__":
    main() 