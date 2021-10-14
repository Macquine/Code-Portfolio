import random
import os
from sys import platform
from GetPathOfFile import get_path

def retrievequestions(category:str, difficulty_level:str, filename:str) -> list:
    """Returns a list with questions and answers based on specified category and level of difficulty: easy/medium/hard/extreme."""
    file_path = get_path(filename)
    file = open(file_path,'r', encoding="utf8")
    data = file.read()
    file.close()
    
    categorydata = data.split('#')
    category_questions = list()
    for line in categorydata:
        categorysplit = line.split('\n')
        if category in categorysplit[0]:
            difficultysplit = line.split('&')
            for chunk in difficultysplit:
                levelquestions = chunk.split('\n')
                if difficulty_level in levelquestions[0]:
                    for level in levelquestions:
                        if difficulty_level in level:
                            continue
                        else:
                            category_questions.append(level)
    return category_questions

def get_questions(total_questions: int, difficulty_level = 'Random',question_type = 'Random') -> dict:
    files =['NormalQuestion.txt','FillinQuestions.txt','PhotoQuestions.txt']
    if question_type == 'Normal':
        filename = files[0]
    elif question_type == 'Fill in':
        filename = files[1]
    elif question_type == 'Photo':
        filename = files[2]
    elif question_type == 'Random':
        rd_int= random.randint(0,1)
        filename = files[rd_int]

    categories = ['Wetenschap','Informatica','Geografie','Sport']
    difficulties = ['Easy','Medium','Hard','Extreme']
    temp_question_dict = dict() #Tijdelijke dictionary
    temporary_cat_q = list() #Opgehaalde vragen op basis van Categorie en Moeilijkheidsgraad
    question_set = set() #Random want unordered
    final_question_dict = dict()
    while len(final_question_dict) < total_questions: #Hij heeft nog niet genoeg vragen opgehaald
        if difficulty_level == 'random':
            rd_int_cat = random.randint(0,len(categories)-1)
            rd_int_dif = random.randint(0,len(difficulties)-1)
            temporary_cat_q = retrievequestions(categories[rd_int_cat],difficulties[rd_int_dif],filename)#Random
        else:
            rd_int_cat = random.randint(0,len(difficulties)-1)
            temporary_cat_q = retrievequestions(categories[rd_int_cat], difficulty_level,filename)#Random
        question_answers = list()
        for line in temporary_cat_q:
            if '^' in line and len(question_answers) != 0:
                question = question_answers[0]
                answers = question_answers[1:]
                question_set.add(question) #Voor randomizatie
                temp_question_dict[question] = answers
                question_answers.clear()
                continue
            else:
                question_answers.append(line)

        if len(question_set) > 0:
            random_question = question_set.pop()
            if random_question in final_question_dict: #Voorkomt dat er toevallig dubbele vragen in komen
                continue
            else:
                final_question_dict[random_question] = temp_question_dict[random_question]
    return final_question_dict
