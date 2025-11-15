from yaml import load

if __name__ == "__main__": 
    print("Configuration:")
    with open("config.yaml", 'r') as f:
        try:
            load(f, Loader=None)
        except Exception as e:
            print(f"Error loading configuration: {e}")