import json
import os

def add_question():
    category = input("Categoría: ")
    question = input("Pregunta: ")
    options = []
    for i in range(4):
        option = input(f"Opción {i+1}: ")
        options.append(option)
    answer = input("Respuesta correcta exactamente como en opciones: ")

    return {
        "category": category,
        "question": question,
        "options": options,
        "answer": answer
    }

def main():
    base_path = os.path.dirname(__file__)
    file_path = os.path.join(base_path, "questions.json")

    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            questions = json.load(file)
    else:
        questions = []

    while True:
        new_question = add_question()
        questions.append(new_question)

        cont = input("¿Agregar otra pregunta? (s/n): ").lower()
        if cont != 's':
            break

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(questions, file, ensure_ascii=False, indent=4)
    print("✅ Preguntas guardadas exitosamente en questions.json.")

if __name__ == "__main__":
    main()
