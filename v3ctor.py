'''
Programm zum Darstellen von 2D-Vektorfelden und zur Visualisierung der Divergenz und Rotation des Feldes
über die jeweiligen Integrale nach Gauss und Stokes. 
Benötigt das Packet sympy und python Version 3.
09.03.2021:
    -Field scanner ausbauen
    - Fehler der Felderzeugung und der Koordinatenachsen behoebn

08.03.2021:
    - Modus Field scanner einbinden

04.03.2021:
    - marginale überarbeitung des layouts
    -scale überarbeiten

02.03.2021:
    -totale Überarbeitungen der GUI
    -einbinden von Hilfe Buttons

15.02.2021:
    -Exe Datei erstellt
    -Icon erstellt
    _label für werte angepasst
    -angefangen an Version 2.0 zu arbeiten -> überarbeitetes Layout

11.02.2021:
    -Berechnen der Div/Rot an einer Stelle mit rechter Maustaste

10.02.2021:
    -Bugfixes
    -englische Version

05.02.2021:
    -weitere Arbeit an Bug fixes
    -Sortieren der GUI
    -Einführen eines Toggels für Normalenvektoren des Rechtecks

02.02.2021 und 05.02.2021:
    -Bug fix der Divergenz/Integral VZ -> Hilfsfkt Transform

01.02.2021:
    - default feld  (x,0)
    - überarbeite des Verzereren des rechtecks
    - Rechtsklick: divergenz bzw Rotation des Feldes an der Stelle
    -herraus und reinzomm interaktiv
    -Label der Achsen anbringen

25.01.2021:
    -entfernen von einigen Terminalausgaben
    -Farbe reduzieren der äußeren Vektoren
    -erzeugen der Checkboxen für partielle Ableitungen

21.01.2021
    - Pfeile im Rechteck bleiben während des veränderen des Rechtecks erhalten
    - x,y antiele der Vektoren innerhalb des Rechtecks anzeigen.

15.01.2021
    - Verändern des Cursors beim überfahren der Rechtecklinie und im Rechteck
    - arbitrary unit für den Wert der Integrale eingefügt
    - Vektorskalierung überarbeitet für konstante Felder
        -> entfernen der Funktion "calc_coordinate", da dies direkt in den Schleifen gelöst wird

11.01.2021
    - größe ändern des rechtecks durch ziehen der Kanten mit der Maus
       -> Beim Beenden des Rechtecks werden nun immer die Koordinaten sortiert  -- Notiz: Kann nun vielleicht auhc in den anderen Funktionen die darauf aufbauen entfernt werden. -> noch zu testen. 
       -> hinzufügen der Koordinaten für das zuvor gezeichnete Rechteck
    -entfernung der activecolor


6.01.2021:
    -vorbereitung für Änderung der Größe des Rechtecks durch aufziehen der Kanten

30.12.2020:
    - Grafische Anpassung an MacOS
       -> Entfernung vom Stipple und Farben des Textes einstellen


29.12.2020: 
    -Layout des Programms durch grid Funktionalität
    -Skalieren der Koordinaten bei Veränderung der Anzahl der Vektoren
    -Skalieren des Wertes des Integrals
    -Erkennung wenn auf eine der Seiten des Rechtecks geklickt wurde


'''

import tkinter as tk  #Modul für GUI
from tkinter import messagebox
import sympy as sy   # Modul für Symbolisieren des Eingabevektorfeldes
import math as mt


class App(tk.Frame):

