import pandas as pd

contextual_clue = (
        "For discussions involving ROE, Return on Equity, Equity Return, etc., use calculate_roe. "
        "For topics related to Cash Flow, Cash Benefit, Financial Benefit, etc., use cash_flow_benefit. "
        "If the query doesn't fit these categories, just answer the question normally. "
    )

def needs_specialized_tool(user_prompt):
    # Clues about when to use which tool, transformed into actionable logic
    clues_for_roe = ["roe", "return on equity", "equity return", "investment return"]
    clues_for_cash_flow = ["cash flow", "cash benefit", "financial benefit"]

    # Combine clues for a comprehensive check, since we're only deciding if ANY tool is needed
    all_clues = clues_for_roe + clues_for_cash_flow

    # Convert the prompt to lowercase to ensure case-insensitive matching
    prompt_lower = user_prompt.lower()

    # Check if the prompt contains any keywords that necessitate using a tool
    for clue in all_clues:
        if clue in prompt_lower:
            return True  # A specialized tool is needed based on the contextual clue

    # If the prompt doesn't match any clues for using a specialized tool, return False
    return False



llm_function_for_roe_calculation = {
        "type": "function",
        "function": {
            "name": "calculate_roe_example",
            "description": "Calculate the annualized ROE of the given transactions.",
            "parameters": {
                "type": "object",
                "properties": {
                    "transactions": {
                        "type": "array",
                        "description": "Array of transaction dictionaries.",
                        "items": {
                            "type": "object",
                            "properties": {
                                "action": {"type": "string"},
                                "year": {"type": "number"}
                            },
                            "required": ["action", "year"]
                        }
                    },
                    "updated_parameters": {
                        "type": "object",
                        "description": "Updated parameters for the ROE calculation",
                        "additionalProperties": True
                    }
                },
                "required": ["transactions"]
            }
        }
    }

llm_function_for_cash_flow_benefit = {
        "type": "function",
        "function": {
            "name": "calculate_cash_flow_benefit",
            "description": "Calculate the cashflow value of the given transactions.",
            "parameters": {
                "type": "object",
                "properties": {
                    "transactions": {
                        "type": "array",
                        "description": "Array of transaction dictionaries.",
                        "items": {
                            "type": "object",
                            "properties": {
                                "action": {"type": "string"},
                                "year": {"type": "number"}
                            },
                            "required": ["action", "year"]
                        }
                    },
                    "updated_parameters": {
                        "type": "object",
                        "description": "Updated parameters for the Cash flow benefit calculation",
                        "additionalProperties": True
                    }
                },
                "required": ["transactions"]
            }
        }
    }
