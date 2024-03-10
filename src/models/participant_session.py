from dataclasses import dataclass

from src.models.participantfile import ParticipantFile

@dataclass
class ParticipantSession:
    textgrid_participant_file: ParticipantFile
    wav_participant_file: ParticipantFile
    participant_audio_id: str