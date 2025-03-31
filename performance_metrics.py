"""
Performance Metrics Module for Code Review Assistant
Provides tools for analyzing and measuring code performance
"""
import os
import re
import ast
import time
import logging
import functools
import statistics
from typing import Dict, List, Any, Optional, Tuple, Callable

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ComplexityAnalyzer:
    """Analyzes code complexity metrics"""
    
    def __init__(self):
        self.reset_metrics()
        
    def reset_metrics(self):
        """Reset all collected metrics"""
        self.cyclomatic_complexity = {}
        self.cognitive_complexity = {}
        self.method_lengths = {}
        self.class_sizes = {}
        self.inheritance_depth = {}
    
    def analyze_file(self, file_path: str) -> Dict[str, Any]:
        """
        Analyze a file and return its complexity metrics
        
        Args:
            file_path: Path to the Python file to analyze
            
        Returns:
            Dictionary containing complexity metrics
        """
        try:
            with open(file_path, 'r') as file:
                code = file.read()
            
            return self.analyze_code(code, file_path)
            
        except Exception as e:
            logger.error(f"Error analyzing file {file_path}: {str(e)}")
            return {"error": str(e)}
    
    def analyze_code(self, code: str, file_name: str = "unknown") -> Dict[str, Any]:
        """
        Analyze code string and return its complexity metrics
        
        Args:
            code: Python code as string
            file_name: Name to identify the code source
            
        Returns:
            Dictionary containing complexity metrics
        """
        self.reset_metrics()
        
        try:
            tree = ast.parse(code)
            
            # Calculate metrics from AST
            self._analyze_cyclomatic_complexity(tree, file_name)
            self._analyze_cognitive_complexity(tree, file_name)
            self._analyze_method_lengths(code)
            self._analyze_class_sizes(code)
            self._analyze_inheritance_depth(tree, file_name)
            
            # Aggregate results
            return {
                "file_name": file_name,
                "cyclomatic_complexity": self.cyclomatic_complexity,
                "cognitive_complexity": self.cognitive_complexity,
                "method_lengths": self.method_lengths,
                "class_sizes": self.class_sizes,
                "inheritance_depth": self.inheritance_depth,
                "summary": {
                    "avg_cyclomatic_complexity": self._average_metric(self.cyclomatic_complexity),
                    "max_cyclomatic_complexity": self._max_metric(self.cyclomatic_complexity),
                    "avg_cognitive_complexity": self._average_metric(self.cognitive_complexity),
                    "max_cognitive_complexity": self._max_metric(self.cognitive_complexity),
                    "avg_method_length": self._average_metric(self.method_lengths),
                    "max_method_length": self._max_metric(self.method_lengths),
                    "avg_class_size": self._average_metric(self.class_sizes),
                    "max_class_size": self._max_metric(self.class_sizes),
                    "max_inheritance_depth": self._max_metric(self.inheritance_depth)
                },
                "issues": self._identify_complexity_issues()
            }
            
        except SyntaxError as e:
            logger.error(f"Syntax error in code: {str(e)}")
            return {"error": f"Syntax error: {str(e)}"}
        except Exception as e:
            logger.error(f"Error analyzing code: {str(e)}")
            return {"error": str(e)}
    
    def _analyze_cyclomatic_complexity(self, tree: ast.AST, file_name: str) -> None:
        """Calculate cyclomatic complexity for each function/method"""
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                complexity = 1  # Base complexity
                
                # Count branches that increase complexity
                for subnode in ast.walk(node):
                    if isinstance(subnode, (ast.If, ast.While, ast.For, ast.AsyncFor)):
                        complexity += 1
                    elif isinstance(subnode, ast.BoolOp) and isinstance(subnode.op, ast.And):
                        complexity += len(subnode.values) - 1
                    elif isinstance(subnode, ast.BoolOp) and isinstance(subnode.op, ast.Or):
                        complexity += len(subnode.values) - 1
                    elif isinstance(subnode, ast.comprehension):
                        if subnode.ifs:
                            complexity += len(subnode.ifs)
                
                name = f"{file_name}::{node.name}"
                self.cyclomatic_complexity[name] = complexity
    
    def _analyze_cognitive_complexity(self, tree: ast.AST, file_name: str) -> None:
        """Calculate cognitive complexity for each function/method"""
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                complexity = 0
                nesting_level = 0
                
                # Count structures that increase cognitive complexity
                for subnode in ast.walk(node):
                    # Increment for control flow structures
                    if isinstance(subnode, (ast.If, ast.While, ast.For, ast.AsyncFor)):
                        complexity += 1 + nesting_level
                        nesting_level += 1
                    # For boolean operations
                    elif isinstance(subnode, ast.BoolOp):
                        complexity += 1
                
                name = f"{file_name}::{node.name}"
                self.cognitive_complexity[name] = complexity
    
    def _analyze_method_lengths(self, code: str) -> None:
        """Calculate method lengths in lines of code"""
        lines = code.split('\n')
        
        # Use regex to find function definitions and their spans
        function_pattern = r'def\s+(\w+)\s*\('
        function_matches = list(re.finditer(function_pattern, code))
        
        for i, match in enumerate(function_matches):
            func_name = match.group(1)
            start_idx = code[:match.start()].count('\n')
            
            # Determine end of function (next def or end of file)
            if i < len(function_matches) - 1:
                end_idx = code[:function_matches[i+1].start()].count('\n')
            else:
                end_idx = len(lines)
            
            length = end_idx - start_idx
            self.method_lengths[func_name] = length
    
    def _analyze_class_sizes(self, code: str) -> None:
        """Calculate class sizes in lines of code"""
        lines = code.split('\n')
        
        # Use regex to find class definitions and their spans
        class_pattern = r'class\s+(\w+)'
        class_matches = list(re.finditer(class_pattern, code))
        
        for i, match in enumerate(class_matches):
            class_name = match.group(1)
            start_idx = code[:match.start()].count('\n')
            
            # Determine end of class (next class or end of file)
            if i < len(class_matches) - 1:
                end_idx = code[:class_matches[i+1].start()].count('\n')
            else:
                end_idx = len(lines)
            
            size = end_idx - start_idx
            self.class_sizes[class_name] = size
    
    def _analyze_inheritance_depth(self, tree: ast.AST, file_name: str) -> None:
        """Calculate inheritance depth for each class"""
        class_bases = {}
        
        # First pass: collect all classes and their immediate bases
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                class_bases[node.name] = [base.id if isinstance(base, ast.Name) else "unknown" 
                                          for base in node.bases 
                                          if isinstance(base, ast.Name)]
        
        # Second pass: calculate inheritance depth
        for class_name, bases in class_bases.items():
            depth = self._calculate_inheritance_depth(class_name, class_bases, set())
            self.inheritance_depth[class_name] = depth
    
    def _calculate_inheritance_depth(self, class_name: str, class_bases: Dict[str, List[str]], visited: set) -> int:
        """Recursively calculate the inheritance depth of a class"""
        if class_name in visited:
            return 0  # Circular inheritance, stop recursion
        
        visited.add(class_name)
        
        if class_name not in class_bases or not class_bases[class_name]:
            return 1  # Base class
        
        max_parent_depth = 0
        for parent in class_bases[class_name]:
            if parent in class_bases:
                parent_depth = self._calculate_inheritance_depth(parent, class_bases, visited.copy())
                max_parent_depth = max(max_parent_depth, parent_depth)
        
        return max_parent_depth + 1
    
    def _average_metric(self, metric_dict: Dict[str, int]) -> float:
        """Calculate average of a metric"""
        if not metric_dict:
            return 0.0
        return statistics.mean(metric_dict.values())
    
    def _max_metric(self, metric_dict: Dict[str, int]) -> int:
        """Find maximum value of a metric"""
        if not metric_dict:
            return 0
        return max(metric_dict.values())
    
    def _identify_complexity_issues(self) -> List[Dict[str, Any]]:
        """Identify issues based on complexity metrics"""
        issues = []
        
        # Check cyclomatic complexity
        for func, complexity in self.cyclomatic_complexity.items():
            if complexity > 10:
                issues.append({
                    "type": "complexity",
                    "issue": f"High cyclomatic complexity ({complexity}) in {func}",
                    "severity": "high" if complexity > 15 else "medium"
                })
        
        # Check cognitive complexity
        for func, complexity in self.cognitive_complexity.items():
            if complexity > 15:
                issues.append({
                    "type": "complexity",
                    "issue": f"High cognitive complexity ({complexity}) in {func}",
                    "severity": "high" if complexity > 20 else "medium"
                })
        
        # Check method length
        for method, length in self.method_lengths.items():
            if length > 100:
                issues.append({
                    "type": "size",
                    "issue": f"Long method ({length} lines) in {method}",
                    "severity": "high" if length > 150 else "medium"
                })
        
        # Check class size
        for cls, size in self.class_sizes.items():
            if size > 500:
                issues.append({
                    "type": "size",
                    "issue": f"Large class ({size} lines) in {cls}",
                    "severity": "high" if size > 750 else "medium"
                })
        
        # Check inheritance depth
        for cls, depth in self.inheritance_depth.items():
            if depth > 5:
                issues.append({
                    "type": "design",
                    "issue": f"Deep inheritance hierarchy ({depth} levels) for {cls}",
                    "severity": "high" if depth > 7 else "medium"
                })
        
        return issues


