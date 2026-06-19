vars = {
        "CURRENT_PARAGRAPH_ID": 1,
    }

def modifyValue(name: str, val: int):
    #updates or adds the value
    vars[name.upper()] = val
    #print(f"updated {name} to: {val}")

def getValue(name : str):
    try:
        return int(vars[name.upper().strip()])
    except:
        return 0