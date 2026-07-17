"""Lightweight test doubles for the external ctgan package."""


class _BaseModel:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs


class CTGAN(_BaseModel):
    pass


class TVAE(_BaseModel):
    pass
