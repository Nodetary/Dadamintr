# Dadamintr

![Tests](https://github.com/Nodetary/dadamintr/workflows/Tests/badge.svg)
![Python](https://img.shields.io/badge/python-3.11-blue.svg)
![License](https://img.shields.io/badge/license-Proprietary-red.svg)

An AI-assisted web scraping framework that combines multiple AI models to help generate, validate, and optimize web scraping solutions.

## Features

- AI-assisted scraping configuration generation
- Multiple AI model support (Claude, GPT-4, Gemini)
- Automatic selector generation and validation
- Interactive setup guidance
- Data quality monitoring
- Progress tracking and resumability
- Multiple export formats

## Setup

1. Configure AI API Keys:
   Copy `app/config/ai_config.template.json` to `app/config/ai_config.json` and add your API keys:
   ```json
   {
     "anthropic": {
       "api_key": "your-claude-key"
     },
     "openai": {
       "api_key": "your-openai-key"
     },
     "gemini": {
       "api_key": "your-gemini-key"
     }
   }
   ```

2. Build and run with Docker:
   ```bash
   docker-compose up --build
   ```

## Usage

1. Start the scraper:
   ```bash
   docker-compose run scraper
   ```

2. Follow the interactive prompts to:
   - Specify the target website
   - Describe the data you want to extract
   - Complete any required authentication
   - Configure site-specific settings

## Directory Structure

```
dadamintr/
├── docker/                 # Docker configuration
├── app/
│   ├── ai_assistant/      # AI model integrations
│   ├── scraper/           # Scraping implementations
│   ├── config/            # Configuration files
│   └── utils/             # Utility modules
├── data/
│   ├── output/            # Scraped data output
│   └── downloads/         # Downloaded files
└── docker-compose.yml     # Docker composition
```

## Legal Notice & Terms of Use

© 2024 The SaaS Cool Era Technologies. All Rights Reserved.

### Proprietary Rights

This software, including but not limited to its source code, documentation, design, architecture, and functionality (collectively, the "Software"), is the exclusive property of The SaaS Cool Era Technologies. All intellectual property rights, including patents, copyrights, trade secrets, and proprietary information contained herein are reserved.

### Confidentiality

1. **Strict Confidentiality**: This Software contains confidential and proprietary information of The SaaS Cool Era Technologies. By accessing this Software, you agree to:
   - Maintain strict confidentiality of all Software components
   - Not disclose any part of the Software to third parties
   - Not use the Software for any purpose not explicitly authorized
   - Not reverse engineer, decompile, or attempt to derive the source code

2. **Access Restrictions**: Access to this Software is granted only to authorized individuals who have:
   - Signed a Non-Disclosure Agreement (NDA)
   - Received explicit written permission from The SaaS Cool Era Technologies
   - Agreed to all terms and conditions herein

### Usage Terms

1. **Limited License**: Any use of this Software is subject to a valid license agreement from The SaaS Cool Era Technologies.

2. **Prohibited Activities**:
   - Commercial use without explicit authorization
   - Modification or creation of derivative works
   - Distribution or sharing of any Software components
   - Integration with other systems without written permission
   - Automated scanning or copying of the Software

3. **Monitoring**: The SaaS Cool Era Technologies reserves the right to:
   - Monitor usage of the Software
   - Audit compliance with these terms
   - Revoke access at any time without notice

### Liability and Warranties

1. **Disclaimer of Warranties**: The Software is provided "AS IS" without any warranties, express or implied, including but not limited to:
   - Merchantability
   - Fitness for a particular purpose
   - Non-infringement
   - Accuracy or completeness of results

2. **Limitation of Liability**: In no event shall The SaaS Cool Era Technologies be liable for:
   - Direct, indirect, incidental, or consequential damages
   - Loss of profits, data, or business opportunities
   - Any claims arising from use or inability to use the Software
   - Any unauthorized access or modifications to the Software

### Enforcement

1. **Legal Action**: Any violation of these terms may result in:
   - Immediate termination of access
   - Legal action for damages
   - Injunctive relief
   - Recovery of attorney fees and legal costs

2. **Jurisdiction**: Any disputes shall be resolved in the courts of Texas, under the laws of Texas, without regard to conflicts of law principles.

### Indemnification

Users agree to indemnify and hold harmless The SaaS Cool Era Technologies, its officers, directors, employees, and agents from any claims, damages, or expenses arising from:
- Violation of these terms
- Unauthorized use of the Software
- Breach of confidentiality obligations

### Contact

For licensing inquiries or permissions, contact:
The SaaS Cool Era Technologies
Hello@TheSaaSCoolEra.Foundation

### Modifications

The SaaS Cool Era Technologies reserves the right to modify these terms at any time without notice. Continued use of the Software constitutes acceptance of any modified terms.