## -------- Constructor

    def __init__(self, master=None):
        tk.Frame.__init__(self,master)
        tk.Frame.config(self,bg=bg)
        self._createVariables()
        self._createGUI()
        self.grid()
        self.changelanguage()
        self._createBinding()
        self._createField()
        self.new_field()



    def _createVariables(self):

        self.rectx0 = 0     #Rechteck Koordinaten
        self.recty0 = 0
        self.rectx1 = 0
        self.recty1 = 0
        self.rectstartCoords = (0,0,0,0)
        self.rectid = None
        self.position_flag = ''    #Flag ob Rechteck ausgewählt ist

        self.canvas_size = 650      #Größe der Anzeigefläche - Quadratisch

        self.x, self.y = sy.symbols('x, y')   # Symbole die sypy zum berechnen benutzen kann.
        self.arrow_space= 2                   # Abstand der Pfeil in px
        self.scale=1                          # Skalierungsfaktor der Pfeile

        self.surface_int=0                     # Wert des Flächenintegrals
        self.line_int=0                       # Wert des Linienintegrls


    def _createGUI(self):

        #HEADER
        self.header_left = tk.Frame(self,bg=bg)
        self.header_left.grid(row=0,column=0,pady=5)


        #HeaderContent

        self.Header_Label_left=tk.Label(self.header_left,text='vere vedi vecu \n Eine forschungsbasierte Simulation zu Vektorfeldern, \n Divergenz und Curl.', font=(font,16),bg=bg,fg=fg)
        self.Header_Label_left.grid(row=0,column=0,columnspan=2,padx=60)

        
        #BODY

        self.body_left=tk.Frame(self, bg=bg, width=width/2)
        self.body_left.grid(row=1, column=0,pady=10,padx=20,sticky=tk.W+tk.N)
        

        self.canvas=tk.Canvas(self, width = self.canvas_size, height = self.canvas_size,bg=bg,highlightthickness=2, highlightbackground="darkblue")
        self.canvas.grid(row=0,column=1,rowspan=2)

        #Sub-Body Left

        self.labInt = tk.Label(self.body_left, text='Auswahl des Integraltheorems: ',font=(font,16),fg=fg,bg=bg)
        self.labInt.grid(row=0,column=0,sticky=tk.W, padx=10,pady=25)

        self.OptionList= ["Satz von Gauss","Satz von Stokes"]
        self.integral_kind = tk.StringVar(self)
        self.integral_kind.set(self.OptionList[0])
        self.Menu = tk.OptionMenu(self.body_left, self.integral_kind, *self.OptionList, command=self.changedDropDown)
        self.Menu.config(width=15, font=(font,12),fg=fg,bg=bg)
        self.Menu.grid(row=0,column=0, padx=(180))
        self.Menu['menu'].entryconfigure('Satz von Stokes',state='disabled')



        self.Image_Latex=tk.PhotoImage(file='Latex_Gauss.png')
        self.Display_Image=tk.Label(self.body_left,image=self.Image_Latex,bg=bg)
        self.Display_Image.grid(row=2, column=0,columnspan=2,pady=20)


        self.Info_Button_Field=tk.Button(self.body_left,text='i',font=('Times',12),bg=bg,fg=fg, border=0, command=self.help_field)
        self.Info_Button_Field.grid(row=3,column=0,sticky=tk.W+tk.N,pady=10)

        self.Field_Label=tk.Label(self.body_left,text='Definiere das Vektorfeld:', font=(font,16),bg=bg,fg=fg)
        self.Field_Label.grid(row=3,column=0,sticky=tk.N+tk.W,pady=10,padx=50)

        #### Field Frame
        self.Field_Frame=tk.Frame(self.body_left,bg=bg)
        self.Field_Frame.grid(row=3,column=0,padx=(260,0))

        self.labEntryX= tk.Label(self.Field_Frame, text=f'x-Komponente:',font=(font,12),fg=fg,bg=bg)
        self.labEntryX.grid(row=0,column=0, sticky=tk.W)

        self.labEntryY= tk.Label(self.Field_Frame, text=f'y-Komponente:',font=(font,12),fg=fg,bg=bg)
        self.labEntryY.grid(row=1,column=0,sticky=tk.W,)

        #Eingabe für das Vektorfeld in x-Richtung
        self.input1 = tk.Entry(self.Field_Frame,textvariable=tk.StringVar(self, value='x'),font=(font,12), width=10,fg=fg,bg=bg)
        self.input1.grid(row=0,column=1)
        #Eingabe fr das Vektorfeld in y-Richtung   
        self.input2 = tk.Entry(self.Field_Frame,textvariable=tk.StringVar(self, value='0'),font=(font,12), width=10,fg=fg,bg= bg)       
        self.input2.grid(row=1,column=1)

        #Button zum erzeugen des Vektorfeldes
        self.but1 = tk.Button(self.Field_Frame, text='Berechne!', command=self.new_field,font=(font,12),fg=fg,bg=bg)
        self.but1['bg']='#FFFFFF'
        self.but1.grid(row=2,column=0,columnspan=2,sticky=tk.W)

        #Slider zum einstellen der Anzahl an Vektoren
        self.slider = tk.Scale(self.Field_Frame,from_=5, to=25, orient=tk.HORIZONTAL, length=250, label='Anzahl der Vektoren',font=(font,12),fg=fg,bg=bg, command=self.zoom) #Slider für Anzahl der Vektoren in einer Spalte/Zeile
        self.slider.set(10)
        self.slider.grid(row=3,column=0,columnspan=2,sticky=tk.W)

        #Schalter zum Einbelden des Koordinatensystems
        self.check_var = tk.BooleanVar()
        self.check_var.set(False)
        self.checkbox = tk.Checkbutton(self.Field_Frame, text='Koordinatensystem einblenden', variable=self.check_var ,command=self.toggleCoordinatelines,font=(font,12),fg=fg,bg=bg) 
        self.checkbox.grid(row=4,column=0,columnspan=2,sticky=tk.W)

        ### Divergenze Frame
        self.Divergenz_Info_Button=tk.Button(self.body_left,text='i',font=('Times',12),bg=bg,fg=fg, border=0, command=self.help_divergenz)
        self.Divergenz_Info_Button.grid(row=4,column=0,sticky=tk.W+tk.N,pady=50)

        self.Divergenz_Frame=tk.Frame(self.body_left,bd=20,bg=bg)
        self.Divergenz_Frame.grid(row=4,column=0,sticky=tk.W+tk.N,padx=(30,0),pady=30)

        self.Divergenz_Label=tk.Label(self.Divergenz_Frame,text='Divergenz von F',font=(font,16),bg=bg,fg=fg)
        self.Divergenz_Label.grid(row=0,sticky=tk.W)
        
        #Fieldscanner
        self.check_fieldscanner_var = tk.BooleanVar()
        self.check_fieldscanner_var.set(False)
        self.fieldscannercheckbox = tk.Checkbutton(self.Divergenz_Frame, text='Feld abtasten', variable=self.check_fieldscanner_var,command=self.switch_fieldscanner,font=(font,12),fg=fg,bg=bg)
        self.fieldscannercheckbox.grid(row=1,sticky=tk.W)
        
        #Abstandsinput fieldscanner
        self.Input_label_fieldscanner=tk.Label(self.Divergenz_Frame,text='Schrittweite des Fieldsanners: ',bg=bg, font=(font,12),fg=fg)
        self.Input_label_fieldscanner.grid(row=2,column=0,sticky=tk.W)
        
        self.Input_fieldscanner=tk.Entry(self.Divergenz_Frame,textvariable=tk.IntVar(self, value=15),width=2,bg=bg,font=(font,12),fg=fg)
        self.Input_fieldscanner.grid(row=2,column=0,padx=(160,0),sticky=tk.W)

        #Schalter zum Einbelden der Partiellen Richtungen in X im Rechteck
        self.check_var_partialx = tk.BooleanVar()
        self.check_var_partialx.set(False)
        self.checkbox_partialx = tk.Checkbutton(self.Divergenz_Frame, text='x-Komponente im Rechteck', variable=self.check_var_partialx , command=self.catch_inRect_vec, font=(font,12),fg=fg,bg=bg) 
        self.checkbox_partialx.grid(row=3,sticky=tk.W)

        #Schalter zum Einbelden der Partiellen Richtungen in Y im Rechteck
        self.check_var_partialy = tk.BooleanVar()
        self.check_var_partialy.set(False)
        self.checkbox_partialy = tk.Checkbutton(self.Divergenz_Frame, text='y-Komponente im Rechteck', variable=self.check_var_partialy , command=self.catch_inRect_vec, font=(font,12),fg=fg,bg=bg) 
        self.checkbox_partialy.grid(row=4,sticky=tk.W)

        self.Divergenz_output_Frame=tk.Frame(self.Divergenz_Frame,bg='darkblue',border=2)
        self.Divergenz_output_Frame.grid(row=5,sticky=tk.W,pady=(5,0))

        self.Divergenz_Output=tk.Label(self.Divergenz_output_Frame,text=' ',font=(font,16),bg=bg,fg=fg,width=12)
        self.Divergenz_Output.grid(sticky=tk.W)


        ### Flux Frame
        self.Flux_Frame=tk.Frame(self.body_left,bd=20,bg=bg)
        self.Flux_Frame.grid(row=4,column=0,sticky=tk.W+tk.N,padx=(310,0),pady=(30,0))

        self.Flux_Label=tk.Label(self.Flux_Frame,text='Fluss durch Fläche',font=(font,16),fg=fg,bg=bg)
        self.Flux_Label.grid(row=0,sticky=tk.W)

        #Toggle für Normal/Lininevektoren des Rechtecks
        self.check_var_RectVec = tk.BooleanVar()
        self.check_var_RectVec.set(False)
        self.checkbox_RectVec = tk.Checkbutton(self.Flux_Frame, text='Normalenvektoren einblenden', variable=self.check_var_RectVec , command=self.toggleRectVec, font=(font,12),fg=fg,bg=bg) 
        self.checkbox_RectVec.grid(row=1,sticky=tk.W,)

        self.Flux_output_Frame=tk.Frame(self.Flux_Frame,bg='darkblue',border=2)
        self.Flux_output_Frame.grid(row=2,sticky=tk.W,padx=2,pady=(90,0))

        self.Flux_Output=tk.Label(self.Flux_output_Frame,text='',font=(font,16),fg=fg,bg=bg,width=12)
        self.Flux_Output.grid()

        #Footer
        
        self.Header_Button_Info=tk.Button(self,text='i',font=('Times',12),bg=bg,fg=fg, command=self.Impressum)
        self.Header_Button_Info.grid(row=2,column=1,sticky=tk.E,padx=(0,340))

        #Button zum Ändern der Sprache
        self.but_change_lang=tk.Button(self, text='Change language to English', command=self.changelanguage, fg=fg,bg=bg, font=(font,12))
        self.but_change_lang.grid(row=2,column=1,sticky=tk.E,padx=(0,100))
        self.checklanguage='DE'

        #Button zum beenden
        self.but_end = tk.Button(self, text='Beenden',font=(font,12), command=ende,fg=fg,bg=bg) 
        self.but_end.grid(row=2,column=1, sticky=tk.E+tk.N, padx=(0,5))


    def _createBinding(self):           #Interaktion mit dem Benutzer an Objekte anhängen
        self.canvas.bind( "<Button-1>", self.B1_pressed)
        self.canvas.bind("<Button-2>", self.B2_pressed)
        self.canvas.bind("<Button-3>", self.B2_pressed)
        self.canvas.bind( "<ButtonRelease-1>", self.B1_released)
        self.canvas.bind( "<B1-Motion>", self.B1_Moved)
        self.canvas.bind("<Motion>", self.checkHand)
        self.input1.bind( "<Return>", self.new_field_return )
        self.input2.bind( "<Return>", self.new_field_return)



    def _createField(self): #liest Feld aus eingabe ein und übergibt sie als Sympy Expression
        fieldstring1=self.input1.get()
        fieldstring2=self.input2.get()
        if fieldstring1== '':
            fieldstring1 = '0'
        if fieldstring2== '':
            fieldstring2 = '0'
        expr1 = sy.S(fieldstring1)
        expr2 = sy.S(fieldstring2)
        print("Fx= ",expr1)
        print("Fy= ",expr2)
        self.F = (expr1,expr2)

    def _createCoordinatelines(self):  #Erzeugen des Koordinantensystems
        if self.check_var.get()==True:

            self.canvas.delete('Coordinateline')
            self.canvas.create_line(int(self.canvas_size/2),0,int(self.canvas_size/2),self.canvas_size, fill='gray' , tags=('Coordinateline',))
            self.canvas.create_line(0,int(self.canvas_size/2),self.canvas_size,int(self.canvas_size/2), fill='gray', tags=('Coordinateline',))

            for i in range(int(self.canvas_size/2),self.canvas_size+1,int(self.max_arrow_size)):      
                x,y=self.Transform(i,i)
                if i == int(self.canvas_size/2): self.canvas.create_text(i,i,text=0, anchor=tk.NE, tags=('Coordinateline',),fill='gray')
                else:
                    self.canvas.create_text(i,int(self.canvas_size/2),text=round(x,1), anchor=tk.N, tags=('Coordinateline',),fill='gray')
                    self.canvas.create_text(int(self.canvas_size/2),i,text=round(y,1), anchor=tk.N, tags=('Coordinateline',),fill='gray')


            for j in range(int(self.canvas_size/2),self.canvas_size+1,int(self.max_arrow_size)):
                i=self.canvas_size-j
                x,y=self.Transform(i,i)
                if i == int(self.canvas_size/2): self.canvas.create_text(i,i,text=0, anchor=tk.NE, tags=('Coordinateline',),fill='gray')
                else:
                    self.canvas.create_text(i,int(self.canvas_size/2),text=round(x,1), anchor=tk.N, tags=('Coordinateline',),fill='gray')
                    self.canvas.create_text(int(self.canvas_size/2),i,text=round(y,1), anchor=tk.N, tags=('Coordinateline',),fill='gray')

            self.canvas.create_text(self.canvas_size/2+10,10, text='y', tags=('Coordinateline',),fill='gray')
            self.canvas.create_text(self.canvas_size,self.canvas_size/2+10, text='x', tags=('Coordinateline',),fill='gray')


    def toggleCoordinatelines(self): #Ein und ausschalten des Koordinatensystems
        state = self.check_var.get()
        if state == True:
            self._createCoordinatelines()
        else:
            self.canvas.delete('Coordinateline')

    def changedDropDown(self,integral_kind):
        if self.rectid != None:
            if self.fintegral_kind.get() == 'Satz von Gauss' or "Gauss' theorem" :
                self.draw_surface_arrows()
            elif self.integral_kind.get() == 'Satz von Stokes' or "Stokes' theorem":
                self.draw_line_arrows()


    def toggleRectVec(self):
        if self.integral_kind.get() == 'Satz von Gauss' or self.integral_kind.get() == "Gauss' theorem" :
            self.draw_surface_arrows()
        elif self.integral_kind.get() == 'Satz von Stokes' or self.integral_kind.get() == "Stokes' theorem":
            self.draw_line_arrows()

    def zoom(self,k):
        self.new_field(zoomed=True)

    def changelanguage(self):
        if self.checklanguage == 'DE':
            self.canvas.delete('rec_arrow','rec', 'partial_x_arrow', 'partial_y_arrow')
            self.rectx0 = 0     
            self.recty0 = 0
            self.rectx1 = 0
            self.recty1 = 0

            self.Menu.destroy()
            self.Header_Label_left.config(text='vere vedi vecu \n A research-based simulation on vector fields,\n divergence, and curl.')
            self.fieldscannercheckbox.config(text='Field scanner')
            self.Input_label_fieldscanner.config(text='Step for fieldscanner: ')
            self.Field_Label.config(text='Define the vector field:')
            self.Divergenz_Label.config(text='Divergence')
            self.Divergenz_Output.config(text='')
            self.Flux_Label.config(text='Flux through area')
            self.Flux_Output.config(text='')
            self.labEntryX.config(text='x-component')
            self.labEntryY.config(text='y-component')
            self.labInt.config(text='Select integral theorem:')
            self.slider.config(label='Number of vectors')
            self.checkbox_partialy.config(text='Highlight y components')
            self.checkbox_partialx.config(text='Highlight x components')
            self.checkbox.config(text='Show coordinate axes ')
            self.checkbox_RectVec.config(text='Highlight the projections onto the outer normal')
            self.but1.config(text='Show field!')
            self.but_change_lang.config(text='Sprache zu Deutsch wechseln')
            self.but_end.config(text='Quit')

            self.OptionList = ["Gauss' theorem","Stokes' theorem"]
            self.integral_kind.set(self.OptionList[0])
            self.Menu = tk.OptionMenu(self.body_left, self.integral_kind, *self.OptionList, command=self.changedDropDown)
            self.Menu.config(width=15, font=(font,12),fg=fg, bg=bg)
            self.Menu.grid(row=0,column=0, padx=180)
            self.Menu['menu'].entryconfigure("Stokes' theorem",state='disabled')

            self.checklanguage='EN'
        else:
            self.canvas.delete('rec_arrow','rec', 'partial_x_arrow', 'partial_y_arrow')
            self.rectx0 = 0     
            self.recty0 = 0
            self.rectx1 = 0
            self.recty1 = 0

            self.Menu.destroy()
            self.Header_Label_left.config(text='vere vedi vecu \n Eine forschungsbasierte Simulation zu Vektorfeldern,\n Divergenz und Curl.')
            self.fieldscannercheckbox.config(text='Fieldscanner')
            self.Input_label_fieldscanner.config(text='Schritt des Fieldscanner: ')
            self.Field_Label.config(text='Definiere das Vektorfeld:')
            self.Divergenz_Label.config(text='Divergenz von F')
            self.Divergenz_Output.config(text='')
            self.Flux_Label.config(text='Fluss durch Fläche')
            self.Flux_Output.config(text='')
            self.labEntryX.config(text='x-Komponente')
            self.labEntryY.config(text='y-Komponente')
            self.labInt.config(text='Auswahl des Integraltheorems:')
            self.slider.config(label='Anzahl der Vektoren')
            self.checkbox_partialy.config(text='y-Komponente im Rechteck')
            self.checkbox_partialx.config(text='x-Komponente im Rechteck')
            self.checkbox.config(text='Koordinatensystem einblenden')
            self.checkbox_RectVec.config(text='Projektion auf die Flächennormale einblenden')
            self.but1.config(text='Berechne!')
            self.but_change_lang.config(text='Change language to English')
            self.but_end.config(text='Beenden')

            self.OptionList = ['Satz von Gauss','Satz von Stokes']
            self.integral_kind.set(self.OptionList[0])
            self.Menu = tk.OptionMenu(self.body_left, self.integral_kind, *self.OptionList, command=self.changedDropDown)
            self.Menu.config(width=15, font=(font,12),fg=fg,bg=bg)
            self.Menu.grid(row=0,column=0, padx=180)
            self.Menu['menu'].entryconfigure('Satz von Stokes',state='disabled')


            self.checklanguage= 'DE'


    def switch_fieldscanner(self):
        if self.check_fieldscanner_var.get() == True:
            self.canvas.itemconfig('field_arrow', fill='gray')
            self.deleteRect()
        else:
            self.canvas.delete('clickarrow','fieldscanner_partial_x','fieldscanner_partial_y') 
            self.canvas.itemconfig('field_arrow', fill='black')
