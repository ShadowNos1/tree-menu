from django.core.management.base import BaseCommand
from tree_menu.models import Menu, MenuItem
class Command(BaseCommand):
    help = "Создать демонстрационное меню для приложения"
    def handle(self, *args, **options):
        menu, created = Menu.objects.get_or_create(name="main_menu")
        MenuItem.objects.filter(menu=menu).delete()
        home = MenuItem.objects.create(menu=menu, title="Home", url="/", order=0)
        about = MenuItem.objects.create(menu=menu, title="About", url="/page/about/", order=10)
        team = MenuItem.objects.create(menu=menu, title="Team", url="/page/about/team/", parent=about, order=0)
        careers = MenuItem.objects.create(menu=menu, title="Careers", url="/page/about/careers/", parent=about, order=1)
        contact = MenuItem.objects.create(menu=menu, title="Contact", url="/page/contact/", order=20)
        self.stdout.write(self.style.SUCCESS("Demo menu created"))
