from dataclasses import dataclass
from parser import ConditionParser, OutcomeParser

class Paragraph:
    def __init__(self, id, data, additional_texts, choices):
        self.id: int = id
        self.base_text: str = data[0]                       #basic text to display, always stays the same
        self.img: str = data[1]                             #img
        self.additional_texts: list = additional_texts      #additional text to display, dependent on variables (also related to current choices)
        self.choices: list = choices                        #all possible choices, to be filtered by show_condition
        self.visible_additional_texts = self.evaluate_visiblity(self.additional_texts)
        self.visible_choices = self.evaluate_choices(self.choices)
        
    def evaluate_visiblity(self, table) -> list:
        res_table = []
        for i in range( len( table ) ):
            show_condition = table[i][0]
            
            if show_condition == None:
                show = True
            else:
                show = ConditionParser().evaluate(show_condition)
            
            if show:
                res_table.append(table[i])
                
        return res_table
    
    def evaluate_choices(self, table) -> list[Choice]:
        res_table = []
        for i in range( len( table ) ):
            show_condition = table[i][0]
            
            if show_condition == None:
                show = True
            else:
                show = ConditionParser().evaluate(show_condition)
            
            if show:
                choice = Choice(table[i][1], table[i][2], table[i][3])
                res_table.append(choice)
                
        return res_table
    
    def __str__(self):
        adds = "\n".join(t[1] for t in self.visible_additional_texts)
        #chs = "\n\t".join(f"{c+1}. {self.visible_choices[c][1]}" for c in range(0, len(self.visible_choices)))
        return self.base_text + ("\n" + adds if adds else "")# + "\n\t" + chs
    
@dataclass
class Choice:
    base_text: str                  #
    outcome: str                    #
    paragraph_id_next: int          #