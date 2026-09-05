import json
import os

from dotenv import load_dotenv

from google import genai
from google.genai import types

from finance_tools import (
    get_revenue,
    get_top_customers,
    get_failed_payments,
    get_product_performance,
    detect_suspicious_transactions
)


# -----------------------------------------
# LOAD GEMINI API KEY
# -----------------------------------------

load_dotenv()


api_key = os.getenv(
    "GEMINI_API_KEY"
)


if not api_key:

    raise ValueError(
        "GEMINI_API_KEY was not found. "
        "Check your .env file."
    )


# -----------------------------------------
# CREATE GEMINI CLIENT
# -----------------------------------------

client = genai.Client(
    api_key=api_key
)


# -----------------------------------------
# OUR PYTHON FUNCTIONS
# -----------------------------------------

available_functions = {

    "get_revenue":
        get_revenue,

    "get_top_customers":
        get_top_customers,

    "get_failed_payments":
        get_failed_payments,

    "get_product_performance":
        get_product_performance,

    "detect_suspicious_transactions":
        detect_suspicious_transactions
}


# -----------------------------------------
# TOOL DEFINITIONS FOR GEMINI
# -----------------------------------------

tools = [

    types.Tool(

        function_declarations=[

            types.FunctionDeclaration(

                name="get_revenue",

                description=(
                    "Get total revenue from "
                    "successful payments and "
                    "the number of successful "
                    "transactions."
                ),

                parameters=types.Schema(

                    type="OBJECT",

                    properties={}

                )
            ),


            types.FunctionDeclaration(

                name="get_top_customers",

                description=(
                    "Get the top 10 customers "
                    "ranked by how much money "
                    "they spent."
                ),

                parameters=types.Schema(

                    type="OBJECT",

                    properties={}

                )
            ),


            types.FunctionDeclaration(

                name="get_failed_payments",

                description=(
                    "Get the number and total "
                    "amount of failed payments."
                ),

                parameters=types.Schema(

                    type="OBJECT",

                    properties={}

                )
            ),


            types.FunctionDeclaration(

                name="get_product_performance",

                description=(
                    "Get revenue generated "
                    "by each product."
                ),

                parameters=types.Schema(

                    type="OBJECT",

                    properties={}

                )
            ),


            types.FunctionDeclaration(

                name=
                    "detect_suspicious_transactions",

                description=(
                    "Find unusually large "
                    "successful transactions "
                    "that may need review."
                ),

                parameters=types.Schema(

                    type="OBJECT",

                    properties={}

                )
            )

        ]
    )
]


# -----------------------------------------
# GEMINI CONFIGURATION
# -----------------------------------------

config = types.GenerateContentConfig(

    tools=tools,

    system_instruction="""

You are PayLens AI.

You are a business finance assistant.

Your job is to help business owners
understand their payment data.

IMPORTANT RULES:

1. Never invent financial numbers.

2. When the user asks about business
   financial data, use the appropriate
   tool to retrieve the real data.

3. Explain results in simple language.

4. Do not say that a transaction is
   definitely fraudulent.

5. Suspicious transactions are only
   transactions that may deserve review.

6. If our data cannot answer a question,
   clearly tell the user.

7. Be concise but useful.

"""
)


# -----------------------------------------
# MAIN AI FUNCTION
# -----------------------------------------

def ask_agent(question):

    # First message from user
    contents = [

        types.Content(

            role="user",

            parts=[
                types.Part(
                    text=question
                )
            ]
        )

    ]


    # -------------------------------------
    # FIRST GEMINI REQUEST
    # -------------------------------------

    response = client.models.generate_content(

        model="gemini-3.7-flash",

        contents=contents,

        config=config
    )


    # -------------------------------------
    # CHECK FOR FUNCTION CALLS
    # -------------------------------------

    function_calls = []


    for part in response.candidates[
        0
    ].content.parts:

        if part.function_call:

            function_calls.append(
                part.function_call
            )


    # -------------------------------------
    # IF GEMINI WANTS A TOOL
    # -------------------------------------

    if function_calls:

        # Add Gemini's response
        # containing the function call
        contents.append(
            response.candidates[
                0
            ].content
        )


        # Store function results
        function_response_parts = []


        for call in function_calls:

            function_name = call.name


            # Find our Python function
            function = (
                available_functions[
                    function_name
                ]
            )


            # Run the function
            result = function()


            # Give result back to Gemini
            function_response_parts.append(

                types.Part.from_function_response(

                    name=function_name,

                    response={
                        "result": result
                    }
                )
            )


        # Add tool results to conversation
        contents.append(

            types.Content(

                role="user",

                parts=function_response_parts

            )
        )


        # ---------------------------------
        # FINAL GEMINI RESPONSE
        # ---------------------------------

        final_response = (
            client.models.generate_content(

                model="gemini-3.7-flash",

                contents=contents,

                config=config
            )
        )


        return final_response.text


    # -------------------------------------
    # IF NO TOOL WAS NEEDED
    # -------------------------------------

    return response.text