## -------- Info Buttons
    def Impressum(self):
        if self.checklanguage == 'DE':
            messagebox.showinfo('Impressum','Die Simulation wurde an der Fakultät für Physik in Göttingen in der Didaktik der Physik für Lehrzwecke entwickelt. Kontakt: Larissa Hahn, Simon Blaue, Pascal Klein. Mail: larissa.hahn@uni-goettingen.de . Der Code ist in Python mit dem MOdul Sympy geschrieben. Version: März 2021')
        else:
            messagebox.showinfo('Impressum','The simulation was developed at the Faculty of Physics at University of Göttingen (Physics Education Research) for teaching purposes. Contact: Larissa Hahn, Simon Blaue, Pascal Klein. Mail: larissa.hahn@uni-goettingen.de . The code was written in Python using the Sympy-package. Version: March 2021')
    def help_field(self):
        if self.checklanguage == 'DE':
            messagebox.showinfo('Feld F','Definiere das Feld über seine Komponenten abhängig von x, y, Skalaren und den Operationen (+, -, *, /). Wurzel-Operationen, Tangensfunktionen, Betragsfunktionen und Exponentialfunktionen sind nicht möglich. Durch Bewegen des Sliders kann die Anzahl der Vektoren pro Zeile/Spalte variiert werden. Durch Aktivierung der unteren Box werden die Koordinatenachsen eingeblendet.')
        else:
            messagebox.showinfo('Field F','Define the field components by entering x, y, scalars, and mathematical operators (+, -, *, /). Root operations, tangensfunctions, exponentialfunctions and absolute operations are not possible. Move the slider to change the number of vectors that are displayed in each row or column. Show or hide the axes of the coordinate system to identify the origin (0,0) and the orientation of the axes.')
    def help_divergenz(self):
        if self.checklanguage == 'DE':
            messagebox.showinfo('Divergenz von F','Mit dem Mauszeiger kann ein Rechteck in das Vektorfeld gezogen werden. Durch Aktivierung der Boxen können x- und y-Komponente innerhalb des Rechtecks und die Normalen-Projektion der Vektoren auf dem Reckteckrand eingeblendet werden. Ein Klick mit der rechten Maustaste an einen beliebigen Ort im Feld gibt den Wert für die Divergenz an. Mit dem Fieldscanner können Vektorpfade nachgezeichnet werden. Ein Klick mit der rechten Maustaste im Feld löscht alle gezeichneten Pfade.')
        else:
            messagebox.showinfo('Divergence of F','Draw rectangles as test areas using the mouse. Click the buttons for highlighting the decomposition of vectors within the test area or visualizing the projections of the field onto the outer normal vector. Use the right mouse button to show the value of divergence at any spot. With the fieldscanner, vector paths can be traced with the left mouse button. A rightclick deletes all drawn paths.')


