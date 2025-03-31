"""
Review Logic Module for Automated Code Review
"""
import os
import re
import logging
from typing import List, Dict, Any, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CodeReviewer:
    """Main code reviewer class that handles the review process"""
    
    def __init__(self, template_dir: str = "review_templates"):
        """
        Initialize the code reviewer with templates
        
        Args:
            template_dir: Directory containing review templates
        """
        self.template_dir = template_dir
        self.templates = self._load_templates()
        
    def _load_templates(self) -> Dict[str, str]:
        """
        Load all review templates from the template directory
        
        Returns:
            Dictionary mapping template names to their content
        """
        templates = {}
        try:
            for filename in os.listdir(self.template_dir):
                if filename.endswith(".md"):
                    template_name = filename.split(".")[0]
                    with open(os.path.join(self.template_dir, filename), 'r') as file:
                        templates[template_name] = file.read()
            return templates
        except Exception as e:
            logger.error(f"Error loading templates: {str(e)}")
            return {}
    
    def review_code(self, file_path: str, template_type: str = "general") -> Dict[str, Any]:
        """
        Review code based on the specified template
        
        Args:
            file_path: Path to the file to review
            template_type: Type of review template to use
            
        Returns:
            Dictionary containing review results
        """
        if template_type not in self.templates:
            logger.error(f"Template {template_type} not found")
            return {"error": f"Template {template_type} not found"}
            
        try:
            with open(file_path, 'r') as file:
                code = file.read()
                
            # Perform review based on template type
            if template_type == "security":
                return self._security_review(code)
            elif template_type == "performance":
                return self._performance_review(code)
            else:
                return self._general_review(code)
                
        except Exception as e:
            logger.error(f"Error reviewing {file_path}: {str(e)}")
            return {"error": str(e)}
    
    def _general_review(self, code: str) -> Dict[str, Any]:
        """Perform general code review"""
        issues = []
        
        # Check for code duplication
        if self._has_code_duplication(code):
            issues.append({
                "type": "code_quality",
                "issue": "Potential code duplication detected",
                "severity": "medium"
            })
            
        # Check for proper commenting
        if not self._has_proper_comments(code):
            issues.append({
                "type": "documentation",
                "issue": "Insufficient code comments",
                "severity": "low"
            })
            
        # Check for commented-out code
        if self._has_commented_code(code):
            issues.append({
                "type": "code_quality",
                "issue": "Commented-out code sections detected",
                "severity": "low"
            })
            
        return {
            "template": "general",
            "issues": issues,
            "issue_count": len(issues)
        }
    
    def _security_review(self, code: str) -> Dict[str, Any]:
        """Perform security-focused code review"""
        issues = []
        
        # Check for hardcoded credentials
        if self._has_hardcoded_credentials(code):
            issues.append({
                "type": "security",
                "issue": "Hardcoded credentials detected",
                "severity": "high"
            })
            
        # Check for SQL injection vulnerabilities
        if self._has_sql_injection_vulnerability(code):
            issues.append({
                "type": "security",
                "issue": "Potential SQL injection vulnerability",
                "severity": "high"
            })
            
        # Check for proper error handling
        if not self._has_proper_error_handling(code):
            issues.append({
                "type": "security",
                "issue": "Improper error handling",
                "severity": "medium"
            })
            
        return {
            "template": "security",
            "issues": issues,
            "issue_count": len(issues)
        }
    
    def _performance_review(self, code: str) -> Dict[str, Any]:
        """Perform performance-focused code review"""
        issues = []
        
        # Check for inefficient algorithms
        if self._has_inefficient_algorithms(code):
            issues.append({
                "type": "performance",
                "issue": "Inefficient algorithm detected",
                "severity": "medium"
            })
            
        # Check for resource leaks
        if self._has_resource_leaks(code):
            issues.append({
                "type": "performance",
                "issue": "Potential resource leak detected",
                "severity": "high"
            })
            
        # Check for unnecessary operations
        if self._has_unnecessary_operations(code):
            issues.append({
                "type": "performance",
                "issue": "Unnecessary operations detected",
                "severity": "low"
            })
            
        return {
            "template": "performance",
            "issues": issues,
            "issue_count": len(issues)
        }
    
    # Helper methods for code analysis
    def _has_code_duplication(self, code: str) -> bool:
        """Simplified check for code duplication"""
        # This is a simplified implementation
        return bool(re.search(r'(def\s+\w+[\s\S]{10,}?)\1', code))
    
    def _has_proper_comments(self, code: str) -> bool:
        """Check if code has proper comments"""
        # Count comment lines vs code lines
        code_lines = code.split('\n')
        comment_lines = [line for line in code_lines if line.strip().startswith('#') or line.strip().startswith('"""')]
        return len(comment_lines) >= len(code_lines) * 0.1  # At least 10% comments
    
    def _has_commented_code(self, code: str) -> bool:
        """Check for commented-out code sections"""
        return bool(re.search(r'#\s*(def|class|if|for|while|return)', code))
    
    def _has_hardcoded_credentials(self, code: str) -> bool:
        """Check for hardcoded credentials"""
        credential_patterns = [
            r'password\s*=\s*[\'"]',
            r'api_key\s*=\s*[\'"]',
            r'secret\s*=\s*[\'"]',
            r'token\s*=\s*[\'"]'
        ]
        for pattern in credential_patterns:
            if re.search(pattern, code, re.IGNORECASE):
                return True
        return False
    
    def _has_sql_injection_vulnerability(self, code: str) -> bool:
        """Check for potential SQL injection vulnerabilities"""
        return bool(re.search(r'execute\s*\(\s*[f]?[\'"][^\']*{\s*\w+\s*}', code))
    
    def _has_proper_error_handling(self, code: str) -> bool:
        """Check for proper error handling"""
        # Check for except blocks that are too broad
        return not bool(re.search(r'except\s*:', code))
    
    def _has_inefficient_algorithms(self, code: str) -> bool:
        """Check for inefficient algorithms"""
        # Look for nested loops as a simple indicator
        return bool(re.search(r'for\s+\w+\s+in\s+.+:\s*\n\s+for\s+\w+\s+in', code))
    
    def _has_resource_leaks(self, code: str) -> bool:
        """Check for potential resource leaks"""
        # Look for file or connection operations without proper closing
        return bool(re.search(r'open\s*\(', code)) and not bool(re.search(r'with\s+open', code))
    
    def _has_unnecessary_operations(self, code: str) -> bool:
        """Check for unnecessary operations"""
        # Look for multiple list comprehensions in sequence
        return bool(re.search(r'\[\s*\w+\s+for\s+\w+\s+in\s+.+\].*\n.*\[\s*\w+\s+for\s+\w+\s+in', code))

