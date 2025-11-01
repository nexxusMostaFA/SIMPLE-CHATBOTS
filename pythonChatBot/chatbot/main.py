import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import string

# Load JSON data from file
def load_json_file(file_path):
    with open(file_path) as file:
        data = json.load(file)
    return data

# Save JSON data to file
def save_json_file(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file)

# Preprocess text by removing punctuation and converting to lowercase
def preprocess(text):
    return ''.join([char.lower() for char in text if char not in string.punctuation])

# Find the best answer using cosine similarity
def find_the_best_answer(user_question, questions):
    # Preprocess questions and user question
    processed_questions = [preprocess(q) for q in questions]
    processed_user_question = preprocess(user_question)

    # Calculate TF-IDF vectors for questions
    vectorizer = TfidfVectorizer().fit(processed_questions)
    questions_tfidf = vectorizer.transform(processed_questions)
    user_question_tfidf = vectorizer.transform([processed_user_question])

    # Compute cosine similarity
    similarities = cosine_similarity(user_question_tfidf, questions_tfidf).flatten()
    best_match_index = similarities.argmax()
    best_match_score = similarities[best_match_index]

    # Check if the similarity score is above a threshold
    threshold = 0.7
    if best_match_score >= threshold:
        return questions[best_match_index]
    return None

# Get response from JSON data based on a matched question
def get_response(user_question, data):
    for category in data["app_help"]["categories"]:
        for q in category["questions"]:
            if q["question"] == user_question:
                return q["answer"]
    return "Sorry, I couldn't find that question."

# Main chatbot function
def chatbot():
    file = load_json_file("file.json")

    while True:
        user_question = input("YOU: ")
        if user_question.lower() == "quit":
            break

        questions = [q["question"] for category in file["app_help"]["categories"] for q in category["questions"]]
        best_match = find_the_best_answer(user_question, questions)

        if best_match:
            answer = get_response(best_match, file)
            print(f'BOT: {answer}')
        else:
            print("Sorry, Can you ask me the question by another way?")

if __name__ == "__main__":
    chatbot()
