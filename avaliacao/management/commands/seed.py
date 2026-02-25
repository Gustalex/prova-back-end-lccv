from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    Comando para popular o banco de dados com dados de exemplo.
    """

    help = "Popula o banco de dados com dados de exemplo"

    def handle(self, *args, **options):
        """
        Executa os comandos para carregar as fixtures.
        """
        self.stdout.write(self.style.NOTICE("Carregando fixtures..."))
        call_command("loaddata", "fixtures/colaboradores")
        call_command("loaddata", "fixtures/tipos_itens_avaliacao")
        self.stdout.write(self.style.SUCCESS("Dados carregados com sucesso!"))
