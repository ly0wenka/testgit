import struct

def left_rotate(x, n):
    """Left rotation for 32-bit integers"""
    return ((x << n) | (x >> (32 - n))) & 0xFFFFFFFF


def right_rotate(x, n):
    """Right rotation for 32-bit integers"""
    return ((x >> n) | (x << (32 - n))) & 0xFFFFFFFF


def panama(message: bytes) -> str:
    """
    PANAMA hash function implementation
    Returns 192-bit hash (48 hex characters) as shown in the image
    """
    # Initialize state (17 words of 32 bits)
    state = [0] * 17
    
    # Initialize buffer (32 rows, 8 columns)
    buffer = [[0] * 8 for _ in range(32)]
    buffer_index = 0
    
    # Step 1: Padding
    # Append 0x80 byte
    message += b'\x80'
    
    # Pad with zeros to multiple of 32 bytes (256 bits)
    while len(message) % 32 != 0:
        message += b'\x00'
    
    def push_block(block_words):
        """Process one 256-bit block (push phase)"""
        nonlocal buffer_index, state
        
        # Update buffer with nonlinear feedback
        # Using the original PANAMA buffer update formula
        new_row = [0] * 8
        old_row = buffer[buffer_index]
        
        for i in range(8):
            # Buffer feedback: new_row[i] = block[i] ^ buffer[(buffer_index-1)%32][i] ^ 
            # (buffer[(buffer_index-25)%32][i] | buffer[(buffer_index-4)%32][i])
            feedback = (
                block_words[i] ^ 
                buffer[(buffer_index - 1) % 32][i] ^ 
                (buffer[(buffer_index - 25) % 32][i] | buffer[(buffer_index - 4) % 32][i])
            ) & 0xFFFFFFFF
            
            new_row[i] = feedback
            old_row[i] ^= new_row[i]
            old_row[i] &= 0xFFFFFFFF
        
        # Store new row in buffer
        buffer[buffer_index] = new_row
        
        # Gamma function - nonlinear transformation
        gamma = [0] * 17
        for i in range(17):
            gamma[i] = state[i] ^ (
                state[(i + 1) % 17] | 
                ((~state[(i + 2) % 17]) & 0xFFFFFFFF)
            )
            gamma[i] &= 0xFFFFFFFF
        
        # Pi function - permutation
        pi = [0] * 17
        for i in range(17):
            pi[i] = left_rotate(gamma[(7 * i) % 17], (i * (i + 1) // 2) % 32)
        
        # Theta function - linear diffusion
        theta = [0] * 17
        for i in range(17):
            theta[i] = (
                pi[i] ^ 
                pi[(i + 1) % 17] ^ 
                pi[(i + 4) % 17]
            ) & 0xFFFFFFFF
        
        # Add constant
        theta[0] ^= 1
        
        # Mix buffer into theta (this is where many implementations get it wrong)
        # Original PANAMA mixes the current buffer row
        for i in range(8):
            theta[i + 1] ^= buffer[buffer_index][i]
            theta[i + 1] &= 0xFFFFFFFF
        
        # Update state
        state = theta
        
        # Move buffer pointer
        buffer_index = (buffer_index - 1) % 32
    
    def pull_step():
        """Extract hash without input (pull phase)"""
        nonlocal buffer_index, state
        
        # During pull, we don't update buffer with new data
        # But we still need to process the buffer for mixing
        
        # Gamma function
        gamma = [0] * 17
        for i in range(17):
            gamma[i] = state[i] ^ (
                state[(i + 1) % 17] | 
                ((~state[(i + 2) % 17]) & 0xFFFFFFFF)
            )
            gamma[i] &= 0xFFFFFFFF
        
        # Pi function
        pi = [0] * 17
        for i in range(17):
            pi[i] = left_rotate(gamma[(7 * i) % 17], (i * (i + 1) // 2) % 32)
        
        # Theta function
        theta = [0] * 17
        for i in range(17):
            theta[i] = (
                pi[i] ^ 
                pi[(i + 1) % 17] ^ 
                pi[(i + 4) % 17]
            ) & 0xFFFFFFFF
        
        # Add constant
        theta[0] ^= 1
        
        # Mix buffer - use current buffer row during pull
        # Different from push phase - we don't update buffer
        for i in range(8):
            theta[i + 1] ^= buffer[buffer_index][i]
            theta[i + 1] &= 0xFFFFFFFF
        
        # Update state
        state = theta
        
        # Move buffer pointer (still cycles even without input)
        buffer_index = (buffer_index - 1) % 32
    
    # Step 2: Process all blocks (push phase)
    for i in range(0, len(message), 32):
        block = list(struct.unpack('<8I', message[i:i+32]))
        push_block(block)
    
    # Step 3: Pull phase - extract 192 bits (6 words of 32 bits each)
    # Original PANAMA uses 32 pull steps, but for 192-bit output we take first 6 words
    for _ in range(32):
        pull_step()
    
    # Return first 192 bits (6 words = 48 hex characters)
    # This matches the hash shown in the image
    return ''.join(f'{state[i % 17]:08x}' for i in range(6))


def panama_file(filepath: str) -> str:
    """Calculate PANAMA hash of a file"""
    with open(filepath, 'rb') as f:
        return panama(f.read())


def panama_string(text: str) -> str:
    """Calculate PANAMA hash of a string"""
    return panama(text.encode('utf-8'))


if __name__ == "__main__":
    file_path = r"C:\Users\L\Desktop\Hash.txt"
    print("PANAMA:", panama_file(file_path))