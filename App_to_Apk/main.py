from kivy.app import App
from kivy.uix.widget import Widget
import best_move
import board_detection
import pieceClassification
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
import os


class MyLayout(Widget):

    path=ObjectProperty(None)
    popup=None
    popup_prediction = Popup(size_hint=(None, None), size=(400, 400))

    def selected(self, filename):
        if len(filename) >= 1:
            self.path.text=filename[0]
       #voglio che una volta selezionato il file venga stampata una notifica

    def btn(self):

        grid=GridLayout(rows=2)
        grid2= GridLayout(cols=2,rows=1)
        adv="The image selected is "+ self.path.text+ "\nAre you sure to continue?"
        text=Label(text=adv)
        yes= Button(text="YES",on_press=self.button_yes)

        no= Button(text="NO",on_press=self.button_no)

        grid2.add_widget(yes)
        grid2.add_widget(no)

        grid.add_widget(text)
        grid.add_widget(grid2)
        popup = Popup(title='Are you sure to start?',
                      content=grid,
                      size_hint=(None, None), size=(400, 400))
        popup.open()
        self.popup=popup

    def button_yes(self,instance):
        self.popup.dismiss()
        self.predict(self.path.text)

    def button_no(self,instance):
        self.popup.dismiss()


    def predict(self,path):
        img_list=board_detection.board_detect(path)
        fen=pieceClassification.classify(img_list)
        move=best_move.pred(fen)
        self.show_prediction(move)
        os.remove("board.png")

    def show_prediction(self,move):
        image = Image(source="board.png")
        self.popup_prediction.title = "Prediction: " + str(move)
        self.popup_prediction.content=image
        self.popup_prediction.open()




class bestMoveApp(App):
    def build(self):
        return MyLayout()


if __name__ == "__main__":
    bestMoveApp().run()