## -------- OnClick Events

    def B1_pressed(self,event):
        if self.check_fieldscanner_var.get() == True:
            self.field_scanner_start(event)
        else:
            self.startRect(event)
            
    def B2_pressed(self,event):
        if self.check_fieldscanner_var.get() == True:
            self.canvas.delete('clickarrow','fieldscanner_partial_x','fieldscanner_partial_y')
        else:
            self.canvas.delete('clickarrow','fieldscanner_partial_x','fieldscanner_partial_y')
            self.field_scanner_start(event)


## ------- OnMove Events
    def B1_Moved(self,event):
        if self.check_fieldscanner_var.get() == True:
            self.field_scanner_moved(event)
        else:
            self.scaleRect(event)


## ------- OnRelease Events
    
    def B1_released(self,event):
        if self.check_fieldscanner_var.get() == True:
            self.field_scanner_stoped(event)
        else:
            self.stopRect(event)


## -------- Neues Feld nach Eingaben Erzeugen
    def new_field_return(self,event):
        self.new_field(zoomed=True)

    def new_field(self,zoomed=False):
        self.scale = 1
        if zoomed == False:
            self.canvas.delete('rec') #Leeren der Canvas
        self.canvas.delete('rec_arrow','field_arrow', 'partial_x_arrow', 'partial_y_arrow','clickarrow','fieldscanner_partial_x','fieldscanner_partial_y')
        self.Divergenz_Output.config(text=f'')
        self.Flux_Output.config(text=f'')
        self.arrow_number=self.slider.get() #festlegen der Pfeile pro Reihe
        self.max_arrow_size = self.canvas_size/self.arrow_number #festlegen der maximalen Pfeillänge
        self._createField() # auslesen des Feldes aus den Textfeldern und in symbolische Were übermitteln # Berechnung des Längsten Vektors im Vektorfeld
        self.scale=self.max_arrow_size/self.max_arrow_length() #Skalierung aller Vektoren festlegen
        self.draw_field()  #Alle Pfeile zeichnen
        self._createCoordinatelines()
        print("max arrow size: " , self.max_arrow_length())
        print('actual max_size: ', self.max_arrow_size)
        print("scale: ", self.scale)
        if zoomed == False:
            self.rectx0 = 0     
            self.recty0 = 0
            self.rectx1 = 0
            self.recty1 = 0
        if self.rectid != None:
            if self.rectx0 == self.rectx1 and self.recty0 == self.recty1:
                if self.integral_kind.get() == 'Satz von Gauss' or self.integral_kind.get() == "Gauss' theorem" :
                        self.show_divergence()
                elif self.integral_kind.get() == 'Satz von Stokes' or integral_kind == "Stokes' theorem":
                        self.show_curl()
            elif self.integral_kind.get() == 'Satz von Gauss' or self.integral_kind.get() == "Gauss' theorem" :
                self.draw_surface_arrows()
            elif self.integral_kind.get() == 'Satz von Stokes' or self.integral_kind.get() == "Stokes' theorem":
                self.draw_line_arrows() 

            if self.check_var_partialx.get() == True or self.check_var_partialy == True:
                self.catch_inRect_vec()
        if self.check_var_partialx.get() == True or self.check_var_partialy == True or self.check_fieldscanner_var.get()==True:
            self.canvas.itemconfig('field_arrow',fill='gray')
        


