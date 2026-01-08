from four_byte import four_byte_hex_sig

BYTE: int = 1
def match_inst(data: list[str], inst: str, idx: int, offset: int, daf, fbf, cfg: dict, dynamo: dict):
    mvmt: int = BYTE
    name: str = ""
    pushed_data: str = ""
    match inst:
        case "00":
            name = "STOP"
        case "01":
            name = "ADD"
        case "02":
            name = "MUL"
        case "03":
            name = "SUB"
        case "04":
            name = "DIV"
        case "05":
            name = "SDIV"
        case "06":
            name = "MOD"
        case "07":
            name = "SMOD"
        case "08":
            name = "ADDMOD"
        case "09":
            name = "MULLMOD"
        case "0a":
            name = "EXP"
        case "0b":
            name = "SIGNEXTEND"
        case "10":
            name = "LT"
        case "11":
            name = "GT"
        case "12":
            name = "SLT"
        case "13":
            name = "SGT"
        case "14":
            name = "EQ"
        case "15":
            name = "ISZERO"
        case "16":
            name = "AND"
        case "17":
            name = "OR"
        case "18":
            name = "XOR"
        case "19":
            name = "NOT"
        case "1a":
            name = "BYTE"
        case "1b":
            name = "SHL"
        case "1c":
            name = "SHR"
        case "1d":
            name = "SAR"
        case "1e":
            name = "CLZ"
        case "20":
            name = "KECCAK256"
        case "30":
            name = "ADDRESS"
        case "31":
            name = "BALANCE"
        case "32":
            name = "ORIGIN"
        case "33":
            name = "CALLER"
        case "34":
            name = "CALLVALUE"
        case "35":
            name = "CALLDATALOAD"
        case "36":
            name = "CALLDATASIZE"
        case "37":
            name = "CALLDATACOPY"
        case "38":
            name = "CODESIZE"
        case "39":
            name = "CODECOPY"
        case "3a":
            name = "GASPRICE"
        case "3b":
            name = "EXTCODESIZE"
        case "3c":
            name = "EXTCODECOPY"
        case "3d":
            name = "RETURNDATASIZE"
        case "3e":
            name = "RETURNDATACOPY"
        case "3f":
            name = "EXTCODEHASH"
        case "40":
            name = "BLOCKHASH"
        case "41":
            name = "COINBASE"
        case "42":
            name = "TIMESTAMP"
        case "43":
            name = "NUMBER"
        case "44":
            name = "PREVRANDAO"
        case "45":
            name = "GASLIMIT"
        case "46":
            name = "CHAINID"
        case "47":
            name = "SELFBALANCE"
        case "48":
            name = "BASEFEE"
        case "49":
            name = "BLOBHASH"
        case "4a":
            name = "BLOBBASEFEE"
        case "50":
            name = "POP"
        case "51":
            name = "MLOAD"
        case "52":
            name = "MSTORE"
        case "53":
            name = "MSTORE8"
        case "54":
            name = "SLOAD"
        case "55":
            name = "SSTORE"
        case "56":
            name = "JUMP"
        case "57":
            name = "JUMPI"
        case "58":
            name = "PC"
        case "59":
            name = "MSIZE"
        case "5a":
            name = "GAS"
        case "5b":
            name = "JUMPDEST"
        case "5c":
            name = "TLOAD"
        case "5d":
            name = "TSTORE"
        case "5e":
            name = "MCOPY"
        case "5f":
            name = "PUSH0"
            pushed_data = "00"
            dynamo['stack'].append({"instruction": name, "data":pushed_data})
        case "60":
            mvmt: int = (BYTE * 1) + 1
            name = "PUSH1"
            pushed_data = push_bytes(data, mvmt, offset)
            dynamo['stack'].append({"instruction": name, "data":pushed_data})
        case "61":
            mvmt: int = (BYTE * 2) + 1
            name = "PUSH2"
            pushed_data = push_bytes(data, mvmt, offset)
            dynamo['stack'].append({"instruction":name, "data":pushed_data})
        case "62":
            mvmt: int = (BYTE * 3) + 1
            name = "PUSH3"
            pushed_data = push_bytes(data, mvmt, offset)
            dynamo['stack'].append({"instruction":name, "data":pushed_data})
        case "63":
            mvmt: int = (BYTE * 4) + 1
            name = "PUSH4"
            pushed_data = push_bytes(data, mvmt, offset)
            dynamo['stack'].append({"instruction":name, "data":pushed_data})

            isDuplicate: bool = False
            for sig in dynamo['four_byte']:
                if pushed_data == sig['hex_signature']:
                    isDuplicate = True
                    break
            if isDuplicate == False:
                four_byte_hex_sig(pushed_data, fbf, cfg)
                dynamo['four_byte'].append({"instruction": name, "hex_signature": pushed_data})
        case "64":
            mvmt: int = (BYTE * 5) + 1
            name = "PUSH5"
            pushed_data = push_bytes(data, mvmt, offset)
            dynamo['stack'].append({"instruction":name, "data":pushed_data})
        case "65":
            mvmt: int = (BYTE * 6) + 1
            name = "PUSH6"
            pushed_data = push_bytes(data, mvmt, offset)
            dynamo['stack'].append({"instruction":name, "data":pushed_data})
        case "66":
            mvmt: int = (BYTE * 7) + 1
            name = "PUSH7"
            pushed_data = push_bytes(data, mvmt, offset)
            dynamo['stack'].append({"instruction":name, "data":pushed_data})
        case "67":
            mvmt: int = (BYTE * 8) + 1
            name = "PUSH8"
            pushed_data = push_bytes(data, mvmt, offset)
            dynamo['stack'].append({"instruction":name, "data":pushed_data})
        case "68":
            mvmt: int = (BYTE * 9) + 1
            name = "PUSH9"
            pushed_data = push_bytes(data, mvmt, offset)
            dynamo['stack'].append({"instruction":name, "data":pushed_data})
        case "69":
            mvmt: int = (BYTE * 10) + 1
            name = "PUSH10"
            pushed_data = push_bytes(data, mvmt, offset)
            dynamo['stack'].append({"instruction":name, "data":pushed_data})
        case "6a":
            mvmt: int = (BYTE * 11) + 1
            name = "PUSH11"
            pushed_data = push_bytes(data, mvmt, offset)
            dynamo['stack'].append({"instruction":name, "data":pushed_data})
        case "6b":
            mvmt: int = (BYTE * 12) + 1
            name = "PUSH12"
            pushed_data = push_bytes(data, mvmt, offset)
            dynamo['stack'].append({"instruction":name, "data":pushed_data})
        case "6c":
            mvmt: int = (BYTE * 13) + 1
            name = "PUSH13"
            pushed_data = push_bytes(data, mvmt, offset)
            dynamo['stack'].append({"instruction":name, "data":pushed_data})
        case "6d":
            mvmt: int = (BYTE * 14) + 1
            name = "PUSH14"
            pushed_data = push_bytes(data, mvmt, offset)
            dynamo['stack'].append({"instruction":name, "data":pushed_data})
        case "6e":
            mvmt: int = (BYTE * 15) + 1
            name = "PUSH15"
            pushed_data = push_bytes(data, mvmt, offset)
            dynamo['stack'].append({"instruction":name, "data":pushed_data})
        case "6f":
            mvmt: int = (BYTE * 16) + 1
            name = "PUSH16"
            pushed_data = push_bytes(data, mvmt, offset)
            dynamo['stack'].append({"instruction":name, "data":pushed_data})
        case "70":
            mvmt: int = (BYTE * 17) + 1
            name = "PUSH17"
            pushed_data = push_bytes(data, mvmt, offset)
            dynamo['stack'].append({"instruction":name, "data":pushed_data})
        case "71":
            mvmt: int = (BYTE * 18) + 1
            name = "PUSH18"
            pushed_data = push_bytes(data, mvmt, offset)
            dynamo['stack'].append({"instruction":name, "data":pushed_data})
        case "72":
            mvmt: int = (BYTE * 19) + 1
            name = "PUSH19"
            pushed_data = push_bytes(data, mvmt, offset)
            dynamo['stack'].append({"instruction":name, "data":pushed_data})
        case "73":
            mvmt: int = (BYTE * 20) + 1
            name = "PUSH20"
            pushed_data = push_bytes(data, mvmt, offset)
            dynamo['stack'].append({"instruction":name, "data":pushed_data})
        case "74":
            mvmt: int = (BYTE * 21) + 1
            name = "PUSH21"
            pushed_data = push_bytes(data, mvmt, offset)
            dynamo['stack'].append({"instruction":name, "data":pushed_data})
        case "75":
            mvmt: int = (BYTE * 22) + 1
            name = "PUSH22"
            pushed_data = push_bytes(data, mvmt, offset)
            dynamo['stack'].append({"instruction":name, "data":pushed_data})
        case "76":
            mvmt: int = (BYTE * 23) + 1
            name = "PUSH23"
            pushed_data = push_bytes(data, mvmt, offset)
            dynamo['stack'].append({"instruction":name, "data":pushed_data})
        case "77":
            mvmt: int = (BYTE * 24) + 1
            name = "PUSH24"
            pushed_data = push_bytes(data, mvmt, offset)
            dynamo['stack'].append({"instruction":name, "data":pushed_data})
        case "78":
            mvmt: int = (BYTE * 25) + 1
            name = "PUSH25"
            pushed_data = push_bytes(data, mvmt, offset)
            dynamo['stack'].append({"instruction":name, "data":pushed_data})
        case "79":
            mvmt: int = (BYTE * 26) + 1
            name = "PUSH26"
            pushed_data = push_bytes(data, mvmt, offset)
            dynamo['stack'].append({"instruction":name, "data":pushed_data})
        case "7a":
            mvmt: int = (BYTE * 27) + 1
            name = "PUSH27"
            pushed_data = push_bytes(data, mvmt, offset)
            dynamo['stack'].append({"instruction":name, "data":pushed_data})
        case "7b":
            mvmt: int = (BYTE * 28) + 1
            name = "PUSH28"
            pushed_data = push_bytes(data, mvmt, offset)
            dynamo['stack'].append({"instruction":name, "data":pushed_data})
        case "7c":
            mvmt: int = (BYTE * 29) + 1
            name = "PUSH29"
            pushed_data = push_bytes(data, mvmt, offset)
            dynamo['stack'].append({"instruction":name, "data":pushed_data})
        case "7d":
            mvmt: int = (BYTE * 30) + 1
            name = "PUSH30"
            pushed_data = push_bytes(data, mvmt, offset)
            dynamo['stack'].append({"instruction":name, "data":pushed_data})
        case "7e":
            mvmt: int = (BYTE * 31) + 1
            name = "PUSH31"
            pushed_data = push_bytes(data, mvmt, offset)
            dynamo['stack'].append({"instruction":name, "data":pushed_data})
        case "7f":
            mvmt: int = (BYTE * 32) + 1
            name = "PUSH32"
            pushed_data = push_bytes(data, mvmt, offset)
            dynamo['stack'].append({"instruction":name, "data":pushed_data})
            # fbf.write(f'PUSH32-FOUR_BYTE {pushed_data}\n')
            if pushed_data[8:] == '00000000000000000000000000000000000000000000000000000000':
                isDuplicate: bool = False
                for sig in dynamo['four_byte']:
                    if pushed_data[:8] == sig['hex_signature']:
                        isDuplicate = True
                        break
                if isDuplicate == False:
                    four_byte_hex_sig(pushed_data[:8], fbf, cfg)
                    dynamo['four_byte'].append({"instruction": name, "hex_signature": pushed_data[:8]})
        case "80":
            name = "DUP1"
        case "81":
            name = "DUP2"
        case "82":
            name = "DUP3"
        case "83":
            name = "DUP4"
        case "84":
            name = "DUP5"
        case "85":
            name = "DUP6"
        case "86":
            name = "DUP7"
        case "87":
            name = "DUP8"
        case "88":
            name = "DUP9"
        case "89":
            name = "DUP10"
        case "8a":
            name = "DUP11"
        case "8b":
            name = "DUP12"
        case "8c":
            name = "DUP13"
        case "8d":
            name = "DUP14"
        case "8e":
            name = "DUP15"
        case "8f":
            name = "DUP16"
        case "90":
            name = "SWAP1"
        case "91":
            name = "SWAP2"
        case "92":
            name = "SWAP3"
        case "93":
            name = "SWAP4"
        case "94":
            name = "SWAP5"
        case "95":
            name = "SWAP6"
        case "96":
            name = "SWAP7"
        case "97":
            name = "SWAP8"
        case "98":
            name = "SWAP9"
        case "99":
            name = "SWAP10"
        case "9a":
            name = "SWAP11"
        case "9b":
            name = "SWAP12"
        case "9c":
            name = "SWAP13"
        case "9d":
            name = "SWAP14"
        case "9e":
            name = "SWAP15"
        case "9f":
            name = "SWAP16"
        case "a0":
            name = "LOGO"
        case "a1":
            name = "LOG1"
        case "a2":
            name = "LOG2"
        case "a3":
            name = "LOG3"
        case "a4":
            name = "LOG4"
        case "f0":
            name = "CREATE"
        case "f1":
            name = "CALL"
        case "f2":
            name = "CALLCODE"
        case "f3":
            name = "RETURN"
        case "f4":
            name = "DELEGATECALL"
        case "f5":
            name = "CREATE2"
        case "fa":
            name = "STATICCALL"
        case "fd":
            name = "REVERT"
        case "fe":
            name = "INVALID"
        case "ff":
            name = "SELFDESTRUCT"
        case _:
            name: str = f"'{inst}'(Unknown Opcode)"

    print_instruction(inst, idx, name, daf, len(data), offset, pushed_data)
    return mvmt

