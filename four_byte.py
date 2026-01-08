import requests
import sys

def four_byte_hex_sig(four_byte_hex: str, fbf, cfg: dict):
    url: str =  cfg['four_byte']['urls']['hex_sig']+four_byte_hex

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        status = response.status_code
        if status > 200:
            fbf.write(f"[ Error     ]: HTTP {status} -> {url} -> {four_byte_hex}\n")
            return
        else:
            result = response.json()
            if "error" in result:
                fbf.write(f"[ Error      ]: {result["error"]}\n", file=sys.stderr)
                sys.exit(1)
             
            
            for result in result['results']:
                text_sig = result['text_signature']
                fbf.write(f'[ {four_byte_hex} ] -> {text_sig}\n')
    
    except requests.exceptions.RequestException as e:
        fbf.write(f"[ Error       ]: Network/request error: {e}\n", file=sys.stderr)
