from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import Question, Category


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://username:password@localhost:5432/trivia'
db = SQLAlchemy(app)




categorie_data = ["Science","Art","Geography","History","Entertainment","Sports"]

questions_data = [{
        "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?",
        "answer": "Maya Angelou",
        "difficulty": "2",
        "category": "4",
},
{
        "question": "What boxer's original name is Cassius Clay?",
        "answer": "Muhammad Ali",
        "difficulty": "1",
        "category": "4",
},
{
        "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?",
        "answer": "Apollo 13",
        "difficulty": "4",
        "category": "5",
},
{
        "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?",
        "answer": "Tom Cruise",
        "difficulty": "4",
        "category": "5",
},
{
        "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?",
        "answer": "Edward Scissorhands",
        "difficulty": "3",
        "category": "5",
},
{
        "question": "Which is the only team to play in every soccer World Cup tournament?",
        "answer": "Brazil",
        "difficulty": "3",
        "category": "6",
},
{
        "question": "Which country won the first ever soccer World Cup in 1930?",
        "answer": "Uruguay",
        "difficulty": "4",
        "category": "6",
},
{
        "question": "Who invented Peanut Butter?",
        "answer": "George Washington Carver",
        "difficulty": "2",
        "category": "4",
},
{
        "question": "What is the largest lake in Africa?",
        "answer": "Lake Victoria",
        "difficulty": "2",
        "category": "3",
},
{
        "question": "In which royal palace would you find the Hall of Mirrors?",
        "answer": "The Palace of Versailles",
        "difficulty": "3",
        "category": "3",
},
{
        "question": "The Taj Mahal is located in which Indian city?",
        "answer": "Agra",
        "difficulty": "2",
        "category": "3",
},
{
        "question": "Which Dutch graphic artist–initials M C was a creator of optical illusions?",
        "answer": "Escher",
        "difficulty": "1",
        "category": "2",
},
{
        "question": "La Giaconda is better known as what?",
        "answer": "Mona Lisa",
        "difficulty": "3",
        "category": "2",
},
{
        "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?",
        "answer": "Jackson Pollock",
        "difficulty": "2",
        "category": "2",
},
{
        "question": "What is the heaviest organ in the human body?",
        "answer": "The Liver",
        "difficulty": "4",
        "category": "1",
},
{
        "question": "Who discovered penicillin?",
        "answer": "Alexander Fleming",
        "difficulty": "3",
        "category": "1",
},
{
        "question": "Hematology is a branch of medicine involving the study of what?",
        "answer": "Blood",
        "difficulty": "4",
        "category": "1",
},
{
        "question": "Which dung beetle was worshipped by the ancient Egyptians?",
        "answer": "Scarab",
        "difficulty": "4",
        "category": "4",
}

]



def load_data():

    # create categories
    categories = []
    for data in categorie_data:
        categories.append(
            Category(type=data))    
    
    # create questions
    questions = []
    for data in questions_data:
        questions.append(
            Question(
                question= data["question"],
                answer= data["answer"],
                difficulty= data["difficulty"],
                category= data["category"],
            )
        )

    db.session.add_all(categories)
    db.session.add_all(questions)
    db.session.commit()


if __name__ == "__main__":
    load_data()
