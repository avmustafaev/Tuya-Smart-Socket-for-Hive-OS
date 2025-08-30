# main.py
import logging
from compose import Compose

def main():
    """Основная точка входа в приложение"""
    try:
        # Инициализация системы
        composer = Compose()
        
        # Шаг 1: Получение всех компонентов
        components = composer.initialize_components()
        
        # Шаг 2: Выполнение начальной инициализации
        composer.initialize_initial_steps(components)
        
        # Шаг 3: Запуск основного цикла (если требуется)
        # Например: components['main_loop'].start()
        
        logging.info("Приложение успешно запущено")
        
    except Exception as e:
        logging.critical(f"Критическая ошибка запуска: {str(e)}")
        raise

if __name__ == "__main__":
    # Настройка логирования
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    main()