class PerformanceProfiler:
    """Tool for profiling code performance"""
    
    def __init__(self):
        self.execution_times = {}
        self.memory_usage = {}
    
    def profile_function(self, func: Callable) -> Callable:
        """
        Decorator to profile function execution time
        
        Args:
            func: Function to profile
            
        Returns:
            Decorated function with profiling
        """
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            
            execution_time = end_time - start_time
            func_name = func.__name__
            
            if func_name in self.execution_times:
                self.execution_times[func_name].append(execution_time)
            else:
                self.execution_times[func_name] = [execution_time]
            
            return result
        
        return wrapper
    
    def get_function_stats(self, func_name: str) -> Dict[str, Any]:
        """
        Get performance statistics for a profiled function
        
        Args:
            func_name: Name of the function
            
        Returns:
            Dictionary with performance statistics
        """
        if func_name not in self.execution_times:
            return {"error": f"No profile data for {func_name}"}
        
        times = self.execution_times[func_name]
        
        return {
            "function": func_name,
            "call_count": len(times),
            "avg_execution_time": statistics.mean(times) if times else 0,
            "min_execution_time": min(times) if times else 0,
            "max_execution_time": max(times) if times else 0,
            "total_execution_time": sum(times),
            "std_dev": statistics.stdev(times) if len(times) > 1 else 0
        }
    
    def get_all_stats(self) -> Dict[str, Any]:
        """
        Get performance statistics for all profiled functions
        
        Returns:
            Dictionary with performance statistics for all functions
        """
        stats = {}
        for func_name in self.execution_times:
            stats[func_name] = self.get_function_stats(func_name)
        
        return stats
    
    def clear_stats(self):
        """Clear all profiling data"""
        self.execution_times = {}
        self.memory_usage = {}


