import sqlite3
import json
import datetime
import os
from pathlib import Path

class GameDb:
    def __init__(self):
        self.connection = sqlite3.connect('.\\gamebook.db')
        self.cursor = self.connection.cursor()
        
    def getParagraphData(self, paragraph_id) -> tuple:
        dat = self.cursor.execute(f"select text, img_name from paragraphs where id = {paragraph_id}").fetchone()
        return (dat[0], dat[1])
    
    def getParagraphAdditionalTexts(self, paragraph_id) -> list:
        return self.cursor.execute(f"select show_condition, paragraph_text_add from choices where paragraph_id = {paragraph_id} and not paragraph_text_add is null").fetchall()

    def getParagraphChoices(self, paragraph_id) -> list:
        return self.cursor.execute(f"select show_condition, choice_text, outcome_str, paragraph_id_next from choices where paragraph_id = {paragraph_id} and not paragraph_id_next is null").fetchall()
    
    def saveGame(self, gamestate):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        # save_folder = os.path.join(dir_path, "save")
        # Path(save_folder).mkdir(exist_ok=True)
        
        # filename = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        # savepath = os.path.join(save_folder, filename)
        
        savepath = os.path.join(dir_path, "save.json")
        with open (savepath, "w") as f:
            json.dump(gamestate, f)
    
    def loadGame(self, loadpath):
        saved_game = None
        
        with open(loadpath, "r") as f:
            saved_game = json.load(f)
        
        return saved_game