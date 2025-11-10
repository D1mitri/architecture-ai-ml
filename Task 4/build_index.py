import os
import glob
import chromadb
from sentence_transformers import SentenceTransformer
import time

def indexing():
    pages_path = os.getenv('STARWARS_PAGES_PATH', './starwars_pages')
    chroma_db_path = os.getenv('CHROMA_DB_PATH', './chroma_db')

    print(f"Путь к данным: {pages_path}")
    print(f"Путь к базе: {chroma_db_path}")
    print(f"Текущая директория: {os.getcwd()}")

    if not os.path.exists(pages_path):
        print(f"Папка '{pages_path}' не найдена")
        print("Содержимое текущей директории:")
        for item in os.listdir('.'):
            print(f"  - {item}")
        return False

    txt_files = glob.glob(os.path.join(pages_path, "*.txt"))
    print(f"Найдено {len(txt_files)} файлов")

    if not txt_files:
        print("Нет .txt файлов в папке")
        print("Файлы в папке:")
        for item in os.listdir(pages_path):
            print(f"  - {item}")
        return False

    try:
        print("\n1. Инициализация ChromaDB")
        client = chromadb.PersistentClient(path=chroma_db_path)

        try:
            client.delete_collection("starwars_documents")
            print("Удалена старая коллекция")
        except:
            print("Старой коллекции не существует")

        collection = client.create_collection(
            name="starwars_documents",
            metadata={"hnsw:space": "cosine"}
        )
        print("ChromaDB коллекция создана")

        print("\n2. Загрузка модели")
        start_time = time.time()
        model = SentenceTransformer('all-MiniLM-L6-v2')
        load_time = time.time() - start_time
        print(f"Модель загружена за {load_time:.1f} секунд")
        print(f"Размерность: {model.get_sentence_embedding_dimension()}D")

        print("\n3. Обработка документов")
        total_chunks = 0
        all_documents = []
        all_embeddings = []
        all_metadatas = []
        all_ids = []

        for file_path in txt_files:
            filename = os.path.basename(file_path)
            print(f"Обработка: {filename}")

            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]

                chunks = []
                for paragraph in paragraphs:
                    words = paragraph.split()
                    if len(words) <= 128:
                        chunks.append(paragraph)
                    else:
                        for i in range(0, len(words), 100):
                            chunk = ' '.join(words[i:i+100])
                            if chunk.strip():
                                chunks.append(chunk)

                print(f"Создано {len(chunks)} чанков")

                for j, chunk in enumerate(chunks):
                    all_documents.append(chunk)
                    all_metadatas.append({
                        "source": filename,
                        "chunk_id": j,
                        "word_count": len(chunk.split()),
                        "total_chunks": len(chunks),
                        "model": "all-MiniLM-L6-v2"
                    })
                    all_ids.append(f"{filename}_{j}")

                total_chunks += len(chunks)

            except Exception as e:
                print(f"Ошибка обработки файла {filename}: {e}")

        print(f"\n4. Создание эмбеддингов для {total_chunks} чанков")

        batch_size = 50
        for i in range(0, len(all_documents), batch_size):
            batch_docs = all_documents[i:i+batch_size]
            batch_metas = all_metadatas[i:i+batch_size]
            batch_ids = all_ids[i:i+batch_size]

            print(f"Обработка батча {i//batch_size + 1}/{(len(all_documents)-1)//batch_size + 1}")

            batch_embeddings = model.encode(batch_docs)

            collection.add(
                documents=batch_docs,
                embeddings=batch_embeddings.tolist(),
                metadatas=batch_metas,
                ids=batch_ids
            )

        print(f"\n5. Проверка результатов")
        count = collection.count()
        print(f"Обработка завершена!")
        print(f"Файлов обработано: {len(txt_files)}")
        print(f"Всего чанков: {total_chunks}")
        print(f"В базе: {count} записей")

        print(f"\n6. Тестовый запрос (Few-shot prompting)")
        try:
            results = collection.query(
                query_texts=["Who is Xarn Velgor?"],
                n_results=1
            )
            if results['documents']:
                print("Тестовый запрос выполнен успешно")
                print("\nQ: Who is Xarn Velgor?")
                print(f"A: {results['documents'][0][0][:50]}...")
            else:
                print("Тестовый запрос не вернул результатов")
        except Exception as e:
            print(f"Ошибка тестового запроса: {e}")

        print(f"\nГотово! База создана в {chroma_db_path}")
        return True

    except Exception as e:
        print(f"Критическая ошибка: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = indexing()
    exit(0 if success else 1)