## -------- Berechnung der Integrale
    def divergence(self):
        F_x,F_y = self.F
        divergence = sy.diff(F_x,self.x)+sy.diff(F_y,self.y)
        return divergence

    def curl(self):
        F_x,F_y = self.F
        curl = sy.diff(F_y,self.x)-sy.diff(F_x,self.y)
        return curl

    def calc_AreaInt(self):
        x0,x1,y1,y0 = self.order_Rec_Coords()
        x0,y0 = self.Transform(x0,y0)
        x1,y1 = self.Transform(x1,y1)
        first_Integration = sy.integrate(f'{self.divergence()}',(self.x,x0,x1))
        Area_Integration = sy.integrate(f'{first_Integration}',(self.y,y0,y1))
        return Area_Integration

    def calc_LineInt(self):
        x0,x1,y1,y0 = self.order_Rec_Coords()
        x0,y0 = self.Transform(x0,y0)
        x1,y1 = self.Transform(x1,y1)
        first_Integration = sy.integrate(f'{self.curl()}',(self.x,x0,x1))
        Area_Integration = sy.integrate(f'{first_Integration}',(self.y,y0,y1))
        return Area_Integration



## -------- Interaktives Rechteck


    def startRect(self, event):
        state = self.whereClick(event)
        print(state)
        #Testing if there is already an rectangle
        if self.rectid != None:
            print(f'In startRec ist die Rectid: {self.rectid} ')          
            if state == 'Inside':
                self.position_flag='Inside'          # Setzt die Flag zum Auswahl des Rechtecks
                return
            elif state == 'Left_side':
                self.position_flag='Left_side'
                return
            elif state == 'Right_side':
                self.position_flag='Right_side'
                return
            elif state == 'Top_side':
                self.position_flag='Top_side'
                return
            elif state == 'Bottom_side':
                self.position_flag='Bottom_side'
                return
            else:
                self.rectx0 = self.canvas.canvasx(event.x)
                self.recty0 = self.canvas.canvasy(event.y)
                self.canvas.delete('rec_arrow','rec','partial_x_arrow', 'partial_y_arrow')
                #Create rectangle
                #!!!  self.rect = self.canvas.create_rectangle(self.rectx0, self.recty0, self.rectx0, self.recty0, tags=('rec',), stipple='gray12', fill='black', activefill='blue')
                self.rect = self.canvas.create_rectangle(self.rectx0, self.recty0, self.rectx0, self.recty0, tags=('rec',), outline='black') #stipple funktioniert auf MacOs nicht :(
                #Get rectangle"s canvas object ID
                self.rectid = self.canvas.find_closest(self.rectx0, self.recty0, halo=2)
                print("Rectangle {0} started at {1} {2} {3} {4} ".format(self.rect, self.rectx0, self.recty0, self.rectx0, self.recty0))
        else:
            self.rectx0 = self.canvas.canvasx(event.x)
            self.recty0 = self.canvas.canvasy(event.y)
            self.canvas.delete('rec_arrow','rec','partial_x_arrow', 'partial_y_arrow')
            #Create rectangle
            #!!!  self.rect = self.canvas.create_rectangle(self.rectx0, self.recty0, self.rectx0, self.recty0, tags=('rec',), stipple='gray12', fill='black', activefill='blue')
            self.rect = self.canvas.create_rectangle(self.rectx0, self.recty0, self.rectx0, self.recty0, tags=('rec',), outline='black') #stipple funktioniert auf MacOs nicht :(
            #Get rectangle"s canvas object ID
            self.rectid = self.canvas.find_closest(self.rectx0, self.recty0, halo=2)
            print("Rectangle {0} started at {1} {2} {3} {4} ".format(self.rect, self.rectx0, self.recty0, self.rectx0, self.recty0))

    def scaleRect(self, event):
        oldrectx0, oldrecty0, oldrectx1, oldrecty1 = self.rectstartCoords
        lastrectx1=self.rectx1
        lastrecty1=self.recty1
        self.rectx1 = self.canvas.canvasx(event.x)
        self.recty1 = self.canvas.canvasy(event.y)   
        if self.position_flag == 'Inside':  #Das Rechteck wird verschoben
            deltax = self.rectx1-lastrectx1
            deltay = self.recty1-lastrecty1
            self.canvas.move(self.rectid,deltax,deltay)  
            self.setRecCoords()
        elif self.position_flag == 'Left_side':
            self.canvas.coords(self.rectid, self.rectx1, oldrecty0, oldrectx1, oldrecty1)
            self.setRecCoords()
        elif self.position_flag == 'Right_side':
            self.canvas.coords(self.rectid, oldrectx0, oldrecty0, self.rectx1, oldrecty1)
            self.setRecCoords()
        elif self.position_flag == 'Bottom_side':
            self.canvas.coords(self.rectid, oldrectx0, oldrecty0, oldrectx1, self.recty1)
            self.setRecCoords()
        elif self.position_flag == 'Top_side':
            self.canvas.coords(self.rectid, oldrectx0, self.recty1, oldrectx1, oldrecty1)
            self.setRecCoords()
        else:   
            #Modify rectangle x1, y1 coordinates
            self.canvas.coords(self.rectid, self.rectx0, self.recty0, self.rectx1, self.recty1)
        # Integrale wärend der Laufzeit berechen    
        if self.integral_kind.get() == 'Satz von Gauss' or self.integral_kind.get() == "Gauss' theorem" :
            self.draw_surface_arrows()
        elif self.integral_kind.get() == 'Satz von Stokes' or self.integral_kind.get() == "Stokes' theorem":
            self.draw_line_arrows() 

        self.catch_inRect_vec()

    def stopRect(self, event):
        if self.position_flag == '':        
            #Translate mouse screen x1,y1 coordinates to canvas coordinates
            self.rectx1 = self.canvas.canvasx(event.x)
            self.recty1 = self.canvas.canvasy(event.y)
            self.rectx0,self.rectx1,self.recty0,self.recty1 = self.order_Rec_Coords()
            #Modify rectangle x1, y1 coordinates (final)
            self.canvas.coords(self.rectid, self.rectx0, self.recty0,self.rectx1, self.recty1)
            print(f'Rectangle {self.rect} ended at {self.rectx0} {self.recty0} {self.rectx1} {self.recty1}')
            if self.rectx0 == self.rectx1 or self.recty0 == self.recty1:
                self.deleteRect()
                

        self.position_flag=''
        self.rectstartCoords = (self.rectx0,self.recty0,self.rectx1,self.recty1)
        if self.rectx0 == self.rectx1 or self.recty0 == self.recty1:
            self.deleteRect()            
            return
        if self.integral_kind.get() == 'Satz von Gauss' or self.integral_kind.get() == "Gauss' theorem" :
            self.draw_surface_arrows()
        elif self.integral_kind.get() == 'Satz von Stokes' or self.integral_kind.get() == "Stokes' theorem":
            self.draw_line_arrows() 

        if self.check_var_partialx.get() == True or self.check_var_partialy == True:
            self.catch_inRect_vec()


    def setRecCoords(self):
        self.rectx0 = self.canvas.coords(self.rectid)[0]
        self.recty0 = self.canvas.coords(self.rectid)[1]
        self.rectx1 = self.canvas.coords(self.rectid)[2]
        self.recty1 = self.canvas.coords(self.rectid)[3]

    def whereClick(self, event):
        x_mouse = self.canvas.canvasx(event.x)
        y_mouse = self.canvas.canvasx(event.y)
        x1,x2,y1,y2= (self.rectx0,self.rectx1,self.recty0,self.recty1)
        if x1<x_mouse<x2 and y1<y_mouse<y2: return 'Inside'
        elif x1 in range(int(x_mouse-3),int(x_mouse+4)) and y1<y_mouse<y2: return 'Left_side'
        elif x2 in range(int(x_mouse-3),int(x_mouse+4)) and y1<y_mouse<y2: return 'Right_side'
        elif y2 in range(int(y_mouse-3),int(y_mouse+4)) and x1<x_mouse<x2: return 'Bottom_side'
        elif y1 in range(int(y_mouse-3),int(y_mouse+4)) and x1<x_mouse<x2: return 'Top_side'

    def checkHand(self,event):#runs on mouse motion
        x_mouse = self.canvas.canvasx(event.x)
        y_mouse = self.canvas.canvasx(event.y)
        if self.rectx0<x_mouse<self.rectx1 and self.recty0<y_mouse<self.recty1:
            self.canvas.config(cursor="fleur")
        elif (self.rectx0 in range(int(x_mouse-3),int(x_mouse+4)) or self.rectx1 in range(int(x_mouse-3),int(x_mouse+4))) and self.recty0<y_mouse<self.recty1 or (self.recty1 in range(int(y_mouse-3),int(y_mouse+4)) or self.recty0 in range(int(y_mouse-3),int(y_mouse+4))) and self.rectx0<x_mouse<self.rectx1 :
            self.canvas.config(cursor="hand2")
        else:  self.canvas.config(cursor="")

    def deleteRect(self):
        self.canvas.delete('rec_arrow','rec','partial_x_arrow', 'partial_y_arrow','clickarrow','fieldscanner_partial_x','fieldscanner_partial_y')
        self.rectx0 = 0
        self.rectx1 = 0
        self.recty0 = 0
        self.recty1 = 0
        self.rectstartCoords = (0,0,0,0)
        self.rectid = None
        self.position_flag = ''
        self.Divergenz_Output.config(text=f'')
        self.Flux_Output.config(text=f'')

