# Pull Request: Add Caesar Cipher Attack Module

## 🎯 Overview
This PR adds a new cryptographic attack module to the GhostfaceFuzzer toolkit - a Caesar cipher decoder designed for ethical hacking and penetration testing scenarios.

## ✨ New Features

### Caesar Cipher Attack (`attacks/cypher/ceasar.py`)
- **Brute Force Decryption**: Attempts all possible shift values (0-25) to decrypt Caesar cipher text
- **Specific Shift Decryption**: Decrypt with a known shift value for targeted analysis
- **Command-Line Interface**: Easy-to-use CLI for penetration testing workflows
- **Error Handling**: Robust input validation and error management
- **Documentation**: Comprehensive docstrings and usage examples

## 🔧 Technical Implementation

### Core Functions
- `caesar_decrypt(ciphertext, shift=None)`: Main decryption function
  - If `shift` is provided: Decrypts with specific shift value
  - If `shift` is None: Brute forces all 26 possible shifts

### Command-Line Usage
```bash
# Brute force all shifts
python attacks/cypher/ceasar.py "PixxgPiksqvo"

# Decrypt with specific shift
python attacks/cypher/ceasar.py "PixxgPiksqvo" -s 8
```

### Example Output
```
Brute forcing all possible shifts:
Shift  0: pixxgpiksqvo
Shift  1: ohwwfohjrpun
...
Shift  8: happyhacking  ← Found the message!
...
Shift 25: qjyyhqjltrwp
```

## 🛡️ Security & Ethics
- **Authorized Use Only**: Designed for penetration testing on systems you have permission to test
- **Educational Purpose**: Helps understand classical cryptography weaknesses
- **Responsible Disclosure**: Includes proper warnings and ethical guidelines

## 📋 Testing
- ✅ Tested with known Caesar cipher examples
- ✅ Verified brute force functionality
- ✅ Confirmed specific shift decryption
- ✅ Validated error handling for invalid inputs

## 🔗 Integration
- Seamlessly integrates with existing `attacks/cypher/` module structure
- Follows project coding standards and documentation patterns
- Ready for integration with web interface (future enhancement)

## 📝 Files Changed
- `attacks/cypher/ceasar.py` - New Caesar cipher attack module

## 🚀 Future Enhancements
- Integration with web interface for GUI-based decryption
- Support for other classical ciphers (Vigenère, Substitution, etc.)
- Frequency analysis for automatic shift detection
- Batch processing for multiple ciphertexts

---

**Note**: This module is intended for educational purposes and authorized security testing only. Always ensure you have proper authorization before testing any system.
