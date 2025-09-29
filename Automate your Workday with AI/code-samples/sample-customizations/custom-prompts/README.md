# Custom Prompts for AI Agents

This directory contains specialized prompts optimized for different domains and use cases, following best practices from the [GitHub Copilot documentation](https://docs.github.com/en/enterprise-cloud@latest/copilot/tutorials/coding-agent/get-the-best-results).

## 📋 Business Process Automation

### Email Response Generation
```yaml
# email-response-prompts.yaml
email_classification:
  prompt: |
    Analyze this email and classify it into one of these categories:
    - URGENT: Requires immediate response (within 1 hour)
    - IMPORTANT: Requires response within 24 hours
    - ROUTINE: Standard business communication
    - SPAM: Promotional or irrelevant content
    
    Email: {email_content}
    
    Respond with: Category: [CATEGORY] | Priority: [1-5] | Suggested Response Time: [timeframe]

auto_reply:
  prompt: |
    Generate a professional email response based on the context and category:
    
    Original Email: {original_email}
    Category: {email_category}
    Sender: {sender_info}
    My Role: {user_role}
    Company Policies: {company_guidelines}
    
    Requirements:
    - Professional tone matching company style
    - Address all questions/requests
    - Include next steps if applicable
    - Keep concise but complete
```

### Meeting Management
```yaml
# meeting-prompts.yaml
agenda_creation:
  prompt: |
    Create a structured meeting agenda based on these inputs:
    
    Meeting Purpose: {meeting_purpose}
    Attendees: {attendee_list}
    Duration: {meeting_duration}
    Previous Action Items: {action_items}
    
    Format:
    1. Opening (5 minutes)
    2. Main Topics (with time allocations)
    3. Decisions Needed
    4. Action Items Review
    5. Next Steps

meeting_summary:
  prompt: |
    Generate a comprehensive meeting summary from these notes:
    
    Meeting Notes: {raw_notes}
    Attendees: {attendees}
    
    Structure:
    - Key Decisions Made
    - Action Items (Owner, Due Date)
    - Follow-up Required
    - Next Meeting Date/Topics
```

## 💻 Code Review & Analysis

### Security-Focused Review
```yaml
# security-review-prompts.yaml
security_analysis:
  prompt: |
    Perform a security-focused code review on this code:
    
    ```{language}
    {code_content}
    ```
    
    Check for:
    - SQL injection vulnerabilities
    - XSS potential
    - Authentication/authorization issues
    - Data exposure risks
    - Input validation problems
    
    Provide:
    1. Risk Level (LOW/MEDIUM/HIGH/CRITICAL)
    2. Specific Issues Found
    3. Recommended Fixes
    4. Prevention Strategies

performance_review:
  prompt: |
    Analyze this code for performance optimization opportunities:
    
    ```{language}
    {code_content}
    ```
    
    Focus on:
    - Algorithm efficiency (Big O analysis)
    - Memory usage patterns
    - Database query optimization
    - Caching opportunities
    - Resource management
    
    Suggest specific improvements with code examples.
```

## 💡 Best Practices for Prompt Engineering

Based on [GitHub's best practices guide](https://docs.github.com/en/enterprise-cloud@latest/copilot/tutorials/coding-agent/get-the-best-results):

1. **Be Specific**: Provide detailed context and clear expectations
2. **Use Examples**: Include concrete examples of desired outputs
3. **Set Constraints**: Define boundaries and limitations clearly
4. **Iterate and Refine**: Test prompts and improve based on results
5. **Version Control**: Track prompt changes and performance metrics

## 🔗 Related Examples

- See [workflow-automation/](../workflow-automation/) for complete automation examples
- Check [performance-optimization/](../performance-optimization/) for speed improvements
- Review [integration-patterns/](../integration-patterns/) for external tool connections