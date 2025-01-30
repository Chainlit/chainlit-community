# chainlit-literalai

[Literal AI](https://www.literal.ai/) integration for [Chainlit](https://chainlit.io/) applications.

## Overview

Official data persistence layer connecting Chainlit with Literal AI's LLM observability platform. Enables production-grade monitoring, evaluation and analytics while maintaining Chainlit's conversation structure.

**Key Features**:
- Full conversation history preservation (threads, steps, elements)
- Multimodal logging (text, images, audio, video)
- User feedback tracking
- Automated performance metrics
- Collaborative prompt versioning & A/B testing

## Setup

1. **Install package**:
```bash
pip install chainlit-literalai
```

2. **Configure environment**:
```bash
# .env file
# Security Best Practices:
# - Restrict .env file permissions
# - Never commit .env to version control
# - Use CI/CD secret management
LITERAL_API_KEY="your-api-key-from-literal-ai"
```

3. **Run your app**:
```bash
chainlit run app.py
```

## Documentation

- [Literal AI Documentation](https://docs.literalai.com)
- [Chainlit + Literal AI Integration Guide](https://docs.chainlit.io/llmops/literalai)

## Data Privacy

- Data retention policy: [literalai.com/security](https://www.literalai.com/security)
- Contact: <contact@chainlit.io>

> **Note**  
> Developed by the Chainlit team for seamless integration.  
> Literal AI is SOC 2 Type 2 compliant.
