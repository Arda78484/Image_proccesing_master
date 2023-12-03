import cv2
import os
import numpy as np 

dir_path = r'C:\Users\ardac\OneDrive\Masaüstü\Çalışmalar\Colour Thresholding\input'
    
def List_input():
    res = []
    for path in os.listdir(dir_path):
        if os.path.isfile(os.path.join(dir_path, path)):
            res.append(path)
            
    print("Choose a file to Color Threshold!")
    print("----------------------------------------------")
    for element in res:
        print(f"{res.index(element)}. {element}")
    print("----------------------------------------------")
    entry = int(input("Insert the order of the file to continue: "))
    in_image = res[entry]
    print(f"{in_image} is choosed.")
    return in_image
    
def Colour_picker():
    
    print("Choose a color to threshold.")
    print("1. Red")
    print("2. Blue")
    print("3. Yellow")
    print("4. Green")
    print("5. Orange")
    print("6. Purple")
    print("7. White")
    print("8. Black")
    
    color_ranges = {
        "Red": {"min": (0, 100, 100), "max": (10, 255, 255)},
        "Blue": {"min": (110, 50, 50), "max": (130, 255, 255)},
        "Yellow": {"min": (20, 100, 100), "max": (30, 255, 255)},
        "Green": {"min": (50, 50, 50), "max": (70, 255, 255)},
        "Orange": {"min": (10, 100, 100), "max": (20, 255, 255)},
        "Purple": {"min": (130, 50, 50), "max": (150, 255, 255)},
        "White": {"min": (0, 0, 200), "max": (255, 30, 255)},
        "Black": {"min": (0, 0, 0), "max": (180, 255, 30)},
    }

    selected_color = None

    while selected_color not in {1, 2, 3, 4, 5, 6, 7, 8}:
        selected_color = int(input("Pick a colour to threshold (1-8): "))
    
        match selected_color:
            case 1:
                selected_color = 'Red'
                break
            case 2:
                selected_color = 'Blue'
                break
            case 3:
                selected_color = 'Yellow'
                break
            case 4:
                selected_color = 'Green'
                break
            case 5:
                selected_color = 'Orange'
                break
            case 6:
                selected_color = 'Purple'
                break
            case 7:
                selected_color = 'White'
                break
            case 8:
                selected_color = 'Black'
                break
            case _:
                print("Wrong entry, please try again.")
                continue
        
    # Get the HSV ranges for the selected color
    min_value = np.array(color_ranges[selected_color]["min"], dtype=np.uint8)
    max_value = np.array(color_ranges[selected_color]["max"], dtype=np.uint8)

    return min_value, max_value
             

def Threshold(in_image, min_value, max_value):
    
    output_path = os.path.join('output', "out_img.png")
    input_path = os.path.join('input', in_image)
    
    img = cv2.imread(input_path, cv2.IMREAD_COLOR)
    
    if img is None:
        print("Could not open or find the image.")
        exit(0)
      
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    img_threshed = cv2.inRange(img_hsv, min_value, max_value)

    
    contours, _ = cv2.findContours(img_threshed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw bounding boxes around contours
    img_final = img.copy()
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(img_final, (x, y), (x + w, y + h), (0, 0, 255), 3)
        
    cv2.imwrite(output_path, img_final)
    return img_final
    
def Show_img(in_img, final_img):
    cv2.imshow("Original Image", cv2.imread(os.path.join('input', in_img)))
    cv2.imshow("Thresholded Image with Bounding Boxes", final_img)
    
    cv2.waitKey(20)  # Add a small delay
    key = cv2.waitKey(0) & 0xFF  # Wait for a key event

    if key == 27:  # Check if the pressed key is ESC (27 is the keycode for ESC)
        cv2.destroyAllWindows()
    
if __name__ == '__main__':
    
    entry = 0
    print("Welcome to Colour Thresholding app.")
    while (entry != -1):
        
        in_img = List_input()
        min_value, max_value = Colour_picker()
        img_final = Threshold(in_img, min_value, max_value)
        option = int(input("Do you want to view the image? (0-Yes,1-No)"))
        if option == 0:
            Show_img(in_img, img_final)
        else:
            entry = int(input("İf you wish to exit the program press -1 otherwise press anything to continue: "))
