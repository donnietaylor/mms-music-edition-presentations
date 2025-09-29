#!/usr/bin/env python3
"""
Prompt Manager for AI Agents
Demonstrates how to manage and use custom prompts for different use cases.
"""

import yaml
import json
from typing import Dict, Any, Optional
from pathlib import Path

class PromptManager:
    """Manages custom prompts for AI agents with variable substitution and validation."""
    
    def __init__(self, prompts_dir: str = "."):
        self.prompts_dir = Path(prompts_dir)
        self.loaded_prompts = {}
        self._load_all_prompts()
    
    def _load_all_prompts(self) -> None:
        """Load all YAML prompt files from the prompts directory."""
        for yaml_file in self.prompts_dir.glob("*.yaml"):
            try:
                with open(yaml_file, 'r', encoding='utf-8') as f:
                    prompts = yaml.safe_load(f)
                    file_key = yaml_file.stem
                    self.loaded_prompts[file_key] = prompts
                    print(f"✅ Loaded prompts from {yaml_file.name}")
            except Exception as e:
                print(f"❌ Error loading {yaml_file.name}: {e}")
    
    def get_prompt(self, category: str, prompt_type: str, **kwargs) -> str:
        """
        Get a formatted prompt with variable substitution.
        
        Args:
            category: The prompt category (e.g., 'email-response-prompts')
            prompt_type: The specific prompt (e.g., 'auto_reply')
            **kwargs: Variables to substitute in the prompt
            
        Returns:
            Formatted prompt string
        """
        if category not in self.loaded_prompts:
            raise ValueError(f"Category '{category}' not found in loaded prompts")
        
        if prompt_type not in self.loaded_prompts[category]:
            raise ValueError(f"Prompt type '{prompt_type}' not found in category '{category}'")
        
        prompt_data = self.loaded_prompts[category][prompt_type]
        prompt_template = prompt_data.get('prompt', '')
        
        try:
            # Substitute variables in the prompt
            formatted_prompt = prompt_template.format(**kwargs)
            return formatted_prompt
        except KeyError as e:
            missing_var = str(e).strip("'")
            raise ValueError(f"Missing required variable: {missing_var}")
    
    def get_examples(self, category: str, prompt_type: str) -> list:
        """Get examples for a specific prompt type."""
        if category not in self.loaded_prompts:
            return []
        
        prompt_data = self.loaded_prompts[category].get(prompt_type, {})
        return prompt_data.get('examples', [])
    
    def list_categories(self) -> list:
        """List all available prompt categories."""
        return list(self.loaded_prompts.keys())
    
    def list_prompt_types(self, category: str) -> list:
        """List all prompt types in a category."""
        if category not in self.loaded_prompts:
            return []
        return list(self.loaded_prompts[category].keys())
    
    def validate_prompt_variables(self, category: str, prompt_type: str, variables: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate that all required variables are provided for a prompt.
        
        Returns:
            Dictionary with validation results
        """
        try:
            prompt = self.get_prompt(category, prompt_type, **variables)
            return {
                'valid': True,
                'message': 'All required variables provided',
                'prompt_length': len(prompt)
            }
        except ValueError as e:
            return {
                'valid': False,
                'message': str(e),
                'prompt_length': 0
            }

# Example usage functions
def demonstrate_email_automation():
    """Demonstrate email automation prompts."""
    print("\n🔔 Email Automation Example")
    print("=" * 50)
    
    prompt_manager = PromptManager()
    
    # Example email classification
    email_content = "URGENT: The production server is experiencing high CPU usage and response times are slow."
    
    try:
        classification_prompt = prompt_manager.get_prompt(
            'email-response-prompts',
            'email_classification',
            email_content=email_content
        )
        print("Classification Prompt:")
        print(classification_prompt)
        print()
        
        # Example auto-reply
        auto_reply_prompt = prompt_manager.get_prompt(
            'email-response-prompts',
            'auto_reply',
            original_email=email_content,
            email_category="URGENT",
            sender_info="John Doe, DevOps Engineer",
            user_role="System Administrator",
            company_guidelines="All production issues require immediate escalation to management"
        )
        print("Auto-Reply Prompt:")
        print(auto_reply_prompt)
        
    except ValueError as e:
        print(f"Error: {e}")

def demonstrate_prompt_validation():
    """Demonstrate prompt validation features."""
    print("\n🔍 Prompt Validation Example")
    print("=" * 50)
    
    prompt_manager = PromptManager()
    
    # Test with complete variables
    complete_vars = {
        'original_email': 'Test email content',
        'email_category': 'IMPORTANT',
        'sender_info': 'Jane Smith, Marketing',
        'user_role': 'Customer Support',
        'company_guidelines': 'Respond within 24 hours'
    }
    
    validation_result = prompt_manager.validate_prompt_variables(
        'email-response-prompts',
        'auto_reply',
        complete_vars
    )
    
    print(f"Complete variables validation: {validation_result}")
    
    # Test with missing variables
    incomplete_vars = {
        'original_email': 'Test email content',
        'email_category': 'IMPORTANT'
        # Missing: sender_info, user_role, company_guidelines
    }
    
    validation_result = prompt_manager.validate_prompt_variables(
        'email-response-prompts',
        'auto_reply',
        incomplete_vars
    )
    
    print(f"Incomplete variables validation: {validation_result}")

def list_available_prompts():
    """List all available prompts and their structure."""
    print("\n📋 Available Prompts")
    print("=" * 50)
    
    prompt_manager = PromptManager()
    
    categories = prompt_manager.list_categories()
    print(f"Found {len(categories)} prompt categories:")
    
    for category in categories:
        print(f"\n📁 {category}")
        prompt_types = prompt_manager.list_prompt_types(category)
        
        for prompt_type in prompt_types:
            examples = prompt_manager.get_examples(category, prompt_type)
            example_count = len(examples)
            print(f"  • {prompt_type} ({example_count} examples)")

def generate_sample_responses():
    """Generate sample responses using the prompt manager."""
    print("\n🤖 Sample AI Responses")
    print("=" * 50)
    
    prompt_manager = PromptManager()
    
    # Sample scenarios
    scenarios = [
        {
            'name': 'Bug Report Email',
            'email': 'Hi, I found a bug in the login system. Users cannot reset their passwords.',
            'category': 'IMPORTANT',
            'sender': 'Alice Johnson, QA Tester',
            'guidelines': 'All bug reports require developer assignment within 4 hours'
        },
        {
            'name': 'Feature Request',
            'email': 'Can we add dark mode to the application? Many users have requested this.',
            'category': 'ROUTINE',
            'sender': 'Bob Wilson, Product Manager',
            'guidelines': 'Feature requests go through product review process'
        }
    ]
    
    for scenario in scenarios:
        print(f"\n🎯 Scenario: {scenario['name']}")
        print("-" * 30)
        
        try:
            response_prompt = prompt_manager.get_prompt(
                'email-response-prompts',
                'auto_reply',
                original_email=scenario['email'],
                email_category=scenario['category'],
                sender_info=scenario['sender'],
                user_role='Technical Lead',
                company_guidelines=scenario['guidelines']
            )
            
            print("Generated Response Prompt:")
            print(response_prompt[:300] + "..." if len(response_prompt) > 300 else response_prompt)
            
        except Exception as e:
            print(f"Error generating response: {e}")

if __name__ == "__main__":
    print("🚀 AI Prompt Manager Demo")
    print("=" * 50)
    
    # Run all demonstrations
    list_available_prompts()
    demonstrate_email_automation()
    demonstrate_prompt_validation()
    generate_sample_responses()
    
    print("\n✅ Demo completed!")
    print("\nNext steps:")
    print("1. Customize the YAML prompt files for your specific use cases")
    print("2. Add more prompt categories (code-review, documentation, etc.)")
    print("3. Integrate with your AI agent or automation workflow")
    print("4. Monitor and optimize prompt performance based on results")