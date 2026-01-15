# Adding Your Tesla Car Image

The integration now includes an icon, but you'll want to add a photo of your specific Tesla for the dashboard.

## Quick Start

### 1. Get Your Car Image

**Option A: Use Your Own Photo**
- Take a photo of your Tesla (side or 3/4 view works best)
- Recommended size: 1920x1080 or 1280x720

**Option B: Download from Tesla.com**
1. Visit the model page:
   - Model Y: https://www.tesla.com/modely
   - Model 3: https://www.tesla.com/model3
   - Model S: https://www.tesla.com/models
   - Model X: https://www.tesla.com/modelx
2. Right-click on a car image → "Save Image As"
3. Choose a high-quality hero shot

**Option C: Free Stock Photos**
- Unsplash: https://unsplash.com/s/photos/tesla-model-y
- Pexels: https://www.pexels.com/search/tesla-model-y/
- Search for your specific model and color

### 2. Add Image to Integration

**Method 1: Via File System**
```
custom_components/teslamate/images/my_tesla.jpg
```

**Method 2: Via www Folder (Recommended)**
```
config/www/tesla_images/my_tesla.jpg
```

### 3. Update Dashboard Configuration

If using `www` folder:
```yaml
type: picture-entity
entity: device_tracker.tesla_location
image: /local/tesla_images/my_tesla.jpg
show_state: false
show_name: false
```

If using integration images folder (HACS):
```yaml
type: picture-entity
entity: device_tracker.tesla_location
image: /local/community/teslamate/images/my_tesla.jpg
show_state: false
show_name: false
```

### 4. Example: Model Y Performance Hero Shot

For a Model Y Performance, here's how to get a great official image:

1. Visit https://www.tesla.com/modely
2. Look for the "Model Y Performance" section
3. Right-click the hero image (usually shows the car at an angle)
4. Save as `model_y_performance.jpg`
5. Place in `config/www/tesla_images/`
6. Reference as `/local/tesla_images/model_y_performance.jpg` in dashboard

## Image Specifications

**Recommended:**
- Format: JPG (for photos) or PNG (for transparency)
- Dimensions: 1920x1080, 1280x720, or 1200x800
- Aspect Ratio: 16:9 or 3:2
- File Size: < 500KB for fast loading
- Orientation: Landscape (horizontal)
- View: Side profile or 3/4 angle

**Avoid:**
- Very large files (> 2MB) - they'll slow down your dashboard
- Portrait orientation - doesn't fit well in cards
- Low resolution images - will look pixelated

## Multiple Cars

If you have multiple Teslas, create separate images:
```
my_model_y.jpg
my_model_3.jpg
```

Then use conditional cards or separate dashboards for each vehicle.

## Testing

After adding your image:
1. Refresh your Home Assistant dashboard (Ctrl+F5)
2. If image doesn't show, check browser console (F12) for errors
3. Verify the file path matches your dashboard YAML
4. Ensure file permissions allow Home Assistant to read the image

## Troubleshooting

**Image not showing?**
- Check file path is correct (case-sensitive on Linux)
- Verify file exists in the correct folder
- Try clearing browser cache (Ctrl+Shift+Delete)
- Check Home Assistant logs for errors

**Image loads slowly?**
- Reduce file size using an image optimizer
- Recommended: use JPG with 80-90% quality
- Resize to max 1920px wide

**Want to change image based on car state?**
- Use conditional cards to show different images when charging, driving, etc.
- See `AUTOMATIONS.md` for examples
