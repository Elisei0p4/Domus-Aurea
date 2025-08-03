from django.core.files.storage import FileSystemStorage
from django.conf import settings

class OverwriteStorage(FileSystemStorage):
    """
    Кастомное хранилище, которое перезаписывает существующие файлы,
    вместо того чтобы добавлять случайный суффикс.
    """
    def get_available_name(self, name, max_length=None):
        # Если файл с таким именем уже существует, удаляем его
        if self.exists(name):
            self.delete(name)
        return name