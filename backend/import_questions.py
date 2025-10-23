import io
import re
from sqlalchemy.orm import Session
from database import get_db
from models import Question, Tag

qa_filename = "./q.md"

def read_questions():
    with io.open(qa_filename, "r", encoding="utf-8") as file:
        full_text = file.read()
        categories = []
        pattern = r"# ([a-zA-Zа-яА-Я -]+) \d+"  # Извлекаем только текст
        categories = re.findall(pattern, full_text)
    return full_text, categories

def get_questions(cat_text):
    pattern = r"\d+ u?f"
    questions = re.findall(pattern, cat_text)
    return questions

def fill_cat(categories_names, cat_name, cat_text, full_question_list):
    questions = get_questions(cat_text)
    print(f"Категория '{cat_name}': найдено {len(questions)} вопросов")
    
    for idx, q in enumerate(questions):
        q_text = cat_text[cat_text.find(q)+len(q):]
        q_text = q_text.split("\n\n")[0].strip()
        question = q_text[:q_text.find("\n")]
        i = 0
        if len(full_question_list) > 0:
            i = full_question_list[-1]["index"] + 1

        full_question_list.append({
            "category": cat_name, 
            "number": q, 
            "question": question, 
            "answer": q_text[q_text.find("\n"):].strip(), 
            "index": i
        })
        if cat_name not in categories_names:
            categories_names.append(cat_name)

def fill_dct(cats, categories_names, full_text, full_question_list):
    # Исправленная логика - используем индексы заголовков
    header_pattern = r"# [a-zA-Zа-яА-Я -]+ \d+"
    header_matches = list(re.finditer(header_pattern, full_text))
    
    print(f"Найдено {len(header_matches)} заголовков")
    
    for i, match in enumerate(header_matches):
        header_text = match.group()
        if "Статистика" in header_text:
            continue
            
        # Извлекаем название категории
        pattern = r"[a-zA-Zа-яА-Я -]+"
        name = re.findall(pattern, header_text)
        cat_name = name[0].strip()
        
        # Определяем границы раздела
        start_pos = match.end()  # После заголовка
        if i + 1 < len(header_matches):
            end_pos = header_matches[i + 1].start()  # До следующего заголовка
        else:
            end_pos = len(full_text)  # До конца файла
        
        cat_text = full_text[start_pos:end_pos].strip()
        
        print(f"Обрабатываем '{cat_name}': позиции {start_pos}-{end_pos}")
        fill_cat(categories_names, cat_name, cat_text, full_question_list)

def import_questions_to_db():
    """Импорт вопросов в базу данных (теги уже существуют)"""
    # Получаем данные из файла
    full_text, categories = read_questions()
    full_question_list = []
    categories_names = []
    fill_dct(categories, categories_names, full_text, full_question_list)
    print(f"Всего найдено: {len(full_question_list)} вопросов")
    
    # Показываем статистику по категориям
    print("\n📊 Статистика по категориям:")
    for cat_name in categories_names:
        count = len([q for q in full_question_list if q['category'] == cat_name])
        print(f"  {cat_name}: {count} вопросов")

    # Подключаемся к БД
    db = next(get_db())
    
    try:
        # Создаем маппинг категорий к существующим тегам
        tag_mapping = {}
        for cat_name in categories_names:
            tag = db.query(Tag).filter(Tag.slug == cat_name).first()
            tag_mapping[cat_name] = tag

        imported_count = 0
        for q_data in full_question_list:
            tag = tag_mapping.get(q_data['category'])
            if not tag:
                print(f"Пропускаем вопрос из категории '{q_data['category']}' - тег не найден")
                continue
                
            # Создаем вопрос
            question = Question(
                q=q_data['question'],
                a=q_data['answer']
            )
            db.add(question)
            db.flush()  # Получаем ID
            
            # Связываем с тегом
            question.tags.append(tag)
            imported_count += 1
        
        db.commit()
        print(f"✅ Импортировано {imported_count} вопросов")
        
        # Показываем статистику по тегам
        print("\n📊 Статистика импорта:")
        for cat_name, tag in tag_mapping.items():
            questions_count = len([q for q in full_question_list if q['category'] == cat_name])
            print(f"  {tag.title}: {questions_count} вопросов")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Ошибка импорта: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    import_questions_to_db()