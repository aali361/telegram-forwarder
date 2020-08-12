# from asgiref.sync import sync_to_async
import time
from django.utils import timezone
from django.core.management.base import BaseCommand
from telethon import TelegramClient, events, sync

from account import models as acc_models


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('account_id', type=int, help='Indicates the id of account')

    def handle(self, *args, **options):
        account_id = options['account_id']
        account = acc_models.Account.objects.get(pk=account_id)
        print('***** Forward msg... {}, time: {}'.format(account.phone, timezone.now()))
        client = TelegramClient(account.phone, account.api_id, account.api_hash)

        try:
            assert client.connect()
        except AssertionError:
            if not client.is_user_authorized():
                client.send_code_request(account.phone)
            me = client.sign_in(account.phone, account.log_in_code)
            client.start()


        @client.on(events.NewMessage(incoming=True))
        async def my_event_handler(event):
            account = acc_models.Account.objects.get(pk=account_id)
            chat = await event.get_chat()
            sender = await event.get_sender()
            if sender.username == account.admin_username:
                account = acc_models.Account.objects.get(pk=account_id)
                print('msg from admin')
                for id in account.ids:
                    try:
                        await event.forward_to(id)
                    except Exception as e:
                        print('error: user id {} not found'.format(id))
                        print(str(e))
                        continue
                    time.sleep(account.delay_between_msg)
                client.disconnect()


        client.run_until_disconnected()