from dataclasses import dataclass

from src.backend.segments import find_missing_segments
from src.backend.switch import switch


@dataclass
class AlignmentResult:
    mapping: list

    def missing_segments(self, long_duration_sec: int, min_gap_sec: int = 3) -> list:
        return find_missing_segments(self.mapping, long_duration_sec, min_gap_sec)

    def to_ass(self, input_ass_path: str, output_ass_path: str):
        switch(input_ass_path, output_ass_path, self.mapping)
