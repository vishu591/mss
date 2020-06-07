import sys
import socket

from Client.Main_client import Client

class FirstClient:
    def main(self):
        client_obj = Client()
        client_obj.select_choice()

if __name__ == "__main__":
    FirstClient().main()