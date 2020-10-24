from PIL import Image
from time import sleep
from io import BytesIO

def take_screenshot(driver,css_selector):
    sr,cl,sw=driver.execute_script(f"""
    let sr=document.querySelector("{css_selector}").scrollHeight;
    let sw=document.querySelector("{css_selector}").scrollWidth;
    let cl=document.querySelector("{css_selector}").clientHeight;
    return [sr,cl,sw]
    """)
    driver.execute_script(f"""
    document.querySelector("{css_selector}").scrollTo(0,0);
    """)
    finalImage = Image.new ("RGB", (sw, sr))
    count=0
    while sr>0:
        objectElement=driver.find_element_by_css_selector(f"{css_selector}")
        count+=1
        img=objectElement.screenshot_as_png
        imageblob = Image.open (BytesIO (img))
        if(0<sr<cl):
            imageblob.crop((0,cl-(cl-sr),sw,cl))
            finalImage.paste (imageblob, (0, count * cl))
            break
        finalImage.paste(imageblob,(0,count*cl))

    # with open(f"test{count}.png", "wb") as file:
    #     file.write(img)
        driver.execute_script(f"""
    document.querySelector("{css_selector}").scrollTo(0,{count*cl});
        """)
        sr-=cl
        sleep(5)
    finalImage.save("final.png")

