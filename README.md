# Photo Quality Finder

A Python application that helps you find higher quality versions of your photos by searching through specified directories. The tool uses computer vision to compare images and find similar ones, making it perfect for finding original, high-quality versions of images that were compressed or sent via messaging apps.

![Screenshot](screenshot.png)  <!-- You can add a screenshot later -->

## Features

- **Multiple Directory Search**: Search for similar images across multiple directories simultaneously
- **Smart Image Comparison**: Uses OpenCV for accurate image similarity detection
- **User-Friendly Interface**: Simple and intuitive GUI built with Tkinter
- **Copy Path Functionality**: Easily copy file paths of found images
- **Quick Preview**: View thumbnails of found images directly in the application
- **Open in Default Viewer**: One-click access to view full-size images
- **Progress Tracking**: Real-time progress updates during search operations

## Getting Started

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/sahilrms/Photo_Finder.git
   cd Photo_Finder
   ```

2. **Create a virtual environment (recommended)**:
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install the required packages**:
   ```bash
   pip install -r requirements.txt
   ```
   
   If you encounter any issues, you can install the packages manually:
   ```bash
   pip install opencv-python numpy Pillow
   ```

## How to Run

1. **Activate your virtual environment** (if you created one):
   ```bash
   # Windows
   .\venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

2. **Run the application**:
   ```bash
   python photo_finder.py
   ```

## Usage Guide

1. **Select a Source Image**:
   - Click the "Browse..." button to select a low-quality photo you want to find a better version of

2. **Add Search Directories**:
   - Click "Add Directory" to add folders where the application should search for similar images
   - You can add multiple directories
   - Use "Remove Selected" to remove any directory from the search list

3. **Start the Search**:
   - Click "Find Similar Photos" to begin searching
   - The progress bar will show the search status

4. **View and Use Results**:
   - The application will display similar images sorted by similarity
   - For each result, you can:
     - View the image thumbnail
     - See the file path and resolution
     - Click "Copy Path" to copy the file path to clipboard
     - Click "Open in Default Viewer" to view the full-size image

## Troubleshooting

### Common Issues

1. **Module Not Found Errors**:
   - Make sure all dependencies are installed: `pip install -r requirements.txt`
   - If using a virtual environment, ensure it's activated

2. **Image Loading Issues**:
   - The application supports JPG, JPEG, PNG, and BMP formats
   - Some corrupted images might not load properly

3. **Performance**:
   - Searching through many large images may take time
   - The application processes images in the background to keep the UI responsive

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with Python, OpenCV, and Tkinter
- Inspired by the need to find original quality photos from compressed versions

## Support

If you find this project useful, consider giving it a ⭐️ on GitHub!

---

<div align="center">
  Made with ❤️ by Your Name
</div>
