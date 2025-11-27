from django.test import TestCase, Client, RequestFactory
from django.template import Template, Context
from .models import Menu, MenuItem
class TreeMenuTests(TestCase):
    def setUp(self):
        self.menu = Menu.objects.create(name="main_menu")
        MenuItem.objects.create(menu=self.menu, title="Главная", url="/", order=0)
        about = MenuItem.objects.create(menu=self.menu, title="О нас", url="/page/about/", order=1)
        MenuItem.objects.create(menu=self.menu, title="Команда", url="/page/about/team/", parent=about, order=0)
        MenuItem.objects.create(menu=self.menu, title="Карьера", url="/page/about/careers/", parent=about, order=1)
        MenuItem.objects.create(menu=self.menu, title="Контакты", url="/page/contact/", order=2)
        self.client = Client()
        self.factory = RequestFactory()
    def test_single_query_for_menu(self):
        template = Template("{% load draw_menu %}{% draw_menu 'main_menu' %}")
        request = self.factory.get("/")
        context = Context({"request": request})
        with self.assertNumQueries(1):
            rendered = template.render(context)
            self.assertIn("tree-menu", rendered)
    def test_active_item_is_detected(self):
        response = self.client.get("/page/about/team/")
        # Проверяем, что пункт меню с заголовком 'Команда' присутствует на странице
        self.assertContains(response, "Команда")
        self.assertContains(response, "menu-item")
