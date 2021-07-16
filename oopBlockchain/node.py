import argparse
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from wallet import Wallet
from blockchain import Blockchain
import json


app = Flask(__name__)


CORS(app)


@app.route("/", methods=["GET"])
def get_node_ui():
    return send_from_directory("ui", "node.html")


@app.route("/network", methods=["GET"])
def get_network_ui():
    return send_from_directory("ui", "network.html")


@app.route("/wallet", methods=["POST"])
def create_keys():
    wallet.create_keys()
    if wallet.save_keys():

        global blockchain
        blockchain = Blockchain(wallet.public_key, port)

        response = {
            "public_key": wallet.public_key,
            "private_key": wallet.private_key,
            "funds": blockchain.get_balance(),
        }

        return jsonify(response), 201
    else:
        response = {"message": "saving keys failed"}
        return jsonify(response), 500


@app.route("/broadcast-transaction", methods=["POST"])
def broadcast_transaction():
    values = request.get_json()

    if not values:
        response = {
            "message": "no data found",
        }
        return response, 400

    required = ["sender", "recipient", "amount", "signature"]
    if not all(key in values for key in required):
        response = {
            "message": "data missing",
        }
        return response, 400

    success = blockchain.add_transaction(
        values["recipient"], values["sender"], values["signature"], values["amount"], is_receiving=True
    )

    if success:
        response = {
            "message": "Transaction created successfully",
            "transaction": {
                "sender": values["sender"],
                "recipient": values["recipient"],
                "signature": values["signature"],
                "amount": values["amount"],
            },
        }
        return jsonify(response), 201
    else:
        response = {"message": "Transaction addition failed"}
        return jsonify(response), 500


@app.route("/broadcast-block", methods=["POST"])
def broadcast_block():
    values = request.get_json()

    if not values:
        response = {
            "message": "no data found",
        }
        return jsonify(response), 400

    if "block" not in values:
        response = {
            "message": "data missing",
        }
        return jsonify(response), 400

    block = values["block"]

    if block["index"] == blockchain.chain[-1].index + 1:
        if blockchain.add_block(block):
            response = {"message": "Block added"}
            return jsonify(response), 201
        else:
            response = {"message": "Block addition failed"}
            return jsonify(response), 500

    elif block["index"] > blockchain.chain[-1].index:
        pass
    else:
        response = {"message": "Incoming block is shorter, doing nothing"}
        return jsonify(response), 409


@app.route("/wallet", methods=["GET"])
def load_keys():
    if wallet.load_keys():
        global blockchain
        blockchain = Blockchain(wallet.public_key, port)

        response = {
            "public_key": wallet.public_key,
            "private_key": wallet.private_key,
            "funds": blockchain.get_balance(),
        }
        return jsonify(response), 200
    else:
        response = {"message": "keys failed to load"}
        return jsonify(response), 500


@app.route("/transaction", methods=["POST"])
def add_transaction():
    values = request.get_json()

    if wallet.public_key == None:
        response = {"message": "no wallet is set up"}
        return jsonify(response), 400

    if not values:
        response = {"message": "no data is provided"}
        return jsonify(response), 400

    required_fields = ["recipient", "amount"]

    if not all(field in values for field in required_fields):
        response = {"message": "required data is missing"}
        return jsonify(response), 400

    recipient = values["recipient"]
    amount = values["amount"]
    signature = wallet.sign_transaction(wallet.public_key, recipient, amount)
    success = blockchain.add_transaction(recipient, wallet.public_key, signature, amount)

    if success:
        response = {
            "message": "Transaction created successfully",
            "transaction": {
                "sender": wallet.public_key,
                "recipient": recipient,
                "signature": signature,
                "amount": amount,
            },
            "funds": blockchain.get_balance(),
        }
        return jsonify(response), 201
    else:
        response = {"message": "Transaction verification failed"}
        return jsonify(response), 500


@app.route("/transactions", methods=["GET"])
def get_open_transaction():
    transactions = blockchain.get_open_transactions()
    dict_transactions = [tx.__dict__ for tx in transactions]
    return jsonify(dict_transactions), 200


@app.route("/balance", methods=["GET"])
def get_balance():
    balance = blockchain.get_balance()
    if balance != None:
        response = {
            "message": "balance retrieved",
            "funds": balance,
        }
        return jsonify(response), 200
    else:
        response = {
            "message": "balance could not be retrieved",
            "wallet_set_up": wallet.public_key != None,
        }
        return jsonify(response), 500


@app.route("/chain", methods=["GET"])
def get_chain():
    chain_snapshot = blockchain.chain
    dict_chain = [block.__dict__.copy() for block in chain_snapshot]

    for dict_block in dict_chain:
        dict_block["transactions"] = [tx.__dict__ for tx in dict_block["transactions"]]

    return jsonify(dict_chain), 200


@app.route("/mine", methods=["POST"])
def mine():
    block = blockchain.mine_block()
    if block != None:
        dict_block = block.__dict__.copy()

        dict_block["transactions"] = [tx.__dict__ for tx in dict_block["transactions"]]

        response = {
            "message": "Block added successfully",
            "wallet_set_up": wallet.public_key != None,
            "block": dict_block,
            "funds": blockchain.get_balance(),
        }

        return jsonify(response), 201
    else:
        response = {"message": "Mining a block failed", "wallet_set_up": wallet.public_key != None}

        return jsonify(response), 500


@app.route("/node", methods=["POST"])
def add_peer_node():
    values = request.get_json()

    if not values:
        response = {"message": "no node is provided"}
        return jsonify(response), 400

    if "node" not in values:
        response = {"message": "no node data found"}
        return jsonify(response), 400

    node = values["node"]
    blockchain.add_peer_node(node)
    response = {
        "message": "added node successfully",
        "all_nodes": blockchain.all_nodes,
    }
    return jsonify(response), 201


@app.route("/node/<node_url>", methods=["DELETE"])
def remove_peer_node(node_url):
    if node_url == "" or node_url == None:
        response = {"message": "no node url is provided"}
        return jsonify(response), 400

    blockchain.remove_peer_node(node_url)
    response = {
        "message": "removed node successfully",
        "all_nodes": blockchain.all_nodes,
    }
    return jsonify(response), 200


@app.route("/node", methods=["GET"])
def get_all_nodes():
    response = {
        "message": "fetched nodes successfully",
        "all_nodes": blockchain.all_nodes,
    }
    return jsonify(response), 200


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("-p", "--port", default=5000, type=int)
    args = parser.parse_args()
    port = args.port

    wallet = Wallet(port)
    blockchain = Blockchain(wallet.public_key, port)
    app.run(host="0.0.0.0", port=port)

