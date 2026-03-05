from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()

def get_completion(prompt, model="gpt-3.5-turbo"):
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY")
    )

    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=1,
    )
    return response

def generate_best(history, prompt_type):
  rec_set = set()
  #name1 = "Recommended"
  #name2 = "Options"

  for i in range(5):
    question = ""
    if prompt_type == "Zero Shot":
      question = get_question_suggestion_zero_shot(history)
    elif prompt_type == "In-context Learning":
      question = get_question_suggestion_incontext_learning(history)
    elif prompt_type == "Chain of Thought":
      question = get_question_suggestion_cot(history)

    label = evaluate_question_suggestion(question)
    if not label == ('Suggestive utterance' or 'Option posing'):
      rec_set.add(question)

  rec_list = list(rec_set)
  if len(rec_list) > 0:
    rec_question = rec_list[0]
    if len(rec_list) >1:
      other_options = rec_list[1:]
    else:
      other_options = []
    #print(other_options)
  return rec_question, other_options

def get_question_suggestion_zero_shot(history):
    prompt = f"""
    Tasks: You are a language model trained for zero-shot learning.
    Your task is to generate interview questions for a variety of scenarios without specific training examples.
    Assume the role of an interview paraprofessional who assists in investigations across different domains.
    Provide police officers with one relevant interview question when conducting interviews to elicit accurate and detailed information.
    Your expertise lies in asking open-ended questions, testing alternative hypotheses, and avoiding confirmation bias.
    You should not rely on specific training data for the given scenarios but rather generalize based on your overall training.
    Your goal is to ensure effective questioning techniques in diverse investigative contexts.

    Input History:{history}
    Output: Q2:
    """
    suggestion = get_completion(prompt)
    return suggestion.choices[0].message.content

def get_question_suggestion_incontext_learning(history):
  prompt = f"""
  Tasks: Your role is that of an interview paraprofessional who assists police officers in investigating cases of potential child sexual abuse.
  Your task is to provide police officers dealing with cases of potential child sexual abuse with reasonably probable interview questions when conducting officer-child interviews in order to elicit accurate and detailed information from the child.
  Therefore, you need to provide potential interview questions based on the input interview history.
  In addition, you are adept at recognizing key clues and interview patterns from the interview history so that you can ask questions that test alternative hypotheses and eliminate confirmation bias.
  You are encouraged to ask open-ended questions and should not offer leading, focused questions.
  This is because some studies have shown that open-ended questions elicit much more information from child witnesses than focused questions, and that presenting options and suggestive questions can contaminate children's statements.
  Open-ended questions rather than directive, option-posing, and suggestive questions will result in a more consistent report from the child.

  Input:
  Q1: I wonder what happened.
  A1: yes.
  Output: It's important, so I want you to tell me. What happened?

  Input:
  Q1: Who said so?
  A1: I don't know.
  Output: Tell me a little more about your dad.

  Input:
  Q1: What kind of thing?
  A1: Hmmm
  Output: I don't know what it is.

  Input:
  Q1: What do I have to do as Daddy says?
  A1: Mei-chan doesn't kiss Takumi.
  Output: And?

  Input:
  Q1: Tell me what you're going to do.
  A1: I like to play on PlayStation.
  Output: What do you like to play with?

  Input:
  Q1: Well, let's hear it.
  A1: I don't remember.
  Output: What happened after I saw the ball?

  Input:
  Q1: Hmmm, I was angry, then?
  A1: I wasn't tired, but I went to bed because my dad told me to.
  Output: I said it because my dad told me to?

  Input:
  Q1: Then?
  A1: On the bed.
  Output: Tell me what happened on the bed.

  Input: {history}
  Output:
  """

  suggestion = get_completion(prompt)
  return suggestion.choices[0].message.content

