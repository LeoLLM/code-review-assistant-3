"""
Performance Visualization Module for Code Review Assistant
Provides visualization tools for performance metrics
"""
import os
import json
import logging
from typing import Dict, List, Any, Optional, Tuple

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    # Optional visualization dependencies
    import matplotlib.pyplot as plt
    import numpy as np
    HAS_VISUALIZATION = True
except ImportError:
    logger.warning("Matplotlib not installed. Visualization features disabled.")
    HAS_VISUALIZATION = False

class PerformanceVisualizer:
    """Generate visualizations for performance metrics"""
    
    def __init__(self, output_dir: str = "reports"):
        """
        Initialize the visualizer
        
        Args:
            output_dir: Directory to save visualization outputs
        """
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    
    def create_complexity_chart(self, metrics: Dict[str, Any], output_file: str = None) -> Optional[str]:
        """
        Create chart visualizing code complexity metrics
        
        Args:
            metrics: Complexity metrics from analysis
            output_file: Output file path (defaults to complexity_chart.png in output_dir)
            
        Returns:
            Path to the generated chart file or None if visualization failed
        """
        if not HAS_VISUALIZATION:
            logger.error("Cannot create visualization: matplotlib not installed")
            return None
        
        try:
            # Extract cyclomatic complexity data
            cyclomatic = metrics.get("cyclomatic_complexity", {})
            if not cyclomatic:
                logger.warning("No cyclomatic complexity data available")
                return None
            
            # Prepare data
            functions = list(cyclomatic.keys())
            if len(functions) > 15:
                # Truncate to top 15 most complex functions
                sorted_functions = sorted(functions, key=lambda f: cyclomatic[f], reverse=True)
                functions = sorted_functions[:15]
            
            complexity_values = [cyclomatic[f] for f in functions]
            
            # For better display, truncate function names if too long
            display_names = [f.split("::")[-1] if "::" in f else f for f in functions]
            display_names = [n[:25] + "..." if len(n) > 28 else n for n in display_names]
            
            # Create figure
            plt.figure(figsize=(12, 8))
            
            # Create horizontal bar chart
            y_pos = np.arange(len(display_names))
            bars = plt.barh(y_pos, complexity_values, align='center')
            
            # Color-code bars based on complexity thresholds
            for i, bar in enumerate(bars):
                if complexity_values[i] <= 5:
                    bar.set_color('green')
                elif complexity_values[i] <= 10:
                    bar.set_color('orange')
                else:
                    bar.set_color('red')
            
            # Add complexity threshold lines
            plt.axvline(x=5, color='green', linestyle='--', alpha=0.7, label='Low Complexity')
            plt.axvline(x=10, color='orange', linestyle='--', alpha=0.7, label='Medium Complexity')
            plt.axvline(x=15, color='red', linestyle='--', alpha=0.7, label='High Complexity')
            
            # Add labels and title
            plt.yticks(y_pos, display_names)
            plt.xlabel('Cyclomatic Complexity')
            plt.title('Code Complexity by Function')
            plt.legend()
            
            # Add values on bars
            for i, v in enumerate(complexity_values):
                plt.text(v + 0.1, i, str(v), va='center')
            
            # Set output file path
            if not output_file:
                output_file = os.path.join(self.output_dir, 'complexity_chart.png')
            
            # Save figure
            plt.tight_layout()
            plt.savefig(output_file)
            plt.close()
            
            logger.info(f"Complexity chart saved to {output_file}")
            return output_file
            
        except Exception as e:
            logger.error(f"Error creating complexity chart: {str(e)}")
            return None
    
    def create_hotspot_map(self, metrics: Dict[str, Any], output_file: str = None) -> Optional[str]:
        """
        Create a visual heat map of code hotspots
        
        Args:
            metrics: Performance metrics including hotspots
            output_file: Output file path (defaults to hotspot_map.png in output_dir)
            
        Returns:
            Path to the generated map file or None if visualization failed
        """
        if not HAS_VISUALIZATION:
            logger.error("Cannot create visualization: matplotlib not installed")
            return None
        
        try:
            # Extract hotspot data
            hotspots = metrics.get("potential_hotspots", [])
            if not hotspots:
                logger.warning("No hotspot data available")
                return None
            
            # Prepare data
            locations = [h.get("location", "unknown") for h in hotspots]
            if len(locations) > 15:
                # Truncate to top 15 hotspots
                locations = locations[:15]
            
            # Assign severity scores
            severity_scores = []
            reasons = []
            for hotspot in hotspots[:15]:  # Match the truncated locations
                reason = hotspot.get("reason", "")
                reasons.append(reason)
                
                # Assign score based on reason keywords
                score = 5  # Default medium score
                if "High" in reason:
                    score = 8
                elif "Long" in reason:
                    score = 7
                elif "complexity" in reason.lower():
                    # Extract complexity value if present
                    try:
                        value = int(re.search(r'\((\d+)\)', reason).group(1))
                        score = min(10, max(1, value // 2))  # Scale to 1-10
                    except (AttributeError, ValueError):
                        pass
                
                severity_scores.append(score)
            
            # For better display, truncate location names
            display_names = [loc.split("::")[-1] if "::" in loc else loc for loc in locations]
            display_names = [n[:25] + "..." if len(n) > 28 else n for n in display_names]
            
            # Create figure
            plt.figure(figsize=(14, 8))
            
            # Create heat map-style visualization
            y_pos = np.arange(len(display_names))
            bars = plt.barh(y_pos, severity_scores, align='center')
            
            # Color gradient based on severity
            cmap = plt.cm.get_cmap('YlOrRd')
            for i, bar in enumerate(bars):
                bar.set_color(cmap(severity_scores[i] / 10.0))
            
            # Add labels and title
            plt.yticks(y_pos, display_names)
            plt.xlabel('Severity Score (1-10)')
            plt.title('Performance Hotspots')
            
            # Add reason annotations
            for i, (score, reason) in enumerate(zip(severity_scores, reasons)):
                plt.text(score + 0.1, i, reason, va='center', fontsize=8)
            
            # Set output file path
            if not output_file:
                output_file = os.path.join(self.output_dir, 'hotspot_map.png')
            
            # Save figure
            plt.tight_layout()
            plt.savefig(output_file)
            plt.close()
            
            logger.info(f"Hotspot map saved to {output_file}")
            return output_file
            
        except Exception as e:
            logger.error(f"Error creating hotspot map: {str(e)}")
            return None
    
    def create_performance_dashboard(self, metrics: Dict[str, Any], output_file: str = None) -> Optional[str]:
        """
        Create a comprehensive performance dashboard with multiple visualizations
        
        Args:
            metrics: Performance metrics data
            output_file: Output file path (defaults to performance_dashboard.png in output_dir)
            
        Returns:
            Path to the generated dashboard file or None if visualization failed
        """
        if not HAS_VISUALIZATION:
            logger.error("Cannot create dashboard: matplotlib not installed")
            return None
        
        try:
            # Extract metrics
            summary = metrics.get("static_analysis", {}).get("summary", {})
            if not summary:
                logger.warning("No summary metrics available for dashboard")
                return None
            
            # Create figure with subplots
            fig, axes = plt.subplots(2, 2, figsize=(16, 12))
            
            # 1. Complexity Distribution (top left)
            complexity_data = {
                'Cyclomatic': summary.get('avg_cyclomatic_complexity', 0),
                'Cognitive': summary.get('avg_cognitive_complexity', 0),
                'Method Length': summary.get('avg_method_length', 0) / 10,  # Scale down for comparison
                'Class Size': summary.get('avg_class_size', 0) / 50  # Scale down for comparison
            }
            
            axes[0, 0].bar(complexity_data.keys(), complexity_data.values(), color='skyblue')
            axes[0, 0].set_title('Complexity Metrics (Scaled)')
            axes[0, 0].set_ylabel('Average Value')
            axes[0, 0].grid(axis='y', linestyle='--', alpha=0.7)
            
            # Add values on bars
            for i, (key, value) in enumerate(complexity_data.items()):
                axes[0, 0].text(i, value + 0.1, f"{value:.2f}", ha='center')
            
            # 2. Issues by Type (top right)
            issues = metrics.get("static_analysis", {}).get("issues", [])
            if issues:
                issue_types = {}
                for issue in issues:
                    issue_type = issue.get("type", "unknown")
                    issue_types[issue_type] = issue_types.get(issue_type, 0) + 1
                
                axes[0, 1].pie(issue_types.values(), labels=issue_types.keys(), autopct='%1.1f%%', 
                        shadow=True, startangle=90)
                axes[0, 1].set_title('Issues by Type')
            else:
                axes[0, 1].text(0.5, 0.5, 'No issues found', ha='center', va='center', fontsize=12)
                axes[0, 1].set_title('Issues by Type')
                axes[0, 1].axis('off')
            
            # 3. Complexity Range Distribution (bottom left)
            cyclomatic = metrics.get("static_analysis", {}).get("cyclomatic_complexity", {})
            if cyclomatic:
                values = list(cyclomatic.values())
                bins = [0, 5, 10, 15, 20, 25, 30, max(values) + 1]
                axes[1, 0].hist(values, bins=bins, edgecolor='black', alpha=0.7, color='lightgreen')
                axes[1, 0].set_title('Cyclomatic Complexity Distribution')
                axes[1, 0].set_xlabel('Complexity Range')
                axes[1, 0].set_ylabel('Number of Functions')
                axes[1, 0].grid(axis='y', linestyle='--', alpha=0.7)
            else:
                axes[1, 0].text(0.5, 0.5, 'No complexity data available', ha='center', va='center', fontsize=12)
                axes[1, 0].set_title('Complexity Distribution')
                axes[1, 0].axis('off')
            
            # 4. Performance Metrics Radar Chart (bottom right)
            # Normalize metrics to 0-10 scale for radar chart
            metrics_names = ['Code\nComplexity', 'Method\nLength', 'Class\nSize', 
                            'Inheritance\nDepth', 'Code\nDuplication']
            
            max_cyclomatic = summary.get('max_cyclomatic_complexity', 0)
            max_method_length = summary.get('max_method_length', 0)
            max_class_size = summary.get('max_class_size', 0)
            max_inheritance = summary.get('max_inheritance_depth', 0)
            
            # Compute normalized scores (lower is better, 10 is worst)
            complexity_score = min(10, max_cyclomatic / 3)
            method_length_score = min(10, max_method_length / 20)
            class_size_score = min(10, max_class_size / 100)
            inheritance_score = min(10, max_inheritance / 1.5)
            duplication_score = 5  # Placeholder since we don't have exact duplication metric
            
            values = [complexity_score, method_length_score, class_size_score, 
                    inheritance_score, duplication_score]
            
            # Radar chart setup
            angles = np.linspace(0, 2*np.pi, len(metrics_names), endpoint=False).tolist()
            values += values[:1]  # Close the polygon
            angles += angles[:1]  # Close the polygon
            metrics_names += metrics_names[:1]  # Close the polygon
            
            ax = axes[1, 1]
            ax.plot(angles, values, 'o-', linewidth=2)
            ax.fill(angles, values, alpha=0.25)
            ax.set_thetagrids(np.degrees(angles[:-1]), metrics_names[:-1])
            ax.set_ylim(0, 10)
            ax.set_title('Performance Risk Indicators (0-10 scale)')
            ax.grid(True)
            
            # Set title for entire dashboard
            plt.suptitle('Code Performance Dashboard', fontsize=16)
            
            # Set output file path
            if not output_file:
                output_file = os.path.join(self.output_dir, 'performance_dashboard.png')
            
            # Save figure
            plt.tight_layout(rect=[0, 0, 1, 0.96])  # Adjust for suptitle
            plt.savefig(output_file)
            plt.close()
            
            logger.info(f"Performance dashboard saved to {output_file}")
            return output_file
            
        except Exception as e:
            logger.error(f"Error creating performance dashboard: {str(e)}")
            return None
    
    def create_html_report(self, metrics: Dict[str, Any], template_content: str, output_file: str = None) -> Optional[str]:
        """
        Create an HTML performance report with visualizations
        
        Args:
            metrics: Performance metrics data
            template_content: Content of the performance review template
            output_file: Output file path (defaults to performance_report.html in output_dir)
            
        Returns:
            Path to the generated HTML file or None if creation failed
        """
        try:
            # First create visualizations if matplotlib is available
            visualizations = {}
            if HAS_VISUALIZATION:
                # Create and save all visualizations
                complexity_chart = self.create_complexity_chart(metrics)
                if complexity_chart:
                    visualizations['complexity_chart'] = os.path.basename(complexity_chart)
                
                hotspot_map = self.create_hotspot_map(metrics)
                if hotspot_map:
                    visualizations['hotspot_map'] = os.path.basename(hotspot_map)
                
                dashboard = self.create_performance_dashboard(metrics)
                if dashboard:
                    visualizations['dashboard'] = os.path.basename(dashboard)
            
            # Prepare HTML content
            summary = metrics.get("static_analysis", {}).get("summary", {})
            issues = metrics.get("static_analysis", {}).get("issues", [])
            hotspots = metrics.get("potential_hotspots", [])
            recommendations = metrics.get("algorithm_recommendations", [])
            
            # Basic HTML template
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Performance Analysis Report</title>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 20px; line-height: 1.6; }}
                    h1, h2, h3 {{ color: #333; }}
                    .metric-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 20px; }}
                    .metric-card {{ background-color: #f5f5f5; border-radius: 5px; padding: 15px; }}
                    .metric-value {{ font-size: 24px; font-weight: bold; color: #0066cc; }}
                    .issue {{ background-color: #fff0f0; padding: 10px; margin-bottom: 10px; border-left: 4px solid #ff6666; }}
                    .hotspot {{ background-color: #fff8e1; padding: 10px; margin-bottom: 10px; border-left: 4px solid #ffb74d; }}
                    .recommendation {{ background-color: #e1f5fe; padding: 10px; margin-bottom: 10px; border-left: 4px solid #29b6f6; }}
                    .high {{ color: #d32f2f; }}
                    .medium {{ color: #f57c00; }}
                    .low {{ color: #388e3c; }}
                    .viz-container {{ margin: 20px 0; text-align: center; }}
                    .template {{ background-color: #f9f9f9; padding: 20px; border: 1px solid #ddd; margin: 20px 0; }}
                </style>
            </head>
            <body>
                <h1>Performance Analysis Report</h1>
                <p>Generated on: {metrics.get("date", "unknown date")}</p>
                <p>File: {metrics.get("file_name", "unknown")}</p>
                
                <h2>Complexity Metrics Summary</h2>
                <div class="metric-grid">
                    <div class="metric-card">
                        <h3>Cyclomatic Complexity</h3>
                        <div class="metric-value">{summary.get('avg_cyclomatic_complexity', 0):.2f}</div>
                        <p>Average | <span {self._get_severity_class(summary.get('max_cyclomatic_complexity', 0), 5, 10, 15)}>{summary.get('max_cyclomatic_complexity', 0)}</span> Maximum</p>
                    </div>
                    
                    <div class="metric-card">
                        <h3>Cognitive Complexity</h3>
                        <div class="metric-value">{summary.get('avg_cognitive_complexity', 0):.2f}</div>
                        <p>Average | <span {self._get_severity_class(summary.get('max_cognitive_complexity', 0), 10, 20, 30)}>{summary.get('max_cognitive_complexity', 0)}</span> Maximum</p>
                    </div>
                    
                    <div class="metric-card">
                        <h3>Method Length</h3>
                        <div class="metric-value">{summary.get('avg_method_length', 0):.2f}</div>
                        <p>Average Lines | <span {self._get_severity_class(summary.get('max_method_length', 0), 50, 100, 150)}>{summary.get('max_method_length', 0)}</span> Maximum</p>
                    </div>
                    
                    <div class="metric-card">
                        <h3>Class Size</h3>
                        <div class="metric-value">{summary.get('avg_class_size', 0):.2f}</div>
                        <p>Average Lines | <span {self._get_severity_class(summary.get('max_class_size', 0), 200, 500, 800)}>{summary.get('max_class_size', 0)}</span> Maximum</p>
                    </div>
                </div>
            """
            
            # Add visualizations if available
            if visualizations:
                html_content += """
                <h2>Performance Visualizations</h2>
                """
                
                if 'dashboard' in visualizations:
                    html_content += f"""
                    <div class="viz-container">
                        <h3>Performance Dashboard</h3>
                        <img src="{visualizations['dashboard']}" alt="Performance Dashboard" style="max-width: 100%;">
                    </div>
                    """
                
                if 'complexity_chart' in visualizations:
                    html_content += f"""
                    <div class="viz-container">
                        <h3>Complexity Chart</h3>
                        <img src="{visualizations['complexity_chart']}" alt="Complexity Chart" style="max-width: 100%;">
                    </div>
                    """
                
                if 'hotspot_map' in visualizations:
                    html_content += f"""
                    <div class="viz-container">
                        <h3>Performance Hotspots</h3>
                        <img src="{visualizations['hotspot_map']}" alt="Hotspot Map" style="max-width: 100%;">
                    </div>
                    """
            
            # Add issues section if there are issues
            if issues:
                html_content += """
                <h2>Performance Issues</h2>
                """
                
                for issue in issues:
                    severity = issue.get("severity", "medium")
                    html_content += f"""
                    <div class="issue">
                        <h3><span class="{severity}">{severity.upper()}</span>: {issue.get("issue", "Unknown Issue")}</h3>
                        <p>Type: {issue.get("type", "unknown")}</p>
                    </div>
                    """
            
            # Add hotspots section if there are hotspots
            if hotspots:
                html_content += """
                <h2>Potential Performance Hotspots</h2>
                """
                
                for hotspot in hotspots:
                    html_content += f"""
                    <div class="hotspot">
                        <h3>{hotspot.get("location", "Unknown Location")}</h3>
                        <p><strong>Reason:</strong> {hotspot.get("reason", "Unknown reason")}</p>
                        <p><strong>Recommendation:</strong> {hotspot.get("recommendation", "No recommendation")}</p>
                    </div>
                    """
            
            # Add recommendations section if there are recommendations
            if recommendations:
                html_content += """
                <h2>Algorithm Recommendations</h2>
                """
                
                for rec in recommendations:
                    html_content += f"""
                    <div class="recommendation">
                        <h3>{rec.get("location", "Unknown Location")}</h3>
                        <p><strong>Issue:</strong> {rec.get("issue", "Unknown issue")}</p>
                        <p><strong>Recommendation:</strong> {rec.get("recommendation", "No recommendation")}</p>
                    </div>
                    """
            
            # Add template reference
            if template_content:
                html_content += """
                <h2>Performance Review Template</h2>
                <div class="template">
                """
                
                # Convert markdown template to simple HTML
                template_html = template_content.replace("\n\n", "<br><br>")
                template_html = template_html.replace("## ", "<h3>").replace("\n- [ ]", "</h3><ul><li>").replace("\n- [x]", "</h3><ul><li>✓ ")
                template_html = template_html.replace("\n###", "</li></ul><h4>").replace("\n##", "</li></ul><h3>")
                template_html = template_html.replace("\n#", "<h2>").replace("\n-", "</h2><ul><li>")
                
                html_content += template_html + """
                </div>
                """
            
            # Close HTML
            html_content += """
            </body>
            </html>
            """
            
            # Write to file
            if not output_file:
                output_file = os.path.join(self.output_dir, 'performance_report.html')
            
            with open(output_file, 'w') as f:
                f.write(html_content)
            
            logger.info(f"HTML report saved to {output_file}")
            return output_file
            
        except Exception as e:
            logger.error(f"Error creating HTML report: {str(e)}")
            return None
    
    def _get_severity_class(self, value: float, low: float, medium: float, high: float) -> str:
        """Helper to determine CSS class based on severity thresholds"""
        if value < low:
            return 'class="low"'
        elif value < medium:
            return 'class="medium"'
        else:
            return 'class="high"'


if __name__ == "__main__":
    # Example usage
    from performance_metrics import RuntimePerformanceAnalyzer
    from review_logic import CodeReviewer
    
    # Analyze a file
    reviewer = CodeReviewer()
    analyzer = RuntimePerformanceAnalyzer()
    results = analyzer.analyze_code_file("review_logic.py")
    
    # Create visualizations
    visualizer = PerformanceVisualizer(output_dir="reports")
    visualizer.create_complexity_chart(results.get("static_analysis", {}))
    visualizer.create_hotspot_map(results)
    visualizer.create_performance_dashboard(results)
    
    # Create HTML report
    with open("review_templates/performance.md", 'r') as f:
        template_content = f.read()
    
    visualizer.create_html_report(results, template_content)