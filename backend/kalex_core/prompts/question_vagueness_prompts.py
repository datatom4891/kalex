from langchain_core.prompts import PromptTemplate

vagueness_text = """
Assess whether the user question below contains enough information for you to provide an accurate and grounded response without hallucinating or\n
making unfounded assumptions with your internal knowledge or an external knowledge source, using the following criteria:
    1. Specificity of Subject Matter
        - Is the topic clearly identified?
        - Are there multiple possible interpretations?
        - Does the query reference specific entities (people, places, products) that require verification?
     2. Temporal Context
        - Does the query ask about current/recent information that may be outside your knowledge cutoff?
        - Is a timeframe specified when it matters (e.g., “best practices” vs. “best practices in 2024”)?
     3. Scope and Constraints
        - Are there implicit requirements that aren’t stated?
        - Does “best,” “recommended,” or “should” require knowing the user’s specific context?
        - Are there multiple valid approaches without additional constraints?
     4. Factual vs. Subjective
        - Does the query ask for objective facts that you can verify?
        - Does it ask for recommendations that depend heavily on unstated preferences or circumstances?
        
If the user question has insufficient information to provide an accurate and grounded response without hallucinating, respond with TRUE and an explanation for insufficient information.\n
If the user question does have sufficient information to provide an accurate and grounded response without hallucinating, respond with FALSE.

USER QUESTION: {user_question}
"""

vagueness_prompt_template = PromptTemplate.from_template(vagueness_text)