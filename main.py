import tkinter as tk
import sys
import os


sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gui.app import VisionStudioApp

def main():
    root = tk.Tk()
    
    # Set window title and initial size
    root.title("Vision Studio - Ultimate CV Project")
    
    # Create the application instance
    app = VisionStudioApp(root)
    
    # Handle window closing properly
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    
    # Start the event loop
    root.mainloop()

if __name__ == "__main__":
    main()