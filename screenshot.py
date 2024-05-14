import base64
import win32api
import win32con
import win32gui
import win32ui

# we take the dimension of the screen
def get_dimensions():
    width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
    height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
    left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
    top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)
    return (width, height, left, top)

def screenshot(name = 'screenshot'):    
    hdesktop = win32gui.GetDesktopWindow()              #win32gui.GetDesktopWindow() -> retrieves a handle to the desktop window.
    width, height, left, top = get_dimensions()         #1

    desktop_dc = win32gui.GetWindowDC(hdesktop)         #GetWindowDC(hdesktop) -> retrieves the device context for the specified window
    img_dc = win32ui.CreateDCFromHandle(desktop_dc)
    #2
    memory_dc = img_dc.CreateCompatibleDC()             #hold a memory device context
    #3
    screenshot = win32ui.CreateBitmap()                 #create a Bitmap object            
    screenshot.CreateCompatibleBitmap(img_dc, width, height)  #we configure screeshot to be compatbile with img_dc with its widht & heigth
    memory_dc.SelectObject(screenshot)                  #selects the screenshot bitmap object into a memory_dc -> which is typically used for off-screen drawing operations

    memory_dc.BitBlt((0,0), (width, height),img_dc, (left, top), win32con.SRCCOPY)  #bit-for-bit copy of the desktop image and store it in memory_dc

    screenshot.SaveBitmapFile(memory_dc, f'{name}.bmp') #we dump the screenshot into the disk
    memory_dc.DeleteDC()                                #we delete the content inside memory_dc after the screenshot is saved
    #4
    win32gui.DeleteObject(screenshot.GetHandle())       #deletes the bitmap object 'screenshot'

def run():
    screenshot()
    with open('screenshot.bmp') as f:
        img = f.read()
    return img


if __name__ == '__main__':
    screenshot()


"""
SCREENSHOT GRABBER

it uses the windows GDI to determine necessary properties, such as the total screen size, and to grab the image 
(Some screenshot software will only grab a picture of the currently active window or application, but we’ll capture the entire screen. )

DEVICE CONTEXT -> The device context is an object that allows you to draw or interact with the window's content (in this case we are obtaing it for taking screenshots) 
MEMORY DC ->  is a virtual drawing surface in memory, which is often used for off-screen rendering or manipulation before transferring the results to an actual visible surface like a window or an image.

Bitmap objects -> data structure used to represent a 2D grid of pixels in computer graphics

OBJECT IN PYTHON
defintion - is a collection of data (variables) and methods (functions) that act on the data. It is an instance of a class, which is a blueprint for creating objects.
attributes - are variables that store data associated with the object. These attributes can be accessed using dot notation 'object.attribute'.
methods - are functions that can operate on the data stored within the object. These methods can also be accessed using dot notation 'object.method()'

==================================================================================================================================================================================================================================================================================================
#1
When you call get_dimensions(), it returns a tuple containing four values: width, height, left, and top. If you directly call get_dimensions() without assigning it to separate variables like width, height, left, and top, you will get back this tuple

#2
CreateCompatibleDC(): This is a method that creates a new device context compatible with the device context it's called on

#3
sets up a bitmap object (screenshot) to capture the screenshot data and configures it to be compatible with the dimensions of an image or display surface (img_dc). Then, it selects this bitmap into a memory device context to prepare for drawing operations

#4
screenshot.GetHandle(), you're essentially asking the bitmap object, "Hey, what's your special identifier?" The object then provides its handle, which can be used for various purposes, such as deleting the object or performing other operations that require identification of the bitmap.

"""