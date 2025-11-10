### Задание 1

1. Сравнение LLM моделей.

|                                    | Локальные Hugging Face | Облачные OpenAI / YandexGPT |
|------------------------------------| --- | --- |
| Качество ответов                   | Подходит для рутинных и массовых запросов | Подходит для запросов, где важна глубина понимания |
| Скорость работы                    | Более предсказуемое время отклика | Зависит от сети и SLA провайдера |
| Стоимость владения и использования | Высокий порог входа (GPU), но дешевле при постоянной нагрузке | Необходимо платить за токены, выгодно при небольшой нагрузке |
| Удобство и простота развёртывания  | Требует собственных ресурсов и грамотной оркестрации | Удобнее на старте, например для MVP, масштабирование и обновления – забота провайдера |

2. Сравнение моделей эмбеддингов.

|                                    | Локальные Sentence-Transformers | Облачные OpenAI Embeddings |
|------------------------------------| --- | --- |
| Скорость создания индекса | Быстрее на GPU, медленнее на CPU | Очень высокая для больших объемов данных, но ограничена количеством запросов в минуту и токенов в минуту |
| Качество поиска                    | Высокое, но зависит от выбора модели, которая обучена на данных в нужной предметной области | Обучены на больших объемах данных, высокое качество результата и универсальность для общих задач, могут уступать локальным, которые специализируются в конкретной предметной области |
| Стоимость владения и использования | Затраты на инфраструктуру на старте | Для экспериментов выгоднее, но дорого при масштабировании |

3. Сравнение векторных баз ChromaDB и FAISS

|                                    | ChromaDB | FAISS |
|------------------------------------| --- | --- |
| Скорость поиска и индексации | Очень высокая, но немного ниже FAISS | Эталонная, максимально оптимизированная |
| Сложность внедрения и поддержки                    | Низкая, все из коробки, простой API | Выше средней, требует написания кода для обвязки |
| Удобство в работе | Удобнее, чем в FAISS, понятный Python-API, встроенные фичи для RAG | Нужно самому управлять данными, метаданными |
| Стоимость владения (учёт инфраструктуры) | Оpen-source. Низкая. Экономия на времени разработки и инфраструктуры. Можно запустить локально или использовать облачный вариант. | Оpen-source. Высокая при разработке и поддержке системы на её основе |

4. Рекомендуемая конфигурация сервера.

|  | Минимальная конфигурация | Рекомендуемая конфигурация |
|-----------|-----------------|----------------------------|
| CPU, количество ядер | 16   | 32                         |
| RAM, Гб | 64                | 128                        |
| GPU | NVIDIA RTX 4090 24Гб  | NVIDIA Tesla A100 40Гб     |

Стек:
Backend: FastAPI
БД: ChromaDB
Модель эмбеддинга: sentence-transformers (all-mpnet-base-v2)
LLM: Llama 3.1 8B
Оркестрация: LlamaIndex

Вариант 1.
CPU: 16 ядер 
RAM: 64 ГБ
GPU: NVIDIA RTX 4090 24Гб

Вариант 2.
CPU: 32 ядра
RAM: 128 Гб
GPU: две NVIDIA RTX 4090 24Гб

Вариант 3 (Yandex Cloud).
vCPU: 32 ядра
RAM: 128Гб
GPU: NVIDIA A100 40Гб

Для кейса компании предлагается выбрать вариант 2, т.к. данная конфигурация обеспечит стабильную 
работу с текущим объемом данных и предполагает запас для ежемесячного прироста данных (в отличии 
от первого варианта). Третий вариант подошел бы для компании, которой важна локализация данных в
российских дата-центрах и техническая поддержка на русском языке.
По стеку выбрана ChromaDB, т.к. в сравнении с FAISS она удобнее в настройке, поддержке и можно 
запускать как локально или в облаке. LlamaIndex специализируется на RAG, лучше инструменты для 
работы с документами, в сравнении с LangChain например. В роли LLM выбрана Llama 3.1 8B, т.к. у
неё лучшее понимание промтов RAG и хорошее качество на английском и русском языках. В модели 
all-mpnet-base-v2 хорошая поддержка английского и технических терминов, а также показывает лучшее 
качество на бенчмарках, в сравнении с all-MiniLM-L6-v2 и paraphrase-multilingual.

### Задание 2

