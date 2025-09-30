# GitHub Copilot Instructions for mms-music-edition-presentations

## Repository Overview

This is a **documentation and code samples repository** for conference presentations at MMS 2025 Music City Edition. It contains presentation materials, code examples, speaker notes, and resources across four main sessions. **This repository contains primarily documentation, code examples, and demo scripts—not a production application.**

**Repository Size**: ~900KB, 96 files, 52 directories

## What This Repository Does

Provides educational materials and working code examples for four conference sessions:
- **Automate your Workday with AI** - AI-powered automation examples, GitHub Agents customization
- **ClickOps to DevOps** - Infrastructure as Code (Terraform) examples, CI/CD patterns
- **Automating Serverless Workflows** - Serverless automation examples
- **Public Speaking 101** - Public speaking resources

## Languages, Frameworks & Tools

**Primary Technologies**:
- **Python 3.9+** - GitHub Agent examples (requires: openai>=1.3.0, PyGithub>=1.59.0, pyyaml>=6.0, redis>=4.5.0, asyncio-throttle>=1.0.2, aiohttp>=3.8.0)
- **Terraform 1.0+** - Infrastructure as Code examples (Azure and AWS providers ~> 3.0)
- **Bash** - Setup and automation scripts
- **YAML/JSON** - Configuration files

**Cloud Providers**: Azure (primary), AWS (examples)

## Repository Structure

### Root Directory Files
```
.
├── README.md                          # Main repository overview
├── .gitignore                         # Python, Terraform, IDE exclusions
├── Automate your Workday with AI/     # AI automation session
├── ClickOps to DevOps/                # Infrastructure as Code session
├── Automating Serverless Workflows/   # Serverless automation session
└── Public Speaking 101/               # Public speaking resources
```

