import sys
from typing import List, TextIO
from dataclasses import dataclass
from pathlib import Path

@dataclass
class Section:
    buffer: List[str]
    var: str
    include: bool
    else_section: 'Section'
    
    def __init__(self, var: str):
        self.var = var
        self.buffer = []
        self.include = False
        self.else_section = None

    def append(self, val: str):
        self.buffer.append(val)

    def add_else(self, else_sec: 'Section'):
        self.else_section = else_sec

def preprocess(file: TextIO) -> List[Section]:
    sections: List[Section] = [Section("__main__")]
    section: Section = None
    for line in file:
        if line.startswith("#"):
            line_without_comment: str = line.lstrip("#")
            if "ifdef" in line_without_comment:
                edited_line: str = line_without_comment.lstrip(" ")
                split_line: List[str]  = edited_line.split(" ")
                sections.append(Section(split_line[1]))
                continue
            elif "elsedef" in line_without_comment:
                if section.var == "__main__":
                    raise SyntaxError("elsedef directive without corresponding ifdef!")
                section.add_else(Section(""))
                section = section.else_section
                continue
            elif "endif" in line_without_comment:
                section = None
                sections.append(Section("__main__"))
                continue

        if section is None:
            section: Section = sections[len(sections)-1]
        section.append(line)
    return sections

def get_defined(sections: List[Section], defined_vars: List[str]) -> List[Section]:
    final_sections: List[Section] = []
    for section in sections:
        if section.var == "__main__":
            final_sections.append(section)
        elif section.var in defined_vars:
            final_sections.append(section)
        else:
            if section.else_section is not None:
                final_sections.append(section.else_section)
    return final_sections

def main():
    args: List[str] = sys.argv
    defined_vars: List[str] = []
    input_file: Path = Path(args[1])
    preprocess_file: Path = Path("pyprocess.txt")

    if not input_file.exists():
        raise FileNotFoundError(f"Can not find {file}!")
    if not preprocess_file.exists():
        raise FileNotFoundError(f"Can not find preprocessing file!")
    
    with open(preprocess_file) as file:
        for line in file:
            defined_vars.append(line.strip(" "))

    if input_file.is_dir():
        raise Exception("Directories not supported yet!")
    else:
        with open(input_file) as file:
            sections: List[Section] = preprocess(file)
            sections = get_defined(sections, defined_vars)
            for section in sections:
                print(section.buffer)


if __name__ == "__main__":
    main()
