
"""
TraceShield LLM Service.

This module provides the LLM layer for TraceShield.

Important design principles:
- The LLM receives verified analytical data.
- The LLM must not invent blockchain transactions.
- The LLM must not independently determine wallet ownership.
- The LLM must not establish criminal activity.
- API keys are loaded from environment variables.
"""

import json
import os
from typing import Any, Dict, Optional

from app.services.ai_service import ai_service


class LLMService:
    """
    Service responsible for preparing investigation data
    for an external Large Language Model.

    The actual LLM provider can be connected later without
    changing the rest of the TraceShield architecture.
    """

    def __init__(self) -> None:
        self.api_key = os.getenv("LLM_API_KEY")
        self.model = os.getenv(
            "LLM_MODEL",
            "default-model"
        )

    def is_configured(self) -> bool:
        """
        Check whether an LLM API key has been configured.
        """

        return bool(self.api_key)

    def build_system_prompt(self) -> str:
        """
        Return the system instructions used for the LLM.
        """

        return """
You are TraceShield AI, an investigation-support assistant.

Your task is to explain verified blockchain analytical
information in a clear and structured manner.

Rules:

1. Use only the evidence and analytical information provided.
2. Never invent transactions, wallet addresses, entities,
   timestamps, values, or evidence.
3. Do not claim that a wallet belongs to a person or organization
   unless verified attribution is explicitly provided.
4. Do not independently establish criminal activity.
5. Clearly distinguish observed facts from analytical interpretation.
6. Mention uncertainty when evidence is incomplete.
7. Preserve transaction hashes and evidence references exactly.
8. Do not remove important limitations from the analysis.
9. Do not make unsupported claims about intent.
10. Produce investigator-friendly explanations.

The output is analytical assistance and must be reviewed
against the underlying evidence.
""".strip()

    def build_prompt(
        self,
        investigation: Any
    ) -> str:
        """
        Build a prompt from verified investigation data.

        The investigation is first converted through the
        existing AIService context builder.
        """

        context = ai_service.build_ai_context(
            investigation
        )

        context_json = json.dumps(
            context,
            indent=2,
            default=str
        )

        prompt = f"""
Analyze the following verified TraceShield investigation data.

Provide a factual investigation explanation containing:

- Investigation overview
- Transaction observations
- Important fund-flow observations
- Wallet relationship observations
- Risk indicators
- Entity intelligence
- Timeline observations
- Evidence references
- Important limitations

Do not create information that is not present in the
provided investigation data.

Verified investigation data:

{context_json}
""".strip()

        return prompt

    def generate_explanation(
        self,
        investigation: Any
    ) -> Dict[str, Any]:
        """
        Prepare the LLM request.

        At this stage, this method does not call an external
        provider. It returns the structured request information
        so the provider can be connected safely later.
        """

        system_prompt = self.build_system_prompt()

        user_prompt = self.build_prompt(
            investigation
        )

        return {
            "configured": self.is_configured(),
            "model": self.model,
            "system_prompt": system_prompt,
            "user_prompt": user_prompt,
        }

    def get_configuration_status(self) -> Dict[str, Any]:
        """
        Return the current LLM configuration status.

        The API key itself is never returned.
        """

        return {
            "configured": self.is_configured(),
            "model": self.model,
            "provider": os.getenv(
                "LLM_PROVIDER",
                "not_configured"
            ),
        }


# Shared LLM service instance
llm_service = LLMService()
