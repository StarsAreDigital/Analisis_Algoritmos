class Node:
    def __init__(self, left=None, right=None, val=None):
        self.left = left
        self.right = right
        self.val = val

    def traverse(self) -> dict[bytes, bytearray]:
        queue = []
        char_codes = {}

        def _traverse(current: Node):
            if current.val is not None:
                char_codes[current.val] = bytearray(queue)
                return
            if current.left is not None:
                queue.append(0)
                _traverse(current.left)
                queue.pop()
            if current.right is not None:
                queue.append(1)
                _traverse(current.right)
                queue.pop()

        _traverse(self)
        return char_codes

    def print(self, level=0, side=""):
        out = ""
        if self is not None:
            if self.left is not None:
                out += self.left.print(level + 1, side=0)
            out += " " * 4 * level + str(side) + " -> " + str(self.val) + "\n"
            if self.right is not None:
                out += self.right.print(level + 1, side=1)
        return out


def frequency_map(filename: str):
    frequency_map = {}
    length = 0
    with open(filename, "rb") as file:
        while char := file.read(1):
            frequency_map[char] = frequency_map.get(char, 0) + 1
            length += 1
    return frequency_map, length


def build_huffman_tree(frequency_map: dict[str, int]):
    sorted_chars = [
        Node(val=char)
        for char, _ in sorted(frequency_map.items(), key=lambda item: item[1])
    ]
    while len(sorted_chars) > 1:
        a = sorted_chars.pop(0)
        b = sorted_chars.pop(0)
        n = Node(a, b)
        sorted_chars.append(n)
    if sorted_chars:
        with open("charmap.txt", "w") as temp:
            temp.write(sorted_chars[0].print())
        return sorted_chars[0].traverse()
    return {}


def encode_huffman(charmap: dict, filename: str):
    codes = []
    with open(filename, "rb") as file:
        while char := file.read(1):
            code = charmap[char]
            codes.extend(code)
    out = []
    for i in range(0, len(codes), 8):
        acc = 0
        for j in range(8):
            acc = (acc << 1) + (codes[i + j] if i + j < len(codes) else 0)
        out.append(acc)
    return bytearray(out)


def save_huffman(charmap: dict[bytes, bytearray], bytes_out: bytearray, filename: str, total_length: int):
    with open(filename, "wb") as file:
        file.write(len(charmap).to_bytes(4))
        file.write(total_length.to_bytes(4))
        for char, code in charmap.items():
            file.write(char)
            file.write(len(code).to_bytes(1))
            acc = 0
            for i in code:
                acc = (acc << 1) + i
            file.write(acc.to_bytes(1))
        file.write(bytes_out)


def huffman(file_in, file_out):
    fmap, total_len = frequency_map(file_in)
    charmap = build_huffman_tree(fmap)

    encoded = encode_huffman(charmap, file_in)
    save_huffman(charmap, encoded, file_out, total_len)


def read_huffman(file_in, file_out):
    out = bytearray()
    with open(file_in, "rb") as file:
        # read and build charmap
        root = Node()
        charmap_size = int.from_bytes(file.read(4))
        original_length = int.from_bytes(file.read(4))
        for _ in range(charmap_size):
            char, code_len, code_bytes = bytearray(file.read(3))
            code = [(code_bytes >> i) & 1 for i in range(code_len - 1, -1, -1)]

            current = root
            for i in code:
                if i == 0:
                    if current.left is None:
                        current.left = Node()
                    current = current.left
                if i == 1:
                    if current.right is None:
                        current.right = Node()
                    current = current.right
            current.val = char

        def get_bit(i: int, byte: bytes):
            n = int.from_bytes(byte)
            return n >> (8 - i - 1) & 1

        current = root
        while byte := file.read(1):
            for i in range(8):
                bit = get_bit(i, byte)
                if bit == 0:
                    current = current.left
                if bit == 1:
                    current = current.right
                if current.val is not None:
                    out.append(current.val)
                    current = root
    
    with open(file_out, "wb") as file:
        for i, code in enumerate(out):
            if i == original_length:
                break
            byte = code.to_bytes()
            file.write(byte)
        


a = "Frankenstein; Or, The Modern Prometheus.txt"
b = "compressed.small"
c = "recovered.txt"

huffman(a, b)
# read_huffman(b, c)