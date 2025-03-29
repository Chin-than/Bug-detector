from pycparser import c_parser, c_ast
import re
from typing import List, Dict, Any
import os

class CCodeAnalyzer:
    def __init__(self):
        self.parser = c_parser.CParser()
        self.common_bugs = {
            'memory_leak': r'malloc\s*\([^;]*\)[^;]*;(?![^}]*free)',
            'buffer_overflow': r'(strcpy|strcat|gets|scanf)\s*\([^;]*\)',
            'null_pointer': r'(\w+)\s*->\s*\w+(?!\s*\w+\s*!=\s*NULL)',
            'uninitialized_var': r'int\s+(\w+)\s*;(?![^;]*=)',
            'infinite_loop': r'while\s*\(\s*1\s*\)|for\s*\(\s*;\s*;\s*\)'
        }

    def analyze_file(self, file_path: str) -> List[Dict[str, Any]]:
        """Analyze a C file for potential bugs"""
        with open(file_path, 'r') as f:
            code = f.read()
        
        bugs = []
        
        # Pattern-based analysis
        for bug_type, pattern in self.common_bugs.items():
            matches = re.finditer(pattern, code)
            for match in matches:
                line_number = code[:match.start()].count('\n') + 1
                bugs.append({
                    'bug_type': bug_type,
                    'line_number': line_number,
                    'description': f'Potential {bug_type} detected at line {line_number}',
                    'severity': self._determine_severity(bug_type)
                })

        # AST-based analysis
        try:
            ast = self.parser.parse(code)
            bugs.extend(self._analyze_ast(ast))
        except Exception as e:
            bugs.append({
                'bug_type': 'syntax_error',
                'line_number': 0,
                'description': f'Syntax error: {str(e)}',
                'severity': 'high'
            })

        return bugs

    def _analyze_ast(self, ast: c_ast.FileAST) -> List[Dict[str, Any]]:
        """Analyze the AST for potential bugs"""
        bugs = []
        
        class BugVisitor(c_ast.NodeVisitor):
            def visit_FuncDef(self, node):
                # Check for missing return statements
                if node.decl.type.type.type.names[0] != 'void':
                    has_return = False
                    if node.body.block_items:
                        for item in node.body.block_items:
                            if isinstance(item, c_ast.Return):
                                has_return = True
                                break
                    if not has_return:
                        bugs.append({
                            'bug_type': 'missing_return',
                            'line_number': node.coord.line,
                            'description': f'Function {node.decl.name} might not return a value',
                            'severity': 'medium'
                        })

        visitor = BugVisitor()
        visitor.visit(ast)
        return bugs

    def _determine_severity(self, bug_type: str) -> str:
        """Determine the severity of a bug type"""
        severity_map = {
            'memory_leak': 'high',
            'buffer_overflow': 'high',
            'null_pointer': 'high',
            'uninitialized_var': 'medium',
            'infinite_loop': 'medium',
            'missing_return': 'low',
            'syntax_error': 'high'
        }
        return severity_map.get(bug_type, 'medium')

    def suggest_fix(self, bug: Dict[str, Any], code: str) -> str:
        """Suggest a fix for a detected bug"""
        lines = code.split('\n')
        if bug['line_number'] <= 0 or bug['line_number'] > len(lines):
            return "Cannot generate fix: invalid line number"

        line = lines[bug['line_number'] - 1]
        
        if bug['bug_type'] == 'memory_leak':
            match = re.search(r'(\w+)\s*=\s*malloc', line)
            if match:
                var_name = match.group(1)
                return f"free({var_name});"
        
        elif bug['bug_type'] == 'buffer_overflow':
            if 'strcpy' in line:
                return line.replace('strcpy', 'strncpy') + f" // Use strncpy with size limit"
            elif 'gets' in line:
                return line.replace('gets', 'fgets') + f" // Use fgets with size limit"
        
        elif bug['bug_type'] == 'null_pointer':
            var_name = line.split('->')[0].strip()
            return f"if ({var_name} != NULL) {{\n    {line}\n}}"
        
        elif bug['bug_type'] == 'uninitialized_var':
            var_name = re.search(r'int\s+(\w+)', line).group(1)
            return line.rstrip(';') + f" = 0;  // Initialize variable"
        
        elif bug['bug_type'] == 'infinite_loop':
            if 'while(1)' in line or 'while (1)' in line:
                return line.replace('while (1)', 'while (condition)') + f" // Add proper exit condition"
        
        return "No automatic fix available" 