class RuntimePerformanceAnalyzer:
    """Analyzes runtime performance characteristics"""
    
    def __init__(self):
        self.complexity_analyzer = ComplexityAnalyzer()
        self.profiler = PerformanceProfiler()
    
    def analyze_code_file(self, file_path: str) -> Dict[str, Any]:
        """
        Perform comprehensive performance analysis on a code file
        
        Args:
            file_path: Path to the file to analyze
            
        Returns:
            Dictionary with performance analysis results
        """
        results = {}
        
        # Static analysis
        complexity_metrics = self.complexity_analyzer.analyze_file(file_path)
        results["static_analysis"] = complexity_metrics
        
        # Identify hotspots based on complexity
        results["potential_hotspots"] = self._identify_hotspots(complexity_metrics)
        
        # Algorithm complexity recommendations
        results["algorithm_recommendations"] = self._generate_algorithm_recommendations(complexity_metrics)
        
        return results
    
    def _identify_hotspots(self, complexity_metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Identify potential performance hotspots based on complexity metrics
        
        Args:
            complexity_metrics: Complexity analysis results
            
        Returns:
            List of potential hotspots with recommendations
        """
        hotspots = []
        
        # Check cyclomatic complexity as potential hotspots
        for func, complexity in complexity_metrics.get("cyclomatic_complexity", {}).items():
            if complexity > 10:
                hotspots.append({
                    "location": func,
                    "reason": f"High cyclomatic complexity ({complexity})",
                    "recommendation": "Consider breaking down this function into smaller, more focused functions"
                })
        
        # Check method length as potential hotspots
        for method, length in complexity_metrics.get("method_lengths", {}).items():
            if length > 100:
                hotspots.append({
                    "location": method,
                    "reason": f"Long method ({length} lines)",
                    "recommendation": "Long methods often contain multiple responsibilities; consider refactoring"
                })
        
        return hotspots
    
    def _generate_algorithm_recommendations(self, complexity_metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate algorithm improvement recommendations
        
        Args:
            complexity_metrics: Complexity analysis results
            
        Returns:
            List of algorithm recommendations
        """
        recommendations = []
        
        # Check for functions with both high complexity and high cognitive complexity
        cyclomatic = complexity_metrics.get("cyclomatic_complexity", {})
        cognitive = complexity_metrics.get("cognitive_complexity", {})
        
        for func in set(cyclomatic.keys()) & set(cognitive.keys()):
            if cyclomatic[func] > 10 and cognitive[func] > 15:
                recommendations.append({
                    "location": func,
                    "issue": "Complex algorithm structure",
                    "recommendation": "This function has high logical and cognitive complexity. Consider simplifying the algorithm or breaking it down into smaller parts."
                })
        
        return recommendations


# Function to generate performance report
def generate_performance_report(analysis_results: Dict[str, Any], output_format: str = "markdown") -> str:
    """
    Generate a human-readable performance report
    
    Args:
        analysis_results: Results from performance analysis
        output_format: Format for the output report
        
    Returns:
        Formatted performance report
    """
    if "error" in analysis_results:
        return f"Error generating performance report: {analysis_results['error']}"
    
    if output_format == "markdown":
        # Create markdown report
        report = "# Performance Analysis Report\n\n"
        
        # Static analysis section
        static_analysis = analysis_results.get("static_analysis", {})
        report += "## Complexity Metrics\n\n"
        
        # Summary statistics
        summary = static_analysis.get("summary", {})
        report += "### Summary\n\n"
        report += f"- Average Cyclomatic Complexity: {summary.get('avg_cyclomatic_complexity', 0):.2f}\n"
        report += f"- Maximum Cyclomatic Complexity: {summary.get('max_cyclomatic_complexity', 0)}\n"
        report += f"- Average Cognitive Complexity: {summary.get('avg_cognitive_complexity', 0):.2f}\n"
        report += f"- Maximum Cognitive Complexity: {summary.get('max_cognitive_complexity', 0)}\n"
        report += f"- Average Method Length: {summary.get('avg_method_length', 0):.2f} lines\n"
        report += f"- Maximum Method Length: {summary.get('max_method_length', 0)} lines\n"
        report += f"- Average Class Size: {summary.get('avg_class_size', 0):.2f} lines\n"
        report += f"- Maximum Class Size: {summary.get('max_class_size', 0)} lines\n"
        report += f"- Maximum Inheritance Depth: {summary.get('max_inheritance_depth', 0)} levels\n\n"
        
        # Issues identified
        issues = static_analysis.get("issues", [])
        if issues:
            report += "### Complexity Issues\n\n"
            for i, issue in enumerate(issues, 1):
                severity = issue.get("severity", "unknown").upper()
                report += f"{i}. **{issue.get('issue')}** ({severity})\n"
            report += "\n"
        
        # Hotspots section
        hotspots = analysis_results.get("potential_hotspots", [])
        if hotspots:
            report += "## Potential Performance Hotspots\n\n"
            for i, hotspot in enumerate(hotspots, 1):
                report += f"### {i}. {hotspot.get('location')}\n"
                report += f"- **Reason**: {hotspot.get('reason')}\n"
                report += f"- **Recommendation**: {hotspot.get('recommendation')}\n\n"
        
        # Algorithm recommendations
        recommendations = analysis_results.get("algorithm_recommendations", [])
        if recommendations:
            report += "## Algorithm Recommendations\n\n"
            for i, rec in enumerate(recommendations, 1):
                report += f"### {i}. {rec.get('location')}\n"
                report += f"- **Issue**: {rec.get('issue')}\n"
                report += f"- **Recommendation**: {rec.get('recommendation')}\n\n"
        
        return report
    else:
        # Simple text format
        lines = [f"Performance Analysis Report for {analysis_results.get('file_name', 'unknown')}"]
        
        # Summarize static analysis
        static_analysis = analysis_results.get("static_analysis", {})
        summary = static_analysis.get("summary", {})
        
        lines.append("\nComplexity Metrics:")
        lines.append(f"- Avg. Cyclomatic Complexity: {summary.get('avg_cyclomatic_complexity', 0):.2f}")
        lines.append(f"- Max. Cyclomatic Complexity: {summary.get('max_cyclomatic_complexity', 0)}")
        lines.append(f"- Avg. Method Length: {summary.get('avg_method_length', 0):.2f} lines")
        
        # List issues
        issues = static_analysis.get("issues", [])
        if issues:
            lines.append("\nIssues Found:")
            for issue in issues:
                severity = issue.get("severity", "unknown").upper()
                lines.append(f"- {issue.get('issue')} ({severity})")
        
        # List hotspots
        hotspots = analysis_results.get("potential_hotspots", [])
        if hotspots:
            lines.append("\nPotential Hotspots:")
            for hotspot in hotspots:
                lines.append(f"- {hotspot.get('location')}: {hotspot.get('reason')}")
        
        return "\n".join(lines)


if __name__ == "__main__":
    # Example usage
    analyzer = RuntimePerformanceAnalyzer()
    results = analyzer.analyze_code_file("review_logic.py")
    print(generate_performance_report(results))