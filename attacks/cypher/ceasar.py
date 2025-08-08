#Author: Santiago Espinosa Giraldo 
#Github: https://github.com/espinosacodes
#Description: Caesar Cipher Decoder for Ethical Hacking/Penetration Testing
#Usage: python attacks/cypher/ceasar.py "your_ciphertext" -s number_of_shift


def caesar_decrypt(ciphertext, shift=None):
    """
    Decrypt a Caesar cipher encrypted text.
    If shift is not provided, it will brute force all possible shifts (0-25).
    """
    decrypted_results = []
    
    # If shift is specified, only try that one
    if shift is not None:
        shift = int(shift) % 26
        result = ""
        for char in ciphertext:
            if char.isalpha():
                shifted = ord(char.lower()) - shift
                if shifted < ord('a'):
                    shifted += 26
                result += chr(shifted)
            else:
                result += char
        return result
    # Otherwise try all possible shifts
    else:
        for s in range(26):
            result = ""
            for char in ciphertext:
                if char.isalpha():
                    shifted = ord(char.lower()) - s
                    if shifted < ord('a'):
                        shifted += 26
                    result += chr(shifted)
                else:
                    result += char
            decrypted_results.append((s, result))
        return decrypted_results

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Caesar Cipher Decoder for authorized penetration testing",
        epilog="Use responsibly and only on systems you have permission to test."
    )
    parser.add_argument("ciphertext", help="The encrypted text to decode")
    parser.add_argument("-s", "--shift", type=int, 
                       help="Specific shift to try (0-25). If not provided, will brute force all shifts.")
    
    args = parser.parse_args()
    
    if args.shift is not None:
        print(f"Decrypted with shift {args.shift}: {caesar_decrypt(args.ciphertext, args.shift)}")
    else:
        print("Brute forcing all possible shifts:")
        results = caesar_decrypt(args.ciphertext)
        for shift, text in results:
            print(f"Shift {shift:2d}: {text}")
            
#Example:
#(base) [santiago@archlinux GhostfaceFuzzer]$ python attacks/cypher/ceasar.py "PixxgPiksqvo" -s 8
#Decrypted with shift 8: happyhacking
#(base) [santiago@archlinux GhostfaceFuzzer]$ 
