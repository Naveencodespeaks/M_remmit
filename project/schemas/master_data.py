from pydantic import BaseModel
from pydantic import BaseModel, Field
from typing import Optional
from ..constant.messages import COUNTRY_STATES_LIST, STATE_LOCATION_LIST 

 
class getMasterData(BaseModel):
    categories:list = Field(...,  description="Available categories ===> md_countries , md_states , md_locations , md_reminder_status , md_task_status , md_tenant_status , md_timezone , md_user_roles , md_user_status,md_occupations")
    country_id:Optional[int] = Field(None,  description=COUNTRY_STATES_LIST)
    state_id:Optional[str] = Field(None,  description=STATE_LOCATION_LIST  ) 
