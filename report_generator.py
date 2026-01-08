"""
HTML Report Generator for LLM Assessment
Generates a comprehensive HTML report with visualizations
"""

from pathlib import Path
from typing import Dict, Any
from datetime import datetime


class HTMLReportGenerator:
    """Generate HTML reports for assessment results"""
    
    def __init__(self, results: Dict[str, Any], config: Dict[str, Any]):
        self.results = results
        self.config = config
    
    def generate(self, output_path: Path):
        """Generate HTML report"""
        html = self._generate_html()
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
    
    def _generate_html(self) -> str:
        """Generate complete HTML document"""
        return f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LLM Assessment Report - {self.results['metadata']['model_name']}</title>
    <style>
        {self._get_css()}
    </style>
</head>
<body>
    <div class="container">
        {self._generate_header()}
        {self._generate_overall_summary()}
        {self._generate_explainability_section()}
        {self._generate_reliability_section()}
        {self._generate_safety_section()}
        {self._generate_footer()}
    </div>
    <script>
        {self._get_javascript()}
    </script>
</body>
</html>"""
    
    def _get_css(self) -> str:
        """Get CSS styles"""
        return """
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .header .subtitle {
            font-size: 1.1em;
            opacity: 0.9;
        }
        
        .section {
            padding: 40px;
            border-bottom: 1px solid #e0e0e0;
        }
        
        .section:last-child {
            border-bottom: none;
        }
        
        .section-title {
            font-size: 1.8em;
            margin-bottom: 20px;
            color: #667eea;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .overall-score {
            text-align: center;
            padding: 40px;
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            border-radius: 10px;
            margin: 20px 0;
        }
        
        .overall-score .score {
            font-size: 4em;
            font-weight: bold;
            margin: 20px 0;
        }
        
        .overall-score .status {
            font-size: 1.5em;
            margin-top: 10px;
        }
        
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        
        .metric-card {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }
        
        .metric-card.pass {
            border-left-color: #28a745;
        }
        
        .metric-card.fail {
            border-left-color: #dc3545;
        }
        
        .metric-card.error {
            border-left-color: #ffc107;
        }
        
        .metric-card .metric-name {
            font-weight: 600;
            margin-bottom: 10px;
            font-size: 1.1em;
        }
        
        .metric-card .metric-value {
            font-size: 2em;
            font-weight: bold;
            margin: 10px 0;
        }
        
        .metric-card .metric-status {
            display: inline-block;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: 600;
        }
        
        .metric-status.pass {
            background: #d4edda;
            color: #155724;
        }
        
        .metric-status.fail {
            background: #f8d7da;
            color: #721c24;
        }
        
        .metric-status.error {
            background: #fff3cd;
            color: #856404;
        }
        
        .metric-status.skipped {
            background: #e2e3e5;
            color: #383d41;
        }
        
        .details-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        
        .details-table th,
        .details-table td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #dee2e6;
        }
        
        .details-table th {
            background: #f8f9fa;
            font-weight: 600;
            color: #495057;
        }
        
        .details-table tr:hover {
            background: #f8f9fa;
        }
        
        .progress-bar {
            width: 100%;
            height: 30px;
            background: #e9ecef;
            border-radius: 15px;
            overflow: hidden;
            margin: 10px 0;
        }
        
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: 600;
            transition: width 0.3s ease;
        }
        
        .footer {
            text-align: center;
            padding: 20px;
            background: #f8f9fa;
            color: #6c757d;
            font-size: 0.9em;
        }
        
        .timestamp {
            color: rgba(255,255,255,0.8);
            margin-top: 10px;
        }
        
        .info-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }
        
        .info-item {
            background: rgba(255,255,255,0.1);
            padding: 15px;
            border-radius: 5px;
        }
        
        .info-label {
            font-size: 0.9em;
            opacity: 0.8;
            margin-bottom: 5px;
        }
        
        .info-value {
            font-size: 1.1em;
            font-weight: 600;
        }
        
        .badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 0.85em;
            font-weight: 600;
            margin: 2px;
        }
        
        .badge.success {
            background: #d4edda;
            color: #155724;
        }
        
        .badge.warning {
            background: #fff3cd;
            color: #856404;
        }
        
        .badge.danger {
            background: #f8d7da;
            color: #721c24;
        }
        
        .badge.info {
            background: #d1ecf1;
            color: #0c5460;
        }
        """
    
    def _get_javascript(self) -> str:
        """Get JavaScript code"""
        return """
        // Animate progress bars on load
        window.addEventListener('load', function() {
            const progressFills = document.querySelectorAll('.progress-fill');
            progressFills.forEach(fill => {
                const targetWidth = fill.style.width;
                fill.style.width = '0%';
                setTimeout(() => {
                    fill.style.width = targetWidth;
                }, 100);
            });
        });
        
        // Add smooth scroll
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });
        """
    
    def _generate_header(self) -> str:
        """Generate header section"""
        metadata = self.results['metadata']
        
        return f"""
        <div class="header">
            <h1>🤖 LLM Assessment Report</h1>
            <div class="subtitle">Comprehensive Evaluation of {metadata['model_name']}</div>
            <div class="info-grid">
                <div class="info-item">
                    <div class="info-label">Model Name</div>
                    <div class="info-value">{metadata['model_name']}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Model Type</div>
                    <div class="info-value">{metadata['model_type']}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Evaluation Date</div>
                    <div class="info-value">{metadata['timestamp'][:10]}</div>
                </div>
            </div>
        </div>
        """
    
    def _generate_overall_summary(self) -> str:
        """Generate overall summary section"""
        overall = self.results.get('overall', {})
        
        if 'score' not in overall:
            return """
            <div class="section">
                <div class="section-title">📊 Overall Assessment</div>
                <div class="metric-card error">
                    <div class="metric-name">Status</div>
                    <div class="metric-status error">Incomplete Evaluation</div>
                </div>
            </div>
            """
        
        score = overall['score']
        status = "PASS" if overall['pass'] else "FAIL"
        status_class = "pass" if overall['pass'] else "fail"
        
        components_html = ""
        if 'components' in overall:
            components_html = "<div class='metrics-grid'>"
            
            for component_name, component_data in overall['components'].items():
                if component_data:
                    comp_score = component_data['score']
                    comp_weight = component_data['weight']
                    components_html += f"""
                    <div class="metric-card">
                        <div class="metric-name">{component_name.title()}</div>
                        <div class="metric-value">{comp_score:.3f}</div>
                        <div>Weight: {comp_weight:.1%}</div>
                    </div>
                    """
            
            components_html += "</div>"
        
        return f"""
        <div class="section">
            <div class="overall-score">
                <h2>Overall Assessment Score</h2>
                <div class="score">{score:.3f}</div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {score*100:.1f}%">
                        {score*100:.1f}%
                    </div>
                </div>
                <div class="status">
                    <span class="badge {'success' if status == 'PASS' else 'danger'}">{status}</span>
                </div>
            </div>
            {components_html}
        </div>
        """
    
    def _generate_explainability_section(self) -> str:
        """Generate explainability section"""
        exp = self.results.get('explainability', {})
        
        if exp.get('status') == 'skipped':
            return self._generate_skipped_section("🔍 Explainability")
        
        if exp.get('status') == 'error':
            return self._generate_error_section("🔍 Explainability", exp.get('error', 'Unknown error'))
        
        if exp.get('status') != 'completed':
            return ""
        
        return f"""
        <div class="section" id="explainability">
            <div class="section-title">🔍 Explainability</div>
            <div class="metrics-grid">
                <div class="metric-card {'pass' if exp['pass'] else 'fail'}">
                    <div class="metric-name">Overall Score</div>
                    <div class="metric-value">{exp['overall_score']:.3f}</div>
                    <span class="metric-status {'pass' if exp['pass'] else 'fail'}">
                        {'✅ PASS' if exp['pass'] else '❌ FAIL'}
                    </span>
                </div>
                {self._generate_cot_card(exp.get('cot', {}))}
                {self._generate_citation_card(exp.get('citation', {}))}
            </div>
        </div>
        """
    
    def _generate_cot_card(self, cot: Dict[str, Any]) -> str:
        """Generate Chain of Thought card"""
        if not cot:
            return ""
        
        return f"""
        <div class="metric-card {'pass' if cot.get('pass') else 'fail'}">
            <div class="metric-name">Chain of Thought (CoT)</div>
            <div class="metric-value">{cot['avg_score']:.3f}</div>
            <div>Model: {cot['model']}</div>
            <div>Count: {cot['count']}</div>
            <div>Threshold: {cot['threshold']}</div>
            <span class="metric-status {'pass' if cot.get('pass') else 'fail'}">
                {'✅ PASS' if cot.get('pass') else '❌ FAIL'}
            </span>
        </div>
        """
    
    def _generate_citation_card(self, citation: Dict[str, Any]) -> str:
        """Generate Citation card"""
        if not citation:
            return ""
        
        return f"""
        <div class="metric-card {'pass' if citation.get('pass') else 'fail'}">
            <div class="metric-name">Citation</div>
            <div class="metric-value">{citation['avg_score']:.3f}</div>
            <div>Response Model: {citation['response_model']}</div>
            <div>Judge Model: {citation['judge_model']}</div>
            <div>Count: {citation['count']}</div>
            <div>Threshold: {citation['threshold']}</div>
            <span class="metric-status {'pass' if citation.get('pass') else 'fail'}">
                {'✅ PASS' if citation.get('pass') else '❌ FAIL'}
            </span>
        </div>
        """
    
    def _generate_reliability_section(self) -> str:
        """Generate reliability section"""
        rel = self.results.get('reliability', {})
        
        if rel.get('status') == 'skipped':
            return self._generate_skipped_section("✅ Reliability")
        
        if rel.get('status') == 'error':
            return self._generate_error_section("✅ Reliability", rel.get('error', 'Unknown error'))
        
        if rel.get('status') != 'completed':
            return ""
        
        ceval_card = ""
        if 'ceval' in rel and rel['ceval'].get('status') == 'completed':
            ceval = rel['ceval']
            ceval_card = f"""
            <div class="metric-card {'pass' if ceval['pass'] else 'fail'}">
                <div class="metric-name">C-Eval (Knowledge Accuracy)</div>
                <div class="metric-value">{ceval['accuracy']:.3f}</div>
                <div>Threshold: {ceval['threshold']}</div>
                <span class="metric-status {'pass' if ceval['pass'] else 'fail'}">
                    {'✅ PASS' if ceval['pass'] else '❌ FAIL'}
                </span>
            </div>
            """
        
        consistency_card = ""
        if 'consistency' in rel and rel['consistency'].get('status') == 'completed':
            consistency = rel['consistency']
            consistency_card = f"""
            <div class="metric-card {'pass' if consistency['pass'] else 'fail'}">
                <div class="metric-name">Consistency</div>
                <div class="metric-value">{consistency['score']:.3f}</div>
                <div>Threshold: {consistency['threshold']}</div>
                <span class="metric-status {'pass' if consistency['pass'] else 'fail'}">
                    {'✅ PASS' if consistency['pass'] else '❌ FAIL'}
                </span>
            </div>
            """
        
        return f"""
        <div class="section" id="reliability">
            <div class="section-title">✅ Reliability</div>
            <div class="metrics-grid">
                <div class="metric-card {'pass' if rel['pass'] else 'fail'}">
                    <div class="metric-name">Overall Score</div>
                    <div class="metric-value">{rel['overall_score']:.3f}</div>
                    <span class="metric-status {'pass' if rel['pass'] else 'fail'}">
                        {'✅ PASS' if rel['pass'] else '❌ FAIL'}
                    </span>
                </div>
                {ceval_card}
                {consistency_card}
            </div>
        </div>
        """
    
    def _generate_safety_section(self) -> str:
        """Generate safety section"""
        safe = self.results.get('safety', {})
        
        if safe.get('status') == 'skipped':
            return self._generate_skipped_section("🛡️ Safety")
        
        if safe.get('status') == 'error':
            return self._generate_error_section("🛡️ Safety", safe.get('error', 'Unknown error'))
        
        if safe.get('status') != 'completed':
            return ""
        
        # Module name mapping for better display
        module_display_names = {
            'bbq': 'BBQ (Bias Benchmark)',
            'bipia': 'BIPIA (Indirect Prompt Injection)',
            'toxicity': 'Toxicity',
            'information_disclosure': 'Information Disclosure',
            'direct_prompt_injection': 'Direct Prompt Injection',
            'misinformation': 'Misinformation'
        }
        
        # Generate cards for all safety modules dynamically
        module_cards = ""
        for module_name, module_data in safe.items():
            # Skip meta fields
            if module_name in ['status', 'overall_score', 'pass', 'threshold']:
                continue
            
            if isinstance(module_data, dict) and module_data.get('status') == 'completed':
                display_name = module_display_names.get(module_name, module_name.replace('_', ' ').title())
                score = module_data.get('score', module_data.get('accuracy', 0))
                is_pass = module_data.get('pass', False)
                threshold = module_data.get('threshold', 0)
                
                # Build additional info
                extra_info = ""
                if 'accuracy' in module_data and 'score' in module_data:
                    extra_info = f"<div>Accuracy: {module_data['accuracy']:.3f}</div>"
                if 'asr' in module_data:
                    extra_info += f"<div>ASR: {module_data['asr']:.3f}</div>"
                if 'pass_rate' in module_data:
                    extra_info += f"<div>Pass Rate: {module_data['pass_rate']:.3f}</div>"
                
                module_cards += f"""
                <div class="metric-card {'pass' if is_pass else 'fail'}">
                    <div class="metric-name">{display_name}</div>
                    <div class="metric-value">{score:.3f}</div>
                    {extra_info}
                    <div>Threshold: {threshold}</div>
                    <span class="metric-status {'pass' if is_pass else 'fail'}">
                        {'✅ PASS' if is_pass else '❌ FAIL'}
                    </span>
                </div>
                """
        
        return f"""
        <div class="section" id="safety">
            <div class="section-title">🛡️ Safety</div>
            <div class="metrics-grid">
                <div class="metric-card {'pass' if safe['pass'] else 'fail'}">
                    <div class="metric-name">Overall Score</div>
                    <div class="metric-value">{safe['overall_score']:.3f}</div>
                    <span class="metric-status {'pass' if safe['pass'] else 'fail'}">
                        {'✅ PASS' if safe['pass'] else '❌ FAIL'}
                    </span>
                </div>
                {module_cards}
            </div>
        </div>
        """
    
    def _generate_skipped_section(self, title: str) -> str:
        """Generate skipped section"""
        return f"""
        <div class="section">
            <div class="section-title">{title}</div>
            <div class="metric-card">
                <div class="metric-name">Status</div>
                <span class="metric-status skipped">⏭️ SKIPPED</span>
                <p style="margin-top: 10px; color: #6c757d;">
                    This evaluation was disabled in the configuration.
                </p>
            </div>
        </div>
        """
    
    def _generate_error_section(self, title: str, error: str) -> str:
        """Generate error section"""
        return f"""
        <div class="section">
            <div class="section-title">{title}</div>
            <div class="metric-card error">
                <div class="metric-name">Status</div>
                <span class="metric-status error">❌ ERROR</span>
                <p style="margin-top: 10px; color: #721c24; background: #f8d7da; padding: 10px; border-radius: 5px;">
                    {error}
                </p>
            </div>
        </div>
        """
    
    def _generate_footer(self) -> str:
        """Generate footer"""
        return f"""
        <div class="footer">
            <p>Generated by LLM Assessment Framework</p>
            <p>Report generated at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        """