## -------- Berechnen der Divergenz/Rotation an einem Punkt

    def field_scanner_start(self,event):
        #self.canvas.delete('clickarrow','fieldscanner_partial_x','fieldscanner_partial_y')
        self.field_scanner_show_vector(event)
        self.draw_vector_components(self.canvas.canvasx(event.x),self.canvas.canvasx(event.y),'fieldscanner_partial_x','fieldscanner_partial_y')
        self.counter=0

    def field_scanner_moved(self,event):
        self.counter+=1
        modulo=int(self.Input_fieldscanner.get())
        if self.counter%modulo == 0:
            self.field_scanner_show_vector(event)
            self.draw_vector_components(self.canvas.canvasx(event.x),self.canvas.canvasx(event.y),'fieldscanner_partial_x','fieldscanner_partial_y')

    def field_scanner_stoped(self,event):
        #self.canvas.itemconfig('clickarrow', fill='black')
        #self.canvas.itemconfig('fieldscanner_partial_x', fill='black')
        #self.canvas.itemconfig('fieldscanner_partial_y', fill='black')
        self.field_scanner_show_vector(event)
        self.draw_vector_components(self.canvas.canvasx(event.x),self.canvas.canvasx(event.y),'fieldscanner_partial_x','fieldscanner_partial_y')


    def field_scanner_show_vector(self,event):
        cordx = self.canvas.canvasx(event.x)
        cordy = self.canvas.canvasy(event.y) 
        x,y = self.Transform(cordx,cordy)
        Fx=self.F[0].evalf(5, subs={self.x: x, self.y:y})*self.scale
        Fy=self.F[1].evalf(5,subs={self.x: x, self.y:y})*self.scale
        x1=cordx+Fx
        y1=cordy-Fy
        vec_leng = mt.sqrt((cordx-x1)**2+(cordy-y1)**2)
        if vec_leng < 4: return
        self.canvas.create_line(cordx, cordy, x1, y1,width=1, arrow=tk.LAST, fill='green', tags=('clickarrow',))
        if self.integral_kind.get() == 'Satz von Gauss' or self.integral_kind.get() =="Gauss' theorem" :
            self.show_divergence(cordx,cordy)
        elif self.integral_kind.get() == 'Satz von Stokes' or self.integral_kind.get() =="Stokes' theorem":
            self.show_curl(cordx,cordy)


    def show_divergence(self,cordx,cordy):
        x,y = self.Transform(cordx,cordy)
        Fx=self.F[0].evalf(5, subs={self.x: x, self.y:y})*self.scale
        Fy=self.F[1].evalf(5,subs={self.x: x, self.y:y})*self.scale
        sy_divergence=self.divergence()
        value = sy_divergence.evalf(2, subs={self.x: x, self.y:y})
        if self.checklanguage == 'DE':
            self.Divergenz_Output.config(text=f'{value} a.u.')
        else:
            self.Divergenz_Output.config(text=f'{value} a.u.')

    def show_curl(self,cordx,cordy):
        x,y = self.Transform(cordx,cordy)
        sy_curl=self.curl()
        value = sy_curl.evalf(2, subs={self.x: x, self.y:y})
        if self.checklanguage == 'DE':
            self.Divergenz_Output.config(text=f'{value} a.u.')
        else:
            self.Divergenz_Output.config(text=f'{value} a.u.')

