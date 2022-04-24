def main(x1, y1, x2, y2):
    if abs(x1-x2) == 1:
        if abs(y1-y2) == 1 or abs(y1-y2) == 3:
            return True
        return False
    if abs(x1-x2) == 2:
        pass
