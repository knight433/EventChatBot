import spacy
import time as tt

nlp = spacy.load('en_core_web_lg')

events_names = ['ai fiesta', 'agones']

event_dic = {
    'ai fiesta': {
        'name': 'AI Fiesta',
        'date': "18/02/2023",
        'week': 38,
        'day': 227,
        'host': 'The department of AIML',
        'event': []
    },
    'agones': {
       'name': "AGONES",
       'date': "17/08/2024",
       'week': 33,
       'day': 228,
       'host': 'RSC',
       'event': ['cricket', 'football']
    }
}

event_dic_events = {
    'agones': {
        'cricket': {'date': '18/08/2024',
                    'registration': 'Will be taken care by the department',
                    'registration_fee': '300 per team',
                    'venue': 'main ground'},
        'football': {'date': '17/08/2024',
                     'registration': 'Will be taken care by the department',
                     'registration_fee': '500 per team',
                     'venue': 'main ground'}
    }
}

current_topic = None


# to check if there are any events in the sentence
def EventNameIdf(text):

    global current_topic  # idk how
    words = text.split()

    for i in range(len(words) - 1):
        event_candidate = f"{words[i]} {words[i+1]}"
        if event_candidate in events_names:
            current_topic = event_candidate
            return event_candidate

    for i in range(len(words)):
        if words[i] in events_names:
            current_topic = words[i]
            return words[i]

    return None


# for any event related queries
def eventRelatedQur(text, token_text):
    event_topic = None
    global current_topic  # idk how
    feast = EventNameIdf(text)
    register_verbs = ['sign', 'register', 'enroll']

    if current_topic is None:

        if feast is None:
            return 'there are no feasts named that'

        else:
            feast = current_topic
            event_list = event_dic[feast]['event']

    elif current_topic != feast and feast is not None:

        current_topic = feast
        event_list = event_dic[feast]['event']
    else:
        feast = current_topic
        event_list = event_dic[current_topic]['event']

    result = []

    for i in token_text:
        if i.tag_ == 'NN' and i.text in event_list:
            event_topic = i.text

    wrb_var = []

    # for when and where query
    for i in token_text:
        if i.tag_ == 'WRB':
            wrb_var.append(i.text)

    if 'where' in wrb_var or 'when' in wrb_var:
        result.append(f'{event_topic} will be held on {event_dic_events[feast][event_topic]["date"]}'
                      f' in {event_dic_events[feast][event_topic]["venue"]}')

    for i in token_text:
        if i.pos_ == 'VERB' and i.lemma_ in register_verbs:
            result.append(f'{event_topic} registration {event_dic_events[feast][event_topic]["registration"]}'
                          f' and will cost {event_dic_events[feast][event_topic]["registration_fee"]}')
            break
        elif i.tag_ == 'WP':
            if i.text == 'what':
                result.append(f'The events are {event_dic[feast]["event"]}')
                break
            else:
                result.append(f'The event is organized by {event_dic[feast]["host"]}')
                break
    return result


# response for time related queries
def timeResponse(time_token, keyword, timeline_number, sen_type):
    time_token_keyword = None
    cur_time = tt.localtime()
    cur_month = cur_time.tm_mon
    cur_year = cur_time.tm_year
    cur_day = cur_time.tm_yday
    cur_week = tt.strftime('%U', cur_time)

    event_list = []

    if sen_type == 1:

        if 'month' in time_token:
            time_token_keyword = 'month'
            for events in events_names:
                if int(event_dic[events]['date'][3:5]) in range(cur_month, cur_month+6):
                    event_list.append(event_dic[events]['name'])

        elif 'year' in time_token:
            time_token_keyword = 'year'
            for events in events_names:
                if int(event_dic[events]['date'][6:10]) in range(cur_year, cur_year+2):
                    event_list.append(event_dic[events]['name'])

        elif 'week' in time_token:

            time_token_keyword = 'week'
            for events in events_names:
                if event_dic[events]['week'] == int(cur_week)+timeline_number:
                    event_list.append(event_dic[events]['name'])

        return f"the upcoming events in next few {time_token_keyword} are: {', '.join(event_list)}"

    if sen_type == 2:
        if 'month' in time_token:
            time_token_keyword = 'month'
            for events in events_names:
                if int(event_dic[events]['date'][3:5]) == cur_month+timeline_number:
                    event_list.append(event_dic[events]['name'])

        elif 'year' in time_token:
            time_token_keyword = 'year'
            for events in events_names:
                if int(event_dic[events]['date'][6:10]) == cur_year+timeline_number:
                    event_list.append(event_dic[events]['name'])

        elif 'week' in time_token:
            time_token_keyword = 'week'
            for events in events_names:
                if event_dic[events]['week'] == int(cur_week)+timeline_number:
                    event_list.append(event_dic[events]['name'])

        elif any(element in time_token for element in ["yesterday", "today", "tomorrow"]):
            time_token_keyword = '(yet to add)'
            for events in events_names:
                if event_dic[events]['day'] == int(cur_day)+timeline_number:
                    event_list.append(event_dic[events]['name'])

        return f"the events in {keyword} {time_token_keyword} are/is: {', '.join(event_list)}"


# to get all the time Related words
def TimeRelatedWords(doc):

    time_related_tokens = []

    for token in doc:
        # Check for adverbs indicating time
        if token.dep_ in ["advmod", "npadvmod"] and token.text.lower() in ["yesterday", "today", "tomorrow"]:
            time_related_tokens.append(token.lemma_)

        # Check for time-related named entities
        if token.ent_type_ == "TIME" or token.ent_type_ == "DATE":
            time_related_tokens.append(token.lemma_)

        if token.text == "when":
            time_related_tokens.append(token.lemma_)

    return time_related_tokens


# response to all time related queries
def preTimeResponse(tokenized_text, time_token, event):
    words = [i.lemma_ for i in tokenized_text]

    if 'when' in words:

        try:
            date = event_dic[event]['date']
            return f'{event} is on {date}'
        except KeyError:
            text = [i.text for i in tokenized_text]
            text = ' '.join(text)
            return eventRelatedQur(text, tokenized_text)

    timeline_number = 0
    keyword = ''

    if 'yesterday' in time_token:
        timeline_number = -1
    elif 'today' in time_token:
        timeline_number = 0
    elif 'tomorrow' in time_token:
        timeline_number = 1
    else:
        keyword = 'this'
        for k in time_token:

            try:
                index = words.index(k)
                if words[index - 1] == 'next':
                    timeline_number = 1
                    keyword = 'next'
                elif words[index - 1] == 'previous':
                    timeline_number = -1
                    keyword = 'previous'
                elif words[index - 1] == 'few':
                    timeline_number = 5
                    keyword = 'few'
            except ValueError as ve:
                print('ValueError:', ve)  # Print the error message for debugging

    if timeline_number > 4:
        return timeResponse(time_token, keyword, timeline_number, 1)

    elif timeline_number <= 1:
        return timeResponse(time_token, keyword, timeline_number, 2)


def reply(msg):
    user_inp = msg.lower()
    token_text = nlp(user_inp)
    time_ = TimeRelatedWords(token_text)

    try:
        return preTimeResponse(token_text, time_, EventNameIdf(user_inp))
    except:
        return eventRelatedQur(user_inp, token_text)
