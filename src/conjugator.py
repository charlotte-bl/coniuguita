import random
import csv

class ConjugatedVerb:
    """
    Class to stock the verbs information
    """
    def __init__(self, mood, tense, infinitive_translation, correct_form, person=None):
        self.mood = mood
        self.tense = tense
        self.person = person
        self.correct_form = correct_form
        self.infinitive_translation = infinitive_translation

def draw_mood(moods):
    """
    Function to randomly draw a verb mood
    """
    base_column_per_mood = {
        "Infinito": 0,  # 0-1
        "Participio": 2,  # 2-3
        "Gerundio": 4,    # 4-5
        "Indicativo": 6,  # 6-53
        "Congiuntivo": 54,  # 54-77
        "Condizionale": 78,  # 78-89
        "Imperativo": 90   # 90-94
    }
    mood = random.choice(moods)
    mood_column = base_column_per_mood.get(mood, 0)
    return mood, mood_column

def get_tense_offset(mood):
    """
    Function to get the offset compared to the tense regarding the mood 
    """
    if mood in ("Infinito", "Participio", "Gerundio"):
        tense_offset = {
            "Presente": 0,
            "Passato": 1
        }
    elif mood in ("Indicativo", "Congiuntivo", "Imperativo"):
        tense_offset = {
            "Presente": 0,  # only tense for imperative
            "Imperfetto": 6,
            "Passato remoto": 12,  # indicative tense
            "Passato": 12,  # subjunctive tense
            "Futuro semplice": 18,  # indicative tense
            "Trapassato": 18,  # subjunctive tense
            "Passato prossimo": 24,
            "Trapassato prossimo": 30,
            "Trapassato remoto": 36,
            "Futuro anteriore": 42,
            "Trapassato": 18
        }
    else:  # mood = condizionale
        tense_offset = {
            "Presente": 0,
            "Passato": 6
        }
    return tense_offset

def get_person_offset(mood):
    """
    Function to get the offset compared to the person regarding the mood (AND the tense implicitely)
    """
    if mood == "Imperativo":
        person_offset = {
            "Tu": 0,
            "Lui/Lei": 1,
            "Noi": 2,
            "Voi": 3,
            "Loro": 4,
        }
    else:
        person_offset = {
            "Io": 0,
            "Tu": 1,
            "Lui/Lei": 2,
            "Noi": 3,
            "Voi": 4,
            "Loro": 5,
        }
    return person_offset

def draw_tense_and_person(mood, mood_column, tenses_per_mood):
    """
    Function to generate a verb according to a set of moods and tenses knowing the mood
    """
    persons_per_mood = {
        "Indicativo": ["Io", "Tu", "Lui/Lei", "Noi", "Voi", "Loro"],
        "Congiuntivo": ["Io", "Tu", "Lui/Lei", "Noi", "Voi", "Loro"],
        "Condizionale": ["Io", "Tu", "Lui/Lei", "Noi", "Voi", "Loro"],
        "Imperativo": ["Tu", "Lui/Lei", "Noi", "Voi", "Loro"],
    }
    available_tenses = tenses_per_mood.get(mood, ["Presente"])
    available_persons = persons_per_mood.get(mood, ["Tu"]) 
    tense = random.choice(available_tenses)
    tense_offset = get_tense_offset(mood)
    tense_column = tense_offset.get(tense, 0) + mood_column
    person = None
    person_column = tense_column
    if mood in ("Indicativo", "Congiuntivo", "Condizionale", "Imperativo"):
        person = random.choice(available_persons)
        person_offset = get_person_offset(mood)
        person_column = person_offset.get(person, 0) + tense_column
    return tense, tense_column, person, person_column

def draw_row():
    """
    Function to randomly select a verb row, with a higher probability for the first few verbs
    """
    if random.randint(1, 10) == 10:
        return random.randint(5, 6)
    else:
        min_row = 7
        max_row = 81
        return random.randint(min_row, max_row)

def access_csv(row, column):
    """
    Function to access the case associated to a row and a column in the .csv file of the verbs
    """
    with open('../data/verbs.csv', 'r', newline='', encoding='latin-1') as file:
        csv_reader = csv.reader(file)
        data = list(csv_reader)
        return data[row][column]

def create_verb(moods,tenses_per_mood):
    """
    Function to generate a verb, a mood, a tense, a person for the tenses with persons and stock it in a class
    """
    mood, mood_column = draw_mood(moods)
    tense, _, person, person_column = draw_tense_and_person(mood, mood_column, tenses_per_mood)
    row = draw_row()
    correct_form = access_csv(row, person_column)
    infinitive = access_csv(row, 0)
    verb = ConjugatedVerb(mood, tense, infinitive, correct_form, person)
    return verb

if __name__ == '__main__':
    moods =["Indicativo", "Condizionale", "Congiuntivo", "Imperativo", "Participio", "Gerundio"]
    tenses_per_mood={
                    "Infinito": ["Presente", "Passato"],
                    "Participio": ["Presente", "Passato"],
                    "Gerundio": ["Presente", "Passato"],
                    "Indicativo": ["Presente", "Imperfetto", "Passato remoto", "Futuro semplice", 
                                   "Passato prossimo", "Trapassato prossimo", "Trapassato remoto", "Futuro anteriore"],
                    "Congiuntivo": ["Presente", "Imperfetto", "Passato", "Trapassato"],
                    "Condizionale": ["Presente", "Passato"],
                    "Imperativo": ["Presente"]
                }
    

    verb = create_verb(moods,tenses_per_mood)
    print(verb.correct_form, verb.infinitive_translation)
