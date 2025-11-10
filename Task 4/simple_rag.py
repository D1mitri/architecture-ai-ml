import chromadb
from sentence_transformers import SentenceTransformer
from transformers import pipeline
import sys
import re

class SimpleRAGBot:
    def __init__(self):
        self.setup()
    
    def setup(self):
        try:
            print("Загрузка компонентов RAG")

            self.client = chromadb.PersistentClient(path="./chroma_db")
            self.collection = self.client.get_collection("starwars_documents")

            self.encoder = SentenceTransformer('all-MiniLM-L6-v2')

            self.generator = pipeline(
                "text2text-generation",
                model="google/flan-t5-small",
                max_length=512,
                temperature=0.3
            )
            
            print("RAG бот готов")
            
        except Exception as e:
            print(f"Ошибка инициализации: {e}")
            self.generator = None
            print("Используется режим только поиска (без генерации)")
    
    def search(self, query, n_results=3):
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results,
                include=["documents", "metadatas", "distances"]
            )
            
            if results['documents']:
                documents = results['documents'][0]
                distances = results['distances'][0] if results['distances'] else []

                filtered_docs = []
                for i, doc in enumerate(documents):

                    similarity = 1 - distances[i] if i < len(distances) else 0.5
                    if similarity > 0.3:
                        filtered_docs.append(doc)
                    else:
                        print(f"Документ отфильтрован (схожесть: {similarity:.3f})")
                
                return filtered_docs
            return []
            
        except Exception as e:
            print(f"Ошибка поиска: {e}")
            return []
    
    def ask(self, question):
        print("Поиск релевантной информации")

        context_docs = self.search(question, n_results=5)
        
        if not context_docs:
            return "Я не знаю"
        
        print(f"Найдено {len(context_docs)} релевантных фрагментов")

        context = "\n".join([f"- {doc}" for doc in context_docs])

        prompt = f"""Вопрос: {question}

Контекст:
{context}

На основе приведенного контекста, дайте точный ответ на вопрос. Если в контексте нет достаточной информации, скажите "Я не знаю".

Ответ:"""

        try:
            if self.generator:
                response = self.generator(
                    prompt,
                    max_length=300,
                    temperature=0.3,
                    do_sample=False,
                    num_return_sequences=1
                )[0]['generated_text']
            else:
                response = context_docs[0][:300] + "..."

            response = response.strip()

            if not response or len(response) < 10:
                return "Я не знаю"

            uncertainty_phrases = [
                "я не знаю", "не могу ответить", "нет информации", 
                "не упоминается", "неизвестно", "не найдено",
                "i don't know", "no information", "not mentioned"
            ]
            
            if any(phrase in response.lower() for phrase in uncertainty_phrases):
                return "Я не знаю"
            
            return response
            
        except Exception as e:
            print(f"Ошибка генерации: {e}")
            if context_docs:
                return f"На основе найденной информации: {context_docs[0][:200]}..."
            else:
                return "Произошла ошибка при обработке вопроса"

def main():
    bot = SimpleRAGBot()
    
    print("\nПростой RAG бот запущен")
    print("Введите вопросы о Star Wars вселенной")
    print("Для выхода введите 'quit'\n")
    
    while True:
        try:
            question = input("Ваш вопрос: ").strip()
            
            if question.lower() in ['quit', 'exit', 'выход']:
                print("Пока")
                break
                
            if question:
                answer = bot.ask(question)
                print(f"Ответ: {answer}\n")
                
        except KeyboardInterrupt:
            print("\nПока")
            break
        except Exception as e:
            print(f"Ошибка: {e}")

if __name__ == "__main__":
    main()
