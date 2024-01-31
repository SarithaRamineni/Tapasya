from transformers import TapasTokenizer, TapasForQuestionAnswering
import pandas as pd
import os
from test import database_query

os.chdir(r'C:\Users\mmoraleszapata\OneDrive - Hitachi Vantara\Desktop\Archivos varios\Hackaton')




def option_mapping(selected_dataset):
    mapping = {'zoom events': 'zoom_data.csv', 'test': 'this.csv',
               'SFDC Campaign': 'sfdc_campaign.csv', 'SFDC Opportunity': 'sfdc_opportunity.csv', 'city': 'city'}
    option_selected = mapping[selected_dataset]
    df_selected = database_query(option_selected)
    #df_selected = pd.read_csv(option_selected)
    print(df_selected)
    df_selected = df_selected.astype(str)
    return df_selected


def questions_processing(input_questions):
    question_lists = input_questions.split(',')
    print(f'THESE ARE THE QUESTIONS: {question_lists}')
    return question_lists

def model_response(selected_dataset, selected_table, input_questions):
    dataset = database_query(selected_dataset, selected_table)
    df_selected = dataset.astype(str)
    questions = questions_processing(input_questions)
    answers, agg = tapas_predict(df_selected, questions)
    return answers, agg


def tapas_predict(dataset, questions):

    model_name = "google/tapas-base-finetuned-wtq"
    model = TapasForQuestionAnswering.from_pretrained(model_name)
    tokenizer = TapasTokenizer.from_pretrained(model_name)
    queries = questions
    table = dataset

    inputs = tokenizer(table=table, queries=queries, padding='max_length', return_tensors="pt",  max_length=3500)
    outputs = model(**inputs)
    predicted_answer_coordinates, predicted_aggregation_indices = tokenizer.convert_logits_to_predictions(
        inputs, outputs.logits.detach(), outputs.logits_aggregation.detach()
    )

    # let's print out the results:
    id2aggregation = {0: "NONE", 1: "SUM", 2: "AVERAGE", 3: "COUNT"}
    aggregation_predictions_string = [id2aggregation[x] for x in predicted_aggregation_indices]
    print(f'COORDINATES {predicted_answer_coordinates}')
    answers = []
    predicted_agg = 'NONE'
    for coordinates in predicted_answer_coordinates:
        if len(coordinates) == 1:
            # only a single cell:
            answers.append(table.iat[coordinates[0]])
        else:
            # multiple cells
            cell_values = []
            for coordinate in coordinates:
                cell_values.append(table.iat[coordinate])
            answers.append(", ".join(cell_values))

    print("")
    for query, answer, predicted_agg in zip(queries, answers, aggregation_predictions_string):
        print(query)
        if predicted_agg == "NONE":
            print("Predicted answer: " + answer)
        else:
            print("Predicted answer: " + predicted_agg + " > " + answer)

    print(f'\n\n THIS ARE THE ANSWERS: {answers}')
    return answers, predicted_agg
