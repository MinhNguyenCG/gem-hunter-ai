from file_manager import FileManager

def main():
    print("Hello, World!")
    # Add your main code logic here

    grid = FileManager.load_grid("testcases/input_3.txt")

    # Print the loaded grid for verification
    if grid is not None:
        for row in grid:
            print(row)
    else:
        print("Failed to load grid.")



if __name__ == "__main__":
    main()