def generate_review_report(review_results: Dict[str, Any], output_format: str = "markdown") -> str:
    """
    Generate a human-readable review report from review results
    
    Args:
        review_results: Results from a code review
        output_format: Format for the output report
        
    Returns:
        Formatted review report
    """
    if "error" in review_results:
        return f"Error generating review: {review_results['error']}"
    
    issues = review_results.get("issues", [])
    
    if output_format == "markdown":
        report = f"# Code Review Report\n\n"
        report += f"## Template: {review_results.get('template', 'unknown')}\n\n"
        report += f"Found {len(issues)} issue(s).\n\n"
        
        if issues:
            report += "## Issues\n\n"
            for i, issue in enumerate(issues, 1):
                severity = issue.get("severity", "unknown").upper()
                report += f"### {i}. {issue.get('issue')}\n"
                report += f"- **Type**: {issue.get('type')}\n"
                report += f"- **Severity**: {severity}\n\n"
        
        return report
    else:
        # Default to simple text format
        report = [f"Code Review Report - Template: {review_results.get('template', 'unknown')}"]
        report.append(f"Found {len(issues)} issue(s).")
        
        if issues:
            report.append("\nIssues:")
            for i, issue in enumerate(issues, 1):
                severity = issue.get("severity", "unknown").upper()
                report.append(f"{i}. {issue.get('issue')} ({issue.get('type')}, {severity})")
        
        return "\n".join(report)

if __name__ == "__main__":
    # Example usage
    reviewer = CodeReviewer()
    results = reviewer.review_code("example_code.py")
    print(generate_review_report(results))