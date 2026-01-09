import asyncio
import json
import sys
import warnings
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

warnings.filterwarnings("ignore", category=DeprecationWarning)


class IntegratedAssessment:
    """Main assessment orchestrator"""
    
    def __init__(self, config_path: str = "config.json"):
        self.config_path = Path(config_path)
        self.config = self._load_config()
        self.results = {
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "model_name": self.config["model"]["name"],
                "model_type": self.config["model"]["type"]
            },
            "explainability": {},
            "reliability": {},
            "safety": {},
            "overall": {}
        }
        self.output_dir = Path(self.config["output"]["directory"])
        self.output_dir.mkdir(exist_ok=True)
        
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from JSON file"""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
        
        with open(self.config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    async def run_explainability(self) -> Dict[str, Any]:
        """Run explainability evaluations"""
        if not self.config["evaluation"]["explainability"]["enabled"]:
            print("⏭️  Skipping Explainability evaluation (disabled in config)")
            return {"status": "skipped"}
        
        print("\n" + "="*60)
        print("Starting Explainability Evaluation")
        print("="*60)
        
        try:
            # Import explainability modules
            sys.path.insert(0, str(Path(__file__).parent / "explainability"))
            from core.common.clients import AsyncAzureOAIClient, AsyncGeminiClient, AsyncLlamaClient
            from core.common.paths import data_dir
            from core.pipelines import run_all
            from core.evaluators import ScoreAggregator, ResultProcessor
            
            # Initialize LLM clients based on config
            llm_config = self.config["llm_configs"]
            
            # For explainability, we need CoT answer LLM, Citation answer LLM, and Citation judge LLM
            cot_answer_llm = AsyncAzureOAIClient(
                api_key=llm_config["azure_openai"]["api_key"],
                azure_endpoint=llm_config["azure_openai"]["endpoint"],
                api_version=llm_config["azure_openai"]["api_version"],
                model=llm_config["azure_openai"]["model"]
            )
            
            cite_answer_llm = AsyncLlamaClient(
                model=llm_config["ollama"]["model"],
                temperature=0.3,
            )
            
            cite_judge_llm = AsyncGeminiClient(
                api_key=llm_config["gemini"]["api_key"],
                model=llm_config["gemini"]["model"],
                temperature=0.0
            )
            
            try:
                exp_config = self.config["evaluation"]["explainability"]["modules"]
                
                reports = await run_all(
                    gsm8k_path=str(Path(__file__).parent / "explainability" / "data" / "gsm8k.parquet"),
                    nq_path=str(Path(__file__).parent / "explainability" / "data" / "nq.parquet"),
                    cot_answer_llm=cot_answer_llm,
                    cite_answer_llm=cite_answer_llm,
                    cite_judge_llm=cite_judge_llm,
                    cot_sample_method="random",
                    cot_n_samples=exp_config["cot"]["sample_size"],
                    cot_random_state=50,
                    citation_sample_method="random",
                    citation_n_samples=exp_config["citation"]["sample_size"],
                    citation_random_state=50,
                )
                
                processor = ResultProcessor()
                success_records, failed_results, cot_scores, citation_scores = processor.process_reports(reports)
                
                aggregator = ScoreAggregator()
                task_scores = aggregator.aggregate_scores(
                    cot_scores=cot_scores,
                    citation_scores=citation_scores,
                )
                
                # Save detailed results
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_dir = Path(__file__).parent / "explainability" / "outputs"
                output_dir.mkdir(exist_ok=True)
                
                with open(output_dir / f'explainability_success_records_{self.config["model"]["name"]}_{timestamp}.json', 'w', encoding='utf-8') as f:
                    json.dump(success_records, f, ensure_ascii=False, indent=2)
                
                with open(output_dir / f'explainability_failed_records_{self.config["model"]["name"]}_{timestamp}.json', 'w', encoding='utf-8') as f:
                    json.dump(failed_results, f, ensure_ascii=False, indent=2)
                
                with open(output_dir / f'explainability_final_results_{self.config["model"]["name"]}_{timestamp}.json', 'w', encoding='utf-8') as f:
                    json.dump(task_scores, f, ensure_ascii=False, indent=2)
                
                print(f"Explainability evaluation completed")
                print(f"   Overall Score: {task_scores['XAI_overall_score']:.3f}")
                print(f"   Status: {'PASS' if task_scores['overall_pass'] else 'FAIL'}")
                
                return {
                    "status": "completed",
                    # "overall_score": task_scores["XAI_overall_score"],
                    "pass": task_scores["overall_pass"],
                    # "threshold": task_scores["overall_threshold"],
                    "cot": task_scores["cot"],
                    "citation": task_scores["citation"]
                }
                
            finally:
                await cite_judge_llm.aclose()
                await cot_answer_llm.aclose()
                await cite_answer_llm.aclose()
                
        except Exception as e:
            print(f"Error during Explainability evaluation: {e}")
            import traceback
            traceback.print_exc()
            return {"status": "error", "error": str(e)}
    
    def run_reliability(self) -> Dict[str, Any]:
        """Run reliability evaluations"""
        if not self.config["evaluation"]["reliability"]["enabled"]:
            print("⏭️  Skipping Reliability evaluation (disabled in config)")
            return {"status": "skipped"}
        
        print("\n" + "="*60)
        print("✅ Starting Reliability Evaluation")
        print("="*60)
        
        results = {}
        rel_config = self.config["evaluation"]["reliability"]["modules"]
        
        # Run C-Eval
        if rel_config["ceval"]["enabled"]:
            try:
                print("\n📚 Running C-Eval Assessment...")
                results["ceval"] = self._run_ceval()
            except Exception as e:
                print(f"❌ Error during C-Eval: {e}")
                import traceback
                traceback.print_exc()
                results["ceval"] = {"status": "error", "error": str(e)}
        
        # Run Consistency Check
        if rel_config["consistency"]["enabled"]:
            try:
                print("\n🔄 Running Consistency Assessment...")
                results["consistency"] = self._run_consistency()
            except Exception as e:
                print(f"❌ Error during Consistency check: {e}")
                import traceback
                traceback.print_exc()
                results["consistency"] = {"status": "error", "error": str(e)}
        
        # Calculate overall reliability score
        scores = []
        for module_name, module_result in results.items():
            if "score" in module_result:
                scores.append(module_result["score"])
        
        if scores:
            overall_score = sum(scores) / len(scores)
            threshold = self.config["evaluation"]["reliability"]["threshold"]
            results["overall_score"] = overall_score
            results["pass"] = overall_score >= threshold
            results["threshold"] = threshold
            results["status"] = "completed"
            
            print(f"\n✅ Reliability evaluation completed")
            print(f"   Overall Score: {overall_score:.3f}")
            print(f"   Status: {'PASS' if results['pass'] else 'FAIL'}")
        else:
            results["status"] = "no_valid_results"
        
        return results
    
    def _run_ceval(self) -> Dict[str, Any]:
        """Run C-Eval assessment"""
        import subprocess
        import json
        
        ceval_config = self.config["evaluation"]["reliability"]["modules"]["ceval"]
        ceval_dir = Path(__file__).parent / "reliability" / "ceval"
        
        # Update run_ceval.py config temporarily or call it with parameters
        # For now, we'll run it directly and parse output
        result = subprocess.run(
            [sys.executable, str(ceval_dir / "run_ceval.py")],
            cwd=str(ceval_dir),
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            raise RuntimeError(f"C-Eval failed: {result.stderr}")
        
        # Find the latest output file
        results_dir = ceval_dir / "results"
        if results_dir.exists():
            json_files = list(results_dir.glob("ceval_*.json"))
            if json_files:
                latest_file = max(json_files, key=lambda p: p.stat().st_mtime)
                with open(latest_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                accuracy = data["summary"]["overall_accuracy"] / 100.0
                return {
                    "status": "completed",
                    "score": accuracy,
                    "accuracy": accuracy,
                    "pass": accuracy >= ceval_config["threshold"],
                    "threshold": ceval_config["threshold"],
                    "details": data
                }
        
        return {"status": "no_output_found"}
    
    def _run_consistency(self) -> Dict[str, Any]:
        """Run consistency check"""
        import subprocess
        import json
        
        consistency_config = self.config["evaluation"]["reliability"]["modules"]["consistency"]
        consistency_dir = Path(__file__).parent / "reliability" / "consistency"
        
        result = subprocess.run(
            [sys.executable, str(consistency_dir / "main.py")],
            cwd=str(consistency_dir),
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            raise RuntimeError(f"Consistency check failed: {result.stderr}")
        
        # Find the latest output file
        output_dir = consistency_dir / "outputs"
        if output_dir.exists():
            json_files = list(output_dir.glob("consistency_*.json"))
            if json_files:
                latest_file = max(json_files, key=lambda p: p.stat().st_mtime)
                with open(latest_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                score = data["meta"]["overall_score"]
                return {
                    "status": "completed",
                    "score": score,
                    "pass": score >= consistency_config["threshold"],
                    "threshold": consistency_config["threshold"],
                    "details": data
                }
        
        return {"status": "no_output_found"}
    
    def run_safety(self) -> Dict[str, Any]:
        """Run safety evaluations"""
        if not self.config["evaluation"]["safety"]["enabled"]:
            print("⏭️  Skipping Safety evaluation (disabled in config)")
            return {"status": "skipped"}
        
        print("\n" + "="*60)
        print("🛡️  Starting Safety Evaluation")
        print("="*60)
        
        try:
            sys.path.insert(0, str(Path(__file__).parent / "safety"))
            from utils.ollama import OllamaLLM
            from utils.aoai import AOAILLM
            
            from BBQ.pipeline import runEvaluation as runBBQEvaluation
            from BIPIA.pipeline import runEvaluation as runBIPIAEvaluation
            from Toxicity.pipeline import runEvaluation as runToxicityEvaluation
            from Toxicity.customLLM import AzureOpenAI as ToxicityAzureOpenAI, OllamaDeepEval as ToxicityOllamaDeepEval
            from InformationDisclosure.pipeline import runEvaluation as runIDEvaluation
            from InformationDisclosure.customLLM import AzureOpenAI as IDAzureOpenAI, OllamaDeepEval as IDOllamaDeepEval
            from DirectPromptInjection.pipeline import runEvaluation as runDPIEvaluation
            from DirectPromptInjection.customLLM import AzureOpenAI as DPIAzureOpenAI, OllamaDeepEval as DPIOllamaDeepEval
            from Misinformation.pipeline import runEvaluation as runMisinformationEvaluation
            
            llm_config = self.config["llm_configs"]
            
            # Initialize LLMs
            ollama_llm = OllamaLLM(
                endpoint=llm_config["ollama"]["endpoint"],
                model=llm_config["ollama"]["model"]
            )
            
            aoai_llm = AOAILLM(
                endpoint=llm_config["azure_openai"]["endpoint"],
                api_key=llm_config["azure_openai"]["api_key"]
            )
            
            # Initialize DeepEval LLMs for Toxicity, Information Disclosure, and Direct Prompt Injection
            simulator_llm_ollama = ToxicityOllamaDeepEval(
                endpoint=llm_config["ollama"]["endpoint"],
                model=llm_config["ollama"]["model"]
            )
            
            evaluator_llm_azure = ToxicityAzureOpenAI(
                openai_api_version=llm_config["azure_openai"]["api_version"],
                azure_deployment=llm_config["azure_openai"]["model"],
                azure_endpoint=llm_config["azure_openai"]["endpoint"],
                openai_api_key=llm_config["azure_openai"]["api_key"]
            )
            
            results = {}
            safety_config = self.config["evaluation"]["safety"]["modules"]
            
            # Run BBQ
            if safety_config["bbq"]["enabled"]:
                try:
                    print("\n🔍 Running BBQ (Bias Benchmark) Assessment...")
                    runBBQEvaluation(
                        target_llm=ollama_llm,
                        sample_size=safety_config["bbq"]["sample_size"]
                    )
                    
                    # Load latest result
                    results_dir = Path(__file__).parent / "safety" / "results"
                    json_files = list(results_dir.glob("bbq_summary_*.json"))
                    if json_files:
                        latest_file = max(json_files, key=lambda p: p.stat().st_mtime)
                        with open(latest_file, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                        
                        accuracy = data["overall"]["accuracy"]
                        results["bbq"] = {
                            "status": "completed",
                            "score": accuracy,
                            "accuracy": accuracy,
                            "pass": accuracy >= safety_config["bbq"]["threshold"],
                            "threshold": safety_config["bbq"]["threshold"],
                            "details": data
                        }
                        print(f"✅ BBQ completed - Accuracy: {accuracy:.3f}")
                    
                except Exception as e:
                    print(f"❌ Error during BBQ: {e}")
                    results["bbq"] = {"status": "error", "error": str(e)}
            
            # Run BIPIA
            if safety_config["bipia"]["enabled"]:
                try:
                    print("\n🧩 Running BIPIA (Indirect Prompt Injection) Assessment...")
                    runBIPIAEvaluation(
                        target_llm=ollama_llm,
                        eval_llm=aoai_llm,
                        sample_size=safety_config["bipia"]["sample_size"]
                    )
                    
                    # Load latest result
                    results_dir = Path(__file__).parent / "safety" / "results"
                    json_files = list(results_dir.glob("bipia_summary_*.json"))
                    if json_files:
                        latest_file = max(json_files, key=lambda p: p.stat().st_mtime)
                        with open(latest_file, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                        
                        # Lower ASR (Attack Success Rate) is better
                        asr = data["overall"]["ASR"]
                        score = 1.0 - asr  
                        results["bipia"] = {
                            "status": "completed",
                            "score": score,
                            "asr": asr,
                            "pass": score >= safety_config["bipia"]["threshold"],
                            "threshold": safety_config["bipia"]["threshold"],
                            "details": data
                        }
                        print(f"✅ BIPIA completed - ASR: {asr:.3f}, Score: {score:.3f}")
                    
                except Exception as e:
                    print(f"Error during BIPIA: {e}")
                    results["bipia"] = {"status": "error", "error": str(e)}
            
            # Run Toxicity
            if safety_config.get("toxicity", {}).get("enabled"):
                try:
                    print("\nRunning Toxicity Assessment...")
                    runToxicityEvaluation(
                        target_llm=ollama_llm,
                        sample_size=safety_config["toxicity"]["sample_size"],
                        simulator_model=simulator_llm_ollama,
                        evaluation_model=evaluator_llm_azure
                    )
                    
                    # Load latest result
                    results_dir = Path(__file__).parent / "safety" / "results"
                    json_files = list(results_dir.glob("toxicity_summary_*.json"))
                    if json_files:
                        latest_file = max(json_files, key=lambda p: p.stat().st_mtime)
                        with open(latest_file, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                        
                        pass_rate = data.get("overall_pass_rate", 0)
                        results["toxicity"] = {
                            "status": "completed",
                            "score": pass_rate,
                            "pass_rate": pass_rate,
                            "pass": pass_rate >= safety_config["toxicity"]["threshold"],
                            "threshold": safety_config["toxicity"]["threshold"],
                            "details": data
                        }
                        print(f"✅ Toxicity completed - Pass Rate: {pass_rate:.3f}")
                    
                except Exception as e:
                    print(f"Error during Toxicity: {e}")
                    results["toxicity"] = {"status": "error", "error": str(e)}
            
            # Run Information Disclosure
            if safety_config.get("information_disclosure", {}).get("enabled"):
                try:
                    print("\nRunning Information Disclosure Assessment...")
                    runIDEvaluation(
                        target_llm=ollama_llm,
                        sample_size=safety_config["information_disclosure"]["sample_size"],
                        simulator_model=IDOllamaDeepEval(
                            endpoint=llm_config["ollama"]["endpoint"],
                            model=llm_config["ollama"]["model"]
                        ),
                        evaluation_model=IDAzureOpenAI(
                            openai_api_version=llm_config["azure_openai"]["api_version"],
                            azure_deployment=llm_config["azure_openai"]["model"],
                            azure_endpoint=llm_config["azure_openai"]["endpoint"],
                            openai_api_key=llm_config["azure_openai"]["api_key"]
                        )
                    )
                    
                    # Load latest result
                    results_dir = Path(__file__).parent / "safety" / "results"
                    json_files = list(results_dir.glob("information_disclosure_summary_*.json"))
                    if json_files:
                        latest_file = max(json_files, key=lambda p: p.stat().st_mtime)
                        with open(latest_file, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                        
                        pass_rate = data.get("overall_pass_rate", 0)
                        results["information_disclosure"] = {
                            "status": "completed",
                            "score": pass_rate,
                            "pass_rate": pass_rate,
                            "pass": pass_rate >= safety_config["information_disclosure"]["threshold"],
                            "threshold": safety_config["information_disclosure"]["threshold"],
                            "details": data
                        }
                        print(f"✅ Information Disclosure completed - Pass Rate: {pass_rate:.3f}")
                    
                except Exception as e:
                    print(f"Error during Information Disclosure: {e}")
                    results["information_disclosure"] = {"status": "error", "error": str(e)}
            
            # Run Direct Prompt Injection
            if safety_config.get("direct_prompt_injection", {}).get("enabled"):
                try:
                    print("\nRunning Direct Prompt Injection Assessment...")
                    runDPIEvaluation(
                        target_llm=ollama_llm,
                        sample_size=safety_config["direct_prompt_injection"]["sample_size"],
                        simulator_model=DPIOllamaDeepEval(
                            endpoint=llm_config["ollama"]["endpoint"],
                            model=llm_config["ollama"]["model"]
                        ),
                        evaluation_model=DPIAzureOpenAI(
                            openai_api_version=llm_config["azure_openai"]["api_version"],
                            azure_deployment=llm_config["azure_openai"]["model"],
                            azure_endpoint=llm_config["azure_openai"]["endpoint"],
                            openai_api_key=llm_config["azure_openai"]["api_key"]
                        )
                    )
                    
                    # Load latest result
                    results_dir = Path(__file__).parent / "safety" / "results"
                    json_files = list(results_dir.glob("directpromptinjection_summary_*.json"))
                    if json_files:
                        latest_file = max(json_files, key=lambda p: p.stat().st_mtime)
                        with open(latest_file, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                        
                        pass_rate = data.get("overall_pass_rate", 0)
                        results["direct_prompt_injection"] = {
                            "status": "completed",
                            "score": pass_rate,
                            "pass_rate": pass_rate,
                            "pass": pass_rate >= safety_config["direct_prompt_injection"]["threshold"],
                            "threshold": safety_config["direct_prompt_injection"]["threshold"],
                            "details": data
                        }
                        print(f"Direct Prompt Injection completed - Pass Rate: {pass_rate:.3f}")
                    
                except Exception as e:
                    print(f"Error during Direct Prompt Injection: {e}")
                    results["direct_prompt_injection"] = {"status": "error", "error": str(e)}
            
            # Run Misinformation
            if safety_config.get("misinformation", {}).get("enabled"):
                try:
                    print("\nRunning Misinformation Assessment...")
                    runMisinformationEvaluation(
                        target_llm=ollama_llm,
                        simulator_model=simulator_llm_ollama,
                        evaluation_model=evaluator_llm_azure,
                        sample_size=safety_config["misinformation"]["sample_size"]
                    )
                    
                    # Load latest result
                    results_dir = Path(__file__).parent / "safety" / "results"
                    json_files = list(results_dir.glob("misinformation_summary_*.json"))
                    if json_files:
                        latest_file = max(json_files, key=lambda p: p.stat().st_mtime)
                        with open(latest_file, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                        
                        pass_rate = data.get("overall_pass_rate", data.get("pass_rate", 0))
                        results["misinformation"] = {
                            "status": "completed",
                            "score": pass_rate,
                            "pass_rate": pass_rate,
                            "pass": pass_rate >= safety_config["misinformation"]["threshold"],
                            "threshold": safety_config["misinformation"]["threshold"],
                            "details": data
                        }
                        print(f"Misinformation completed - Pass Rate: {pass_rate:.3f}")
                    
                except Exception as e:
                    print(f"Error during Misinformation: {e}")
                    results["misinformation"] = {"status": "error", "error": str(e)}
            
            # Calculate overall safety score
            scores = []
            for module_name, module_result in results.items():
                if "score" in module_result:
                    scores.append(module_result["score"])
            
            if scores:
                overall_score = sum(scores) / len(scores)
                threshold = self.config["evaluation"]["safety"]["threshold"]
                results["overall_score"] = overall_score
                results["pass"] = overall_score >= threshold
                results["threshold"] = threshold
                results["status"] = "completed"
                
                print(f"\nSafety evaluation completed")
                print(f"   Overall Score: {overall_score:.3f}")
                print(f"   Status: {'PASS' if results['pass'] else 'FAIL'}")
            else:
                results["status"] = "no_valid_results"
            
            return results
            
        except Exception as e:
            print(f"Error during Safety evaluation: {e}")
            import traceback
            traceback.print_exc()
            return {"status": "error", "error": str(e)}
    
    async def run_all(self):
        """Run all evaluations"""
        print("\n" + "="*60)
        print("Starting Integrated LLM Assessment")
        print("="*60)
        print(f"Model: {self.config['model']['name']} ({self.config['model']['type']})")
        print(f"Timestamp: {self.results['metadata']['timestamp']}")
        
        # Run evaluations
        self.results["explainability"] = await self.run_explainability()
        self.results["reliability"] = self.run_reliability()
        self.results["safety"] = self.run_safety()
        
        # Calculate overall score
        self._calculate_overall_score()
        
        # Save results
        self._save_results()
        
        # Generate report
        if self.config["output"]["generate_html_report"]:
            self._generate_html_report()
        
        # Print summary
        self._print_summary()
    
    def _calculate_overall_score(self):
        """Calculate weighted overall score"""
        eval_config = self.config["evaluation"]
        
        scores = []
        weights = []
        
        # Explainability
        if self.results["explainability"].get("status") == "completed":
            scores.append(self.results["explainability"]["overall_score"])
            weights.append(eval_config["explainability"]["weight"])
        
        # Reliability
        if self.results["reliability"].get("status") == "completed":
            scores.append(self.results["reliability"]["overall_score"])
            weights.append(eval_config["reliability"]["weight"])
        
        # Safety
        if self.results["safety"].get("status") == "completed":
            scores.append(self.results["safety"]["overall_score"])
            weights.append(eval_config["safety"]["weight"])
        
        if scores and weights:
            # Normalize weights
            total_weight = sum(weights)
            normalized_weights = [w / total_weight for w in weights]
            
            # Calculate weighted score
            overall_score = sum(s * w for s, w in zip(scores, normalized_weights))
            
            self.results["overall"] = {
                "score": overall_score,
                "pass": (
                    self.results["explainability"].get("pass", True) and
                    self.results["reliability"].get("pass", True) and
                    self.results["safety"].get("pass", True)
                ),
                "components": {
                    "explainability": {
                        "score": self.results["explainability"].get("overall_score"),
                        "weight": normalized_weights[0] if len(normalized_weights) > 0 else 0
                    } if self.results["explainability"].get("status") == "completed" else None,
                    "reliability": {
                        "score": self.results["reliability"].get("overall_score"),
                        "weight": normalized_weights[1] if len(normalized_weights) > 1 else 0
                    } if self.results["reliability"].get("status") == "completed" else None,
                    "safety": {
                        "score": self.results["safety"].get("overall_score"),
                        "weight": normalized_weights[2] if len(normalized_weights) > 2 else 0
                    } if self.results["safety"].get("status") == "completed" else None,
                }
            }
    
    def _save_results(self):
        """Save results to JSON file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        model_name = self.config["model"]["name"].replace(":", "_").replace("/", "_")
        output_file = self.output_dir / f"assessment_results_{model_name}_{timestamp}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)
        
        print(f"\n📄 Results saved to: {output_file}")
    
    # def _generate_html_report(self):
    #     """Generate HTML report"""
    #     try:
    #         from report_generator import HTMLReportGenerator
            
    #         generator = HTMLReportGenerator(self.results, self.config)
    #         timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    #         model_name = self.config["model"]["name"].replace(":", "_").replace("/", "_")
    #         report_file = self.output_dir / f"assessment_report_{model_name}_{timestamp}.html"
            
    #         generator.generate(report_file)
    #         print(f"📊 HTML report generated: {report_file}")
    #     except ImportError:
    #         print("⚠️  HTML report generator not available")
    #     except Exception as e:
    #         print(f"⚠️  Error generating HTML report: {e}")
    
    def _print_summary(self):
        """Print evaluation summary"""
        print("\n" + "="*60)
        print("📊 EVALUATION SUMMARY")
        print("="*60)
        
        # Explainability
        if self.results["explainability"].get("status") == "completed":
            exp = self.results["explainability"]
            print(f"\n🔍 Explainability: {exp['overall_score']:.3f} {'✅ PASS' if exp['pass'] else '❌ FAIL'}")
            if "cot" in exp:
                print(f"   - CoT (Chain of Thought): {exp['cot']['avg_score']:.3f} {'✅' if exp['cot']['pass'] else '❌'}")
            if "citation" in exp:
                print(f"   - Citation: {exp['citation']['avg_score']:.3f} {'✅' if exp['citation']['pass'] else '❌'}")
        
        # Reliability
        if self.results["reliability"].get("status") == "completed":
            rel = self.results["reliability"]
            print(f"\n✅ Reliability: {rel['overall_score']:.3f} {'✅ PASS' if rel['pass'] else '❌ FAIL'}")
            if "ceval" in rel and rel["ceval"].get("status") == "completed":
                print(f"   - C-Eval: {rel['ceval']['accuracy']:.3f} {'✅' if rel['ceval']['pass'] else '❌'}")
            if "consistency" in rel and rel["consistency"].get("status") == "completed":
                print(f"   - Consistency: {rel['consistency']['score']:.3f} {'✅' if rel['consistency']['pass'] else '❌'}")
        
        # Safety
        if self.results["safety"].get("status") == "completed":
            safe = self.results["safety"]
            print(f"\nSafety: {safe['overall_score']:.3f} {'✅ PASS' if safe['pass'] else 'FAIL'}")
            
            # Module name mapping for better display
            module_display_names = {
                'bbq': 'BBQ (Bias)',
                'bipia': 'BIPIA (Prompt Injection)',
                'toxicity': 'Toxicity',
                'information_disclosure': 'Information Disclosure',
                'direct_prompt_injection': 'Direct Prompt Injection',
                'misinformation': 'Misinformation'
            }
            
            # Dynamically print all safety modules
            for module_name, module_data in safe.items():
                # Skip meta fields
                if module_name in ['status', 'overall_score', 'pass', 'threshold']:
                    continue
                
                if isinstance(module_data, dict) and module_data.get("status") == "completed":
                    display_name = module_display_names.get(module_name, module_name.replace('_', ' ').title())
                    score = module_data.get('score', module_data.get('accuracy', 0))
                    is_pass = module_data.get('pass', False)
                    print(f"   - {display_name}: {score:.3f} {'✅' if is_pass else '❌'}")
        
        # Overall
        if "score" in self.results["overall"]:
            print(f"\n{'='*60}")
            print(f"OVERALL SCORE: {self.results['overall']['score']:.3f}")
            print(f"STATUS: {'✅ PASS' if self.results['overall']['pass'] else '❌ FAIL'}")
            print(f"{'='*60}\n")


async def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Integrated LLM Assessment Framework")
    parser.add_argument(
        "--config",
        type=str,
        default="config.json",
        help="Path to configuration file (default: config.json)"
    )
    
    args = parser.parse_args()
    
    try:
        assessment = IntegratedAssessment(config_path=args.config)
        await assessment.run_all()
    except KeyboardInterrupt:
        print("\n\nAssessment interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nFatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
