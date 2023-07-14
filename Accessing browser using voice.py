import speech_recognition as sr
from selenium import webdriver

# Initialize the recognizer
r = sr.Recognizer()

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

# Function to control Google Chrome based on voice commands
def control_chrome(command):
    if "open" in command:
        website = command.split("open ")[-1]
        url = f"https://www.google.com"
        driver.get(url)
    elif "search" in command:
        query = command.split("search ")[-1]
        search_box = driver.find_element("name", "q")  # Locate the search box element
        search_box.send_keys(query)  # Enter the search query
        search_box.submit()  # Submit the search form
    elif "scroll up" in command:
        driver.execute_script("window.scrollBy(0, -250)")  # Scroll up by 250 pixels
    elif "scroll down" in command:
        driver.execute_script("window.scrollBy(0, 250)")  # Scroll down by 250 pixels
    elif "write email" in command:
        # Perform actions to write an email
        # Implement your email writing logic here
        print("Writing email...")
    elif "zoom in" in command:
        driver.execute_script("document.body.style.zoom = '1.2'")  # Zoom in by 20%
    elif "zoom out" in command:
        driver.execute_script("document.body.style.zoom = '0.8'")  # Zoom out by 20%
    elif "click" in command:
        element = command.split("click ")[-1]
        try:
            clickable_element = driver.find_element_by_xpath(f"//*[text()='{element}']")
            clickable_element.click()
            print(f"Clicked on element: {element}")
        except NoSuchElementException:
            print(f"Element not found: {element}")
    elif "go back" in command:
        driver.back()
        print("Navigated back")
    elif "go forward" in command:
        driver.forward()
        print("Navigated forward")
    elif "refresh" in command:
        driver.refresh()
        print("Page refreshed")
    elif "close" in command:
        driver.close()
        print("Closed the current tab")
    elif "new tab" in command:
        driver.execute_script("window.open()")
        print("Opened a new tab")
    elif "switch tab" in command:
        tab_number = command.split("switch tab ")[-1]
        handles = driver.window_handles
        if len(handles) >= int(tab_number):
            driver.switch_to.window(handles[int(tab_number) - 1])
            print(f"Switched to tab {tab_number}")
        else:
            print(f"Invalid tab number: {tab_number}")
    elif "scroll to top" in command:
        driver.execute_script("window.scrollTo(0, 0)")  # Scroll to the top of the page
        print("Scrolled to the top of the page")
    elif "scroll to bottom" in command:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")  # Scroll to the bottom of the page
        print("Scrolled to the bottom of the page")
    elif "scroll to element" in command:
        element = command.split("scroll to element ")[-1]
        try:
            target_element = driver.find_element_by_xpath(f"//*[text()='{element}']")
            driver.execute_script("arguments[0].scrollIntoView();", target_element)
            print(f"Scrolled to element: {element}")
        except NoSuchElementException:
            print(f"Element not found: {element}")
    elif "scroll left" in command:
        driver.find_element("tag name", "body").send_keys(Keys.LEFT)  # Scroll left
        print("Scrolled left")
    elif "scroll right" in command:
        driver.find_element("tag name", "body").send_keys(Keys.RIGHT)  # Scroll right
        print("Scrolled right")
    elif "scroll to top" in command:
        driver.execute_script("window.scrollTo(0, 0)")  # Scroll to the top of the page
        print("Scrolled to the top of the page")
    elif "scroll to bottom" in command:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")  # Scroll to the bottom of the page
        print("Scrolled to the bottom of the page")
    # elif "scroll to element" in command:
    #     element = command.split("scroll to element ")[-1]
    #     try:
    #         target_element = driver.find_element_by_xpath(f"//*[text()='{element}']")
    #         driver.execute_script("arguments[0].scrollIntoView();", target_element)
    #         print(f"Scrolled to element: {element}")
    #     except NoSuchElementException:
    #         print(f"Element not found: {element}")
    elif "scroll left" in command:
        driver.find_element("tag name", "body").send_keys(Keys.LEFT)  # Scroll left
        print("Scrolled left")
    elif "scroll right" in command:
        driver.find_element("tag name", "body").send_keys(Keys.RIGHT)  # Scroll right
        print("Scrolled right")
    elif "scroll to top" in command:
        driver.execute_script("window.scrollTo(0, 0)")  # Scroll to the top of the page
        print("Scrolled to the top of the page")
    elif "scroll to bottom" in command:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")  # Scroll to the bottom of the page
        print("Scrolled to the bottom of the page")
    elif "scroll to element" in command:
        element = command.split("scroll to element ")[-1]
        try:
            target_element = driver.find_element_by_xpath(f"//*[text()='{element}']")
            driver.execute_script("arguments[0].scrollIntoView();", target_element)
            print(f"Scrolled to element: {element}")
        except NoSuchElementException:
            print(f"Element not found: {element}")
    elif "scroll left" in command:
        driver.find_element("tag name", "body").send_keys(Keys.LEFT)  # Scroll left
        print("Scrolled left")
    elif "scroll right" in command:
        driver.find_element("tag name", "body").send_keys(Keys.RIGHT)  # Scroll right
        print("Scrolled right")
    elif "scroll to top" in command:
        driver.execute_script("window.scrollTo(0, 0)")  # Scroll to the top of the page
        print("Scrolled to the top of the page")
    elif "scroll to bottom" in command:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")  # Scroll to the bottom of the page
        print("Scrolled to the bottom of the page")
    elif "scroll to element" in command:
        element = command.split("scroll to element ")[-1]
        try:
            target_element = driver.find_element_by_xpath(f"//*[text()='{element}']")
            driver.execute_script("arguments[0].scrollIntoView();", target_element)
            print(f"Scrolled to element: {element}")
        except NoSuchElementException:
            print(f"Element not found: {element}")
    elif "scroll left" in command:
        driver.find_element("tag name", "body").send_keys(Keys.LEFT)  # Scroll left
        print("Scrolled left")
    elif "scroll right" in command:
        driver.find_element("tag name", "body").send_keys(Keys.RIGHT)  # Scroll right
        print("Scrolled right")
    elif "switch window" in command:
        handles = driver.window_handles
        if len(handles) > 1:
            driver.switch_to.window(handles[-1])  # Switch to the last opened window
            print("Switched to the new window")
        else:
            print("No new window found")
    elif "close window" in command:
        handles = driver.window_handles
        if len(handles) > 1:
            driver.close()  # Close the current window
            driver.switch_to.window(handles[-2])  # Switch to the previous window
            print("Closed the current window")
        else:
            print("Unable to close the current window")
    else:
        print("Command not recognized.")


# Set up the Chrome driver
driver = webdriver.Chrome()

# Main program loop
while True:
    try:
        # Capture audio from the microphone
        with sr.Microphone() as source:
            print("Listening...")
            audio = r.listen(source)

        # Use Google Speech Recognition to convert speech to text
        command = r.recognize_google(audio).lower()
        print("You said:", command)

        # Control Google Chrome based on the command
        control_chrome(command)

    except sr.UnknownValueError:
        print("Unable to understand audio")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
