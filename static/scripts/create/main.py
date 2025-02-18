import utils.lib

def main():
    args = utils.lib.get_args()
    manifest = utils.lib.Manifest.load()
    print("Args:", *args)

if __name__ == "__main__":
    main()
