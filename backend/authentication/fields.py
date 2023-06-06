from django.db import models

class UpperCaseMixin:
    
    def from_db_value(self, value, expression, connection, *args):
        if value is None:
            return value
        return value.upper()
        
    
    def get_db_prep_value(self, value, connection, prepared=False):
        if not isinstance(value, str):
            raise Exception('value must be string')
        return super().get_db_prep_value(value, connection, prepared)
        




class UpperStringField(models.CharField, UpperCaseMixin):
    pass

   
