import game

# Starting the game
def main():
    mygame = game.Game()
    front_page = mygame.open_page()
    if front_page:
        mygame.run()
if __name__ == "__main__":
    main()