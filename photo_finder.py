import os
import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import threading
import webbrowser
from tkinter.scrolledtext import ScrolledText
from tkinter import font as tkfont

class PhotoFinderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Photo Quality Finder")
        self.root.geometry("1000x700")
        
        # Variables
        self.source_image_path = ""
        self.search_dirs = []
        self.similar_images = []
        
        # Create UI
        self.create_widgets()
    
    def create_widgets(self):
        # Configure styles
        style = ttk.Style()
        style.configure('TButton', padding=5)
        style.configure('TFrame', padding=5)
        
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Left panel for controls
        control_frame = ttk.LabelFrame(main_frame, text="Controls", padding=10)
        control_frame.pack(side='left', fill='y', padx=(0, 10))
        
        # Source image selection
        ttk.Label(control_frame, text="1. Select the low-quality photo:").pack(anchor='w', pady=(0, 5))
        
        self.source_frame = ttk.Frame(control_frame)
        self.source_frame.pack(fill='x', pady=5)
        
        self.source_entry = ttk.Entry(self.source_frame)
        self.source_entry.pack(side='left', fill='x', expand=True, padx=(0, 5))
        
        ttk.Button(
            self.source_frame, 
            text="Browse...", 
            command=self.browse_source,
            width=10
        ).pack(side='right')
        
        # Search directories selection
        ttk.Label(control_frame, text="2. Add directories to search in:").pack(anchor='w', pady=(15, 5))
        
        # Directory list with scrollbar
        dir_list_frame = ttk.Frame(control_frame)
        dir_list_frame.pack(fill='both', expand=True, pady=5)
        
        self.dir_listbox = tk.Listbox(
            dir_list_frame, 
            height=5,
            selectmode=tk.SINGLE,
            relief='solid',
            borderwidth=1
        )
        self.dir_listbox.pack(side='left', fill='both', expand=True, pady=(0, 5))
        
        # Scrollbar for directory list
        scrollbar = ttk.Scrollbar(dir_list_frame, orient='vertical')
        scrollbar.config(command=self.dir_listbox.yview)
        scrollbar.pack(side='right', fill='y')
        self.dir_listbox.config(yscrollcommand=scrollbar.set)
        
        # Directory buttons frame
        dir_buttons_frame = ttk.Frame(control_frame)
        dir_buttons_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Button(
            dir_buttons_frame,
            text="Add Directory",
            command=self.browse_directory,
            width=15
        ).pack(side='left', padx=(0, 5))
        
        ttk.Button(
            dir_buttons_frame,
            text="Remove Selected",
            command=self.remove_directory,
            width=15
        ).pack(side='left')
        
        # Search button
        self.search_btn = ttk.Button(
            control_frame, 
            text="Find Similar Photos", 
            command=self.start_search_thread,
            style='Accent.TButton',
            state='disabled'
        )
        self.search_btn.pack(fill='x', pady=10)
        
        # Progress bar
        self.progress = ttk.Progressbar(
            control_frame, 
            orient='horizontal', 
            mode='indeterminate'
        )
        
        # Right panel for results
        results_frame = ttk.Frame(main_frame)
        results_frame.pack(side='right', fill='both', expand=True)
        
        # Results header
        self.results_header = ttk.Label(
            results_frame,
            text="Results will appear here",
            font=('Helvetica', 10, 'bold')
        )
        self.results_header.pack(anchor='w', pady=(0, 5))
        
        # Canvas and scrollbar for results
        self.canvas = tk.Canvas(results_frame, bd=0, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        self.status_bar = ttk.Label(
            self.root, 
            textvariable=self.status_var, 
            relief=tk.SUNKEN, 
            anchor=tk.W,
            padding=5
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Bind events
        self.source_entry.bind('<KeyRelease>', self.check_ready)
        
        # Configure grid weights
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Create a custom style for the copy button
        style.configure('Copy.TButton', background='#e1f5fe', font=('Arial', 8))
    
    def browse_source(self):
        filetypes = (
            ('Image files', '*.jpg *.jpeg *.png *.bmp'),
            ('All files', '*.*')
        )
        filename = filedialog.askopenfilename(
            title='Select a photo',
            filetypes=filetypes
        )
        if filename:
            self.source_entry.delete(0, tk.END)
            self.source_entry.insert(0, filename)
            self.source_image_path = filename
            self.check_ready()
    
    def browse_directory(self):
        directory = filedialog.askdirectory(title='Select directory to search in')
        if directory and directory not in self.search_dirs:
            self.search_dirs.append(directory)
            self.dir_listbox.insert(tk.END, directory)
            self.check_ready()
    
    def remove_directory(self):
        selection = self.dir_listbox.curselection()
        if selection:
            index = selection[0]
            self.search_dirs.pop(index)
            self.dir_listbox.delete(index)
            self.check_ready()
    
    def copy_to_clipboard(self, text):
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.status_var.set("Path copied to clipboard!")
        self.root.after(3000, lambda: self.status_var.set(""))
    
    def check_ready(self, event=None):
        if self.source_entry.get() and self.dir_listbox.size() > 0:
            self.search_btn['state'] = 'normal'
        else:
            self.search_btn['state'] = 'disabled'
    
    def start_search_thread(self):
        self.search_btn['state'] = 'disabled'
        self.progress.pack(fill='x', pady=5)
        self.progress.start(10)
        self.status_var.set("Searching for similar photos...")
        
        # Clear previous results
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        # Start search in a separate thread
        threading.Thread(target=self.find_similar_photos, daemon=True).start()
    
    def find_similar_photos(self):
        try:
            # Load source image
            source_img = cv2.imread(self.source_image_path)
            if source_img is None:
                raise ValueError("Could not load the source image")
                
            # Convert to grayscale and resize for faster comparison
            source_gray = cv2.cvtColor(source_img, cv2.COLOR_BGR2GRAY)
            source_gray = cv2.resize(source_gray, (100, 100))
            
            # Get list of image files in all directories
            image_extensions = ('.jpg', '.jpeg', '.png', '.bmp')
            image_files = []
            
            for directory in self.search_dirs:
                for root, _, files in os.walk(directory):
                    for file in files:
                        if file.lower().endswith(image_extensions):
                            image_files.append(os.path.join(root, file))
            
            if not image_files:
                raise ValueError("No image files found in the selected directories")
            
            self.similar_images = []
            total_images = len(image_files)
            
            # Compare with each image
            for idx, img_path in enumerate(image_files):
                try:
                    # Skip the source image
                    if os.path.abspath(img_path) == os.path.abspath(self.source_image_path):
                        continue
                        
                    # Load and preprocess image
                    img = cv2.imread(img_path, cv2.IMREAD_COLOR)
                    if img is None:
                        continue
                        
                    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    img_gray = cv2.resize(img_gray, (100, 100))
                    
                    # Calculate similarity (mean squared error)
                    mse = np.mean((source_gray.astype("float") - img_gray.astype("float")) ** 2)
                    
                    # Store image and similarity score
                    self.similar_images.append((img_path, mse, img.shape[0] * img.shape[1]))
                    
                    # Update progress
                    progress = (idx + 1) / total_images * 100
                    self.root.after(100, self.update_progress, progress)
                    
                except Exception as e:
                    print(f"Error processing {img_path}: {str(e)}")
            
            # Sort by similarity (lower MSE is more similar)
            self.similar_images.sort(key=lambda x: x[1])
            
            # Display results
            self.root.after(100, self.display_results)
            
        except Exception as e:
            self.root.after(100, self.show_error, str(e))
        finally:
            self.root.after(100, self.search_complete)
    
    def update_progress(self, value):
        self.status_var.set(f"Searching... {int(value)}% complete")
    
    def display_results(self):
        # Clear previous results
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        if not self.similar_images:
            ttk.Label(
                self.scrollable_frame, 
                text="No similar images found.",
                padding=10
            ).pack()
            return
            
        # Display source image
        source_frame = ttk.LabelFrame(self.scrollable_frame, text="Source Image")
        source_frame.pack(fill='x', padx=5, pady=5)
        self.display_image(self.source_image_path, source_frame)
        
        # Display similar images
        results_label = ttk.Label(
            self.scrollable_frame, 
            text=f"Found {len(self.similar_images)} potential matches:",
            padding=(5, 15, 5, 5),
            font=('Helvetica', 10, 'bold')
        )
        results_label.pack(anchor='w')
        
        for img_path, mse, resolution in self.similar_images[:20]:  # Show top 20 matches
            frame = ttk.Frame(self.scrollable_frame, borderwidth=1, relief='solid')
            frame.pack(fill='x', padx=5, pady=5, ipady=5)
            
            # Display image
            img_frame = ttk.Frame(frame)
            img_frame.pack(side='left', padx=5, pady=5)
            self.display_image(img_path, img_frame, max_size=(200, 200))
            
            # Display info
            info_frame = ttk.Frame(frame)
            info_frame.pack(side='left', fill='x', expand=True, padx=5, pady=5)
            
            # File name with copy button
            file_frame = ttk.Frame(info_frame)
            file_frame.pack(fill='x', pady=(0, 5))
            
            ttk.Label(
                file_frame, 
                text=f"File: {os.path.basename(img_path)}",
                font=('Helvetica', 9, 'bold')
            ).pack(side='left')
            
            # Copy path button
            copy_btn = ttk.Button(
                file_frame,
                text="Copy Path",
                command=lambda p=img_path: self.copy_to_clipboard(p),
                style='Copy.TButton',
                width=10
            )
            copy_btn.pack(side='right', padx=5)
            
            # Path display with scrollable text
            path_frame = ttk.Frame(info_frame)
            path_frame.pack(fill='x', pady=(0, 5))
            
            path_text = ScrolledText(
                path_frame,
                height=1,
                wrap=tk.NONE,
                font=('Courier', 8),
                borderwidth=1,
                relief='solid',
                padx=2,
                pady=2
            )
            path_text.insert('1.0', img_path)
            path_text.configure(state='disabled')
            path_text.pack(fill='x', expand=True)
            
            # Image details
            details_frame = ttk.Frame(info_frame)
            details_frame.pack(fill='x', pady=(5, 0))
            
            ttk.Label(
                details_frame,
                text=f"Resolution: {resolution} pixels\n"
                     f"Similarity Score: {mse:.2f} (lower is better)",
                justify='left'
            ).pack(anchor='w')
            
            # Open button
            ttk.Button(
                info_frame,
                text="Open in Default Viewer",
                command=lambda p=img_path: self.open_image(p)
            ).pack(side='right', anchor='se', pady=5)
            
            # Add separator between results
            ttk.Separator(self.scrollable_frame, orient='horizontal').pack(fill='x', pady=5)
        
        # Update the canvas scroll region
        self.canvas.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
    
    def display_image(self, img_path, parent, max_size=(300, 300)):
        try:
            # Load image with PIL
            img = Image.open(img_path)
            
            # Resize while maintaining aspect ratio
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            # Convert to PhotoImage
            photo = ImageTk.PhotoImage(img)
            
            # Keep a reference to avoid garbage collection
            if not hasattr(parent, 'image_references'):
                parent.image_references = []
            parent.image_references.append(photo)
            
            # Create label with image
            label = ttk.Label(parent, image=photo)
            label.image = photo
            label.pack()
            
        except Exception as e:
            print(f"Error displaying image {img_path}: {str(e)}")
    
    def open_image(self, img_path):
        try:
            # Open the image with the default application
            os.startfile(os.path.normpath(img_path))
        except Exception as e:
            messagebox.showerror("Error", f"Could not open image: {str(e)}")
    
    def search_complete(self):
        self.progress.stop()
        self.progress.pack_forget()
        self.search_btn['state'] = 'normal'
        self.status_var.set(f"Search complete. Found {len(self.similar_images)} potential matches.")
    
    def show_error(self, message):
        messagebox.showerror("Error", message)
        self.status_var.set("Error occurred. See message box for details.")
        self.search_btn['state'] = 'normal'
        self.progress.stop()
        self.progress.pack_forget()

def main():
    root = tk.Tk()
    
    # Set window icon and theme
    try:
        root.iconbitmap(default='icon.ico')  # You can add an icon file if desired
    except:
        pass  # Use default icon if custom icon not found
    
    # Set a modern theme if available
    try:
        import ttkthemes
        style = ttkthemes.ThemedStyle(root)
        style.set_theme("arc")  # Try 'arc', 'clearlooks', or 'plastik'
    except ImportError:
        pass  # Use default theme if ttkthemes is not available
    
    app = PhotoFinderApp(root)
    
    # Make the window resizable
    root.minsize(900, 600)
    
    # Center the window
    window_width = 1000
    window_height = 700
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    root.geometry(f'{window_width}x{window_height}+{x}+{y}')
    
    root.mainloop()

if __name__ == "__main__":
    main()
