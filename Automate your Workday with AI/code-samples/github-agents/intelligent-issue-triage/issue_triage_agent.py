#!/usr/bin/env python3
"""
Intelligent Issue Triage Agent
Demonstrates smart classification, prioritization, and routing
"""

import os
import re
import json
import yaml
import asyncio
import time
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
import openai
from github import Github
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

@dataclass
class IssueClassification:
    labels: List[str]
    severity: str
    priority_score: int
    component: str
    team: str
    intent: str
    confidence: float
    is_duplicate: bool
    duplicate_of: Optional[int] = None

class IssueTriage:
    def __init__(self):
        self.github = Github(os.getenv('GITHUB_TOKEN'))
        self.openai_client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        # Load configurations
        self.load_configurations()
        
        # Initialize components
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        self.issue_cache = {}  # Cache for recent issues
        
        # Performance metrics
        self.metrics = {
            'start_time': time.time(),
            'issues_processed': 0,
            'classifications_made': 0,
            'duplicates_found': 0,
            'auto_responses_sent': 0
        }
    
    def load_configurations(self):
        """Load classification rules and settings"""
        try:
            with open('classification-rules.yaml', 'r') as f:
                self.rules = yaml.safe_load(f)
            print("✅ Classification rules loaded")
        except FileNotFoundError:
            print("⚠️ Using default classification rules")
            self._load_default_rules()
    
    def _load_default_rules(self):
        """Load minimal default rules"""
        self.rules = {
            'classification_rules': {
                'labels': {
                    'bug': {'keywords': ['error', 'bug', 'issue'], 'weight': 0.8},
                    'feature': {'keywords': ['feature', 'enhancement'], 'weight': 0.7}
                },
                'severity': {
                    'high': {'keywords': ['urgent', 'critical'], 'score': 8},
                    'medium': {'keywords': ['important'], 'score': 5},
                    'low': {'keywords': ['minor'], 'score': 2}
                }
            }
        }
    
    async def classify_issue(self, issue_data: Dict) -> IssueClassification:
        """Classify issue using multiple approaches"""
        title = issue_data.get('title', '').lower()
        body = issue_data.get('body', '').lower()
        text = f"{title} {body}"
        
        print(f"🔍 Classifying issue: {issue_data.get('title', 'Untitled')[:50]}...")
        
        # 1. Rule-based classification
        rule_based_result = self._classify_rule_based(text)
        
        # 2. AI-powered classification for complex cases
        ai_result = await self._classify_with_ai(issue_data)
        
        # 3. Combine results with confidence weighting
        classification = self._combine_classifications(rule_based_result, ai_result)
        
        # 4. Check for duplicates
        classification.is_duplicate, classification.duplicate_of = await self._check_duplicates(issue_data)
        
        self.metrics['classifications_made'] += 1
        return classification
    
    def _classify_rule_based(self, text: str) -> Dict:
        """Fast rule-based classification using keyword matching"""
        rules = self.rules.get('classification_rules', {})
        
        # Label classification
        labels = []
        label_scores = {}
        
        for label, config in rules.get('labels', {}).items():
            score = 0
            keywords = config.get('keywords', [])
            patterns = config.get('patterns', [])
            weight = config.get('weight', 0.5)
            
            # Keyword matching
            for keyword in keywords:
                if keyword in text:
                    score += 1
            
            # Pattern matching
            for pattern in patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    score += 2
            
            if score > 0:
                final_score = score * weight
                label_scores[label] = final_score
                if final_score > 0.5:
                    labels.append(label)
        
        # Severity classification
        severity = 'medium'
        severity_score = 0
        
        for sev_level, config in rules.get('severity', {}).items():
            score = 0
            for keyword in config.get('keywords', []):
                if keyword in text:
                    score += 1
            
            if score > severity_score:
                severity_score = score
                severity = sev_level
        
        # Component identification
        component = 'general'
        team = 'general-team'
        
        for comp, config in rules.get('components', {}).items():
            score = 0
            for keyword in config.get('keywords', []):
                if keyword in text:
                    score += 1
            
            if score > 0:
                component = comp
                team = config.get('team', 'general-team')
                break
        
        return {
            'labels': labels,
            'severity': severity,
            'component': component,
            'team': team,
            'confidence': min(max(sum(label_scores.values()) / len(label_scores) if label_scores else 0, 0), 1),
            'label_scores': label_scores
        }
    
    async def _classify_with_ai(self, issue_data: Dict) -> Dict:
        """AI-powered classification for complex issues"""
        try:
            prompt = f"""
Analyze this GitHub issue and provide classification:

Title: {issue_data.get('title', '')}
Body: {issue_data.get('body', '')[:1000]}...

Classify this issue and respond with JSON:
{{
    "labels": ["bug", "feature", "question", "security", "performance", "ui_ux"],
    "severity": "critical|high|medium|low",
    "component": "frontend|backend|mobile|infrastructure|security",
    "intent": "bug_report|feature_request|question|documentation",
    "confidence": 0.95,
    "reasoning": "Brief explanation"
}}
"""
            
            response = await asyncio.to_thread(
                self.openai_client.chat.completions.create,
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
                temperature=0.1
            )
            
            # Parse AI response
            ai_response = response.choices[0].message.content
            try:
                ai_classification = json.loads(ai_response)
                return ai_classification
            except json.JSONDecodeError:
                print("⚠️ AI response not valid JSON, using rule-based only")
                return {}
                
        except Exception as e:
            print(f"⚠️ AI classification failed: {e}")
            return {}
    
    def _combine_classifications(self, rule_based: Dict, ai_based: Dict) -> IssueClassification:
        """Combine rule-based and AI classifications with confidence weighting"""
        
        # Combine labels (prefer rule-based for high confidence)
        labels = list(set(rule_based.get('labels', []) + ai_based.get('labels', [])))
        
        # Choose severity (AI for complex cases, rules for clear patterns)
        severity = rule_based.get('severity', 'medium')
        if ai_based.get('confidence', 0) > 0.8:
            severity = ai_based.get('severity', severity)
        
        # Calculate priority score
        severity_scores = {'critical': 10, 'high': 8, 'medium': 5, 'low': 2}
        base_score = severity_scores.get(severity, 5)
        
        # Apply boosts
        priority_score = base_score
        if 'security' in labels:
            priority_score += 3
        if 'critical' in labels or severity == 'critical':
            priority_score += 2
        
        priority_score = min(priority_score, 10)  # Cap at 10
        
        # Determine team assignment
        component = rule_based.get('component', ai_based.get('component', 'general'))
        team = rule_based.get('team', f"{component}-team")
        
        # Calculate overall confidence
        rule_confidence = rule_based.get('confidence', 0.5)
        ai_confidence = ai_based.get('confidence', 0.5)
        combined_confidence = (rule_confidence + ai_confidence) / 2
        
        return IssueClassification(
            labels=labels,
            severity=severity,
            priority_score=priority_score,
            component=component,
            team=team,
            intent=ai_based.get('intent', 'unknown'),
            confidence=combined_confidence,
            is_duplicate=False
        )
    
    async def _check_duplicates(self, issue_data: Dict) -> Tuple[bool, Optional[int]]:
        """Check if issue is duplicate using similarity analysis"""
        if not self.rules.get('duplicate_detection', {}).get('enabled', False):
            return False, None
        
        try:
            repo = self.github.get_repo(os.getenv('GITHUB_REPOSITORY'))
            current_title = issue_data.get('title', '')
            current_body = issue_data.get('body', '')
            
            # Get recent issues for comparison
            threshold = self.rules.get('duplicate_detection', {}).get('similarity_threshold', 0.85)
            lookback_days = self.rules.get('duplicate_detection', {}).get('lookback_days', 90)
            since_date = datetime.now() - timedelta(days=lookback_days)
            
            recent_issues = repo.get_issues(state='all', since=since_date)
            
            # Prepare text for similarity comparison
            current_text = f"{current_title} {current_body}"
            issue_texts = [current_text]
            issue_numbers = [None]  # Current issue has no number yet
            
            for issue in list(recent_issues)[:50]:  # Limit to 50 recent issues
                if issue.number != issue_data.get('number'):
                    issue_text = f"{issue.title} {issue.body or ''}"
                    issue_texts.append(issue_text)
                    issue_numbers.append(issue.number)
            
            if len(issue_texts) < 2:
                return False, None
            
            # Calculate similarity using TF-IDF
            tfidf_matrix = self.vectorizer.fit_transform(issue_texts)
            similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
            
            # Find most similar issue
            max_similarity = np.max(similarities)
            if max_similarity >= threshold:
                most_similar_idx = np.argmax(similarities) + 1
                duplicate_number = issue_numbers[most_similar_idx]
                print(f"🔍 Found potential duplicate: #{duplicate_number} (similarity: {max_similarity:.2f})")
                self.metrics['duplicates_found'] += 1
                return True, duplicate_number
            
        except Exception as e:
            print(f"⚠️ Duplicate detection failed: {e}")
        
        return False, None
    
    async def apply_classification(self, issue_number: int, classification: IssueClassification):
        """Apply classification results to the GitHub issue"""
        try:
            repo = self.github.get_repo(os.getenv('GITHUB_REPOSITORY'))
            issue = repo.get_issue(issue_number)
            
            print(f"🏷️ Applying classification to issue #{issue_number}")
            
            # Add labels
            current_labels = [label.name for label in issue.labels]
            new_labels = list(set(current_labels + classification.labels))
            
            if new_labels != current_labels:
                issue.edit(labels=new_labels)
                print(f"   Added labels: {classification.labels}")
            
            # Add assignees based on team
            if classification.team and classification.team != 'general-team':
                # This would typically lookup team members from configuration
                print(f"   Suggested team: {classification.team}")
            
            # Set priority label
            priority_labels = [f"priority-{classification.severity}", f"score-{classification.priority_score}"]
            issue.edit(labels=new_labels + priority_labels)
            
            # Add classification comment
            await self._add_classification_comment(issue, classification)
            
            # Handle duplicates
            if classification.is_duplicate and classification.duplicate_of:
                await self._handle_duplicate(issue, classification.duplicate_of)
            
            # Send auto-responses if needed
            await self._send_auto_response(issue, classification)
            
        except Exception as e:
            print(f"❌ Failed to apply classification: {e}")
    
    async def _add_classification_comment(self, issue, classification: IssueClassification):
        """Add classification summary comment"""
        confidence_emoji = "🎯" if classification.confidence > 0.8 else "🤔" if classification.confidence > 0.5 else "❓"
        
        comment = f"""## {confidence_emoji} Issue Triage Summary

**Classification**: {', '.join(classification.labels)}
**Severity**: {classification.severity.upper()}
**Priority Score**: {classification.priority_score}/10
**Component**: {classification.component}
**Team**: {classification.team}
**Confidence**: {classification.confidence:.0%}

**Next Steps**:
- Assigned to {classification.team}
- SLA: {self._get_sla_hours(classification.severity)} hours
- Priority: {self._get_priority_description(classification.priority_score)}

*Automated triage by AI Issue Triage Agent*
"""
        
        issue.create_comment(comment)
        print("   📝 Added classification comment")
    
    async def _handle_duplicate(self, issue, duplicate_of: int):
        """Handle duplicate issue"""
        comment = f"""## 🔍 Potential Duplicate Detected

This issue appears to be similar to #{duplicate_of}.

Please review and close as duplicate if confirmed, or provide additional context if this is a unique issue.

*Duplicate detection by AI Issue Triage Agent*
"""
        issue.create_comment(comment)
        issue.edit(labels=list(issue.labels) + ['duplicate'])
        print(f"   🔍 Marked as potential duplicate of #{duplicate_of}")
    
    async def _send_auto_response(self, issue, classification: IssueClassification):
        """Send automatic response based on classification"""
        auto_responses = self.rules.get('auto_responses', {})
        
        for response_key, config in auto_responses.items():
            condition = config.get('condition', '')
            
            # Simple condition checking (would be more sophisticated in production)
            should_respond = False
            
            if 'label:bug' in condition and 'bug' in classification.labels:
                if 'missing_reproduction_steps' in condition:
                    # Check if issue lacks reproduction steps
                    body = issue.body or ''
                    if 'steps to reproduce' not in body.lower() and 'reproduce' not in body.lower():
                        should_respond = True
            
            elif 'label:security' in condition and 'security' in classification.labels:
                should_respond = True
            
            if should_respond:
                template = config.get('template', '')
                issue.create_comment(template)
                print(f"   📧 Sent auto-response: {response_key}")
                self.metrics['auto_responses_sent'] += 1
                break
    
    def _get_sla_hours(self, severity: str) -> int:
        """Get SLA hours for severity level"""
        sla_map = {'critical': 2, 'high': 8, 'medium': 24, 'low': 72}
        return sla_map.get(severity, 24)
    
    def _get_priority_description(self, score: int) -> str:
        """Get priority description from score"""
        if score >= 9:
            return "URGENT - Immediate attention required"
        elif score >= 7:
            return "HIGH - Should be addressed today"
        elif score >= 5:
            return "MEDIUM - Address within SLA"
        else:
            return "LOW - Can be scheduled"
    
    async def process_issue(self, issue_number: int):
        """Process a single issue through the triage pipeline"""
        try:
            repo = self.github.get_repo(os.getenv('GITHUB_REPOSITORY'))
            issue = repo.get_issue(issue_number)
            
            issue_data = {
                'number': issue.number,
                'title': issue.title,
                'body': issue.body,
                'labels': [label.name for label in issue.labels],
                'created_at': issue.created_at,
                'user': issue.user.login
            }
            
            print(f"🎯 Processing issue #{issue_number}: {issue.title[:50]}...")
            
            # Classify the issue
            classification = await self.classify_issue(issue_data)
            
            # Apply classification
            await self.apply_classification(issue_number, classification)
            
            self.metrics['issues_processed'] += 1
            
            return classification
            
        except Exception as e:
            print(f"❌ Error processing issue #{issue_number}: {e}")
            return None
    
    def print_metrics(self):
        """Print performance metrics"""
        total_time = time.time() - self.metrics['start_time']
        print("\n📊 Triage Performance Metrics:")
        print(f"   Total Time: {total_time:.1f}s")
        print(f"   Issues Processed: {self.metrics['issues_processed']}")
        print(f"   Classifications Made: {self.metrics['classifications_made']}")
        print(f"   Duplicates Found: {self.metrics['duplicates_found']}")
        print(f"   Auto-responses Sent: {self.metrics['auto_responses_sent']}")
        if self.metrics['issues_processed'] > 0:
            print(f"   Avg Time/Issue: {total_time/self.metrics['issues_processed']:.1f}s")

async def main():
    """Main execution function"""
    issue_number = int(os.getenv('ISSUE_NUMBER', '1'))
    
    triage = IssueTriage()
    classification = await triage.process_issue(issue_number)
    
    if classification:
        print(f"\n✅ Issue #{issue_number} triaged successfully")
        print(f"   Labels: {classification.labels}")
        print(f"   Severity: {classification.severity}")
        print(f"   Team: {classification.team}")
        print(f"   Confidence: {classification.confidence:.0%}")
    
    triage.print_metrics()

if __name__ == "__main__":
    asyncio.run(main())