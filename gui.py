import PySimpleGUI as sg      
import gensim
import time
from make import one_recipe
from parts.simple import recipeClass

sg.theme('DarkBlue2')    # Keep things interesting for your users

def load_model():
    loadinglayout = [[sg.Text('Please wait while the Waffle Chef loads.')]]  
    window = sg.Window('AI Waffle Chef', loadinglayout)
    event, values = window.read(timeout=0)
    model = gensim.models.KeyedVectors.load_word2vec_format('data/GoogleNews-vectors-negative300.bin', limit=1600000, binary=True)
    window.close()
    return model

def run_chef(model):
    waffle_ascii = """
    _.-------._
  .' _|_|_|_|_ '.
 / _|_|_|_|_|_|_ \\
| |_|_|_|_|_|_|_| |
|_|_|_|_|_|_|_|_|_|
| |_|_|_|_|_|_|_| |
| |_|_|_|_|_|_|_| |
 \ -|_|_|_|_|_|- /
  '. -|_|_|_|- .'
    `---------`"""
    thinking = """
 _____ _     _       _    _                         
|_   _| |   (_)     | |  (_)                        
  | | | |__  _ _ __ | | ___ _ __   __ _             
  | | | '_ \| | '_ \| |/ / | '_ \ / _` |            
  | | | | | | | | | |   <| | | | | (_| |  _   _   _ 
  \_/ |_| |_|_|_| |_|_|\_\_|_| |_|\__, | (_) (_) (_)
                                   __/ |            
                                  |___/             """
    layout = [[sg.Text('AI Waffle Chef')],        
            [sg.Text('Creativity:'), sg.Text('', key='_OUTPUT_')],  
            [sg.Slider((1,100), key='_SLIDER_', orientation='h', enable_events=True, disable_number_display=False),  
            sg.T('    1', key='_RIGHT_')], 
            [sg.Text('Food Pairing:'), sg.Text('', key='_OUTPUT1_')],  
            [sg.Slider((1,100), key='_SLIDER2_', orientation='h', enable_events=True, disable_number_display=False),  
            sg.T('    1', key='_RIGHT2_')],
            [sg.Text('Number of People to Feed:'), sg.Text('', key='_OUTPUT2_')],  
            [sg.Slider((1,32), key='_SLIDER3_', orientation='h', enable_events=True, disable_number_display=False),  
            sg.T('    1', key='_RIGHT3_')],
            [sg.Text('Waffle inspiration:' ), sg.InputText(key='INSPIRATION')],
            [sg.Button("Make a waffle recipe!"), sg.Exit()],
            [sg.Text("Waffle: ")],
            [sg.Text(waffle_ascii, key='WAFFLE', font='Courier 10', size=(60, 50))]]    
    window = sg.Window('AI Waffle Chef', layout, size=(800,800)) # size=(800,600)
    while True:                             # The Event Loop
        event, values = window.read() 
        print(event, values)       
        if event in (None, 'Exit'):      
            break      
        creativity_score = int(values['_SLIDER_'])
        pairing_score = int(values['_SLIDER2_'])
        people_count = int(values['_SLIDER3_'])
        inspiration = (values['INSPIRATION']).lower()
        window['_RIGHT_'].update(creativity_score)  
        window['_RIGHT2_'].update(pairing_score)  
        window['_RIGHT3_'].update(people_count) 
        if event == "Make a waffle recipe!":   
            # window['WAFFLE'].update(thinking)        
            try:
                recipe = one_recipe(model, creativity_score, pairing_score, people_count, inspiration)
                printable = recipe.ingredients_string() + recipe.print_recipe()
                window['WAFFLE'].update(printable) 
            except Exception as error:
                print(error)
                window['WAFFLE'].update(waffle_ascii) 
    window.close()

model = load_model()
run_chef(model)