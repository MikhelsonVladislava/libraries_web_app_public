

def get_object_slug(model_object):
    """Возвращает слаг объекта"""
    return model_object.slug


def get_order_objects(objects, *args):
    """Возвращает отсортированные объекты модели"""
    return objects.order_by(*args)


def get_filter_objects(objects, **kwargs):
    """Возвращает отфильтрованные объекты модели"""
    return objects.filter(**kwargs).order_by('name')

def get_field(model_object, field):
    """Возвращает значение поля экземпляра модели"""
    return getattr(model_object, field)


def set_field(model_object, field, field_value):
    """Назначает значение полю объекта модели"""
    setattr(model_object, field, field_value)


def save_object(save_obj, commit=True):
    if (not commit):
        return save_obj.save(commit=False)
    else:
        save_obj.save()

def get_object(objects, **kwargs):
    """Возвращает объект модели отсортированный по параметрам"""
    return objects.get(**kwargs)