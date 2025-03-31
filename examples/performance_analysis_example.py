"""
Example script demonstrating how to use the performance metrics features
"""
import os
import sys
import logging

# Add parent directory to Python path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import project modules
from review_logic import CodeReviewer, generate_review_report
from performance_metrics import RuntimePerformanceAnalyzer, generate_performance_report
from performance_visualization import PerformanceVisualizer

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    """
    Main function demonstrating performance metrics functionality
    """
    # Create output directory for reports
    reports_dir = "performance_reports"
    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir)
    
    # Step 1: Initialize the code reviewer and analyzer
    logger.info("Initializing code review tools...")
    reviewer = CodeReviewer()
    analyzer = RuntimePerformanceAnalyzer()
    visualizer = PerformanceVisualizer(output_dir=reports_dir)
    
    # Step 2: Analyze a file using the code reviewer
    target_file = "../review_logic.py"  # Path relative to this example script
    if not os.path.exists(target_file):
        target_file = "review_logic.py"  # Try alternate path
    
    logger.info(f"Reviewing file: {target_file}")
    review_results = reviewer.review_code(target_file, template_type="performance")
    
    # Step 3: Generate a standard review report
    report_file = os.path.join(reports_dir, "review_report.md")
    with open(report_file, "w") as f:
        f.write(generate_review_report(review_results))
    logger.info(f"Basic review report saved to: {report_file}")
    
    # Step 4: Perform more detailed performance analysis
    logger.info("Performing detailed performance analysis...")
    performance_results = analyzer.analyze_code_file(target_file)
    
    # Step 5: Generate a detailed performance report
    detailed_report_file = os.path.join(reports_dir, "detailed_performance_report.md")
    with open(detailed_report_file, "w") as f:
        f.write(generate_performance_report(performance_results))
    logger.info(f"Detailed performance report saved to: {detailed_report_file}")
    
    # Step 6: Generate visualizations
    logger.info("Generating performance visualizations...")
    try:
        complexity_chart = visualizer.create_complexity_chart(
            performance_results.get("static_analysis", {}),
            os.path.join(reports_dir, "complexity_chart.png")
        )
        if complexity_chart:
            logger.info(f"Complexity chart saved to: {complexity_chart}")
        
        hotspot_map = visualizer.create_hotspot_map(
            performance_results,
            os.path.join(reports_dir, "hotspot_map.png")
        )
        if hotspot_map:
            logger.info(f"Hotspot map saved to: {hotspot_map}")
        
        dashboard = visualizer.create_performance_dashboard(
            performance_results,
            os.path.join(reports_dir, "performance_dashboard.png")
        )
        if dashboard:
            logger.info(f"Performance dashboard saved to: {dashboard}")
    except Exception as e:
        logger.warning(f"Visualization generation failed: {str(e)}")
        logger.warning("This may be due to missing matplotlib. Install with: pip install matplotlib numpy")
    
    # Step 7: Generate HTML report
    logger.info("Generating HTML report with visualizations...")
    try:
        # Get template content
        template_file = "../review_templates/performance.md"  # Path relative to this example script
        if not os.path.exists(template_file):
            template_file = "review_templates/performance.md"  # Try alternate path
        
        template_content = ""
        try:
            with open(template_file, 'r') as f:
                template_content = f.read()
        except Exception as e:
            logger.warning(f"Could not read template file: {str(e)}")
        
        # Add file name to metrics for the report
        performance_results["file_name"] = os.path.basename(target_file)
        
        # Generate HTML report
        html_report = visualizer.create_html_report(
            performance_results,
            template_content,
            os.path.join(reports_dir, "performance_report.html")
        )
        if html_report:
            logger.info(f"HTML performance report saved to: {html_report}")
    except Exception as e:
        logger.error(f"HTML report generation failed: {str(e)}")
    
    logger.info("Performance analysis completed successfully!")
    logger.info(f"All reports and visualizations saved to directory: {reports_dir}")


if __name__ == "__main__":
    main()