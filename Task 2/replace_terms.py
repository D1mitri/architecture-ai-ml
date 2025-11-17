import glob
import os

def simple_replace():

    replacements = {
        "Darth Vader": "Xarn Velgor",
        "Death Star": "Void Core",
        "The Force": "Synth Flux",
        "Luke Skywalker": "Ekul Reklawyks",
        "First Order": "Second Order",
        "George Lucas": "Luc Besson",
        "Senator Amidala": "Senator Aladin",
        "Anakin Skywalker": "Nikana Reklawyks",
        "Yoda": "Splinter"
    }

    output_dir = "knowledge_base/"
    os.makedirs(output_dir, exist_ok=True)
    
    total_changes = 0
    
    for file_path in glob.glob("starwars_pages/*.txt"):
        filename = os.path.basename(file_path)
        output_path = os.path.join(output_dir, filename)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            file_changes = 0

            for old, new in replacements.items():
                content_lower = content.lower()
                old_lower = old.lower()
                
                start = 0
                while True:
                    pos = content_lower.find(old_lower, start)
                    if pos == -1:
                        break

                    content = content[:pos] + new + content[pos + len(old):]
                    content_lower = content.lower()
                    file_changes += 1
                    start = pos + len(new)
            
            if file_changes > 0:
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"{filename}: {file_changes} замен")
                total_changes += file_changes
            else:
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(original_content)
                
        except Exception as e:
            print(f"Ошибка в {filename}: {e}")

    print(f"Готово! Всего замен: {total_changes}")
    print(f"Файлы сохранены в: {output_dir}")

simple_replace()
