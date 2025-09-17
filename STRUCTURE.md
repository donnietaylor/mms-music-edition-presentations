# MMS Music 2025 - Repository Structure Overview

This document provides a comprehensive overview of the repository organization for MMS Music 2025 presentations.

## Top-Level Directory Structure

```
mms-music-presentations/
├── presentations/           # Main presentation content by topic
├── templates/              # Template files for consistency
├── shared-resources/       # Common branding and media assets
├── media/                  # Audio, video, and interactive content
├── code-examples/          # Programming language examples
├── references/             # Bibliography and citation materials
├── README.md              # Main repository documentation
├── STRUCTURE.md           # This file - structure overview
└── .gitignore            # Git ignore rules
```

## Presentation Topics

Each topic has a dedicated folder with standardized subdirectories:

### 🎵 Available Topics
1. **mathematical-foundations** - Mathematical concepts in music
2. **digital-signal-processing** - Audio DSP and synthesis
3. **music-information-retrieval** - MIR algorithms and systems
4. **algorithmic-composition** - Computer-assisted composition
5. **music-theory-analysis** - Computational music theory
6. **performance-systems** - Interactive and real-time systems
7. **music-education-tech** - Educational technology applications
8. **keynotes-plenaries** - Major conference presentations

### 📁 Standard Subdirectories (per topic)
- **slides/** - Presentation slides (PPT, PDF, HTML)
- **notes/** - Speaker notes and scripts
- **handouts/** - Audience materials
- **code/** - Topic-specific code examples
- **media/** - Topic-specific media files
- **references/** - Topic-specific bibliography

## Quick Start Guide

### Adding a New Presentation
1. Choose appropriate topic folder in `presentations/`
2. Copy template from `templates/presentation-template.md`
3. Create presentation materials in relevant subdirectories
4. Use shared resources from `shared-resources/` when possible

### Using Templates
- **presentation-template.md** - Main presentation structure
- **abstract-template.md** - Conference abstract format
- **code-demo-template.py** - Code demonstration template

### Media Guidelines
- Place shared media in `media/` directory
- Place presentation-specific media in topic folders
- Optimize file sizes for presentation use
- Include proper attribution for external content

## File Naming Conventions

- Use descriptive names with dates: `2025-01-15_fourier-analysis.pptx`
- Use lowercase with hyphens: `audio-processing-demo.py`
- Include version numbers for iterations: `v1`, `v2`, etc.

## Best Practices

1. **Consistency** - Use provided templates
2. **Attribution** - Credit all external resources
3. **Testing** - Verify all code examples work
4. **Documentation** - Include clear README files
5. **Optimization** - Compress media files appropriately