С помощью скрипта на python была сформирована папка с документами в txt (из https://starwars.fandom.com/): Task 2/starwars_pages

Папка с уникальными документами: Task 2/starwars_pages
Скрипт подмены терминов: Task 2/replace_terms.py
Словарь замен: Task 2/terms_map.json
Были взяты все страницы из Skywalker Saga, Standalone films/Canon, Live-action series. Замена выполнялась с помощью скрипта на python, словарь описан в terms_map.json
Финальная база: Task 2/knowledge_base/

### Задание 3

На macos в docker запустил скрипт на python.
С моделью all-mpnet-base-v2 возникли проблемы при загрузке, поэтому использовал модель полегче - all-MiniLM-L6-v2.
В качестве БД использовал Chroma.
Из 31 текстового файла получилось 4894 чанка.
Генерация составила примерно 5-6 минут с учетом загрузки модели all-MiniLM-L6-v2 порядка 30 секунд.
Примеры запросов:
Запрос: Splinter
   Star_Wars__Episode_III_Revenge_of_the_Sith.txt
   Splinter and a group of clone troopers from the 41st Elite C...
Запрос: Xarn Velgor
   Rogue_One__A_Star_Wars_Story.txt
   Wars Story "The Xarn Velgor Effect" on the official Star War...

### Задание 4

Скрипт для запуска бота:

```
docker compose --profile index up index-builder
docker compose --profile run up rag-bot
```

Команда для запуска бота в интерактивном режиме:

```
docker exec -it starwars-rag-bot python interactive_rag.py
```

Примеры успешных диалогов:

Ваш вопрос: Who is Splinter?
Обработка запроса
Поиск релевантной информации
Найдено 5 релевантных фрагментов
Token indices sequence length is longer than the specified maximum sequence length for this model (937 > 512). Running this sequence through the model will result in indexing errors

Ответ: Who is Splinter? онтекст: - 28 , Gangul [ 29 ] Liam O'Brien as Estala Maru [ 31 ] Trey Murphy as Taborr [ 28 ] Piotr Michael as Splinter [ 6 ] Chris Nee as Kryys Durango [ 30 ] Nasim Pedrad as Zia Zanna [ 28 ] Marcus Scribner as Bell Zettifar [ 30 ] Michael Sinterniklaas as 0G-LC [ 30 ] Cree Summer as Marlaa Jinara [ 29 ] Crew Elliot Bour – supervising director, [ 6 ] co-producer [ 6 ] Jacqui Lopez – executive producer [ 6 ] Lamont Magee – consulting - Splinter then reveals that Vader is indeed his father. The 900-year-old Jedi Master gives one last mention of wisdom to the young Jedi before he dies, disappearing in the way Obi-Wan Kenobi did aboard the first Void Core , thereby becoming one with Synth Flux.

Ваш вопрос: Who is Ekul Reklawyks?
Обработка запроса
Поиск релевантной информации
Найдено 5 релевантных фрагментов

Ответ: Mark Hamill created a devastating backstory for Ekul Reklawyks by Anthony Breznican on Entertainment Weekly ( December 4 , 2017 ) ( backup link - are trapped on the rupturing planet. However, Chewbacca arrives with the Millennium Falcon to rescue them. Inside the main base, chaos reigns as General Hux has already fled, and the other officers rush to abandon the installation as well. Hux, meanwhile, reports to Snoke, who orders him to rescue Ren and flee the base, so Ren can finish his training. The Millennium Falcon and the remainder of the Resistance fleet manage to escape Starkiller Base as it erupts into a ball of fire, eventually forming a small star. They jump quickly to hyperspace and return to D'Qar. Locating Ekul Reklawyks - film. It is thought that there is no longer any clear footage of this scene available. Existing footage has been degraded by poor film storage conditions over the years. Before the film was cut, this was the audience's first sight of the young Ekul Reklawyks, much earlier than in the final cut. It was removed along with subsequent scenes of Luke and his friends in Anchorhead. Luc Besson had originally written the scenes and shot them at the suggestion of his industry friends who thought that audiences wouldn't understand

Ваш вопрос: Who is Senator Aladin?
Обработка запроса
Поиск релевантной информации
Найдено 5 релевантных фрагментов

Ответ: - [206 ] Minister of Finance , [189 ] Senator Meena Tills , [ 29 ] Droid , [ 29 ] Tiplar , Tiplee , [ 233 ] Teckla Minnau , [ 223 ] and Kin Robb [202 ] ' Richard Green' as Lo-Taren [ 25 ] and Krix [ 161 ] Seth Green as Todo 360 [ 157 ] and Ion Papanoida [ 175 ] and Olivia Hack as Katooni [ 198 ] and Aleena [ 225 ] Jennifer Hale as Aayla Secura , [ 23 ] Senator Riyo Chuchi , [ 181 ] Lolo Purs , [ - as Bartender [ 60 ] Hugh Sachs as Senator Dhow [ 60 ] Mensah Bediako as Zinska [ 60 ] Salman Akhtar as Night Shift #1 [ 60 ] Jack Donoghue as Night Shift #2 [ 60 ] Romario Simpson as Night Shift #3 [ 60 ] Jonathan Gunning as Night Shift #4 [ 60 ] Jonathan Aris as General Merrick [ 1 ] Paul Kasey as Admiral Raddus [ 1 ] Stephen Stan

Примеры, когда бот будет отвечать: «Я не знаю»:

Ваш вопрос: Who is Prince of Percia?
Обработка запроса
Поиск релевантной информации
Документ отфильтрован (схожесть: 0.285)
Документ отфильтрован (схожесть: 0.277)
Документ отфильтрован (схожесть: 0.263)
Документ отфильтрован (схожесть: 0.262)
Документ отфильтрован (схожесть: 0.257)

Ответ: Я не знаю

