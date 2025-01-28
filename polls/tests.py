from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from django.contrib.auth.models import User
from selenium.webdriver.support.ui import Select
class MySeleniumTests(StaticLiveServerTestCase):
    # carregar una BD de test
    fixtures = ['testdb.json',]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        opts = Options()
        cls.selenium = WebDriver(options=opts)
        cls.selenium.implicitly_wait(5)

    @classmethod
    def tearDownClass(cls):
        # tanquem browser
        # comentar la propera línia si volem veure el resultat de l'execució al navegador
        cls.selenium.quit()
        super().tearDownClass()


    def test_login(self):

        #Crear usuario
        User.objects.create_superuser(username='isard',password='pirineus',email='admin@admin.com')

        # anem directament a la pàgina d'accés a l'admin panel
        self.selenium.get('%s%s' % (self.live_server_url, '/admin/login/'))

        # comprovem que el títol de la pàgina és el que esperem
        self.assertEqual( self.selenium.title , "Log in | Django site admin" )

        # introduïm dades de login i cliquem el botó "Log in" per entrar
        username_input = self.selenium.find_element(By.NAME,"username")
        username_input.send_keys('isard')
        password_input = self.selenium.find_element(By.NAME,"password")
        password_input.send_keys('pirineus')
        self.selenium.find_element(By.XPATH,'//input[@value="Log in"]').click()

        # testejem que hem entrat a l'admin panel comprovant el títol de la pàgina
        self.assertEqual(self.selenium.title, "Site administration | Django site admin")
        #Hacemos click en add que sera para añadir un usuario
        self.selenium.find_element(By.XPATH, '//a[@href="/admin/auth/user/add/"]').click()
        #Introducimos datos del usuario que vamos a crear
        username_input = self.selenium.find_element(By.NAME,"username")
        username_input.send_keys('admin')
        password_input1 = self.selenium.find_element(By.NAME,"password1")
        password_input1.send_keys('Admin2025.')
        password_input2 = self.selenium.find_element(By.NAME,"password2")
        password_input2.send_keys('Admin2025.')

        #Le damos a guardar
        self.selenium.find_element(By.XPATH,'//input[@value="Save"]').click()

        #Asignamos permisos de Staff

        self.selenium.find_element(By.ID,"id_is_staff").click()

        #Asignamos permisos para que pueda visualizar las questions
        input = self.selenium.find_element(By.ID,"id_user_permissions_input")
        input.send_keys('question')

        menu = self.selenium.find_element(By.ID,"id_user_permissions_from")
        eleccion = Select(menu)
        eleccion.select_by_value("4")

        self.selenium.find_element(By.ID,"id_user_permissions_add_link").click()

        #Guardamos el usuario con los permisos
        self.selenium.find_element(By.NAME,"_save").click()

        #Cerramos sesion del usuario actual
        self.selenium.find_element(By.XPATH, '//form[@id="logout-form"]//button[@type="submit"]').click()

        #Hacemos click en login
        self.selenium.find_element(By.XPATH, '//a[@href="/admin/"]').click()

        #Iniciamos sesion con el usuario que hemos creado
        username_input = self.selenium.find_element(By.NAME,"username")
        username_input.send_keys('admin')
        password_input = self.selenium.find_element(By.NAME,"password")
        password_input.send_keys('Admin2025.')
        self.selenium.find_element(By.XPATH,'//input[@value="Log in"]').click()

        #Hacemos click en view para poder visualizar las questions
        self.selenium.find_element(By.CLASS_NAME,"viewlink").click()

        #Comprobamos que podemos visualizar las questions
        self.assertTrue(self.selenium.find_element(By.TAG_NAME, 'h1').text == "Select question to view")

        #Comprobamos que pueda eliminar questions
        self.selenium.find_element(By.XPATH,'//a[@href="/admin/polls/question/1/change/"]').click()
        self.selenium.get(f'{self.live_server_url}/admin/polls/question/1/delete/')
        url = self.selenium.current_url
        self.assertNotEqual(url, f'{self.live_server_url}/admin/polls/question/1/delete',"No puedes acceder por falta de permisos. ")


        #Comprobamos si no puede añadir questions
        self.selenium.get(f'{self.live_server_url}/admin/polls/question/add')

        url= self.selenium.current_url
        self.assertNotEqual(url, f'{self.live_server_url}/admin/polls/question/add',"No puedes acceder por falta de permisos. ")

