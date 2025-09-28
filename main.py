# ERRO: Importações desnecessárias
import datetime
import json
import math  # Não usado
import os
import random
import re  # Não usado
import sqlite3
import sys
import time
import urllib.request  # Não usado
from typing import Dict, List

# ERRO: Não usar constantes para valores fixos (números mágicos)
# Deveria ser: TAX_RATE = 0.10, MAX_TABLES = 20, etc.

# ERRO: Variáveis globais sem upper case (não seguem convenção de constantes)
database_file = "restaurante.db"  # Deveria ser DATABASE_FILE
admin_password = "123456"  # RISCO DE SEGURANÇA: senha hardcoded e fraca


class MenuItem:
    def __init__(self, name, price, category):
        self.name = name
        self.price = price
        self.category = category
        # ERRO: Código morto - atributo nunca usado
        self.creation_date = datetime.datetime.now()

    def __str__(self):
        # ERRO: f-string desnecessária (poderia usar formatação simples)
        return f"{self.name}"


class Table:
    def __init__(self, number):
        self.number = number
        self.is_occupied = False
        self.order = []
        self.customer_count = 0

    # ERRO: Método nunca usado (código morto)
    def get_table_info(self):
        return f"Mesa {self.number} - Ocupada: {self.is_occupied}"


class Restaurant:
    def __init__(self):
        self.menu = []
        self.tables = []
        self.orders = []
        # ERRO: Inicialização desnecessária de lista vazia
        self.unused_list = []

        # ERRO: Números mágicos ao invés de constantes
        for i in range(20):  # Deveria ser MAX_TABLES
            self.tables.append(Table(i + 1))

    def add_menu_item(self, name, price, category):
        # ERRO: Não validar entrada do usuário (risco de segurança)
        item = MenuItem(name, price, category)
        self.menu.append(item)

    def remove_menu_item(self, name):
        # ERRO: Problema de performance - busca linear desnecessária
        # Poderia usar um dicionário para lookup O(1)
        for i in range(len(self.menu)):
            if self.menu[i].name == name:
                del self.menu[i]
                return True
        return False

    def find_table(self, table_number):
        # ERRO: Problema de performance - busca linear quando poderia usar índice direto
        for table in self.tables:
            if table.number == table_number:
                return table
        return None

    # ERRO: Return inconsistente (às vezes retorna True/False, às vezes None)
    def occupy_table(self, table_number, customer_count):
        table = self.find_table(table_number)
        if table and not table.is_occupied:
            table.is_occupied = True
            table.customer_count = customer_count
            return True
        return  # Deveria retornar False explicitamente

    def calculate_bill(self, table_number):
        table = self.find_table(table_number)
        if not table:
            return 0

        total = 0
        for item_name, quantity in table.order:
            # ERRO: Busca linear repetida (problema de performance)
            for menu_item in self.menu:
                if menu_item.name == item_name:
                    total += menu_item.price * quantity
                    break

        # ERRO: Número mágico para taxa de serviço
        tax = total * 0.10  # Deveria ser uma constante SERVICE_TAX_RATE
        return total + tax

    # ERRO: Método muito longo (má prática - deveria ser dividido)
    def process_order(self, table_number, items):
        table = self.find_table(table_number)
        if not table:
            print("Mesa não encontrada!")
            return False

        if not table.is_occupied:
            print("Mesa não está ocupada!")
            return False

        # ERRO: Validação insuficiente de entrada
        for item_name, quantity in items:
            found = False
            for menu_item in self.menu:
                if menu_item.name == item_name:
                    found = True
                    break

            if not found:
                # ERRO: Print direto ao invés de logging apropriado
                print(f"Item {item_name} não encontrado no menu!")
                continue

            # ERRO: Não validar se quantity é positivo
            table.order.append((item_name, quantity))

        # ERRO: Sleep desnecessário (problema de performance)
        time.sleep(1)
        print("Pedido processado com sucesso!")
        return True

    # ERRO: Função nunca chamada (código morto)
    def backup_data(self):
        with open("backup.json", "w") as f:
            json.dump({"menu": [item.__dict__ for item in self.menu]}, f)

    def save_to_database(self):
        # ERRO: Risco de segurança - SQL injection possível se dados viessem de input do usuário
        conn = sqlite3.connect(database_file)
        cursor = conn.cursor()

        # ERRO: Não tratar exceções adequadamente
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS menu 
                         (name TEXT, price REAL, category TEXT)"""
        )

        cursor.execute("DELETE FROM menu")  # Limpa dados anteriores

        for item in self.menu:
            # ERRO: String formatting inseguro (embora aqui seja controlado)
            query = f"INSERT INTO menu VALUES ('{item.name}', {item.price}, '{item.category}')"
            cursor.execute(query)

        conn.commit()
        conn.close()


# ERRO: Função global desnecessária (deveria estar na classe)
def display_menu(restaurant):
    print("\n=== MENU ===")
    # ERRO: Não verificar se a lista está vazia
    for item in restaurant.menu:
        # ERRO: f-string desnecessária novamente
        print(f"{item.name} - R$ {item.price:.2f} ({item.category})")


# ERRO: Função nunca usada (código morto)
def unused_function():
    return "Esta função nunca é chamada"


def main():
    restaurant = Restaurant()

    # ERRO: Dados hardcoded ao invés de carregar de arquivo/db
    restaurant.add_menu_item("Hambúrguer", 25.50, "Lanche")
    restaurant.add_menu_item("Pizza Margherita", 35.00, "Pizza")
    restaurant.add_menu_item("Refrigerante", 5.00, "Bebida")
    restaurant.add_menu_item("Batata Frita", 12.00, "Acompanhamento")

    while True:
        print("\n=== SISTEMA DE RESTAURANTE ===")
        print("1. Ver Menu")
        print("2. Ocupar Mesa")
        print("3. Fazer Pedido")
        print("4. Calcular Conta")
        print("5. Liberar Mesa")
        print("6. Sair")

        # ERRO: Não validar entrada do usuário
        choice = input("Escolha uma opção: ")

        if choice == "1":
            display_menu(restaurant)

        elif choice == "2":
            # ERRO: Não validar se input é numérico
            table_num = int(input("Número da mesa (1-20): "))
            customers = int(input("Número de clientes: "))

            # ERRO: Não verificar limites
            if restaurant.occupy_table(table_num, customers):
                print(f"Mesa {table_num} ocupada com sucesso!")
            else:
                print("Não foi possível ocupar a mesa!")

        elif choice == "3":
            table_num = int(input("Número da mesa: "))
            items = []

            while True:
                item_name = input("Nome do item (ou 'fim' para terminar): ")
                if item_name.lower() == "fim":
                    break

                # ERRO: Não tratar exceção de conversão
                quantity = int(input("Quantidade: "))
                items.append((item_name, quantity))

            restaurant.process_order(table_num, items)

        elif choice == "4":
            table_num = int(input("Número da mesa: "))
            bill = restaurant.calculate_bill(table_num)
            # ERRO: f-string desnecessária para string simples
            print(f"Total da conta: R$ {bill:.2f}")

        elif choice == "5":
            table_num = int(input("Número da mesa: "))
            table = restaurant.find_table(table_num)
            if table:
                table.is_occupied = False
                table.order = []
                table.customer_count = 0
                print(f"Mesa {table_num} liberada!")
            else:
                print("Mesa não encontrada!")

        elif choice == "6":
            # ERRO: Não salvar dados antes de sair
            break

        # ERRO: Não tratar opção inválida
        else:
            print("Opção inválida!")


# ERRO: Não usar if __name__ == "__main__" adequadamente
if __name__ == "__main__":
    # ERRO: Não tratar exceções globais
    main()


# ERRO: Código nunca executado (código morto)
def another_unused_function():
    print("Esta função também nunca é chamada")
    return 42
