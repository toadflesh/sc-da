import os
import sys
import requests
import json
from dotenv import load_dotenv
from inst import match_inst


def load_urls_and_keys():
    load_dotenv()

    ALCHEMY_API_KEY = os.getenv('ALCHEMY_API_KEY')
    ALCHEMY_ARB_URL = os.getenv('ALCHEMY_ARB_URL')
    ALCHEMY_ETH_URL = os.getenv('ALCHEMY_ETH_URL')
    ALCHEMY_SOL_URL = os.getenv('ALCHEMY_SOL_URL')
    FOUR_BYTE_HEX_SIGNATURE_URL = os.getenv('FOUR_BYTE_HEX_SIGNATURE_URL')
    return {
        "alchemy": {
            "api_key": ALCHEMY_API_KEY,
            "urls": {
                "arb": ALCHEMY_ARB_URL,
                "eth": ALCHEMY_ETH_URL,
                "sol": ALCHEMY_SOL_URL
            }
        },
        "four_byte": {
            "urls": {
                "hex_sig": FOUR_BYTE_HEX_SIGNATURE_URL
            }
        }
    }

def assemble_url(network: str, cfg: dict):
    url: str = ""
    alchemy_api_key = cfg['alchemy']['api_key']
    alchemy_eth_rpc_url = cfg['alchemy']['urls']['eth']
    alchemy_arb_rpc_url = cfg['alchemy']['urls']['arb']
    alchemy_sol_rpc_url = cfg['alchemy']['urls']['sol']

    match network:
        case 'eth': 
            if alchemy_api_key != None and alchemy_eth_rpc_url != None:
                url = alchemy_eth_rpc_url+alchemy_api_key
        case 'arb':
            if alchemy_api_key != None and alchemy_arb_rpc_url != None:
                url = alchemy_arb_rpc_url+alchemy_api_key
        case 'sol':
            if alchemy_api_key != None and alchemy_sol_rpc_url != None:
                url = alchemy_sol_rpc_url+alchemy_api_key
        case _:
            url = ""
    return url

def snag_data(network: str, contract_address: str, cfg: dict):
    url: str = assemble_url(network, cfg) 
    if url == "":
        print("NO URL RETURNED - EXITING...")
        sys.exit(1)

    payload = {
        "id": 1,
        "jsonrpc": "2.0",
        "method": "eth_getCode",
        "params": [contract_address, "latest"]
    }

    headers = {
        "Content-Type":"application/json"
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        result = response.json()
        if "error" in result:
            print(f"RPC Error: {result["error"]}", file=sys.stderr)
            sys.exit(1)
        
        code = result.get("result")

        if code == "0x" or code is None:
            print(f"contract_address {contract_address} has no code (EOA or address doesn't exist)", file=sys.stderr)
            sys.exit(1)
        return code
    
    except requests.exceptions.RequestException as e:
        print(f"Network/request error: {e}", file=sys.stderr)
        sys.exit(1)

        d_str: str = data[2:].decode('utf-8')
        d_lst = []
        while offset+2 < len(data):
            b = d_str[offset:offset+2]
            d_lst.append(b)
            offset+=2
        return d_lst

def code_to_list(data: str):
    offset = 0
    d_lst = []
    if data[:2] == '0x':
        d_str = data[2:]
    else:
        d_str = data
    while offset+2 <= len(d_str):
        b = d_str[offset:offset+2]
        d_lst.append(b)
        offset+=2
    return d_lst

def disassemble(network: str, contract_address: str, cfg: dict):
    r_data = snag_data(network, contract_address, cfg)
    data = code_to_list(r_data)

    with open(f'da_{contract_address}.txt', 'w') as daf:
        daf.write('disassembly for -> '+contract_address+'\n')

        instruction_idx = 0
        offset = 0
        stack = []
        memory = []
        storage = []
        four_byte = []

        dynamo = {
            "stack": stack,
            "memory": memory,
            "storage":storage,
            "four_byte": four_byte
            }

        with open(f'four_byte_{contract_address}.txt', 'w') as fbf:
            with open(f'logs_{contract_address}.txt', 'w') as lf:
                while offset < len(data):
                    lf.write(f'[INSTRUCTION : {instruction_idx:06}] -> data[{offset:06d}] : {data[offset]}\n')    
                    inst: str = data[offset]
                    print(f'data[{offset}] -> {inst}')
                    movement: int = match_inst(data, inst, instruction_idx, offset, daf, fbf, cfg, dynamo)
                    offset+=movement
                    instruction_idx+=1
        print()
        print('PUSH INSTRUCTIONS:')
        for idx, item in enumerate(dynamo['stack']):
            if len(item['instruction']) > 5:
                print(f'[{idx:06d}] -> {item['instruction']} -> 0x{int(item['data'], 16):064x}')
            else:
                print(f'[{idx:06d}] -> {item['instruction']}  -> 0x{int(item['data'], 16):064x}')
        print()
        print('FOUR_BYTE SIGS:')
        for idx, item in enumerate(dynamo['four_byte']):
            if len(item['instruction']) > 5:
                print(f'[{idx:06d}] -> {item['instruction']} -> 0x{item['hex_signature']}')
            else:
                print(f'[{idx:06d}] -> {item['instruction']}  -> 0x{item['hex_signature']}')
        

def print_invalid_arg_msg(msg: str):
    print(msg)
    print("USAGE: uv run main.py <eth | arb | sol> <contract_address>")

def main():
    args = sys.argv
    if len(args) != 3:
        print_invalid_arg_msg(f"invalid number of args -> {len(args)}")
        sys.exit(1)
    
    network = args[1].lower().strip()
    contract_address = args[2].lower().strip()
    
    if network != 'eth' and network != 'arb' and network != 'sol':
        print_invalid_arg_msg(f"network : {network} - not supported")
        sys.exit(1)
    
    if contract_address[:2] != '0x' or len(contract_address) != 42:
        print_invalid_arg_msg(f"invalid contract address entered -> {contract_address}")
        sys.exit(1)
    
    cfg: dict = load_urls_and_keys()
    disassemble(network, contract_address, cfg)

if __name__ == "__main__":
    main()
