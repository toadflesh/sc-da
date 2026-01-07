import os
import sys
import requests
from dotenv import load_dotenv
from inst import match_inst

load_dotenv()
ALCHEMY_API_KEY = os.getenv('ALCHEMY_API_KEY')
ALCHEMY_ARB_URL = os.getenv('ALCHEMY_ARB_URL')
ALCHEMY_ETH_URL = os.getenv('ALCHEMY_ETH_URL')
ALCHEMY_SOL_URL = os.getenv('ALCHEMY_SOL_URL')

def assemble_url(network: str):
    url: str = ""
    match network:
        case 'eth': 
            if ALCHEMY_API_KEY != None and ALCHEMY_ETH_URL != None:
                url = ALCHEMY_ETH_URL+ALCHEMY_API_KEY
        case 'arb':
            if ALCHEMY_API_KEY != None and ALCHEMY_ARB_URL != None:
                url = ALCHEMY_ARB_URL+ALCHEMY_API_KEY
        case 'sol':
            if ALCHEMY_API_KEY != None and ALCHEMY_SOL_URL != None:
                url = ALCHEMY_SOL_URL+ALCHEMY_API_KEY
        case _:
            return url
    return url

def snag_data(network: str, contract_address: str):
    url: str = assemble_url(network) 
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

def disassemble(network: str, contract_address: str):
    r_data = snag_data(network, contract_address)
    data = code_to_list(r_data)

    with open('dis.txt', 'w') as wf:
        wf.write('disassembly for -> '+contract_address+'\n')

        instruction_idx = 0
        offset = 0
        with open('logs.txt', 'w') as lf:
            while offset < len(data):
                lf.write(f'[INSTRUCTION : {instruction_idx:06}] -> data[{offset:06d}] : {data[offset]}\n')    
                inst: str = data[offset]
                print(f'data[{offset}] -> {inst}')
                movement: int = match_inst(data, inst, instruction_idx, offset, wf)
                offset+=movement
                instruction_idx+=1

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
    
    disassemble(network, contract_address)

if __name__ == "__main__":
    main()