## -------- Visualisierung der Integrale 

    def draw_surface_arrows(self): #Berechnet und zeichnet das Flächenintegral

        self.canvas.delete('rec_arrow')

        self.AreaInt_value = self.calc_AreaInt().evalf(2)

        if self.check_var_RectVec.get() == True:


            x1,x2,y1,y2 = self.order_Rec_Coords()


            for i in range(int(x1),int(x2),int(self.max_arrow_size/2)):
                    x1,y1_d =(i,y1)  #entlang der unteren Kante des Rechtecks
                    x1,y1_u = (i,y2) #entlang der oberen Kante des Rechtecks
                    cordx,cordy_d = self.Transform(x1,y1_d)
                    cordx,cordy_u = self.Transform(x1,y1_u)
                    Fy_d=self.F[1].evalf(0, subs={self.x: cordx, self.y:cordy_d})*self.scale  #stärke der Vektoren an der unteren Kante entlang der Y-Richtung
                    Fy_u=self.F[1].evalf(0, subs={self.x: cordx, self.y:cordy_u})*self.scale #stärke der Vektoren an der obern Kante entlang der Y-Richtung
                    y2_d=y1_d-Fy_d
                    y2_u=y1_u-Fy_u
                    if Fy_d == Fy_u or self.AreaInt_value == 0:
                        self.equal_flag = True
                    else:
                        self.equal_flag = False
                    if -Fy_d<0:
                        self.arrow_rec_create( x1, y1_d, x1, y2_d, c='#2AA138')
                    elif -Fy_d>0:
                        self.arrow_rec_create( x1, y1_d, x1, y2_d, c='#E0260C')
                    if -Fy_u>0:
                        self.arrow_rec_create( x1, y1_u, x1, y2_u, c='#2AA138')
                    elif -Fy_u<0:
                        self.arrow_rec_create( x1, y1_u, x1, y2_u, c='#E0260C')


            if self.rectx0>self.rectx1: #Reset der x Werte
                x1=self.rectx1
                x2=self.rectx0
            else:
                x1=self.rectx0
                x2=self.rectx1


            for i in range(int(y1),int(y2),int(self.max_arrow_size/2)):
                    x1_l,y =(x1,i)  #entlang der linke Kante des Rechtecks
                    x1_r,y = (x2,i) #entlang der rechten Kante des Rechtecks
                    cordx_l,cordy=self.Transform(x1_l,y)
                    cordx_r,cordy=self.Transform(x1_r,y)
                    Fx_l=self.F[0].evalf(0, subs={self.x: cordx_l, self.y:cordy})*self.scale  #stärke der Vektoren an der linken Kante entlang der X-Richtung
                    Fx_r=self.F[0].evalf(0, subs={self.x: cordx_r, self.y:cordy})*self.scale #stärke der Vektoren an der rechten Kante entlang der X-Richtung
                    x2_l=x1_l+Fx_l
                    x2_r=x1_r+Fx_r
                    if Fx_l == Fx_r or self.AreaInt_value == 0:
                        self.equal_flag = True
                    else:
                        self.equal_flag = False
                    if Fx_l<0:
                        self.arrow_rec_create( x1_l, y, x2_l, y, c='#2AA138') #grün
                    elif Fx_l>0:
                        self.arrow_rec_create( x1_l, y, x2_l, y, c='#E0260C') #rot
                    if Fx_r>0:
                        self.arrow_rec_create( x1_r, y, x2_r, y, c='#2AA138')
                    elif Fx_r<0:
                        self.arrow_rec_create( x1_r, y, x2_r, y, c='#E0260C')

        
        if self.checklanguage == 'DE':
            self.Flux_Output.config(text=f'{self.AreaInt_value} a.u.')
        else:
            self.Flux_Output.config(text=f'{self.AreaInt_value} a.u.')



    def draw_line_arrows(self):

        self.canvas.delete('rec_arrow')

        self.LineInt_value = self.calc_LineInt().evalf(2)

        if self.check_var_RectVec.get() == True:

            x1,x2,y1,y2 = self.order_Rec_Coords()

            for i in range(int(x1),int(x2),int(self.max_arrow_size)):
                x1_d,y_d =(i,y1)  #entlang der unteren Kante des Rechtecks (down)
                x1_u,y_u = (i,y2) #entlang der oberen Kante des Rechtecks (up)
                cordx_d,cordy_d=self.Transform(x1_d,y_d)
                cordx_u,cordy_u=self.Transform(x1_u,y_u)
                Fx_d=self.F[0].evalf(0, subs={self.x: cordx_d, self.y:-cordy_d})*self.scale #stärke der Vektoren an der unteren Kante entlang der X-Richtung
                Fx_u=self.F[0].evalf(0, subs={self.x: cordx_u, self.y:-cordy_u})*self.scale #stärke der Vektoren an der obern Kante entlang der X-Richtung
                x2_d=x1_d+Fx_d
                x2_u=x1_u+Fx_u
                if Fx_d == Fx_u or self.LineInt_value == 0:
                    self.equal_flag = True
                else:
                    self.equal_flag = False
                if Fx_d<0:
                    self.arrow_rec_create( x1_d, y_d, x2_d, y_d, c='#2AA138')
                elif Fx_d>0:
                    self.arrow_rec_create( x1_d, y_d, x2_d, y_d, c='#E0260C')
                if Fx_u>0:
                    self.arrow_rec_create( x1_u, y_u, x2_u, y_u, c='#2AA138')
                elif Fx_u<0:
                    self.arrow_rec_create( x1_u, y_u, x2_u, y_u, c='#E0260C')


            if self.rectx0>self.rectx1: #Reset der x Werte
                x1=self.rectx1
                x2=self.rectx0
            else:
                x1=self.rectx0
                x2=self.rectx1

            for j in range(int(y1),int(y2),int(self.max_arrow_size)):
                x_l,y1_l =(x1,j)  #entlang der linke Kante des Rechtecks
                x_r,y1_r = (x2,j) #entlang der rechten Kante des Rechtecks
                cordx_l,cordy_l=self.Transform(x_l,y1_l)
                cordx_r,cordy_r=self.Transform(x_r,y1_r)
                Fy_l=self.F[1].evalf(0, subs={self.x: cordx_l, self.y:-cordy_l})*self.scale  #stärke der Vektoren an der linken Kante entlang der Y-Richtung
                Fy_r=self.F[1].evalf(0, subs={self.x: cordx_r, self.y:-cordy_r})*self.scale #stärke der Vektoren an der rechten Kante entlang der Y-Richtung
                y2_l=y1_l-Fy_l
                y2_r=y1_r-Fy_r
                if Fy_l == Fy_r or self.LineInt_value == 0:
                    self.equal_flag = True
                else:
                    self.equal_flag = False
                if -Fy_l>0:
                    self.arrow_rec_create( x_l, y1_l, x_l, y2_l, c='#2AA138') #grün
                elif -Fy_l<0:
                    self.arrow_rec_create( x_l, y1_l, x_l, y2_l, c='#E0260C') #rot
                if -Fy_r<0:
                    self.arrow_rec_create( x_r, y1_r, x_r, y2_r, c='#2AA138')
                elif -Fy_r>0:
                    self.arrow_rec_create( x_r, y1_r, x_r, y2_r, c='#E0260C')


        
        if self.checklanguage == 'DE':
            self.Flux_Output.config(text=f'{self.LineInt_value} a.u.')
        else:
            self.Flux_Output.config(text=f'{self.LineInt_value} a.u.')

