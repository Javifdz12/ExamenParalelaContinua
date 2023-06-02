import threading
import random
import time
import hashlib
from flask import Flask, jsonify, request

class Transaction:
    def __init__(self, attacker, defender):
        self.attacker = attacker
        self.defender = defender
        self.timestamp = time.time()

    def calculate_hash(self):
        data = self.attacker + self.defender + str(self.timestamp)
        return hashlib.sha256(data.encode()).hexdigest()

class Pokemon:
    def __init__(self, name, level, hp):
        self.name = name
        self.level = level
        self.hp = hp
        self.attacks = ["Ataque 1", "Ataque 2", "Ataque 3", "Ataque 4"]

    def attack(self, opponent):
        attack_name = random.choice(self.attacks)
        attack_power = random.randint(10, 20)
        print(f"{self.name} ataca a {opponent.name} con {attack_name} y causa {attack_power} puntos de daño.")
        opponent.receive_damage(attack_power)

    def receive_damage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            print(f"{self.name} ha sido derrotado.")

    def battle(self, opponent, blockchain):
        while self.hp > 0 and opponent.hp > 0:
            self.attack(opponent)
            transaction = Transaction(self.name, opponent.name)
            blockchain.add_transaction(transaction)
            time.sleep(1)  # Esperar un segundo entre ataques

        if self.hp > 0:
            print(f"{self.name} ha ganado la batalla.")
        else:
            print(f"{opponent.name} ha ganado la batalla.")

class Block:
    def __init__(self, previous_hash):
        self.transactions = []
        self.previous_hash = previous_hash
        self.timestamp = time.time()
        self.nonce = 0
        self.hash = self.calculate_hash()
    def calculate_hash(self):
        data = str(self.transactions) + self.previous_hash + str(self.timestamp) + str(self.nonce)
        return hashlib.sha256(data.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
    def create_genesis_block(self):
        return Block("0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_transaction(self, transaction):
        latest_block = self.get_latest_block()
        latest_block.transactions.append(transaction)
        return True

    def mine_block(self, nonce_difficulty):
        latest_block = self.get_latest_block()
        prefix_zeros = "0" * nonce_difficulty

        while latest_block.hash[:nonce_difficulty] != prefix_zeros:
            latest_block.nonce += 1
            latest_block.hash = latest_block.calculate_hash()

        self.chain.append(latest_block)

# Crear dos Pokémon para la batalla
pokemon1 = Pokemon("Pikachu", 10, 100)
pokemon2 = Pokemon("Charizard", 15, 150)

blockchain = Blockchain()

app = Flask(__name__)

@app.route('/Users/usuario/ExamenParalelaContinua/sucio.py', methods=['GET'])
def get_transactions():
    # Obtener todas las transacciones de la blockchain
    transactions = []
    for block in blockchain.chain:
        transactions.extend(block.transactions)

    # Devolver las transacciones en formato JSON
    return jsonify(transactions)

@app.route('/Users/usuario/ExamenParalelaContinua/sucio.py', methods=['POST'])
def add_transaction():
    # Obtener los datos de la transacción del cuerpo de la solicitud
    data = request.get_json()
    attacker = data['attacker']
    defender = data['defender']

    # Crear una nueva transacción
    transaction = Transaction(attacker, defender)

    # Agregar la transacción a la blockchain
    blockchain.add_transaction(transaction)

    # Devolver una respuesta exitosa
    return jsonify({'message': 'Transaction added successfully'})

@app.route('/Users/usuario/ExamenParalelaContinua/sucio.py', methods=['GET'])
def get_battles():
    # Obtener la información de las batallas de la blockchain
    battles = []
    for block in blockchain.chain:
        for transaction in block.transactions:
            battles.append({
                'attacker': transaction.attacker,
                'defender': transaction.defender
            })

    # Devolver la información de las batallas en formato JSON
    return jsonify(battles)

# Resto del código existente

if __name__ == '__main__':
    # Crear hilos para simular la batalla entre los dos Pokémon
    thread1 = threading.Thread(target=pokemon1.battle, args=(pokemon2, blockchain))
    thread2 = threading.Thread(target=pokemon2.battle, args=(pokemon1, blockchain))

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

    for block in blockchain.chain:
        print(f"Hash: {block.hash}")
        print(f"Previous Hash: {block.previous_hash}")
        print(f"Transactions: {block.transactions}")
        print()

    app.run()