### Session Structure (Consistent Pattern)
Each session directory contains:
- **code-samples/** - Working code examples and demos
- **presentations/** - Slide decks and visual materials
- **notes/** - Speaker notes and key takeaways
- **resources/** - Additional tools, links, and materials

### Key Directories

#### Automate your Workday with AI
```
Automate your Workday with AI/code-samples/github-agents/
├── ai-code-review-agent/          # Code review automation
│   ├── code_review_agent.py       # Main agent implementation
│   ├── requirements.txt           # Python dependencies
│   ├── prompts.yaml               # Custom AI prompts
│   ├── rules.json                 # Automation rules
│   ├── performance-config.yaml    # Speed optimization config
│   └── workflow.yml               # GitHub Actions workflow
├── ai-documentation-agent/        # Documentation generation
├── smart-deployment-agent/        # Intelligent deployment
├── multi-agent-workflow/          # Agent orchestration
├── intelligent-issue-triage/      # Issue classification
└── copilot-instructions.md        # Example custom instructions
```

#### ClickOps to DevOps
```
ClickOps to DevOps/code-samples/terraform/
├── installation/                  # Terraform setup guides
├── simple-resources/              # Basic deployments
│   ├── azure/                     # Azure examples (main.tf, variables.tf, outputs.tf)
│   ├── aws/                       # AWS examples
│   └── multi-cloud/               # Multi-cloud examples
├── state-management/
│   └── remote-state/              # Remote state setup
│       ├── setup-azure-backend.sh # Azure backend setup script
│       └── azure-backend.tf       # Backend configuration
└── drift-detection/
    ├── scenarios/                 # Drift scenarios
    └── workflows/                 # CI/CD workflows
        └── github-actions-drift-detection.yml
```

## Build, Test, and Validation

### Important: No Build System or Tests
**This repository has NO test suite, NO CI/CD pipeline, and NO build process.** It contains educational examples that users copy and run in their own environments. Do NOT attempt to add build infrastructure unless explicitly requested.

### Validation Approaches

#### Python Code Examples
These are **demonstration scripts** that require external services (OpenAI API, GitHub API):

```bash
# Syntax validation only (no execution without credentials)
python3 -m py_compile "Automate your Workday with AI/code-samples/github-agents/ai-code-review-agent/code_review_agent.py"

# Check for syntax errors across all Python files
find . -name "*.py" -exec python3 -m py_compile {} \;
```

**Note**: Do NOT attempt to run these scripts or install their dependencies unless working on that specific example. They require API keys and external services.

#### Terraform Examples
These require Azure/AWS credentials and should NOT be executed during code changes:

```bash
# Validate syntax only (no terraform init/plan/apply)
cd "ClickOps to DevOps/code-samples/terraform/simple-resources/azure/"
terraform fmt -check -recursive .
terraform validate  # Only after terraform init (not recommended)
```

**Critical**: Do NOT run `terraform init`, `terraform plan`, or `terraform apply` unless explicitly working on Terraform code AND you have proper credentials configured. These commands make API calls and may create billable resources.

#### Shell Scripts
```bash
# Syntax check only
bash -n "ClickOps to DevOps/code-samples/terraform/state-management/remote-state/setup-azure-backend.sh"

# Do NOT execute scripts unless working on them specifically
```

### Making Changes to Code Examples

When modifying code examples:

1. **Python Changes**: 
   - Verify syntax with `python3 -m py_compile <file>`
   - Ensure imports are available in requirements.txt
   - Follow PEP 8 conventions
   - Do NOT run the script without proper credentials

2. **Terraform Changes**:
   - Run `terraform fmt` to format code
   - Do NOT initialize or plan unless necessary
   - Verify variables are documented in variables.tf
   - Check README has correct usage instructions

3. **Documentation Changes**:
   - Update relevant README.md files
   - Ensure code examples in docs match actual files
   - Verify markdown formatting
   - No validation needed beyond readability

## Architecture & Key Files

### Configuration Files

**Python Agent Configurations**:
- `prompts.yaml` - AI prompt templates for different review types
- `rules.json` - Automation rules for auto-approval/rejection
- `performance-config.yaml` - Speed optimization settings (caching, parallel processing)
- `requirements.txt` - Python dependencies (only in ai-code-review-agent/)

**Terraform Configurations**:
- `main.tf` - Resource definitions
- `variables.tf` - Input parameters with validation
- `outputs.tf` - Output values after deployment
- `terraform.tfvars.example` - Example variable values (never commit actual .tfvars)

**Workflow Files**:
- `workflow.yml` - GitHub Actions examples (not active in this repo)
- `github-actions-drift-detection.yml` - Example drift detection workflow

### No Active CI/CD

**Important**: The workflow YAML files in this repository are **example files for educational purposes only**. They are NOT in `.github/workflows/` and do NOT run automatically. Do not move them or attempt to activate them unless explicitly requested.

## Common Pitfalls & Workarounds

### Avoid These Mistakes

1. **Do NOT install Python dependencies globally** - Examples require external APIs
2. **Do NOT run Terraform commands** without Azure/AWS credentials configured
3. **Do NOT execute the Azure backend setup script** unless setting up actual infrastructure
4. **Do NOT create .github/workflows/** unless explicitly requested
5. **Do NOT run Python agent scripts** without GITHUB_TOKEN and OPENAI_API_KEY

### Expected Patterns

- **Terraform state files** (.tfstate) should NEVER be committed (in .gitignore)
- **backend.hcl** files are generated by scripts (in .gitignore)
- **__pycache__/** directories should be ignored (in .gitignore)
- **Example files** use .example suffix (terraform.tfvars.example)

## File Organization Rules

### What Lives Where

**Documentation** (README.md):
- Root: Overall repository overview
- Session root: Session-specific overview
- code-samples/: Quick start and usage instructions
- Subdirectories: Specific example documentation

**Python Code**:
- All in `Automate your Workday with AI/code-samples/github-agents/*/`
- Each agent in its own directory
- requirements.txt only where needed (not at root)

**Terraform Code**:
- All in `ClickOps to DevOps/code-samples/terraform/*/`
- Organized by topic (installation, simple-resources, state-management, drift-detection)
- Each example is self-contained with main.tf, variables.tf, outputs.tf

**Shell Scripts**:
- Located with related examples (e.g., setup-azure-backend.sh in remote-state/)
- Must have proper shebang (#!/bin/bash) and be executable

## Search and Navigation Tips

### Finding Relevant Files

**For Python agent work**:
```bash
find "Automate your Workday with AI/code-samples/github-agents" -name "*.py"
find "Automate your Workday with AI/code-samples/github-agents" -name "requirements.txt"
```

**For Terraform examples**:
```bash
find "ClickOps to DevOps/code-samples/terraform" -name "*.tf"
find "ClickOps to DevOps/code-samples/terraform" -name "README.md"
```

**For configuration files**:
```bash
find . -name "*.yaml" -o -name "*.yml" | grep -v ".git"
find . -name "*.json" | grep -v ".git"
```

### Dependencies Not Obvious from Structure

- Python agents expect OpenAI API and GitHub API credentials via environment variables
- Terraform examples expect Azure CLI (`az login`) or AWS CLI authentication
- Shell scripts may require `openssl` for random string generation
- READMEs often reference external installation guides

## Trust These Instructions

These instructions are comprehensive and validated. When working in this repository:

1. **Trust that there are no tests to run** - Don't search for test files
2. **Trust that code examples should not be executed** - They're for educational reference
3. **Trust the validation commands provided** - Use syntax checks only
4. **Only search further if** you find these instructions incomplete or incorrect

When in doubt, check the relevant README.md file first - they contain specific usage instructions for each example.

## Quick Reference: Common Tasks

**Adding a new Python agent example**:
1. Create directory in `Automate your Workday with AI/code-samples/github-agents/`
2. Add Python file(s), requirements.txt, README.md, and config files
3. Follow existing agent patterns (see ai-code-review-agent/)
4. Verify syntax: `python3 -m py_compile <file>`

**Adding a new Terraform example**:
1. Create directory in `ClickOps to DevOps/code-samples/terraform/`
2. Add main.tf, variables.tf, outputs.tf, README.md, terraform.tfvars.example
3. Format: `terraform fmt -recursive .`
4. Document usage in README.md with step-by-step commands

**Updating documentation**:
1. Edit relevant README.md file(s)
2. Ensure consistency with actual code
3. No validation needed - just ensure clarity

**Key reminder**: This is a presentation materials repository. Focus on clarity, educational value, and accurate documentation rather than production-grade code or extensive testing.
