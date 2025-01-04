from typing import Dict, Any
from datetime import datetime

class TokenTracker:
    def __init__(self):
        self.stats = {
            "summary": {
                "total_prompts": 0,
                "total_input_tokens": 0,
                "total_output_tokens": 0,
                "total_tokens": 0,
                "average_tokens_per_prompt": 0
            },
            "detailed_history": []
        }
    
    def track_usage(self, response: Dict[str, Any]) -> None:
        """Track token usage from a response."""
        try:
            metadata = response.get("metadata", {})
            token_count = metadata.get("token_count", 0)
            
            # Update summary stats
            self.stats["summary"]["total_prompts"] += 1
            self.stats["summary"]["total_tokens"] += token_count
            
            # Calculate average
            if self.stats["summary"]["total_prompts"] > 0:
                self.stats["summary"]["average_tokens_per_prompt"] = (
                    self.stats["summary"]["total_tokens"] /
                    self.stats["summary"]["total_prompts"]
                )
            
            # Add to detailed history
            self.stats["detailed_history"].append({
                "timestamp": datetime.now().isoformat(),
                "token_count": token_count,
                "response_time": metadata.get("response_time", 0)
            })
            
        except Exception as e:
            print(f"Error tracking tokens: {e}")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get current token usage statistics."""
        return self.stats
    
    def generate_report(self) -> str:
        """Generate a formatted usage report."""
        summary = self.stats["summary"]
        
        report = f"""
        TOKEN USAGE REPORT
        =================
        Total Prompts: {summary['total_prompts']}
        Total Tokens: {summary['total_tokens']:,}
        Average Tokens/Prompt: {summary['average_tokens_per_prompt']:.2f}
        
        Detailed History:
        """
        
        for entry in self.stats["detailed_history"][-5:]:  # Last 5 entries
            report += f"\n{entry['timestamp']}: {entry['token_count']:,} tokens"
        
        return report
