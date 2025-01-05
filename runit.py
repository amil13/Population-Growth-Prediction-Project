import subprocess
import webbrowser
import time


# Build and run the container
subprocess.run(["docker-compose", "up", "--build"], check=True)

# Wait for streamlit to be setup
time.sleep(5)

while True:
    try:
        subprocess.run(["curl", "-s", "http://localhost:8501"], check=True)
        break
    except subprocess.CalledProcessError as e:
        # If Streamlit is not yet available, retry after 1 second
        time.sleep(1)

# Open the browser
webbrowser.open_new_tab("http://localhost:8501")            


