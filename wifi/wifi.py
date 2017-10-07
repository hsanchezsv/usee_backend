import kivy,sqlite3,time,signal,subprocess,os

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.clock import Clock
from threading import Thread

class MyApp(App):

	_layout=GridLayout(rows=1)
	_data=[]
	_displaying=0
	_num_controls=0
	_name_controls=[]
	_temp_ans=[]
	_ssid='net'
	_spass='passnet'

	def load_data(self):
		data=[]
		r = subprocess.Popen('sudo iwlist wlan0 scan', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		for line in r.stdout.readlines():
			#print line
			if "ESSID:" in line:
				line=line.replace("ESSID:","")
				line=line.replace("\"","")
				line=line.strip()
				print line
				data.append(line)
		return data

	def callback(self,instance):
		layout_res=self.pass_screen(instance.id)
		self._layout.add_widget(layout_res)
		print('The button <%s> is being pressed' % instance.id)

	def save_network(self,instance):
		n_conf=True
		str_conf="""\nnetwork={\n\tssid=\""""+ self._ssid +"""\"\n\tpsk=\""""+ self._t_input.text +"""\"\n}""" 
		print str_conf
		preconfig="country=GB\nctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev\nupdate_config=1\n\n"
		open("/etc/wpa_supplicant/wpa_supplicant.conf","wb").write(preconfig)
		os.system("""sudo wpa_passphrase \""""+ self._ssid +"""\" \""""+ self._t_input.text +"""\" >> /etc/wpa_supplicant/wpa_supplicant.conf""")
		
		#country=GB \n ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev \n update_config=1
		# wpa_passphrase "testing" "testingPassword" >> /etc/wpa_supplicant/wpa_supplicant.conf
		self.final_screen()

	def pass_screen(self,ssid):
		self._ssid=ssid
		self._layout.clear_widgets()
		layout_res=BoxLayout(padding=60,orientation='vertical',spacing=10)
		lbl_1=Label(text="Wifi Manager", font_size=22,halign='center')
		layout_res.add_widget(lbl_1)
		lbl_2=Label(text="Ingrese el password", font_size=20,halign='center')
		layout_res.add_widget(lbl_2)
		self._t_input = TextInput(text='', multiline=False,size_hint = (1,.5))
		layout_res.add_widget(self._t_input)
		b_save = Button(text="Guardar",size_hint = (1,.3))
		layout_res.add_widget(b_save)
		b_save.bind(on_press=self.save_network)
		
		b_exit = Button(text="Salir",size_hint = (1,.3))
		layout_res.add_widget(b_exit)
		b_exit.bind(on_press=self.exit_app)
		return layout_res


	def create_btn(self,items):
		layout_res=BoxLayout(padding=10,orientation='vertical',spacing=5)
		
		lbl_pre=Label(text="Wifi Manager", font_size=24,halign='center')
		layout_res.add_widget(lbl_pre)
		
		for item in items:
			self._name_controls.append(self._num_controls)
			self._name_controls[self._num_controls] = Button(text=item, id=item,size_hint = (1,.3))
			self._name_controls[self._num_controls].bind(on_press=self.callback)
			layout_res.add_widget(self._name_controls[self._num_controls])
			self._num_controls+=1
			
		b_exit = Button(text="Salir",size_hint = (1,.3))
		layout_res.add_widget(b_exit)
		b_exit.bind(on_press=self.exit_app)
		
		return layout_res

	def exit_app(self,instance):
		os.system("clear")
		MyApp.get_running_app().stop()

	def exit_last_app(self):
		os.system("sudo iwconfig")
		MyApp.get_running_app().stop()

	def final_screen(self):
		self._layout.clear_widgets()
		layout_res=BoxLayout(padding=60,orientation='vertical',spacing=10)
		lbl_1=Label(text="Red configurada", font_size=28,halign='center')
		layout_res.add_widget(lbl_1)
		
		lbl_2=Label(text="Espere mientras se conecta ...",font_size=16)
		layout_res.add_widget(lbl_2)
		self._layout.add_widget(layout_res)
		os.system("clear")
		os.system("sudo wpa_cli reconfigure")
		Clock.schedule_once(lambda dt: self.exit_last_app(), 5)
		#Clock.schedule_once(lambda dt: os.system("sudo shutdown -r now"), 5)
		return 

	def show_components(self,data):
		self._layout.clear_widgets()
		layout_res=self.create_btn(data)
		self._layout.add_widget(layout_res)
		self._displaying+=1
		return 

	def main(self):
		self._data=[]
		self._displaying=0
		self._num_controls=0
		self._name_controls=[]
		self._temp_ans=[]

		self._data=self.load_data()
		self.show_components(self._data)

	def build(self):
		Thread(target=self.main, args=()).start()
		return self._layout


if __name__ == '__main__':
    MyApp().run()
