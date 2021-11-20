from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

from Crypto.PublicKey import RSA

from reg.models import Key


class Command(BaseCommand):

    help = 'Cli-команда, создающая ключи RSA для РЦ.'

    def handle(self, *args, **kwargs) -> None:

        """
        "manage.py add_keys"
        """

        private_key = RSA.generate(2048)
        public_key = private_key.publickey()

        key, _ = Key.objects.get_or_create(type=Key.KeyType.Reg, active=True)

        key.private_key.save(
            f'private_key.pem',
            ContentFile(private_key.export_key('PEM')),
            save=True
        )
        key.public_key.save(
            f'public_key.pem',
            ContentFile(public_key.export_key('PEM')),
            save=True
        )

        self.stdout.write(self.style.SUCCESS('The RSA keys generated.'))
