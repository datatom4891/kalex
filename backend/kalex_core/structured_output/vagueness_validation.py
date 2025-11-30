from pydantic import BaseModel, Field

class IsQuestionVague(BaseModel):
  """Is a user's question vague or not. 
     - TRUE for it's vague and more information is needed
     - FALSE for it's not vague, no additional information or rephrasing of the question needed
  """
  flag: bool
  reason: str