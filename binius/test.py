from binary_fields import BinaryFieldElement as B
from utils import extend
from simple_binius import simple_binius_proof, verify_simple_binius_proof
from packed_binius import (
    packed_binius_proof, verify_packed_binius_proof
)

def test_binary_operations():
    assert (B(3) + B(14)) * B(15) == B(3) * B(15) + B(14) * B(15)
    assert len(set((B(x) * 3).value for x in range(256))) == 256
    assert B(13) ** 255 == 1
    print("Verified basic operations")

def test_simple_binius():
    z = [B(int(bit)) for bit in bin(3**7890)[2:][:1024]]
    proof = simple_binius_proof(z, [B(x) for x in [3, 14, 15, 92, 65, 35, 89, 79, 32, 38]])
    print("Generated simple-binius proof")
    print("t_prime:", proof["t_prime"])
    verify_simple_binius_proof(proof)
    print("Verified simple-binius proof")

def test_packed_binius():
    z = [B(int(bit)) for bit in bin(3**7890)[2:][:8192]]
    proof = packed_binius_proof(z, [B(x) for x in [3, 14, 15, 92, 65, 35, 89, 79, 32, 38, 46, 26, 43]])
    print("Generated packed-binius proof")
    print("t_prime:", proof["t_prime"])
    verify_packed_binius_proof(proof)
    print("Verified packed-binius proof")

if __name__ == '__main__':
    test_binary_operations()
    test_simple_binius()
    test_packed_binius()