## --------- Visualisierung der Partiellen Ableitungen

    def catch_inRect_vec(self):
        self.canvas.delete('partial_x_arrow', 'partial_y_arrow','fieldscanner_partial_x','fieldscanner_partial_y')
        self.canvas.itemconfig('field_arrow', fill='gray')
        if self.check_fieldscanner_var.get() == True:
            vector_list = self.canvas.find_withtag('clickarrow')
            print('Vectorlist: ',vector_list)
        else:
            vector_list = self.canvas.find_enclosed(self.rectx0+2, self.recty1-2, self.rectx1-2, self.recty0+2)  #in dem rechteck von oben links nach unten rechts
        
        for v in vector_list:
            x0, y0 = (self.canvas.coords(v)[0], self.canvas.coords(v)[1])
            if self.check_fieldscanner_var == True:
                self.draw_vector_components(x0,y0,tagx='fieldscanner_partial_x',tagy='fieldscanner_partial_y')
            else:
                self.draw_vector_components(x0,y0,tagx='partial_x_arrow',tagy='partial_y_arrow')

    def draw_vector_components(self,x0,y0,tagx,tagy):        
            x,y = self.Transform(x0,y0)
            Fx=self.F[0].evalf(5, subs={self.x: x, self.y:y})*self.scale
            Fy=self.F[1].evalf(5,subs={self.x: x, self.y:y})*self.scale
            x1=x0+Fx
            y1=y0-Fy
            if self.check_var_partialx.get() == True:
                self.canvas.create_line(x0,y0,x1,y0,width=1, arrow=tk.LAST, fill='blue', tags=(tagx,))
            if self.check_var_partialy.get() == True:
                self.canvas.create_line(x0,y0,x0,y1,width=1, arrow=tk.LAST, fill='orange', tags=(tagy,))
            if self.check_var_partialx.get() == True or self.check_var_partialy.get() == True:
                self.canvas.itemconfig('field_arrow', fill='gray')

## -------- Zeichnungsfunktionen
    def arrow_create(self,x1,y1,x2,y2, c='black'): #erzeugt einen einzelenen Pfeil
        vec_leng = mt.sqrt((x1-x2)**2+(y1-y2)**2)
        if vec_leng < 4: return
        self.canvas.create_line(x1, y1, x2, y2,width=1, arrow=tk.LAST, fill=c, tags=('field_arrow',))

    def arrow_rec_create(self,x1,y1,x2,y2, c='black'):
        vec_leng = mt.sqrt((x1-x2)**2+(y1-y2)**2)
        if vec_leng < 4: return
        if self.equal_flag:
            c= self.reduce_color(c)
        self.canvas.create_line(x1, y1, x2, y2,width=1, arrow=tk.LAST, fill=c, tags=('rec_arrow',))

    def reduce_color(self,c):
        if c == '#2AA138':
            c = '#99E099'
        else:
            c = '#E1A198'
        return c

    def draw_field(self): # Zeichnet alle Vektropfeile
        for i in range(int(self.canvas_size/2),self.canvas_size+1,int(self.max_arrow_size)):      #X-Koordinate int(max_arrow_size)
            for j in range(int(self.canvas_size/2),self.canvas_size+1,int(self.max_arrow_size)):  #Y-Koordinate
                x1,y1 =self.Transform(i,j)
                Fx=self.F[0].evalf(5, subs={self.x: x1, self.y:y1})*self.scale
                Fy=self.F[1].evalf(5,subs={self.x: x1, self.y:y1})*self.scale
                x2=i+Fx
                y2=j-Fy
                self.arrow_create( i, j, x2, y2)
            for k in range(int(self.canvas_size/2),self.canvas_size+1,int(self.max_arrow_size)):
                j=self.canvas_size-k
                x1,y1 =self.Transform(i,j)
                Fx=self.F[0].evalf(5, subs={self.x: x1, self.y:y1})*self.scale
                Fy=self.F[1].evalf(5,subs={self.x: x1, self.y:y1})*self.scale
                x2=i+Fx
                y2=j-Fy
                self.arrow_create( i, j, x2, y2)

        for l in range(int(self.canvas_size/2),self.canvas_size+1,int(self.max_arrow_size)):      #X-Koordinate int(max_arrow_size)
            i = self.canvas_size-l
            for j in range(int(self.canvas_size/2),self.canvas_size+1,int(self.max_arrow_size)):  #Y-Koordinate
                x1,y1 =self.Transform(i,j)
                Fx=self.F[0].evalf(5, subs={self.x: x1, self.y:y1})*self.scale
                Fy=self.F[1].evalf(5,subs={self.x: x1, self.y:y1})*self.scale
                x2=i+Fx
                y2=j-Fy
                self.arrow_create( i, j, x2, y2)
            for k in range(int(self.canvas_size/2),self.canvas_size+1,int(self.max_arrow_size)):
                j=self.canvas_size-k
                x1,y1 =self.Transform(i,j)
                Fx=self.F[0].evalf(5, subs={self.x: x1, self.y:y1})*self.scale
                Fy=self.F[1].evalf(5,subs={self.x: x1, self.y:y1})*self.scale
                x2=i+Fx
                y2=j-Fy
                self.arrow_create( i, j, x2, y2)


    def max_arrow_length(self): #Berechnet den längsten Vektor zum Skalieren aller Vektoren
        max_length=0
        for i in range(0,self.canvas_size+1,int(self.max_arrow_size)):      #X-Koordinate int(max_arrow_size)
            for j in range(0,self.canvas_size+1,int(self.max_arrow_size)):  #Y-Koordinate
                x1,y1 = self.Transform(i,j)
                Fx=self.F[0].evalf(5, subs={self.x: x1, self.y:y1})
                Fy=self.F[1].evalf(5,subs={self.x: x1, self.y:y1})
                arrowlength= mt.sqrt((Fx)**2+(Fy)**2)
                if arrowlength> max_length:
                    max_length = arrowlength
        return max_length+self.arrow_space

## -------- Hilfsfunktionen

    def order_Rec_Coords(self):
        if self.rectx0>self.rectx1: #jede aufziehrichtung des Rechtecks abfangen
            x1=self.rectx1
            x2=self.rectx0
        else:
            x1=self.rectx0
            x2=self.rectx1

        if self.recty0>self.recty1:
            y1=self.recty1
            y2=self.recty0
        else:
            y1=self.recty0
            y2=self.recty1
        return(x1,x2,y1,y2)

    def Transform(self,x,y):  #koordinatentransformation für jeweils ein Tupel (x,y)
        c = self.canvas_size/2
        skale_by_vectornumber=self.canvas_size/self.slider.get()
        x = (x-c)/skale_by_vectornumber
        y = (c-y)/skale_by_vectornumber
        return (x,y)






## -------------------------------  MAIN  --------------------------------- ##


bg = 'white'
font = 'Times'
fg = 'black'
width=1400
height=800

def ende():             #Beenden des Programms
    app.master.destroy()


app = App()
app.master.geometry("1400x800")
app.master.title('vere vedi vecu')
app.master.iconphoto(True, tk.PhotoImage(file='icon.png'))
app.master.config(bg=bg)
app.mainloop()
