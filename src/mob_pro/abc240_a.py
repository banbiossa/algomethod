def main(a, b):
    if abs(a-b) == 1 or abs(a-b) == 9:
        return "Yes"
    else:
        return "No"

def test_main():
    assert main(3, 4) == "Yes"
    assert main(3, 4) == "Yes"
