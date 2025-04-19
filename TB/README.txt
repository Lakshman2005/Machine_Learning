# 🩺 Tuberculosis-Affected Chest X-ray - 3D Visualization

**Author:** Ch Lakshman Manmadha Abhiram  
**Email:** bussiness886@gmail.com  
**GitHub:** [Lakshman2005](https://github.com/Lakshman2005)

## 📌 Overview
This project visualizes a 2D TB-affected chest X-ray as a 3D revolved structure, using a mask to identify infected regions. The TB-affected area is clearly highlighted in red within the 3D model, aiding medical understanding and interpretation.

## 📂 Project Files

| File Name       | Description                                      |
|------------------|--------------------------------------------------|
| `Chest_X-Ray.png` | Original chest X-ray image (grayscale)          |
| `TB_Mask.tif`    | TB mask image showing affected regions          |
| `main.py`        | Main script that builds and displays the 3D plot |
| `README.md`      | Project description and setup guide             |
| `requirements.txt` | Required Python libraries to run the code smoothly |

## 🛠️ Dependencies
Ensure you have Python 3 installed. Then install the required libraries using:

```bash
pip install opencv-python numpy matplotlib plotly scipy
```

Alternatively, install everything from the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

## 🚀 How to Run
1. Place `Chest_X-Ray.png` (X-ray image) and `TB_Mask.tif` (mask) in the project directory.
2. Run the script:

```bash
python main.py
```

The script will display:
- A 2D overlay of the mask on the X-ray.
- A 3D interactive model of the chest with the TB-affected region highlighted.

## 🧠 How It Works
1. **Image Loading:** The chest X-ray and TB mask are loaded using OpenCV.
2. **Resizing:** The mask is resized to match the X-ray dimensions.
3. **Overlay Display:** A 2D plot is shown with the TB-affected area in red.
4. **Profile Extraction:** A vertical profile from the mask determines the radius for 3D revolution.
5. **Smoothing:** Gaussian smoothing is applied to produce a cleaner profile.
6. **3D Generation:** The profile is rotated 360° using meshgrids.
7. **Color Mapping:**
   - **Gray:** Intensity from the X-ray.
   - **Red:** Areas marked as TB-affected by the mask.
8. **Visualization:** The 3D model is rendered using Plotly with interactive controls.

## 🎯 Features
- 📷 X-ray & mask visualization
- 🔁 3D radial revolution of TB-affected profile
- 🎨 Intensity-based color shading with TB mask highlight
- 🧪 Medical image enhancement
- 🖱️ Interactive 3D plot with zoom/rotate support

## ✅ Use Cases
- Medical imaging analysis
- Tuberculosis education tools
- Radiology visualization demos
- Data science & ML project demonstrations

## ⚠️ Notes
- The project assumes the TB mask and X-ray are pre-aligned.
- The red highlight in 3D is based on the segmentation mask (`TB_Mask.tif`).
- Plotly’s 3D plot opens in the browser or interactive window.

## 📬 Contact
For queries or collaborations:
- 📧 Email: ch.lakshman2907@gmail.com
- 🧑‍💻 GitHub: [Lakshman2005](https://github.com/Lakshman2005)

## 🪪 License
This project is open-source and free to use for academic, educational, or research purposes. Attribution is appreciated.

## 🙏 Acknowledgements
- OpenCV and Plotly for the visualization tools.
- Open datasets from TB image research and academic resources.
