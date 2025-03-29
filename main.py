import os
from database.db_handler import DatabaseHandler
from analyzer.c_analyzer import CCodeAnalyzer
from ml.bug_detector import BugDetector
from typing import List, Dict, Any

class BugDetectionSystem:
    def __init__(self):
        self.db = DatabaseHandler()
        self.analyzer = CCodeAnalyzer()
        self.detector = BugDetector()
        self._load_or_train_model()

    def _load_or_train_model(self):
        """Load existing model or train a new one"""
        try:
            self.detector.load_model()
        except:
            # Train on existing data if available
            code_samples = self.db.get_code_samples()
            if code_samples:
                self.detector.train(code_samples)
                self.detector.save_model()

    def analyze_file(self, file_path: str) -> List[Dict[str, Any]]:
        """Analyze a C file for bugs using both static analysis and ML"""
        # Read the file
        with open(file_path, 'r') as f:
            code_content = f.read()

        # Static analysis
        static_bugs = self.analyzer.analyze_file(file_path)

        # ML-based analysis
        ml_bugs = self.detector.predict(code_content)

        # Combine results
        all_bugs = static_bugs + ml_bugs

        # Store in database
        code_sample_id = self.db.add_code_sample(
            file_name=os.path.basename(file_path),
            code_content=code_content,
            has_bugs=len(all_bugs) > 0
        )

        # Store bugs and their fixes
        for bug in all_bugs:
            bug_id = self.db.add_bug(
                code_sample_id=code_sample_id,
                bug_type=bug['bug_type'],
                description=bug['description'],
                line_number=bug.get('line_number', 0),
                severity=bug.get('severity', 'medium')
            )

            # Generate and store fix if available
            fix = self.analyzer.suggest_fix(bug, code_content)
            if fix:
                self.db.add_fix(
                    bug_id=bug_id,
                    fixed_code=fix,
                    fix_description=f"Automated fix for {bug['bug_type']}"
                )

        return all_bugs

    def get_fixes_for_file(self, file_path: str) -> List[Dict[str, Any]]:
        """Get all fixes for a specific file"""
        with open(file_path, 'r') as f:
            code_content = f.read()

        bugs = self.analyzer.analyze_file(file_path)
        fixes = []
        
        for bug in bugs:
            fix = self.analyzer.suggest_fix(bug, code_content)
            if fix:
                fixes.append({
                    'bug_type': bug['bug_type'],
                    'line_number': bug['line_number'],
                    'fix': fix
                })

        return fixes

def main():
    # Example usage
    system = BugDetectionSystem()
    
    # Analyze a C file
    file_path = "example.c"  # Replace with actual file path
    if os.path.exists(file_path):
        bugs = system.analyze_file(file_path)
        print(f"Found {len(bugs)} potential bugs:")
        for bug in bugs:
            print(f"- {bug['description']}")
            
        fixes = system.get_fixes_for_file(file_path)
        print("\nSuggested fixes:")
        for fix in fixes:
            print(f"- For {fix['bug_type']} at line {fix['line_number']}:")
            print(f"  {fix['fix']}")
    else:
        print(f"File {file_path} not found")

if __name__ == "__main__":
    main() 