def push_bytes(data: list[str], mvmt: int, offset: int):
    pushed_data: str = ""
    for i in range(mvmt-1):
        pushed_data = pushed_data + data[offset+BYTE+i]
    return pushed_data
     

def print_instruction(inst: str, idx: int, name: str, daf, len: int, offset: int, pushed_data=""):
    space_factor = 15

    # MORE VERBOSE
    # if pushed_data == "":
    #     msg: str = f'[ INSTRUCTION : {idx:06} - {name}{' '*(space_factor - len(name))}] -> {inst}'
    #     daf.write(msg+'\n')
    # else:
    #     msg: str = f'[ INSTRUCTION : {idx:06} - {name}{' '*(space_factor - len(name))}] -> {inst} -> {name} -> {pushed_data}'
    #     daf.write(msg+'\n')

    # LESS VERBOSE (LIKE ETHERSCAN)
    if offset+1 == len:
        if pushed_data != "":
            daf.write(f'{name} 0x{pushed_data}')
            # print(FOUR_BYTE_HEX_SIGNATURE_URL)
        else:
            daf.write(f'{name}')
            # print(FOUR_BYTE_HEX_SIGNATURE_URL)
    else:
        if pushed_data != "":
            daf.write(f'{name} 0x{pushed_data}\n')
            # print(FOUR_BYTE_HEX_SIGNATURE_URL)
        else:
            daf.write(f'{name}\n')
            # print(FOUR_BYTE_HEX_SIGNATURE_URL)