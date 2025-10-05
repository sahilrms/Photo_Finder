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

## Requirements

- Python 3.7 or higher
- OpenCV
- NumPy
- Pillow (PIL Fork)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/photo-quality-finder.git
   cd photo-quality-finder
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```bash
   python photo_finder.py
   ```

2. In the application:
   - Click "Browse..." to select a low-quality photo
   - Click "Add Directory" to add directories to search in
   - Click "Find Similar Photos" to start the search
   - Browse the results and use the "Copy Path" or "Open in Default Viewer" buttons as needed

## How It Works

The application uses Mean Squared Error (MSE) to compare the visual similarity between images. Here's a quick overview of the process:

1. The source image and all target images are converted to grayscale
2. All images are resized to a standard size (100x100 pixels) for consistent comparison
3. The MSE is calculated between the source image and each target image
4. Results are sorted by similarity (lower MSE = more similar)
5. The most similar images are displayed with their details

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
# Photo_Finder
