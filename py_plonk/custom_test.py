import compiler as c
import prover as p
import verifier as v
import json
from mini_poseidon import rc, mds, poseidon_hash

def basic_test():
    setup = c.Setup.from_file('powersOfTau28_hez_final_11.ptau')
    print("Extracted setup")
    vk = c.make_verification_key(setup, 8, ['c <== a * b'])#py_plonk에서 생성한 vk
    print("Generated verification key")
    their_output = json.load(open('main.plonk.vkey.json')) #zkrepl에서 생성한 vk 파일
    for key in ('Qm', 'Ql', 'Qr', 'Qo', 'Qc', 'S1', 'S2', 'S3', 'X_2'): #py_plonk에서 생성한 vk와 zkrepl에서 생성한 vk를 비교
        if c.interpret_json_point(their_output[key]) != vk[key]:
            raise Exception("Mismatch {}: ours {} theirs {}"
                            .format(key, vk[key], their_output[key]))
    assert vk['w'] == int(their_output['w'])
    print("Basic test success")
    return setup


def custom_test(setup):
    print("Beginning test: prove you know small integers that multiply to 91")
    eqs = """
        x2 <== x1 * x1
        x4 <== x3 * x3
        x6 <== x5 * x5
        x6 === x2 + x4
    """
    #public = [91]
    vk = c.make_verification_key(setup, 16, eqs)
    print("Generated verification key")
    assignments = c.fill_variable_assignments(eqs, {
        'x1': 3, 'x3': 4, 'x5': 5,
    })
    proof = p.prove_from_witness(setup, 16, eqs, assignments)
    print("Generated proof")
    assert v.verify_proof(setup, 16, vk, proof, optimized=True)
    print("Factorization test success!")


if __name__ == '__main__':
    setup = basic_test()
    custom_test(setup)
