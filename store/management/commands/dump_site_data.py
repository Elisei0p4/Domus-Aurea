import os
import shutil
import subprocess
from django.conf import settings
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Dumps all relevant app data and archives the media folder.'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING("= НАЧАЛО ПРОЦЕССА СОЗДАНИЯ 'СНИМКА' САЙТА ="))

        DUMP_PATH = settings.BASE_DIR / 'seed_data' / 'dump'
        os.makedirs(DUMP_PATH, exist_ok=True)


        MODELS_TO_DUMP = [
            'auth.user',
            'store.category',
            'store.product',
            'store.productimage',
            'store.review',
            'store.feature',
            'store.slide',
            'store.specialoffer',
            'blog.tag',
            'blog.article',
            'blog.comment',
            'orders.promocode',
        ]
        
        self.stdout.write("--> Шаг 1: Создание JSON-фикстур...")
        for model_name in MODELS_TO_DUMP:
            app_label, model_file_name = model_name.split('.')
            output_file = DUMP_PATH / f"{model_file_name}.json"
            
            self.stdout.write(f"    - Выгрузка {model_name} в {output_file}...")
            
            try:
                command = [
                    'python', 'manage.py', 'dumpdata', model_name,
                    '--indent=2',
                    '--natural-foreign',
                    '--natural-primary',
                    f'--output={output_file}'
                ]
                subprocess.run(command, check=True, capture_output=True, text=True)
                self.stdout.write(self.style.SUCCESS(f"    Успешно выгружено: {model_name}"))
            except subprocess.CalledProcessError as e:
                self.stdout.write(self.style.ERROR(f"Ошибка при выгрузке {model_name}: {e.stderr}"))
                return

        self.stdout.write(self.style.SUCCESS("--> Шаг 1 завершен: Все JSON-фикстуры созданы."))

        self.stdout.write("--> Шаг 2: Архивирование папки media...")
        media_root = settings.MEDIA_ROOT
        archive_name = DUMP_PATH / 'media_dump'
        
        if os.path.exists(media_root) and os.listdir(media_root):
            try:
                shutil.make_archive(str(archive_name), 'gztar', str(media_root))
                self.stdout.write(self.style.SUCCESS(f"    Папка media успешно заархивирована в {archive_name}.tar.gz"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"    Ошибка при архивировании media: {e}"))
        else:
            self.stdout.write(self.style.WARNING("    Папка media пуста или не существует. Архив не создан."))

        self.stdout.write(self.style.SUCCESS("= 'СНИМОК' САЙТА УСПЕШНО СОЗДАН! ="))
        self.stdout.write(self.style.NOTICE("ВАЖНО: Не забудьте закоммитить изменения в папке 'seed_data/dump/'!"))