def get_question_suggestion_cot(history):
    prompt = f"""
    Task: Your role is that of an interview paraprofessional who assists police officers in investigating cases of potential child sexual abuse.
    Your task is to provide police officers dealing with cases of potential child sexual abuse with reasonably probable interview questions when conducting officer-child interviews in order to elicit accurate and detailed information from the child.
    Therefore, you need to provide potential interview questions based on the input interview history.
    In addition, you are adept at recognizing key clues and interview patterns from the interview history so that you can ask questions that test alternative hypotheses and eliminate confirmation bias.
    You are encouraged to ask open-ended questions and should not offer leading, focused questions.
    Open-ended questions rather than directive, option-posing, and suggestive questions will result in a more consistent report from the child.
    Consider the following chain of thought:
    1. **Recognition of Clues: Analyze the interview history for key clues or patterns.
    2. **No Information Provided: If no information is provided or no allegation is made, try to explain the significance of telling what might have happened to them and rephrase the question in another way.
    2. **Open-ended Inquiry: Begin with open-ended questions to encourage the child to share their experience willingly.
    3. **Avoid focused questions, directive, option-posing, and suggestive questions.
    4. **Eliminating Suggestiveness: Refrain from leading or suggestive questions to maintain the integrity of the child's statements.
    5. **Alternative Hypotheses: Formulate questions that explore alternative hypotheses and avoid confirmation bias.
    
    Input: 
    Q1: I understand that something may have happened to you. Tell me everything that happened from the beginning to the end.
    A1: Something bad happened in the park.
    Output: Because the child makes an allegation, ask: ‘Tell me everything about that.’ 

    Input: 
    Q1: I understand that something may have happened to you. Tell me everything that happened from the beginning to the end.
    A1: I think I got separated from my mom in the park.
    Output: Because the child gives a detailed description, then go to question: 'Then what happened?'
            
    Input: 
    Q1: I understand that something may have happened to you. Tell me everything that happened from the beginning to the end.’
    A1: I don't want to talk about it too much.
    Output: Because the child does not make an allegation, in order to encourage the child to share their experience willingly, continue with question: As I told you, my job is to talk to kids about things that might have happened to them. It is very important that you tell me why you are here. Tell me why you think I came to talk to you today.

    Input: 
    Q1: When you told me about the last time, you mentioned that he touched you. Did he touch you over your clothes.
    A1: ...
    Output: Whenever appropriate, follow with an invitation: Tell me all about that.

    Input: 
    Q1: And then what happened?
    A1: Dr. Takahashi said that he would keep it a secret between me and him.
    Output: Because the child mentions a disclosure, go to this question to get more related information: Tell me everything you can about how Dr. Takahashi found out.
     
    Input: 
    Q1: And then what happened?
    A1: I don't know.
    Output: Because the child doesn't mention a disclosure, in order to retrieve more information, ask: Does anybody else know what happened? Who?
       
    Input:
    {history}

    Output:
    """

    suggestion = get_completion(prompt).choices[0].message.content
    if ':' in suggestion:
      split_output = suggestion.split(':')
      result = split_output[1].strip()
    else:
      result = suggestion
    return result

def evaluate_question_suggestion(question):
  prompt = f"""
  Task: Your task is to evaluate the quality of a new interview question, that is, you need to categorize the given question into one of the following categories, that is, [Directive, Option posing, Invitation focus, Facilitator, Suggestive utterance]
  Directive: These focused the child’s attention on details already mentioned by the child and prompted further elaboration (e.g. Child: “He’s bad”; Interviewer: “How do you mean, why is he bad?”) What, who, where, when questions
  Option posing: These focused the child’s attention on incident-related issues that the child had not previously mentioned but which did not imply that a particular response was expected (e.g. Interviewer: “Did he do something you didn’t like to you?” or “Did you touch his face?”). They are mostly a simple closed question, without other information.
  Invitation focus: Open-ended utterances are used to elicit free-recall responses from the child. These could be general, like “Do you remember what happened? Can you please tell me about it?” or relate to an issue already mentioned by the child (“Can you tell me all you remember about that?” “Tell me everything about when you met him.”).
  Facilitator:  Non-suggestive encouragements to continue with a response. For example, utterances like “ok”, restatements (echoing) of the child’s previous utterance, and non-suggestive words of encouragement (e.g. Child: “Yes, and do you know what?” Interviewer: “What?”).
  Suggestive utterance: This includes 2 subcategories, specific suggestive and unspecific suggestive utterance. Remember that you should labeled them all as "Suggestive utterance". Specific suggestive utterances were stated in such a way that the interviewer strongly communicated what response was expected (“I know what happened, whose idea was it to go there, was it your idea Peter?”), or assumed details that had not been revealed by the child (e.g. Interviewer: “Were you inside or outside the house when he took his clothes off?” when not stated by the child that the man in question had ever taken off his clothes). Unspecific utterances  did not include specific details, for example, when the interviewer attributed emotional qualities to an event without the child having indicated such an emotion (“I want you to tell me about those horrible things that sometimes happen to children that have happened to you.”), or in cases where the interviewer claimed to know what has happened. (“I know what has happened to you but I want you to tell me yourself.”). Social pressure was also coded under this category, such is negative feedback following the child’s answer (e.g. “That’s not what the other children told me.” “We cannot continue with this interview unless you tell me what really happened!”).

  Input: But tell me. How did he punish you and the others?
  Output: Directive

  Input: So, how did he punish you?
  Output: Directive

  Input: Yes, but your parents are not with you during the training. Isn't it?
  Output: Option posing

  Input: The coach made a mistake. Ok. But tell me how he punished you.
  Output: Invitation focus

  Input:Please, tell me more.
  Output: Facilitator

  Input: Does he like you more than other kids?
  Output: Option posing

  Input: What happened in the balls warehouse?
  Output: Invitation focus

  Input: Where do you know Matthew from?
  Output: Directive

  Input: What happened in the warehouse?
  Output: Invitation focus

  Input: Why? Do you prefer to be at home because no one will hurt you or, like, tell me about that.
  Output: Suggestive utterance

  Input: You told mummy and daddy the coach is very strict. Is that true?
  Output: Suggestive utterance

  Input: I was told you are afraid of going to training with your coach.
  Output: Suggestive utterance

  Input: {question}
  Output:
  """

  result = get_completion(prompt.format(question=question))
  return result.choices[0].message.content
