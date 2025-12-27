from app.managers.base_manager import BaseManager

class BaseService:
    def __init__(self, manager : BaseManager):
        self.manager = manager
