from NavigationBar import *
from Data import Data
#from Authentication import create_authentication_screen


data = Data()
data.root = root = Tk()
root.title("Birdnet")
root.geometry("800x500")
data.interface = interface = dict()

create_navigation_bar_screen(data)
create_authentication_screen(data)
root.mainloop()
