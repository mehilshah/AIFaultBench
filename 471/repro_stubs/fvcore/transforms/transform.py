class Transform:
    def __init__(self):
        pass
    def _set_attributes(self, locals_dict):
        for k, v in locals_dict.items():
            if k != "self":
                setattr(self, k, v)
    @classmethod
    def register_type(cls, name, func):
        return func

class TransformList(list):
    pass
class HFlipTransform(Transform):
    def __init__(self, width=None):
        self.width = width
class NoOpTransform(Transform):
    pass
class CropTransform(Transform):
    def __init__(self, *args):
        self.args = args
class BlendTransform(Transform):
    pass
