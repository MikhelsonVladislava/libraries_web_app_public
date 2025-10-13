import os
import django

# Настройка окружения Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library.settings')
django.setup()

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

def create_user_groups():
    """
    Создает группы пользователей 'user' и 'moderator' с соответствующими разрешениями
    """
    
    # Разрешения для группы 'user'
    user_permissions_codenames = [
        'view_directory',
        'view_lib', 
        'view_topic',
        'view_entry',
        'view_command',
        'view_uploadentryphoto',
    ]
    
    # Базовые разрешения для группы 'moderator' (включая все разрешения user)
    moderator_permissions_codenames = user_permissions_codenames + [
        # Directory permissions
        'add_directory', 'change_directory', 'delete_directory',
        # Lib permissions
        'add_lib', 'change_lib', 'delete_lib',
        # Topic permissions
        'add_topic', 'change_topic', 'delete_topic',
        # Entry permissions
        'add_entry', 'change_entry', 'delete_entry',
        # Chapter permissions
        'add_chapter', 'change_chapter', 'delete_chapter',
        # Command permissions
        'add_command', 'change_command', 'delete_command',
        # UploadEntryPhoto permissions
        'add_uploadentryphoto', 'change_uploadentryphoto', 'delete_uploadentryphoto',
        # LogEntry permissions
        'add_logentry', 'change_logentry', 'delete_logentry', 'view_logentry',
        # Permission permissions
        'add_permission', 'change_permission', 'delete_permission', 'view_permission',
    ]
    
    try:
        # Создаем или получаем группу 'user'
        user_group, created = Group.objects.get_or_create(name='user')
        if created:
            print("Группа 'user' создана")
        else:
            print("Группа 'user' уже существует")
        
        # Добавляем разрешения для группы 'user'
        user_permissions = Permission.objects.filter(codename__in=user_permissions_codenames)
        user_group.permissions.set(user_permissions)
        print(f"Добавлено {user_permissions.count()} разрешений для группы 'user'")
        
        # Создаем или получаем группу 'moderator'
        moderator_group, created = Group.objects.get_or_create(name='moderator')
        if created:
            print("Группа 'moderator' создана")
        else:
            print("Группа 'moderator' уже существует")
        
        # Добавляем базовые разрешения для группы 'moderator'
        all_permissions = Permission.objects.all()
        moderator_group.permissions.set(all_permissions)
        print(f"Добавлено {all_permissions.count()} базовых разрешений для группы 'moderator'")
        
        print("\nИтоговые разрешения:")
        print(f"Группа 'user': {user_group.permissions.count()} разрешений")
        print(f"Группа 'moderator': {moderator_group.permissions.count()} разрешений")
        
        # Выводим список всех разрешений для проверки
        print("\nРазрешения группы 'user':")
        for perm in user_group.permissions.all().order_by('codename'):
            print(f"  - {perm.codename}")
            
        print("\nРазрешения группы 'moderator' (первые 20):")
        for perm in moderator_group.permissions.all().order_by('codename')[:20]:
            print(f"  - {perm.codename}")
        if moderator_group.permissions.count() > 20:
            print(f"  ... и еще {moderator_group.permissions.count() - 20} разрешений")
            
    except Exception as e:
        print(f"Ошибка при создании групп: {e}")

def check_missing_permissions():
    """
    Проверяет, существуют ли все указанные разрешения в базе данных
    """
    expected_permissions = [
        'view_directory', 'view_lib', 'view_topic', 'view_entry', 'view_command', 
        'view_uploadentryphoto', 'add_directory', 'change_directory', 'delete_directory',
        'add_lib', 'change_lib', 'delete_lib', 'add_topic', 'change_topic', 'delete_topic',
        'add_entry', 'change_entry', 'delete_entry', 'add_chapter', 'change_chapter', 
        'delete_chapter', 'add_command', 'change_command', 'delete_command',
        'add_uploadentryphoto', 'change_uploadentryphoto', 'delete_uploadentryphoto',
        'add_logentry', 'change_logentry', 'delete_logentry', 'view_logentry',
        'add_permission', 'change_permission', 'delete_permission', 'view_permission'
    ]
    
    print("Проверка существующих разрешений:")
    missing_permissions = []
    
    for codename in expected_permissions:
        exists = Permission.objects.filter(codename=codename).exists()
        status = "✓" if exists else "✗"
        print(f"  {status} {codename}")
        
        if not exists:
            missing_permissions.append(codename)
    
    if missing_permissions:
        print(f"\nПредупреждение: следующие разрешения не найдены: {missing_permissions}")
        print("Убедитесь, что соответствующие модели зарегистрированы в админке и миграции применены.")

if __name__ == "__main__":
    print("Создание групп пользователей...")
    check_missing_permissions()
    print("\n" + "="*50)
    create_user_groups()