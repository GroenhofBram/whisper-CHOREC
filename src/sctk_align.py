from pandas import DataFrame

from models.participant_session import ParticipantSession


def get_repr_df(sesh_id_words_id, words) -> DataFrame:
    data = {
        'utterance_id': [sesh_id_words_id],
        'transcript': [words]
    }
    return DataFrame(data=data)
    