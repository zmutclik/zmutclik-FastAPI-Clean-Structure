from typing import Union, Optional, Any 
from pythondi import inject 
 
from sqlalchemy import or_, select 
from datatables import DataTable 
 
from core.db.session import async_engine 
from app.coresystem.domain import CoreSYSTEM 
from app.coresystem.repository import CoreSYSTEMRepo 
from app.coresystem.schema import CoreSYSTEMSchema 
from app.coresystem.exceptions import CoreSYSTEMNotFoundException 
 
 
class CoreSYSTEMQueryService: 
    @inject() 
    def __init__(self, coresystem_repo: CoreSYSTEMRepo): 
        self.coresystem_repo = coresystem_repo 
 
    async def get_coresystem_by_id(self, coresystem_id: str) -> Optional[CoreSYSTEMSchema]: 
        data_get = self.coresystem_repo.get_by_id(coresystem_id) 
        if not data_get: 
            raise CoreSYSTEMNotFoundException 
        return data_get 
 
    async def get_coresystem(self, coresystem: str) -> Optional[CoreSYSTEMSchema]: 
        data_get = self.coresystem_repo.get(coresystem) 
        if not data_get: 
            raise CoreSYSTEMNotFoundException 
        return data_get 
 
    async def datatable_coresystem(self, params: dict[str, Any]): 
        query = select(CoreSYSTEM, CoreSYSTEM.id.label("DT_RowId")).where(CoreSYSTEM.deleted_at == None) 
        datatable: DataTable = DataTable( 
            request_params=params, 
            table=query, 
            column_names=["DT_RowId", "id", "coresystem"], 
            engine=async_engine, 
            # callbacks=callbacks, 
        ) 
        return datatable.output_result() 
