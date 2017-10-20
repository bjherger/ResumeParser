import logging

from gensim.utils import simple_preprocess

import lib

EMAIL_REGEX = r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}"
PHONE_REGEX = r"\(?(\d{3})?\)?[\s\.-]{0,2}?(\d{3})[\s\.-]{0,2}(\d{4})"


def candidate_name_extractor(input_string, nlp):
    input_string = unicode(input_string)

    doc = nlp(input_string)

    # Extract entities
    doc_entities = doc.ents

    # Subset to person type entities
    doc_persons = filter(lambda x: x.label_ == 'PERSON', doc_entities)
    doc_persons = filter(lambda x: len(x.text.strip().split()) >= 2, doc_persons)
    doc_persons = map(lambda x: x.text.strip(), doc_persons)

    # Assuming that the first Person entity with more than two tokens is the candidate's name
    candidate_name = doc_persons[0]
    return candidate_name


def extract_skills(resume_text):
    potential_skills_dict = dict()
    matched_skills = set()

    # TODO This skill input formatting could happen once per run, instead of once per observation.
    for skill_input in lib.get_conf('skills'):

        # Format list inputs
        if type(skill_input) is list and len(skill_input) >= 1:
            potential_skills_dict[skill_input[0]] = skill_input

        # Format string inputs
        elif type(skill_input) is str:
            potential_skills_dict[skill_input] = [skill_input]
        else:
            logging.warn('Unknown skill listing type: {}. Please format as either a single string or a list of strings'
                         ''.format(skill_input))

    for (skill_name, skill_alias_list) in potential_skills_dict.items():

        skill_matches = 0
        # Iterate through aliases
        for skill_alias in skill_alias_list:
            # Add the number of matches for each alias
            skill_matches += lib.term_count(resume_text, skill_alias.lower())

        # If at least one alias is found, add skill name to set of skills
        if skill_matches > 0:
            matched_skills.add(skill_name)

    return matched_skills


def extract_universities(resume_text):

    # Reference variables
    matched_universities = set()
    normalized_resume_text = ' '.join(simple_preprocess(resume_text))

    # Iterate through possible universities
    for university in lib.get_conf('universities'):

        university = ' '.join(simple_preprocess(university))
        university_count = lib.term_count(normalized_resume_text, university)

        if university_count > 0:
            matched_universities.add(university)

    return matched_universities
